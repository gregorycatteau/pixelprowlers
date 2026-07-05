import { computed, reactive, ref } from 'vue';
import {
  refonteIdentitySchema,
  type RefonteIdentity,
} from '~/validation/schemas';

export type RefonteQuestionType = 'text' | 'select' | 'radio' | 'checkbox' | 'boolean';

export type RefonteQuestion = {
  id: string;
  label: string;
  type: RefonteQuestionType;
  options?: string[];
  placeholder?: string;
};

export type RefonteSeries = {
  id: string;
  label: string;
  questions: RefonteQuestion[];
};

export type RefonteAnswers = Record<string, string | string[] | boolean>;

export type RefonteAuditResult = {
  reference: string;
  site_url: string;
  analysis_status: 'en_cours' | 'termine' | 'echec_partiel' | 'non_analysable' | 'echec';
  technical_report: Record<string, any>;
  pagespeed_report: Record<string, any>;
  heuristic_report: Array<{ name: string; score: string; justification: string }>;
  analysis_error: string;
  date_creation: string;
  date_maj: string;
};

export const refonteSeries: RefonteSeries[] = [
  {
    id: 'contexte_objectifs',
    label: 'Contexte & objectifs',
    questions: [
      { id: 'refonte_raison', label: 'Pourquoi envisagez-vous une refonte maintenant ?', type: 'text', placeholder: 'Ce qui déclenche la réflexion aujourd’hui' },
      { id: 'objectif_principal', label: "Quel est l'objectif principal ?", type: 'select', options: ['Plus de leads', 'Image de marque', 'Vente en ligne', 'Clarifier l’offre', 'Autre'] },
      { id: 'budget_approx', label: 'Avez-vous une enveloppe approximative en tête ?', type: 'select', options: ['À cadrer ensemble', 'Petite enveloppe', 'Enveloppe intermédiaire', 'Projet stratégique', 'Je ne sais pas'] },
      { id: 'delai_lancement', label: 'Sous quel délai souhaitez-vous lancer le nouveau site ?', type: 'radio', options: ['Dès que possible', 'Sous 1 à 3 mois', 'Sous 3 à 6 mois', 'Plus tard', 'À définir'] },
      { id: 'decisionnaires', label: 'Qui est impliqué dans la décision ?', type: 'checkbox', options: ['Moi seul', 'Associé', 'Équipe', 'Direction', 'Partenaire externe'] },
    ],
  },
  {
    id: 'existant',
    label: 'Existant',
    questions: [
      { id: 'fonctionne_bien', label: "Qu'est-ce qui fonctionne bien sur votre site actuel ?", type: 'text', placeholder: 'Pages, contenus ou usages à préserver' },
      { id: 'frustrations', label: "Qu'est-ce qui ne fonctionne pas ou vous frustre ?", type: 'text', placeholder: 'Lenteur, maintenance, image, conversions...' },
      { id: 'contenus_a_conserver', label: 'Y a-t-il du contenu à conserver absolument ?', type: 'text', placeholder: 'Textes, images, articles, ressources...' },
      { id: 'cms_actuel', label: 'Le site actuel est-il sur un CMS particulier ?', type: 'select', options: ['WordPress', 'Shopify', 'Webflow', 'Prestashop', 'Développement maison', 'Je ne sais pas', 'Autre'] },
      { id: 'acces_hebergement', label: "Avez-vous accès aux identifiants d'hébergement/nom de domaine ?", type: 'radio', options: ['Oui', 'Non', 'Partiellement', 'Je ne sais pas'] },
    ],
  },
  {
    id: 'cible_positionnement',
    label: 'Cible & positionnement',
    questions: [
      { id: 'client_ideal', label: 'Qui est votre client idéal ?', type: 'text', placeholder: 'Profil, besoin, secteur ou niveau de maturité' },
      { id: 'concurrents_inspiration', label: 'Avez-vous des sites concurrents ou inspirants ?', type: 'text', placeholder: 'URLs ou noms, si vous en avez' },
      { id: 'ton_marque', label: 'Comment décririez-vous le ton de votre marque ?', type: 'checkbox', options: ['Sérieux', 'Chaleureux', 'Premium', 'Fun', 'Sobre', 'Engagé'] },
      { id: 'charte_graphique', label: 'Avez-vous une charte graphique existante ?', type: 'radio', options: ['Oui complète', 'Logo seulement', 'Quelques couleurs', 'Non', 'À reprendre'] },
      { id: 'portee_public', label: 'Le site doit-il parler à quel public ?', type: 'select', options: ['Local', 'Régional', 'National', 'International', 'Plusieurs publics'] },
    ],
  },
  {
    id: 'fonctionnalites',
    label: 'Fonctionnalités souhaitées',
    questions: [
      { id: 'boutique_paiement', label: "Avez-vous besoin d'une boutique en ligne ou paiement ?", type: 'boolean' },
      { id: 'blog_contenu', label: "Avez-vous besoin d'un blog ou contenu régulièrement mis à jour ?", type: 'boolean' },
      { id: 'multilingue', label: 'Le site doit-il être multilingue ?', type: 'boolean' },
      { id: 'integrations', label: "Avez-vous besoin d'intégrations spécifiques ?", type: 'checkbox', options: ['CRM', 'Newsletter', 'Prise de rendez-vous', 'Paiement', 'Analytics', 'Autre'] },
      { id: 'espace_client', label: 'Le site doit-il gérer un espace client ou membre connecté ?', type: 'boolean' },
    ],
  },
];

const questionIds = refonteSeries.flatMap((serie) => serie.questions.map((question) => question.id));

const defaultAnswers = () => Object.fromEntries(
  refonteSeries.flatMap((serie) => serie.questions.map((question) => [
    question.id,
    question.type === 'checkbox' ? [] : question.type === 'boolean' ? false : '',
  ])),
) as RefonteAnswers;

export const useRefonteAudit = () => {
  const identity = ref<RefonteIdentity | null>(null);
  const answers = reactive<RefonteAnswers>(defaultAnswers());
  const currentSeriesIndex = ref(0);
  const reference = ref('');
  const createError = ref('');
  const isSubmitting = ref(false);

  const activeSeries = computed(() => refonteSeries[currentSeriesIndex.value]);
  const isLastSeries = computed(() => currentSeriesIndex.value === refonteSeries.length - 1);
  const progressPercent = computed(() => ((currentSeriesIndex.value + 1) / refonteSeries.length) * 100);
  const progressLabel = computed(() => `Bloc ${currentSeriesIndex.value + 1} sur ${refonteSeries.length}`);
  const hasIdentity = computed(() => Boolean(identity.value));

  const canContinue = computed(() => activeSeries.value.questions.every((question) => isAnswered(answers[question.id])));
  const canSubmit = computed(() => Boolean(identity.value) && questionIds.every((id) => isAnswered(answers[id])));

  const setIdentity = (payload: RefonteIdentity) => {
    const parsed = refonteIdentitySchema.safeParse(payload);
    if (!parsed.success) {
      createError.value = 'Les coordonnées sont incomplètes.';
      return false;
    }
    identity.value = parsed.data;
    createError.value = '';
    return true;
  };

  const nextSeries = () => {
    if (canContinue.value && currentSeriesIndex.value < refonteSeries.length - 1) {
      currentSeriesIndex.value += 1;
    }
  };

  const previousSeries = () => {
    if (currentSeriesIndex.value > 0) {
      currentSeriesIndex.value -= 1;
    }
  };

  const submit = async () => {
    if (!identity.value || !canSubmit.value) return '';

    isSubmitting.value = true;
    createError.value = '';

    try {
      const response = await $fetch<{ reference: string; analysis_status: string }>('/api/audit-refonte', {
        method: 'POST',
        body: {
          ...identity.value,
          reponses: answers,
        },
      });
      reference.value = response.reference;
      await navigateTo(`/audit-refonte/resultat?reference=${encodeURIComponent(response.reference)}`);
      return response.reference;
    } catch (error) {
      createError.value = typeof error === 'object' && error && 'statusMessage' in error
        ? String(error.statusMessage)
        : "Impossible d'enregistrer l'audit refonte pour le moment.";
      return '';
    } finally {
      isSubmitting.value = false;
    }
  };

  return {
    answers,
    identity,
    reference,
    currentSeriesIndex,
    activeSeries,
    isLastSeries,
    progressPercent,
    progressLabel,
    hasIdentity,
    canContinue,
    canSubmit,
    createError,
    isSubmitting,
    setIdentity,
    nextSeries,
    previousSeries,
    submit,
  };
};

function isAnswered(value: string | string[] | boolean) {
  if (Array.isArray(value)) return value.length > 0;
  if (typeof value === 'boolean') return true;
  return value.trim().length > 0;
}
