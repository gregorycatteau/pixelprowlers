import { computed, onMounted, reactive, ref, watch } from 'vue';
import { isEmailLike, maskEmail } from '~/utils/formatDate';
import { graphqlRequest, parseGraphqlJson } from '~/utils/graphql';

type DiagnosticPath = 'CRITICAL' | 'AUDIT' | 'TRANSMISSION' | 'MAINTENANCE';
type RiskLevel = 'faible' | 'moyen' | 'critique';

type DiagnosticRadioStep = {
  id: 'structure' | 'stress' | 'siteState' | 'dependency';
  type: 'radio';
  question: string;
  options: Array<{ label: string; value: string }>;
};

export type DiagnosticStep = DiagnosticRadioStep;

export type DiagnosticTicket = {
  id: string;
  organization: string;
  email: string;
  phone?: string;
  message: string;
  answers: Record<string, string>;
  diagnosticResult: {
    path: DiagnosticPath;
    scores: {
      urgency: number;
      fragility: number;
      dependency: number;
      total: number;
    };
    timestamp: string;
  };
  emailConfirmation?: {
    status: 'sent' | 'not_configured' | 'failed';
  };
};

export type ResultContent = {
  kicker: string;
  title: string;
  context: string;
  advice: string;
  reasons: string[];
  pixelTitle: string;
  pixelItems: string[];
  alternativeItems: string[];
  honestAdvice: string;
  cta: string;
  ctaHref: string;
};

export type ImmediateDiagnosticResult = {
  path: DiagnosticPath;
  riskLevel: RiskLevel;
  title: string;
  context: string;
  consequence: string;
  recommendation: string;
  nextStepReason: string;
  urgencyMessage: string;
  outcomeMessage: string;
  selectionMessage: string;
  cta: string;
  ctaHref: string;
  reasons: string[];
  scores: DiagnosticTicket['diagnosticResult']['scores'];
};

type DiagnosticTicketGraphql = {
  id: string;
  ticketId: string;
  organization: string;
  email: string;
  phone?: string;
  message: string;
  answers: string | Record<string, string>;
  diagnosticResult: string | DiagnosticTicket['diagnosticResult'];
  emailConfirmation?: string | DiagnosticTicket['emailConfirmation'];
};

const DIAGNOSTIC_TICKET_FIELDS = /* GraphQL */ `
  {
    id
    ticketId
    organization
    email
    phone
    message
    answers
    diagnosticResult
    emailConfirmation
  }
`;

const CREATE_DIAGNOSTIC_TICKET_MUTATION = /* GraphQL */ `
  mutation CreateDiagnosticTicket(
    $organization: String!
    $email: String!
    $phone: String
    $message: String!
    $answers: JSONString!
  ) {
    createDiagnosticTicket(
      organization: $organization
      email: $email
      phone: $phone
      message: $message
      answers: $answers
    ) {
      redirectTo
      ticket ${DIAGNOSTIC_TICKET_FIELDS}
    }
  }
`;

const DIAGNOSTIC_TICKET_QUERY = /* GraphQL */ `
  query DiagnosticTicket($ticketId: String!) {
    diagnosticTicket(ticketId: $ticketId) ${DIAGNOSTIC_TICKET_FIELDS}
  }
`;

const mapDiagnosticTicket = (ticket: DiagnosticTicketGraphql): DiagnosticTicket => ({
  id: ticket.ticketId || ticket.id,
  organization: ticket.organization,
  email: ticket.email,
  phone: ticket.phone || '',
  message: ticket.message,
  answers: parseGraphqlJson(ticket.answers, {}),
  diagnosticResult: parseGraphqlJson(ticket.diagnosticResult, {
    path: 'MAINTENANCE',
    scores: {
      urgency: 0,
      fragility: 0,
      dependency: 0,
      total: 0,
    },
    timestamp: new Date().toISOString(),
  }),
  emailConfirmation: parseGraphqlJson(ticket.emailConfirmation, { status: 'not_configured' }),
});

export const diagnosticSteps: DiagnosticStep[] = [
  {
    id: 'structure',
    type: 'radio',
    question: 'Vous êtes ?',
    options: [
      { label: 'Une association / collectif', value: 'association' },
      { label: 'Une école ou structure éducative', value: 'school' },
      { label: 'Une TPE / petite entreprise', value: 'small-business' },
      { label: 'Un indépendant / freelancer', value: 'freelance' },
      { label: 'Autre (précisez)', value: 'other' },
    ],
  },
  {
    id: 'stress',
    type: 'radio',
    question: 'Ça vous stresse en ce moment ?',
    options: [
      { label: "Oui, mon site ralentit et c'est un problème quotidien", value: 'site-slow' },
      { label: "Oui, on dépend trop d'une personne et c'est fragile", value: 'single-person' },
      { label: "Oui, on perd des données ou on n'a pas de sauvegardes testées", value: 'backups' },
      { label: "Un peu, mais on s'en sort", value: 'some' },
      { label: 'Pas vraiment, on veut juste vérifier la sécu', value: 'check' },
    ],
  },
  {
    id: 'siteState',
    type: 'radio',
    question: "Votre site web, c'est ?",
    options: [
      { label: "On n'en a pas", value: 'none' },
      { label: 'On en a un mais il est vieux/fragile/ralentit', value: 'fragile' },
      { label: 'On en a un et ça va, mais on doute', value: 'doubt' },
      { label: "On en a un et ça marche, on veut juste vérifier la sécu", value: 'security-check' },
    ],
  },
  {
    id: 'dependency',
    type: 'radio',
    question: 'Qui gère votre site et vos accès en ce moment ?',
    options: [
      { label: 'Une seule personne', value: 'one' },
      { label: 'Deux personnes mais on ne sait pas bien qui fait quoi', value: 'unclear' },
      { label: "Deux personnes, c'est clair", value: 'two-clear' },
      { label: "Une petite équipe, c'est documenté", value: 'team-clear' },
    ],
  },
];

const pathMeta: Record<DiagnosticPath, Pick<ImmediateDiagnosticResult, 'title' | 'recommendation' | 'consequence' | 'nextStepReason' | 'urgencyMessage' | 'outcomeMessage' | 'selectionMessage' | 'cta' | 'ctaHref'>> = {
  CRITICAL: {
    title: 'Risque critique',
    consequence: 'Sans qualification rapide, vous risquez une panne visible, une perte de contrôle sur les accès ou une intervention faite dans l’urgence.',
    recommendation: 'Priorité : qualifier l’urgence avant toute refonte ou sécurisation.',
    nextStepReason: 'On commence par l’urgence parce qu’il faut d’abord stabiliser ce qui peut bloquer votre activité.',
    urgencyMessage: 'Un site fragile finit souvent par casser au pire moment. Chaque semaine sans correction augmente le risque de blocage ou de perte.',
    outcomeMessage: 'Vous retrouvez le contrôle de votre site, avec les urgences triées et les prochaines actions dans le bon ordre.',
    selectionMessage: 'Ce service est conçu pour des sites en production ou en difficulté, pas pour des projets exploratoires.',
    cta: 'Être accompagné sur mon problème',
    ctaHref: '/urgence',
  },
  AUDIT: {
    title: 'Risque moyen',
    consequence: 'Sans vérification, les ralentissements, accès flous ou sauvegardes non testées peuvent provoquer une perte de trafic ou un blocage futur.',
    recommendation: 'Priorité : lancer un audit pour distinguer les vrais risques des simples irritants.',
    nextStepReason: 'L’audit est la bonne suite parce qu’il évite de corriger au hasard et classe les actions par impact.',
    urgencyMessage: 'Les problèmes d’accès ou de sécurité empirent rarement seuls. Chaque semaine sans correction augmente le risque de blocage ou de perte.',
    outcomeMessage: 'Vous savez exactement quoi faire, dans le bon ordre, sans dépendre d’un prestataire flou.',
    selectionMessage: 'Nous intervenons sur des situations réelles, pas des projets exploratoires.',
    cta: 'Faire analyser mon site',
    ctaHref: '/audit-site-web',
  },
  TRANSMISSION: {
    title: 'Risque moyen',
    consequence: 'Si la personne clé n’est plus disponible, vous pouvez perdre du temps, des accès ou la capacité de maintenir votre site.',
    recommendation: 'Priorité : reprendre la main sur les accès, les rôles et la documentation.',
    nextStepReason: 'La transmission est la bonne suite parce que votre risque principal est organisationnel avant d’être technique.',
    urgencyMessage: 'Les problèmes d’accès ou de sécurité empirent rarement seuls. Le jour où la personne clé manque, le coût devient immédiat.',
    outcomeMessage: 'Vos accès sont sécurisés et centralisés. Vous n’êtes plus dépendant d’un prestataire flou.',
    selectionMessage: 'Ce service est utile quand un site ou des accès existent déjà et doivent être clarifiés.',
    cta: 'Sécuriser mon site maintenant',
    ctaHref: '/transmission-acces',
  },
  MAINTENANCE: {
    title: 'Risque faible',
    consequence: 'Sans routine minimale, un site stable peut se dégrader lentement : mises à jour oubliées, sauvegardes non testées, accès anciens.',
    recommendation: 'Priorité : valider une routine simple de maintenance et de contrôle.',
    nextStepReason: 'Un rendez-vous court suffit parce que vos réponses ne montrent pas de signal critique immédiat.',
    urgencyMessage: 'Les problèmes d’accès ou de sécurité empirent rarement seuls. Une vérification courte évite souvent une intervention plus coûteuse.',
    outcomeMessage: 'Vous savez si tout tient vraiment, et quoi surveiller avant que cela devienne urgent.',
    selectionMessage: 'Si tout fonctionne parfaitement, ce ne sera probablement pas utile.',
    cta: 'Obtenir un diagnostic clair',
    ctaHref: '/rendez-vous',
  },
};

const buildImmediateContext = (answers: Record<string, string>, reasons: string[]) => {
  const structure = describeStructure(answers);
  const readableReasons = reasons.length
    ? reasons.map((reason) => reason.toLowerCase()).join(', ')
    : 'une situation globalement stable';

  return `${structure} présente ${readableReasons}. On voit surtout ce qui peut gêner votre continuité : accès, maintenance, sauvegardes ou dépendance technique.`;
};

export const buildImmediateDiagnosticResult = (answers: Record<string, string>): ImmediateDiagnosticResult => {
  let urgency = 0;
  let fragility = 0;
  let dependency = 0;
  const reasons: string[] = [];

  if (answers.stress === 'backups') {
    urgency += 4;
    fragility += 3;
    reasons.push('Sauvegardes ou données incertaines');
  } else if (answers.stress === 'site-slow') {
    urgency += 3;
    fragility += 3;
    reasons.push('Ralentissement devenu récurrent');
  } else if (answers.stress === 'single-person') {
    dependency += 4;
    reasons.push('Dépendance forte à une personne');
  } else if (answers.stress === 'some') {
    urgency += 1;
    fragility += 1;
  }

  if (answers.siteState === 'fragile') {
    fragility += 4;
    reasons.push('Site perçu comme vieux, fragile ou lent');
  } else if (answers.siteState === 'none') {
    fragility += 2;
    reasons.push('Présence web à structurer');
  } else if (answers.siteState === 'doubt') {
    fragility += 2;
  }

  if (answers.dependency === 'one') {
    dependency += 4;
    reasons.push('Une seule personne tient les accès ou la maintenance');
  } else if (answers.dependency === 'unclear') {
    dependency += 3;
    reasons.push('Responsabilités numériques floues');
  }

  const total = urgency + fragility + dependency;
  let path: DiagnosticPath = 'MAINTENANCE';

  if (urgency >= 4 && fragility >= 4) {
    path = 'CRITICAL';
  } else if (dependency >= 5) {
    path = 'TRANSMISSION';
  } else if (total >= 4) {
    path = 'AUDIT';
  }

  const riskLevel: RiskLevel = path === 'CRITICAL' ? 'critique' : path === 'MAINTENANCE' ? 'faible' : 'moyen';
  const meta = pathMeta[path];

  return {
    path,
    riskLevel,
    ...meta,
    context: buildImmediateContext({ ...answers }, reasons),
    reasons: reasons.length ? reasons : ['Aucun signal critique dans vos réponses'],
    scores: {
      urgency,
      fragility,
      dependency,
      total,
    },
  };
};

const describeStructure = (answers: Record<string, string>) => {
  if (answers.structure === 'association') return 'Votre association ou collectif';
  if (answers.structure === 'school') return 'Votre structure éducative';
  if (answers.structure === 'small-business') return 'Votre petite entreprise';
  if (answers.structure === 'freelance') return 'Votre activité indépendante';
  if (answers.structureOther) return answers.structureOther;
  return 'Votre organisation';
};

export const buildContext = (ticket: DiagnosticTicket) => {
  const structure = describeStructure(ticket.answers);
  const fragments: string[] = [];

  if (ticket.answers.siteState === 'fragile') {
    fragments.push('un site vieux, fragile ou lent');
  } else if (ticket.answers.siteState === 'none') {
    fragments.push("pas encore de site web");
  } else if (ticket.answers.siteState === 'doubt') {
    fragments.push('un site qui fonctionne mais inspire des doutes');
  } else if (ticket.answers.siteState === 'security-check') {
    fragments.push('un site qui marche et une envie de vérifier la sécurité');
  }

  if (ticket.answers.dependency === 'one') {
    fragments.push('une dépendance forte à une seule personne');
  } else if (ticket.answers.dependency === 'unclear') {
    fragments.push('des responsabilités floues entre deux personnes');
  } else if (ticket.answers.dependency === 'team-clear') {
    fragments.push('une équipe et une documentation déjà en place');
  }

  if (ticket.answers.stress === 'backups') {
    fragments.push('un doute sérieux sur les sauvegardes ou les données');
  } else if (ticket.answers.stress === 'site-slow') {
    fragments.push('un ralentissement devenu quotidien');
  } else if (ticket.answers.stress === 'single-person') {
    fragments.push('un point de fragilité humain identifié');
  }

  return `${structure} arrive avec ${fragments.join(', ') || 'une situation plutôt stable'}. Ce n'est pas un verdict définitif, mais c'est assez clair pour recommander une prochaine étape.`;
};

export const buildResultContent = (ticket: DiagnosticTicket): ResultContent => {
  const context = buildContext(ticket);

  if (ticket.diagnosticResult.path === 'CRITICAL') {
    return {
      kicker: 'Refonte urgente',
      title: 'Vous avez un vrai problème. Et il faut le régler.',
      context: `${context} Site fragile, dépendance humaine et sauvegardes floues, c'est la combinaison qui bloque une équipe quand ça casse.`,
      advice: "Refonte urgente : reconstruire un site simple, documenté, que l'équipe peut maintenir.",
      reasons: ['Éviter une panne critique', "Former l'équipe à la maintenance", 'Prévoir 3 à 4 semaines selon le périmètre'],
      pixelTitle: 'On vous aide',
      pixelItems: ['Audit initial : 2 jours', 'Refonte : 3-4 semaines', 'Formation : 2 jours', 'Cadrage humain avant toute intervention'],
      alternativeItems: ['Contacter une agence locale', 'Engager un freelance avec exigence de documentation', 'Le faire en interne si une personne a le temps réel'],
      honestAdvice: 'Évitez un freelance solo non documenté. Vous avez déjà ce problème. Pensez transmission et documentation, pas juste développement.',
      cta: 'Être accompagné sur mon problème',
      ctaHref: '/refonte-site',
    };
  }

  if (ticket.diagnosticResult.path === 'AUDIT') {
    return {
      kicker: 'Vérification prudente',
      title: 'Vous vous posez les bonnes questions.',
      context,
      advice: 'Audit de sécurité et de stabilité : vérifier ce qui tient, ce qui va casser, et par quoi commencer.',
      reasons: ['Identifier les vrais risques', 'Savoir par où commencer', "Décider si une refonte est utile ou si une réparation suffit"],
      pixelTitle: 'On audite pour vous',
      pixelItems: ['Audit complet : 2-3 jours', 'Rapport lisible, pas du charabia', 'Priorités claires', 'Suite définie après échange humain'],
      alternativeItems: ['Faire un audit en interne avec une checklist', 'Engager un consultant sécurité local', 'Attendre et voir, avec le risque de gérer une panne plus lourde ensuite'],
      honestAdvice: 'Un audit pro prend 2-3 jours. Il évite souvent de gérer la situation dans la panique.',
      cta: 'Faire analyser mon site',
      ctaHref: '/audit-site-web',
    };
  }

  if (ticket.diagnosticResult.path === 'TRANSMISSION') {
    return {
      kicker: 'Transmission',
      title: "Vous êtes trop dépendants d'une personne.",
      context: `${context} Ça peut marcher aujourd'hui, mais le risque est simple : si la personne clé part ou n'est pas disponible, tout ralentit.`,
      advice: 'Transmission et documentation : reprendre la main, clarifier les accès, écrire les procédures.',
      reasons: ['Réduire la dépendance', "Former l'équipe", 'Avoir un plan de secours'],
      pixelTitle: 'On documente avec vous',
      pixelItems: ['Audit des accès : 1 jour', 'Documentation : 3-5 jours', 'Formation équipe : 2 jours', 'Suite définie après inventaire'],
      alternativeItems: ['Demander à la personne clé de tout documenter', 'Engager quelqu’un localement', 'Attendre une urgence et gérer sous pression'],
      honestAdvice: 'Documentez maintenant, ou vous le regretterez.',
      cta: 'Sécuriser mon site maintenant',
      ctaHref: '/transmission-acces',
    };
  }

  return {
    kicker: 'Maintenance',
    title: 'Vous vous en sortez bien.',
    context,
    advice: 'Continuez comme ça. Vérifiez régulièrement.',
    reasons: ['Mises à jour mensuelles', 'Test de restauration de sauvegarde tous les 3 mois', 'Révision des accès chaque trimestre', 'Review sécurité annuelle'],
    pixelTitle: 'Audit léger',
    pixelItems: ['Vérification ponctuelle : 1-2 jours', 'Retour clair sur les priorités', 'Suite adaptée selon le périmètre'],
    alternativeItems: ['Utiliser une checklist gratuite', 'Installer un monitoring simple', 'Rester attentifs aux accès et sauvegardes'],
    honestAdvice: "Vous êtes en bonne forme. Une vérification annuelle serait bien, mais ce n'est pas urgent.",
    cta: 'Obtenir un diagnostic clair',
    ctaHref: '/audit-site-web',
  };
};

export const emailConfirmationLabel = (ticket: DiagnosticTicket | null) => {
  const status = ticket?.emailConfirmation?.status;

  if (status === 'sent') {
    return 'Email de confirmation envoyé à';
  }

  if (status === 'failed') {
    return "Email de confirmation non envoyé, adresse prévue";
  }

  return 'Email de confirmation prêt pour';
};

export const useDiagnostic = () => {
  const router = useRouter();
  const currentStep = ref(0);
  const immediateResult = ref<ImmediateDiagnosticResult | null>(null);
  const progressSessionId = ref('');
  const answers = reactive<Record<string, string>>({
    structure: '',
    structureOther: '',
    stress: '',
    siteState: '',
    dependency: '',
  });
  const contact = reactive({
    name: '',
    email: '',
    phone: '',
    message: '',
  });
  const isSubmitting = ref(false);
  const submitError = ref('');

  const activeStep = computed(() => diagnosticSteps[currentStep.value]);
  const isLastStep = computed(() => currentStep.value === diagnosticSteps.length - 1);
  const progressPercent = computed(() => ((currentStep.value + 1) / diagnosticSteps.length) * 100);
  const dossierStatus = computed(() => {
    if (isSubmitting.value) {
      return 'Analyse en cours';
    }

    if (immediateResult.value) {
      return 'Analyse prête';
    }

    if (currentStep.value === 0) {
      return 'Dossier créé';
    }

    return `Étape ${currentStep.value} complétée`;
  });

  const canContinue = computed(() => {
    const step = activeStep.value;

    const value = answers[step.id];
    return Boolean(value && (value !== 'other' || answers.structureOther.trim()));
  });

  const canSubmit = computed(() => (
    contact.name.trim().length > 0
    && isEmailLike(contact.email)
    && contact.message.trim().length > 0
  ));

  const nextStep = () => {
    if (!canContinue.value) {
      return;
    }

    if (currentStep.value < diagnosticSteps.length - 1) {
      currentStep.value += 1;
      return;
    }

    immediateResult.value = buildImmediateDiagnosticResult({ ...answers });
  };

  const previousStep = () => {
    immediateResult.value = null;
    if (currentStep.value > 0) {
      currentStep.value -= 1;
    }
  };

  const submit = async () => {
    if (!canSubmit.value || isSubmitting.value || !immediateResult.value) {
      return;
    }

    isSubmitting.value = true;
    submitError.value = '';

    try {
      const result = await graphqlRequest<{ createDiagnosticTicket: { redirectTo: string } }>(CREATE_DIAGNOSTIC_TICKET_MUTATION, {
        organization: contact.name,
        email: contact.email,
        phone: contact.phone,
        message: contact.message,
        answers: JSON.stringify({
          ...answers,
          immediateResult: immediateResult.value,
          progressSessionId: progressSessionId.value,
        }),
      });
      router.push(result.createDiagnosticTicket.redirectTo);
    } catch {
      submitError.value = "Impossible d'enregistrer le diagnostic pour le moment. Vous pouvez réessayer dans quelques instants.";
    } finally {
      isSubmitting.value = false;
    }
  };

  onMounted(() => {
    const storageKey = 'pixelprowlers:diagnostic-session';
    const existing = window.localStorage.getItem(storageKey);
    const sessionId = existing || crypto.randomUUID();
    progressSessionId.value = sessionId;
    window.localStorage.setItem(storageKey, sessionId);

    const saved = window.localStorage.getItem(`${storageKey}:answers`);
    if (saved) {
      Object.assign(answers, parseGraphqlJson(saved, {}));
    }
  });

  watch(answers, () => {
    if (!progressSessionId.value) {
      return;
    }
    window.localStorage.setItem('pixelprowlers:diagnostic-session:answers', JSON.stringify({ ...answers }));
  }, { deep: true });

  return {
    currentStep,
    answers,
    contact,
    immediateResult,
    progressSessionId,
    dossierStatus,
    activeStep,
    isLastStep,
    progressPercent,
    isSubmitting,
    submitError,
    canContinue,
    canSubmit,
    nextStep,
    previousStep,
    submit,
  };
};

export const useDiagnosticResult = () => {
  const ticket = ref<DiagnosticTicket | null>(null);
  const isLoading = ref(false);
  const error = ref('');
  const content = computed(() => ticket.value ? buildResultContent(ticket.value) : null);
  const maskedEmail = computed(() => maskEmail(ticket.value?.email || ''));

  const load = async (ticketId: string) => {
    if (!ticketId) {
      error.value = 'Le lien ne contient pas de numéro de ticket.';
      return;
    }

    isLoading.value = true;
    error.value = '';

    try {
      const result = await graphqlRequest<{ diagnosticTicket: DiagnosticTicketGraphql }>(DIAGNOSTIC_TICKET_QUERY, { ticketId });
      ticket.value = mapDiagnosticTicket(result.diagnosticTicket);
    } catch {
      ticket.value = null;
      error.value = 'Le ticket est absent ou a expiré côté serveur.';
    } finally {
      isLoading.value = false;
    }
  };

  return { ticket, isLoading, error, content, maskedEmail, load };
};
