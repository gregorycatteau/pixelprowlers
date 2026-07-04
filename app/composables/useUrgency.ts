import { computed, reactive, ref } from 'vue';
import { isEmailLike } from '~/utils/formatDate';

export type UrgencyProblemType =
  | 'site_down'
  | 'suspected_hack'
  | 'broken_form'
  | 'email_dns_domain'
  | 'content_modified'
  | 'critical_error'
  | 'massive_slowdown'
  | 'other';

export type UrgencyImpactLevel = 'minor' | 'disrupted' | 'blocked' | 'security_data_risk';
export type UrgencyContactPreference = 'email' | 'phone' | 'either';
export type UrgencyExpectedNextStep =
  | 'understand_first'
  | 'quick_callback'
  | 'secure_before_action'
  | 'prepare_intervention'
  | 'need_guidance';

export type UrgencyResponse = {
  reference: string;
  status: 'open';
  clientEmailStatus: 'sent' | 'not_configured' | 'failed';
  message: string;
};

export const urgencyProblemOptions: Array<{ label: string; value: UrgencyProblemType }> = [
  { label: 'Site inaccessible', value: 'site_down' },
  { label: 'Suspicion de piratage', value: 'suspected_hack' },
  { label: 'Formulaire cassé', value: 'broken_form' },
  { label: 'Problème email / DNS / domaine', value: 'email_dns_domain' },
  { label: 'Contenu modifié', value: 'content_modified' },
  { label: 'Erreur critique', value: 'critical_error' },
  { label: 'Ralentissement massif', value: 'massive_slowdown' },
  { label: 'Autre', value: 'other' },
];

export const urgencyImpactOptions: Array<{ label: string; value: UrgencyImpactLevel }> = [
  { label: 'Simple gêne', value: 'minor' },
  { label: 'Activité perturbée', value: 'disrupted' },
  { label: 'Activité bloquée', value: 'blocked' },
  { label: 'Risque sécurité / données', value: 'security_data_risk' },
];

export const urgencyContactOptions: Array<{ label: string; value: UrgencyContactPreference }> = [
  { label: 'Email', value: 'email' },
  { label: 'Téléphone', value: 'phone' },
  { label: 'Le plus simple pour vous', value: 'either' },
];

export const urgencyNextStepOptions: Array<{ label: string; value: UrgencyExpectedNextStep }> = [
  { label: 'Je veux d’abord comprendre ce qui se passe', value: 'understand_first' },
  { label: 'Je souhaite être rappelé rapidement', value: 'quick_callback' },
  { label: 'Je veux sécuriser la situation avant d’agir', value: 'secure_before_action' },
  { label: 'Je veux préparer une intervention si nécessaire', value: 'prepare_intervention' },
  { label: 'Je ne sais pas encore, j’ai besoin d’être guidé', value: 'need_guidance' },
];

const createUrgencyForm = () => ({
  problemType: '' as UrgencyProblemType | '',
  impactLevel: '' as UrgencyImpactLevel | '',
  affectedUrl: '',
  shortDescription: '',
  sinceWhen: '',
  name: '',
  organization: '',
  email: '',
  phone: '',
  contactPreference: 'either' as UrgencyContactPreference,
  callbackSlot: '',
  expected_next_step: '' as UrgencyExpectedNextStep | '',
  consentToContact: false,
  noSecretsConfirmed: false,
  website: '',
});

export const useUrgency = () => {
  const form = reactive(createUrgencyForm());
  const result = ref<UrgencyResponse | null>(null);
  const submitError = ref('');
  const isSubmitting = ref(false);

  const canSubmit = computed(() => (
    Boolean(form.problemType)
    && Boolean(form.impactLevel)
    && form.affectedUrl.trim().length > 0
    && form.shortDescription.trim().length > 0
    && form.sinceWhen.trim().length > 0
    && form.name.trim().length > 0
    && form.organization.trim().length > 0
    && isEmailLike(form.email)
    && form.phone.trim().length >= 6
    && Boolean(form.contactPreference)
    && form.callbackSlot.trim().length > 0
    && Boolean(form.expected_next_step)
    && form.consentToContact
    && form.noSecretsConfirmed
  ));

  const reset = () => {
    Object.assign(form, createUrgencyForm());
    result.value = null;
    submitError.value = '';
  };

  // Envoie uniquement les informations utiles au triage, sans fichier ni secret volontaire.
  const submit = async () => {
    if (!canSubmit.value || isSubmitting.value) {
      return;
    }

    isSubmitting.value = true;
    submitError.value = '';

    try {
      result.value = await $fetch<UrgencyResponse>('/api/urgency', {
        method: 'POST',
        body: form,
      });
    } catch (error) {
      const statusMessage = typeof error === 'object' && error && 'statusMessage' in error
        ? String(error.statusMessage)
        : '';
      submitError.value = statusMessage || "Impossible d'enregistrer l'urgence pour le moment. Réessayez dans quelques instants.";
    } finally {
      isSubmitting.value = false;
    }
  };

  return {
    form,
    result,
    submitError,
    isSubmitting,
    canSubmit,
    reset,
    submit,
  };
};
