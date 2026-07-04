import { computed, reactive, ref } from 'vue';
import { isEmailLike } from '~/utils/formatDate';

export type ContactDemandType = 'diagnostic' | 'urgency' | 'audit' | 'refonte' | 'transmission' | 'partnership';
export type ContactStatus = 'open' | 'in_progress' | 'waiting_customer' | 'resolved' | 'closed';

export type ContactTicket = {
  ticketId: string;
  secretToken: string;
  organization: string;
  email: string;
  phone: string;
  demandType: ContactDemandType;
  demandLabel: string;
  message: string;
  status: ContactStatus;
  messages: Array<{
    id: string;
    author: 'customer' | 'support' | 'system';
    authorName: string;
    message: string;
    createdAt: string;
  }>;
  emailConfirmation: {
    status: 'sent' | 'not_configured' | 'failed';
  };
  createdAt: string;
  updatedAt: string;
};

export const contactDemandOptions: Array<{ label: string; value: ContactDemandType }> = [
  { label: 'Je veux un diagnostic', value: 'diagnostic' },
  { label: "J'ai une urgence maintenant", value: 'urgency' },
  { label: "Je veux parler d'un audit", value: 'audit' },
  { label: "Je veux parler d'une refonte", value: 'refonte' },
  { label: 'Je veux parler de transmission', value: 'transmission' },
  { label: 'Partenariat / autre', value: 'partnership' },
];

export const contactEmailLabel = (ticket: ContactTicket | null) => {
  const status = ticket?.emailConfirmation?.status;

  if (status === 'sent') {
    return 'Email de confirmation envoyé à';
  }

  if (status === 'failed') {
    return "Email de confirmation non envoyé, adresse prévue";
  }

  return 'Email de confirmation prêt pour';
};

export const statusLabel = (status: ContactStatus) => ({
  open: 'Ouvert',
  in_progress: 'En cours',
  waiting_customer: 'En attente client',
  resolved: 'Résolu',
  closed: 'Fermé',
}[status] || status);

export const useContactForm = () => {
  const form = reactive({
    demandType: '' as ContactDemandType | '',
    organization: '',
    email: '',
    phone: '',
    message: '',
  });
  const ticket = ref<ContactTicket | null>(null);
  const submitError = ref('');
  const isSubmitting = ref(false);

  const canSubmit = computed(() => (
    Boolean(form.demandType)
    && form.organization.trim().length > 0
    && isEmailLike(form.email)
    && form.message.trim().length > 0
  ));

  const submit = async () => {
    if (!canSubmit.value || isSubmitting.value) {
      return null;
    }

    isSubmitting.value = true;
    submitError.value = '';

    try {
      const created = await $fetch<ContactTicket & { confirmationUrl: string }>('/api/contact', {
        method: 'POST',
        body: form,
      });
      ticket.value = created;
      return created;
    } catch {
      submitError.value = "Impossible d'ouvrir le ticket pour le moment. Vous pouvez réessayer dans quelques instants.";
      return null;
    } finally {
      isSubmitting.value = false;
    }
  };

  return { form, ticket, submitError, isSubmitting, canSubmit, submit };
};

export const useContactTicket = () => {
  const ticket = ref<ContactTicket | null>(null);
  const error = ref('');
  const isLoading = ref(false);
  const reply = ref('');
  const replyError = ref('');
  const isAddingReply = ref(false);

  const load = async (token: string) => {
    if (!token) {
      ticket.value = null;
      error.value = 'Le lien ne contient pas de token de suivi.';
      return;
    }

    isLoading.value = true;
    error.value = '';

    try {
      ticket.value = await $fetch<ContactTicket>(`/api/contact/${token}`);
    } catch {
      ticket.value = null;
      error.value = 'Le ticket est absent ou a expiré côté serveur.';
    } finally {
      isLoading.value = false;
    }
  };

  const addMessage = async () => {
    if (!ticket.value || !reply.value.trim() || isAddingReply.value) {
      return;
    }

    isAddingReply.value = true;
    replyError.value = '';

    try {
      ticket.value = await $fetch<ContactTicket>(`/api/contact/${ticket.value.secretToken}/add_message`, {
        method: 'POST',
        body: {
          message: reply.value,
          authorName: ticket.value.organization,
        },
      });
      reply.value = '';
    } catch {
      replyError.value = "Impossible d'ajouter ce message pour le moment.";
    } finally {
      isAddingReply.value = false;
    }
  };

  return { ticket, error, isLoading, reply, replyError, isAddingReply, load, addMessage };
};
