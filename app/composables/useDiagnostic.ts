import {
  computed,
  onMounted,
  reactive,
  ref,
  watch,
} from 'vue';

import {
  contactPhoneSchema,
  diagnosticAnswersSchema,
  diagnosticContactSchema,
  formatFrenchPhone,
} from '~/validation/schemas';

import { maskEmail } from '~/utils/formatDate';
import {
  graphqlRequest,
  parseGraphqlJson,
} from '~/utils/graphql';

type DiagnosticPath =
  | 'CRITICAL'
  | 'AUDIT'
  | 'TRANSMISSION'
  | 'MAINTENANCE';

type RiskLevel =
  | 'faible'
  | 'modéré'
  | 'élevé';

type DiagnosticStepId =
  | 'structure'
  | 'stress'
  | 'siteState'
  | 'dependency';

type DiagnosticAnswerKey =
  | DiagnosticStepId
  | 'structureOther';

type DiagnosticAnswersState = Record<
  DiagnosticAnswerKey,
  string
>;

type DiagnosticAnswersLike = Partial<
  Record<DiagnosticAnswerKey, string>
>;

type DiagnosticContactField =
  | 'name'
  | 'email'
  | 'phone'
  | 'message'
  | 'privacyAcknowledged';

type DiagnosticRadioStep = {
  id: DiagnosticStepId;
  type: 'radio';
  question: string;
  options: Array<{
    label: string;
    value: string;
  }>;
};

export type DiagnosticStep = DiagnosticRadioStep;

export type DiagnosticTicket = {
  id: string;
  organization: string;
  email: string;
  phone: string;
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
  diagnosticResult:
    | string
    | DiagnosticTicket['diagnosticResult'];
  emailConfirmation?:
    | string
    | DiagnosticTicket['emailConfirmation'];
};

const PRIVACY_NOTICE_VERSION = '2026-07-17';

const answerKeys: DiagnosticAnswerKey[] = [
  'structure',
  'structureOther',
  'stress',
  'siteState',
  'dependency',
];

const contactFields: DiagnosticContactField[] = [
  'name',
  'email',
  'phone',
  'message',
  'privacyAcknowledged',
];

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
    $phone: String!
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
    diagnosticTicket(ticketId: $ticketId)
      ${DIAGNOSTIC_TICKET_FIELDS}
  }
`;

const mapDiagnosticTicket = (
  ticket: DiagnosticTicketGraphql,
): DiagnosticTicket => ({
  id: ticket.ticketId || ticket.id,
  organization: ticket.organization,
  email: ticket.email,
  phone: ticket.phone || '',
  message: ticket.message,
  answers: parseGraphqlJson(ticket.answers, {}),
  diagnosticResult: parseGraphqlJson(
    ticket.diagnosticResult,
    {
      path: 'MAINTENANCE',
      scores: {
        urgency: 0,
        fragility: 0,
        dependency: 0,
        total: 0,
      },
      timestamp: new Date().toISOString(),
    },
  ),
  emailConfirmation: parseGraphqlJson(
    ticket.emailConfirmation,
    {
      status: 'not_configured',
    },
  ),
});

export const diagnosticSteps: DiagnosticStep[] = [
  {
    id: 'structure',
    type: 'radio',
    question: 'Quelle est votre situation ?',
    options: [
      {
        label: 'Association ou collectif',
        value: 'association',
      },
      {
        label: 'École ou structure éducative',
        value: 'school',
      },
      {
        label: 'TPE ou petite entreprise',
        value: 'small-business',
      },
      {
        label: 'Indépendant ou freelance',
        value: 'freelance',
      },
      {
        label: 'Autre situation',
        value: 'other',
      },
    ],
  },
  {
    id: 'stress',
    type: 'radio',
    question: 'Quelle situation vous préoccupe le plus actuellement ?',
    options: [
      {
        label: 'Le site ralentit ou perturbe régulièrement l’activité',
        value: 'site-slow',
      },
      {
        label: 'Le fonctionnement dépend trop d’une seule personne',
        value: 'single-person',
      },
      {
        label: 'Les sauvegardes ou les données ne sont pas suffisamment maîtrisées',
        value: 'backups',
      },
      {
        label: 'La situation présente quelques fragilités, mais reste gérable',
        value: 'some',
      },
      {
        label: 'Aucun incident particulier : nous souhaitons vérifier la sécurité',
        value: 'check',
      },
    ],
  },
  {
    id: 'siteState',
    type: 'radio',
    question: 'Comment décririez-vous votre site web ?',
    options: [
      {
        label: 'Nous n’avons pas encore de site',
        value: 'none',
      },
      {
        label: 'Il est ancien, fragile ou régulièrement ralenti',
        value: 'fragile',
      },
      {
        label: 'Il fonctionne, mais nous avons des doutes',
        value: 'doubt',
      },
      {
        label: 'Il fonctionne correctement et nous souhaitons vérifier sa sécurité',
        value: 'security-check',
      },
    ],
  },
  {
    id: 'dependency',
    type: 'radio',
    question: 'Comment sont gérés votre site et vos accès ?',
    options: [
      {
        label: 'Une seule personne détient l’essentiel des informations',
        value: 'one',
      },
      {
        label: 'Deux personnes interviennent, mais les responsabilités restent floues',
        value: 'unclear',
      },
      {
        label: 'Deux personnes interviennent avec des rôles clairement définis',
        value: 'two-clear',
      },
      {
        label: 'Une petite équipe intervient avec une documentation à jour',
        value: 'team-clear',
      },
    ],
  },
];

const pathMeta: Record<
  DiagnosticPath,
  Pick<
    ImmediateDiagnosticResult,
    | 'title'
    | 'recommendation'
    | 'consequence'
    | 'nextStepReason'
    | 'urgencyMessage'
    | 'outcomeMessage'
    | 'selectionMessage'
    | 'cta'
    | 'ctaHref'
  >
> = {
  CRITICAL: {
    title: 'Une qualification rapide est recommandée',
    consequence:
      'Vos réponses cumulent plusieurs signaux de fragilité. Elles ne permettent toutefois pas de confirmer à elles seules une panne, une faille ou une perte de données.',
    recommendation:
      'Commencez par faire qualifier la situation avant toute modification importante.',
    nextStepReason:
      'Cette qualification permet de distinguer ce qui doit être stabilisé rapidement de ce qui peut être traité dans un second temps.',
    urgencyMessage:
      'Priorité indicative : élevée. Si votre activité est déjà bloquée ou si un incident est en cours, utilisez le parcours urgence.',
    outcomeMessage:
      'L’objectif est d’obtenir un état des lieux compréhensible, un ordre de priorité et un cadre d’intervention validé.',
    selectionMessage:
      'Le périmètre, les délais et les accès éventuellement nécessaires sont confirmés après un échange humain.',
    cta: 'Demander une qualification',
    ctaHref: '/urgence',
  },

  AUDIT: {
    title: 'Une vérification structurée est recommandée',
    consequence:
      'Vos réponses montrent des fragilités possibles, sans permettre de confirmer leur origine ou leur gravité.',
    recommendation:
      'Un audit ciblé permettra de vérifier les faits avant de choisir entre réparation, sécurisation ou refonte.',
    nextStepReason:
      'Cette étape évite de modifier le site au hasard et permet de classer les actions selon leur impact réel.',
    urgencyMessage:
      'Priorité indicative : modérée. Aucun incident critique n’est établi par ce questionnaire.',
    outcomeMessage:
      'L’objectif est de savoir ce qui fonctionne, ce qui doit être corrigé et ce qui peut attendre.',
    selectionMessage:
      'La recommandation définitive dépendra de l’examen du contexte et du périmètre réel.',
    cta: 'Demander un audit',
    ctaHref: '/audit-site-web',
  },

  TRANSMISSION: {
    title: 'La maîtrise des accès doit être renforcée',
    consequence:
      'Vos réponses indiquent une dépendance organisationnelle susceptible de compliquer la maintenance ou la continuité de l’activité.',
    recommendation:
      'Commencez par inventorier les accès, les responsabilités et la documentation disponible.',
    nextStepReason:
      'Le principal risque semble lié à la transmission et à la gouvernance avant d’être purement technique.',
    urgencyMessage:
      'Priorité indicative : modérée. La situation doit être clarifiée avant qu’une indisponibilité ne transforme cette dépendance en blocage.',
    outcomeMessage:
      'L’objectif est que votre organisation sache qui possède quoi, qui peut intervenir et comment reprendre la main.',
    selectionMessage:
      'Aucun transfert d’accès ni changement de compte n’est réalisé sans validation explicite.',
    cta: 'Clarifier mes accès',
    ctaHref: '/transmission-acces',
  },

  MAINTENANCE: {
    title: 'Aucun signal prioritaire ne ressort de vos réponses',
    consequence:
      'Ce résultat ne garantit pas l’absence de vulnérabilité ou de défaut, car aucun contrôle technique n’a encore été effectué.',
    recommendation:
      'Conservez une routine simple de maintenance, de sauvegarde et de vérification des accès.',
    nextStepReason:
      'Une vérification ponctuelle peut suffire si vous souhaitez confirmer la stabilité de la situation.',
    urgencyMessage:
      'Priorité indicative : faible. Vos réponses ne décrivent pas de blocage immédiat.',
    outcomeMessage:
      'L’objectif est de vérifier les points essentiels sans engager de chantier disproportionné.',
    selectionMessage:
      'Si aucun besoin concret n’est identifié après échange, aucune intervention ne sera proposée.',
    cta: 'Demander une vérification',
    ctaHref: '/rendez-vous',
  },
};

const describeStructure = (
  answers: DiagnosticAnswersLike,
) => {
  if (answers.structure === 'association') {
    return 'Votre association ou collectif';
  }

  if (answers.structure === 'school') {
    return 'Votre structure éducative';
  }

  if (answers.structure === 'small-business') {
    return 'Votre petite entreprise';
  }

  if (answers.structure === 'freelance') {
    return 'Votre activité indépendante';
  }

  if (answers.structureOther) {
    return answers.structureOther;
  }

  return 'Votre organisation';
};

const buildImmediateContext = (
  answers: DiagnosticAnswersLike,
  reasons: string[],
) => {
  const structure = describeStructure(answers);

  const readableReasons = reasons.length
    ? reasons
      .map((reason) => reason.toLowerCase())
      .join(', ')
    : 'une situation globalement stable';

  return `${structure} présente, d’après vos réponses, ${readableReasons}. Ce pré-diagnostic est déclaratif : il ne vérifie ni votre site, ni vos accès, ni vos sauvegardes.`;
};

export const buildImmediateDiagnosticResult = (
  answers: DiagnosticAnswersLike,
): ImmediateDiagnosticResult => {
  let urgency = 0;
  let fragility = 0;
  let dependency = 0;

  const reasons: string[] = [];

  if (answers.stress === 'backups') {
    urgency += 4;
    fragility += 3;
    reasons.push('Sauvegardes ou données insuffisamment maîtrisées');
  } else if (answers.stress === 'site-slow') {
    urgency += 3;
    fragility += 3;
    reasons.push('Ralentissements devenus récurrents');
  } else if (answers.stress === 'single-person') {
    dependency += 4;
    reasons.push('Dépendance importante à une seule personne');
  } else if (answers.stress === 'some') {
    urgency += 1;
    fragility += 1;
  }

  if (answers.siteState === 'fragile') {
    fragility += 4;
    reasons.push('Site perçu comme ancien, fragile ou lent');
  } else if (answers.siteState === 'none') {
    fragility += 2;
    reasons.push('Présence web encore à structurer');
  } else if (answers.siteState === 'doubt') {
    fragility += 2;
    reasons.push('Doutes sur la stabilité du site');
  }

  if (answers.dependency === 'one') {
    dependency += 4;
    reasons.push(
      'Accès ou maintenance concentrés auprès d’une seule personne',
    );
  } else if (answers.dependency === 'unclear') {
    dependency += 3;
    reasons.push('Responsabilités numériques insuffisamment définies');
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

  const riskLevel: RiskLevel = path === 'CRITICAL'
    ? 'élevé'
    : path === 'MAINTENANCE'
      ? 'faible'
      : 'modéré';

  const meta = pathMeta[path];

  return {
    path,
    riskLevel,
    ...meta,
    context: buildImmediateContext(answers, reasons),
    reasons: reasons.length
      ? reasons
      : ['Aucun signal prioritaire déclaré dans vos réponses'],
    scores: {
      urgency,
      fragility,
      dependency,
      total,
    },
  };
};

export const buildContext = (
  ticket: DiagnosticTicket,
) => {
  const structure = describeStructure(ticket.answers);
  const fragments: string[] = [];

  if (ticket.answers.siteState === 'fragile') {
    fragments.push('un site décrit comme ancien, fragile ou lent');
  } else if (ticket.answers.siteState === 'none') {
    fragments.push('une présence web encore à construire');
  } else if (ticket.answers.siteState === 'doubt') {
    fragments.push('un site fonctionnel qui suscite des doutes');
  } else if (ticket.answers.siteState === 'security-check') {
    fragments.push('un souhait de vérifier la sécurité du site');
  }

  if (ticket.answers.dependency === 'one') {
    fragments.push('une dépendance forte à une seule personne');
  } else if (ticket.answers.dependency === 'unclear') {
    fragments.push('des responsabilités insuffisamment définies');
  } else if (ticket.answers.dependency === 'team-clear') {
    fragments.push('une équipe et une documentation déjà en place');
  }

  if (ticket.answers.stress === 'backups') {
    fragments.push('une incertitude sur les sauvegardes ou les données');
  } else if (ticket.answers.stress === 'site-slow') {
    fragments.push('des ralentissements récurrents');
  } else if (ticket.answers.stress === 'single-person') {
    fragments.push('un point de dépendance humaine identifié');
  }

  const situation = fragments.join(', ')
    || 'une situation déclarée comme globalement stable';

  return `${structure} décrit ${situation}. Ce résultat repose sur les réponses fournies et ne constitue ni un audit technique, ni une garantie de sécurité.`;
};

export const buildResultContent = (
  ticket: DiagnosticTicket,
): ResultContent => {
  const context = buildContext(ticket);

  if (ticket.diagnosticResult.path === 'CRITICAL') {
    return {
      kicker: 'Pré-diagnostic — priorité élevée',
      title: 'Faites qualifier la situation avant toute modification',
      context,
      advice:
        'La première étape consiste à confirmer les symptômes, les impacts et les accès disponibles avant de décider d’une réparation ou d’une refonte.',
      reasons: [
        'Distinguer un incident actif d’une fragilité potentielle',
        'Préserver les données et les accès existants',
        'Définir un ordre d’intervention compréhensible',
      ],
      pixelTitle: 'Ce que PixelProwlers peut cadrer',
      pixelItems: [
        'Qualification de la situation et de son impact',
        'Inventaire des accès et sauvegardes disponibles',
        'Priorisation des actions sans modification non autorisée',
        'Périmètre et délais confirmés après analyse',
      ],
      alternativeItems: [
        'Contacter votre hébergeur si son infrastructure est concernée',
        'Faire intervenir votre prestataire actuel s’il possède le contexte',
        'Solliciter un spécialiste local pour une qualification indépendante',
      ],
      honestAdvice:
        'Si votre activité est actuellement bloquée, signalez clairement l’incident. Ne transmettez aucun mot de passe dans un formulaire ou un email non prévu à cet effet.',
      cta: 'Demander une qualification',
      ctaHref: '/urgence',
    };
  }

  if (ticket.diagnosticResult.path === 'AUDIT') {
    return {
      kicker: 'Pré-diagnostic — vérification recommandée',
      title: 'Vérifiez les faits avant de choisir les travaux',
      context,
      advice:
        'Un audit ciblé peut distinguer les défauts avérés, les risques potentiels et les améliorations simplement souhaitables.',
      reasons: [
        'Identifier les problèmes réellement observables',
        'Classer les actions selon leur impact',
        'Déterminer si une réparation suffit',
      ],
      pixelTitle: 'Ce que PixelProwlers peut examiner',
      pixelItems: [
        'Stabilité et fonctionnement visible du site',
        'Accès, sauvegardes et dépendances déclarées',
        'Restitution lisible avec priorités',
        'Proposition séparée si des travaux sont nécessaires',
      ],
      alternativeItems: [
        'Réaliser une vérification interne avec une checklist documentée',
        'Demander un audit indépendant à un autre prestataire',
        'Consulter votre hébergeur sur les éléments relevant de son service',
      ],
      honestAdvice:
        'Le questionnaire ne permet pas de confirmer une faille. Une recommandation définitive exige un périmètre clair et des vérifications adaptées.',
      cta: 'Demander un audit',
      ctaHref: '/audit-site-web',
    };
  }

  if (ticket.diagnosticResult.path === 'TRANSMISSION') {
    return {
      kicker: 'Pré-diagnostic — transmission',
      title: 'Réduisez la dépendance autour de vos accès',
      context,
      advice:
        'Commencez par identifier les comptes, les propriétaires, les responsabilités et les procédures réellement disponibles.',
      reasons: [
        'Éviter qu’une absence bloque l’activité',
        'Clarifier les responsabilités',
        'Préparer une transmission réversible',
      ],
      pixelTitle: 'Ce que PixelProwlers peut organiser',
      pixelItems: [
        'Inventaire partagé des comptes et responsabilités',
        'Identification des accès manquants ou incertains',
        'Documentation des procédures essentielles',
        'Plan de transmission validé avec votre organisation',
      ],
      alternativeItems: [
        'Organiser l’inventaire avec la personne actuellement responsable',
        'Centraliser la documentation dans un espace maîtrisé',
        'Faire vérifier l’inventaire par un prestataire indépendant',
      ],
      honestAdvice:
        'Ne changez pas tous les accès sans inventaire ni plan de retour. Une transmission fiable doit préserver la continuité de service.',
      cta: 'Clarifier mes accès',
      ctaHref: '/transmission-acces',
    };
  }

  return {
    kicker: 'Pré-diagnostic — vigilance courante',
    title: 'Aucun signal prioritaire ne ressort du questionnaire',
    context,
    advice:
      'Maintenez une routine documentée pour les mises à jour, les sauvegardes et la révision des accès.',
    reasons: [
      'Contrôler régulièrement les mises à jour',
      'Tester la restauration des sauvegardes',
      'Supprimer les accès devenus inutiles',
      'Conserver une documentation à jour',
    ],
    pixelTitle: 'Ce que PixelProwlers peut vérifier',
    pixelItems: [
      'Contrôle ponctuel des points essentiels',
      'Identification des améliorations réellement utiles',
      'Restitution lisible et proportionnée',
      'Aucun chantier proposé sans besoin identifié',
    ],
    alternativeItems: [
      'Utiliser une checklist de maintenance interne',
      'Activer un suivi de disponibilité simple',
      'Planifier une révision périodique des accès',
    ],
    honestAdvice:
      'Ce résultat ne garantit pas l’absence de vulnérabilité. Il indique seulement qu’aucun signal prioritaire ne ressort de vos réponses.',
    cta: 'Demander une vérification',
    ctaHref: '/rendez-vous',
  };
};

export const emailConfirmationLabel = (
  ticket: DiagnosticTicket | null,
) => {
  const status = ticket?.emailConfirmation?.status;

  if (status === 'sent') {
    return 'Email de confirmation envoyé à';
  }

  if (status === 'failed') {
    return 'Email de confirmation non envoyé — adresse prévue';
  }

  return 'Adresse email enregistrée';
};

const createProgressSessionId = () => {
  if (
    typeof window !== 'undefined'
    && typeof window.crypto?.randomUUID === 'function'
  ) {
    return window.crypto.randomUUID();
  }

  return `diagnostic-${Date.now()}-${Math.random()
    .toString(16)
    .slice(2)}`;
};

export const useDiagnostic = () => {
  const router = useRouter();

  const currentStep = ref(0);
  const immediateResult = ref<ImmediateDiagnosticResult | null>(null);
  const progressSessionId = ref('');
  const isSubmitting = ref(false);
  const submitError = ref('');
  const hasAttemptedSubmit = ref(false);

  const answers = reactive<DiagnosticAnswersState>({
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
    privacyAcknowledged: false,
  });

  const contactErrors = reactive<
    Partial<Record<DiagnosticContactField, string>>
  >({});

  const activeStep = computed(
    () => diagnosticSteps[currentStep.value],
  );

  const isLastStep = computed(
    () => currentStep.value === diagnosticSteps.length - 1,
  );

  const progressPercent = computed(
    () => (
      (currentStep.value + 1)
      / diagnosticSteps.length
    ) * 100,
  );

  const dossierStatus = computed(() => {
    if (isSubmitting.value) {
      return 'Enregistrement de la demande en cours';
    }

    if (immediateResult.value) {
      return 'Résultat indicatif du pré-diagnostic prêt';
    }

    if (currentStep.value === 0) {
      return 'Pré-diagnostic démarré';
    }

    return `Étape ${currentStep.value} sur ${diagnosticSteps.length} complétée`;
  });

  const canContinue = computed(() => {
    const step = activeStep.value;

    if (!step) {
      return false;
    }

    const value = answers[step.id];

    return Boolean(
      value
      && (
        value !== 'other'
        || answers.structureOther.trim().length >= 2
      ),
    );
  });

  const canSubmit = computed(
    () => diagnosticContactSchema.safeParse(contact).success,
  );

  const clearContactErrors = () => {
    for (const field of contactFields) {
      delete contactErrors[field];
    }
  };

  const validateContact = () => {
    const result = diagnosticContactSchema.safeParse(contact);

    clearContactErrors();

    if (!result.success) {
      for (const issue of result.error.issues) {
        const field = issue.path[0];

        if (
          typeof field === 'string'
          && contactFields.includes(
            field as DiagnosticContactField,
          )
          && !contactErrors[field as DiagnosticContactField]
        ) {
          contactErrors[field as DiagnosticContactField] = issue.message;
        }
      }
    }

    return result;
  };

  const formatPhoneOnBlur = () => {
    const result = contactPhoneSchema.safeParse(contact.phone);

    if (result.success) {
      contact.phone = formatFrenchPhone(result.data);
    }
  };

  const nextStep = () => {
    submitError.value = '';

    if (!canContinue.value) {
      return;
    }

    const step = activeStep.value;

    if (
      step
      && step.id === 'structure'
      && answers.structure !== 'other'
    ) {
      answers.structureOther = '';
    }

    if (currentStep.value < diagnosticSteps.length - 1) {
      currentStep.value += 1;
      return;
    }

    const result = diagnosticAnswersSchema.safeParse({
      ...answers,
    });

    if (!result.success) {
      submitError.value =
        'Vérifiez vos réponses avant d’afficher le résultat.';
      return;
    }

    immediateResult.value = buildImmediateDiagnosticResult(
      result.data,
    );
  };

  const previousStep = () => {
    const resultWasDisplayed = Boolean(immediateResult.value);

    immediateResult.value = null;
    submitError.value = '';

    if (
      !resultWasDisplayed
      && currentStep.value > 0
    ) {
      currentStep.value -= 1;
    }
  };

  const submit = async () => {
    if (isSubmitting.value || !immediateResult.value) {
      return;
    }

    hasAttemptedSubmit.value = true;
    submitError.value = '';

    const contactValidation = validateContact();

    const answersValidation = diagnosticAnswersSchema.safeParse({
      ...answers,
    });

    if (!contactValidation.success) {
      submitError.value =
        'Vérifiez les informations demandées avant d’envoyer le formulaire.';
      return;
    }

    if (!answersValidation.success) {
      submitError.value =
        'Les réponses du pré-diagnostic sont incomplètes. Revenez au questionnaire pour les vérifier.';
      return;
    }

    isSubmitting.value = true;

    try {
      const normalizedContact = contactValidation.data;

      const result = await graphqlRequest<{
        createDiagnosticTicket: {
          redirectTo: string;
        };
      }>(
        CREATE_DIAGNOSTIC_TICKET_MUTATION,
        {
          organization: normalizedContact.name,
          email: normalizedContact.email,
          phone: normalizedContact.phone,
          message: normalizedContact.message,
          answers: JSON.stringify({
            ...answersValidation.data,
            immediateResult: immediateResult.value,
            progressSessionId: progressSessionId.value,
            privacyAcknowledged: true,
            privacyNoticeVersion: PRIVACY_NOTICE_VERSION,
          }),
        },
      );

      await router.push(
        result.createDiagnosticTicket.redirectTo,
      );
    } catch {
      submitError.value =
        'Impossible d’enregistrer votre demande pour le moment. Vous pouvez réessayer ou appeler PixelProwlers au 06 68 14 51 52.';
    } finally {
      isSubmitting.value = false;
    }
  };

  onMounted(() => {
    const storageKey = 'pixelprowlers:diagnostic-session';

    try {
      const existingSessionId = window.localStorage.getItem(
        storageKey,
      );

      const sessionId = existingSessionId
        || createProgressSessionId();

      progressSessionId.value = sessionId;

      window.localStorage.setItem(
        storageKey,
        sessionId,
      );

      const saved = window.localStorage.getItem(
        `${storageKey}:answers`,
      );

      if (!saved) {
        return;
      }

      const savedAnswers = parseGraphqlJson(
        saved,
        {},
      ) as Record<string, unknown>;

      for (const key of answerKeys) {
        const value = savedAnswers[key];

        if (
          typeof value === 'string'
          && value.length <= 160
        ) {
          answers[key] = value;
        }
      }
    } catch {
      progressSessionId.value = createProgressSessionId();
    }
  });

  watch(
    answers,
    () => {
      if (
        !import.meta.client
        || !progressSessionId.value
      ) {
        return;
      }

      try {
        window.localStorage.setItem(
          'pixelprowlers:diagnostic-session:answers',
          JSON.stringify({ ...answers }),
        );
      } catch {
        /*
         * Le stockage local améliore seulement la reprise du parcours.
         * Son indisponibilité ne doit jamais bloquer le formulaire.
         */
      }
    },
    {
      deep: true,
    },
  );

  watch(
    contact,
    () => {
      if (hasAttemptedSubmit.value) {
        validateContact();
      }
    },
    {
      deep: true,
    },
  );

  return {
    currentStep,
    answers,
    contact,
    contactErrors,
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
    formatPhoneOnBlur,
    nextStep,
    previousStep,
    submit,
  };
};

export const useDiagnosticResult = () => {
  const ticket = ref<DiagnosticTicket | null>(null);
  const isLoading = ref(false);
  const error = ref('');

  const content = computed(
    () => (
      ticket.value
        ? buildResultContent(ticket.value)
        : null
    ),
  );

  const maskedEmail = computed(
    () => maskEmail(ticket.value?.email || ''),
  );

  const load = async (ticketId: string) => {
    if (!ticketId) {
      error.value =
        'Le lien ne contient pas de numéro de ticket.';
      return;
    }

    isLoading.value = true;
    error.value = '';

    try {
      const result = await graphqlRequest<{
        diagnosticTicket: DiagnosticTicketGraphql;
      }>(
        DIAGNOSTIC_TICKET_QUERY,
        {
          ticketId,
        },
      );

      ticket.value = mapDiagnosticTicket(
        result.diagnosticTicket,
      );
    } catch {
      ticket.value = null;
      error.value =
        'Le ticket demandé est absent ou a expiré.';
    } finally {
      isLoading.value = false;
    }
  };

  return {
    ticket,
    isLoading,
    error,
    content,
    maskedEmail,
    load,
  };
};