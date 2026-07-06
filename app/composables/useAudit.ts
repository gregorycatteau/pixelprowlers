import { computed, reactive, ref } from 'vue';
import {
  auditIdentitySchema,
  createAuditAnswersSchema,
  type AuditIdentity,
} from '~/validation/schemas';
import {
  CREATE_AUDIT_DOSSIER_MUTATION,
  graphqlErrorMessage,
  graphqlRequest,
  parseGraphqlJson,
  SUBMIT_AUDIT_REPONSES_MUTATION,
} from '~/utils/graphql';

export type AuditPersonType = 'individu' | 'association' | 'entreprise';

export type AuditQuestion = {
  id: string;
  label: string;
};

export type AuditSeries = {
  id: string;
  label: string;
  questions: AuditQuestion[];
};

export type AuditScoreSeries = Record<string, { label: string; score: number | string }>;

export type AuditResult = {
  numero_dossier: string;
  statut: string;
  scores_series: AuditScoreSeries;
  score_global: number | string;
  pilier_faible: string;
  notification_status: Record<string, string>;
};

export const auditSeries: AuditSeries[] = [
  {
    id: 'visibilite_presence',
    label: 'Visibilité & Présence en ligne',
    questions: [
      { id: 'visibilite_presence_1', label: 'Votre site permet-il de comprendre clairement qui vous êtes et ce que vous proposez ?' },
      { id: 'visibilite_presence_2', label: 'Votre site inspire-t-il confiance dès les premières secondes de navigation ?' },
      { id: 'visibilite_presence_3', label: 'Vos informations essentielles sont-elles faciles à trouver pour un visiteur ?' },
      { id: 'visibilite_presence_4', label: 'Votre présence en ligne reflète-t-elle votre activité actuelle ?' },
      { id: 'visibilite_presence_5', label: 'Vos contenus sont-ils suffisamment à jour pour éviter les malentendus ?' },
    ],
  },
  {
    id: 'organisation_processus',
    label: 'Organisation interne & Processus',
    questions: [
      { id: 'organisation_processus_1', label: 'Votre équipe sait-elle qui est responsable des outils numériques importants ?' },
      { id: 'organisation_processus_2', label: 'Vos procédures numériques sont-elles documentées et accessibles ?' },
      { id: 'organisation_processus_3', label: 'Pouvez-vous retrouver rapidement les informations utiles en cas de problème ?' },
      { id: 'organisation_processus_4', label: 'Vos accès sont-ils transmis proprement quand une personne change de rôle ?' },
      { id: 'organisation_processus_5', label: 'Votre organisation peut-elle continuer à fonctionner si la personne référente est absente ?' },
    ],
  },
  {
    id: 'outils_infrastructure',
    label: 'Outils & Infrastructure numérique',
    questions: [
      { id: 'outils_infrastructure_1', label: 'Vos outils numériques sont-ils adaptés à vos usages réels ?' },
      { id: 'outils_infrastructure_2', label: 'Vos sauvegardes sont-elles régulières et vérifiées ?' },
      { id: 'outils_infrastructure_3', label: 'Vos comptes importants sont-ils protégés par des accès robustes ?' },
      { id: 'outils_infrastructure_4', label: 'Votre site et vos services restent-ils performants dans les moments importants ?' },
      { id: 'outils_infrastructure_5', label: 'Votre infrastructure peut-elle être maintenue sans dépendance excessive à un prestataire unique ?' },
    ],
  },
  {
    id: 'relation_engagement',
    label: 'Relation & Engagement',
    questions: [
      { id: 'relation_engagement_1', label: 'Vos visiteurs savent-ils facilement comment vous contacter ?' },
      { id: 'relation_engagement_2', label: 'Vos formulaires ou canaux de contact fonctionnent-ils de manière fiable ?' },
      { id: 'relation_engagement_3', label: "Votre communication numérique donne-t-elle envie d'engager un échange ?" },
      { id: 'relation_engagement_4', label: 'Vos réponses aux demandes entrantes sont-elles suivies et organisées ?' },
      { id: 'relation_engagement_5', label: 'Votre présence numérique aide-t-elle réellement votre relation avec vos publics ?' },
    ],
  },
];

const phoneFrPattern = /^(?:\+33|0)[1-9](?:[\s.-]?\d{2}){4}$/;
const auditQuestionIds = auditSeries.flatMap((serie) => serie.questions.map((question) => question.id));
const auditAnswersSchema = createAuditAnswersSchema(auditQuestionIds);

const createIdentity = () => ({
  prenom: '',
  nom: '',
  email: '',
  telephone: '',
  type_personne: '' as AuditPersonType | '',
  nom_structure: '',
  consentement_rgpd: false,
});

const initialAnswers = () => Object.fromEntries(
  auditSeries.flatMap((serie) => serie.questions.map((question) => [question.id, 5])),
) as Record<string, number>;

export const useAudit = () => {
  const identity = reactive(createIdentity());
  const answers = reactive<Record<string, number>>(initialAnswers());
  const numeroDossier = ref('');
  const currentSeriesIndex = ref(0);
  const result = ref<AuditResult | null>(null);
  const createError = ref('');
  const submitError = ref('');
  const isCreatingDossier = ref(false);
  const isSubmittingResponses = ref(false);

  const activeSeries = computed(() => auditSeries[currentSeriesIndex.value]);
  const hasDossier = computed(() => Boolean(numeroDossier.value));
  const isLastSeries = computed(() => currentSeriesIndex.value === auditSeries.length - 1);
  const progressLabel = computed(() => `Step ${currentSeriesIndex.value + 1}/4`);
  const progressPercent = computed(() => ((currentSeriesIndex.value + 1) / auditSeries.length) * 100);
  const needsStructure = computed(() => identity.type_personne === 'association' || identity.type_personne === 'entreprise');

  const canCreateDossier = computed(() => auditIdentitySchema.safeParse(identity).success);

  type CreateAuditDossierResponse = {
    createAuditDossier: {
      dossier: {
        numeroDossier: string;
        statut: string;
      };
    };
  };

  type SubmitAuditReponsesResponse = {
    submitAuditReponses: {
      numero_dossier: string;
      statut: string;
      scores_series: AuditScoreSeries | string;
      score_global: number | string;
      pilier_faible: string;
      notification_status: Record<string, string> | string;
    };
  };

  const createDossier = async (payload?: AuditIdentity) => {
    const parsedIdentity = payload || auditIdentitySchema.safeParse(identity);

    if (isCreatingDossier.value) {
      return;
    }

    isCreatingDossier.value = true;
    createError.value = '';

    try {
      const data = 'success' in parsedIdentity
        ? parsedIdentity.success ? parsedIdentity.data : null
        : parsedIdentity;

      if (!data) {
        createError.value = 'Certains champs du dossier sont encore invalides.';
        return;
      }

      const response = await graphqlRequest<CreateAuditDossierResponse>(CREATE_AUDIT_DOSSIER_MUTATION, {
        consentementRgpd: data.consentement_rgpd,
        email: data.email,
        nom: data.nom,
        nomStructure: data.nom_structure || null,
        prenom: data.prenom,
        telephone: data.telephone,
        typePersonne: data.type_personne,
      });
      numeroDossier.value = response.createAuditDossier.dossier.numeroDossier;
    } catch (error) {
      createError.value = graphqlErrorMessage(error, "Impossible de créer le dossier d'audit pour le moment.");
    } finally {
      isCreatingDossier.value = false;
    }
  };

  const previousSeries = () => {
    if (currentSeriesIndex.value > 0) {
      currentSeriesIndex.value -= 1;
    }
  };

  const nextSeries = () => {
    if (currentSeriesIndex.value < auditSeries.length - 1) {
      currentSeriesIndex.value += 1;
    }
  };

  const submitResponses = async () => {
    if (!numeroDossier.value || isSubmittingResponses.value) {
      return;
    }

    isSubmittingResponses.value = true;
    submitError.value = '';

    try {
      const parsedAnswers = auditAnswersSchema.safeParse(answers);

      if (!parsedAnswers.success) {
        submitError.value = 'Une réponse a été modifiée hors des valeurs autorisées. Merci de vérifier le questionnaire.';
        return;
      }

      const response = await graphqlRequest<SubmitAuditReponsesResponse>(SUBMIT_AUDIT_REPONSES_MUTATION, {
        numeroDossier: numeroDossier.value,
        reponses: JSON.stringify(parsedAnswers.data),
      });

      result.value = {
        numero_dossier: response.submitAuditReponses.numero_dossier,
        statut: response.submitAuditReponses.statut,
        scores_series: parseGraphqlJson<AuditScoreSeries>(
          response.submitAuditReponses.scores_series,
          {},
        ),
        score_global: response.submitAuditReponses.score_global,
        pilier_faible: response.submitAuditReponses.pilier_faible,
        notification_status: parseGraphqlJson<Record<string, string>>(
          response.submitAuditReponses.notification_status,
          {},
        ),
      };
    } catch (error) {
      submitError.value = graphqlErrorMessage(error, "Impossible d'enregistrer les réponses pour le moment.");
    } finally {
      isSubmittingResponses.value = false;
    }
  };

  return {
    identity,
    answers,
    numeroDossier,
    currentSeriesIndex,
    result,
    createError,
    submitError,
    isCreatingDossier,
    isSubmittingResponses,
    activeSeries,
    hasDossier,
    isLastSeries,
    progressLabel,
    progressPercent,
    needsStructure,
    canCreateDossier,
    createDossier,
    previousSeries,
    nextSeries,
    submitResponses,
  };
};
