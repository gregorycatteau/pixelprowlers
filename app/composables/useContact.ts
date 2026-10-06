import { computed, reactive, ref } from 'vue';
import { isEmailLike } from '~/utils/formatDate';
import { graphqlRequest, parseGraphqlJson } from '~/utils/graphql';
import { buildContactMessage, contactApiMapping, CONTACT_MESSAGE_LIMIT, resolveContactNeed, type ContactNeed } from '~/utils/contactNeeds';

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


type ContactGraphql = {
  ticketId: string;
  secretToken: string;
  name: string;
  email: string;
  phone: string;
  company: string;
  demandType: ContactDemandType | '';
  demandLabel: string;
  message: string;
  status: ContactStatus;
  messages: ContactTicket['messages'];
  emailConfirmation: string | ContactTicket['emailConfirmation'];
  createdAt: string;
  updatedAt: string;
};

const CONTACT_FIELDS = /* GraphQL */ `
  {
    ticketId
    secretToken
    name
    email
    phone
    company
    demandType
    demandLabel
    message
    status
    messages {
      id
      author
      authorName
      message
      createdAt
    }
    emailConfirmation
    createdAt
    updatedAt
  }
`;

const CREATE_CONTACT_MUTATION = /* GraphQL */ `
  mutation CreateContact(
    $name: String!
    $email: String!
    $company: String
    $phone: String
    $serviceType: String!
    $demandType: String
    $message: String!
    $privacyConsent: Boolean
    $startedAt: Float
  ) {
    createContact(
      name: $name
      email: $email
      company: $company
      phone: $phone
      serviceType: $serviceType
      demandType: $demandType
      message: $message
      privacyConsent: $privacyConsent
      startedAt: $startedAt
    ) {
      contact ${CONTACT_FIELDS}
    }
  }
`;

const CONTACT_BY_TOKEN_QUERY = /* GraphQL */ `
  query ContactByToken($token: String!) {
    contactByToken(token: $token) ${CONTACT_FIELDS}
  }
`;

const ADD_CONTACT_MESSAGE_MUTATION = /* GraphQL */ `
  mutation AddContactMessage($token: String!, $message: String!, $authorName: String!) {
    addContactMessage(token: $token, message: $message, authorName: $authorName) {
      contact ${CONTACT_FIELDS}
    }
  }
`;


const mapContact = (contact: ContactGraphql): ContactTicket => ({
  ticketId: contact.ticketId,
  secretToken: contact.secretToken,
  organization: contact.company || contact.name,
  email: contact.email,
  phone: contact.phone || '',
  demandType: contact.demandType || 'partnership',
  demandLabel: contact.demandLabel,
  message: contact.message,
  status: contact.status,
  messages: contact.messages || [],
  emailConfirmation: parseGraphqlJson(contact.emailConfirmation, { status: 'not_configured' }),
  createdAt: contact.createdAt,
  updatedAt: contact.updatedAt,
});

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

/** Prépare et envoie une demande compatible avec l’API publiée, en conservant la saisie après erreur. */
export const useContactForm = (initialNeed: ContactNeed | '' = '') => {
  const form = reactive({
    need: resolveContactNeed(initialNeed),
    deviceType: '', model: '', usage: '', budget: '', repairContext: '',
    organization: '',
    email: '',
    phone: '',
    message: '',
  });
  const ticket = ref<ContactTicket | null>(null);
  const submitError = ref('');
  const isSubmitting = ref(false);

  const canSubmit = computed(() => (
    Boolean(resolveContactNeed(form.need))
    && form.organization.trim().length > 0 && form.organization.trim().length <= 160
    && isEmailLike(form.email) && form.email.trim().length <= 254
    && form.message.trim().length >= 20 && form.message.length <= 500
    && buildContactMessage(form).length <= CONTACT_MESSAGE_LIMIT
  ));

  const submit = async () => {
    if (!canSubmit.value || isSubmitting.value) {
      return null;
    }

    const need = resolveContactNeed(form.need);
    if (!need) return null;
    const message = buildContactMessage(form);
    isSubmitting.value = true;
    submitError.value = '';

    try {
      const response = await graphqlRequest<{ createContact: { contact: ContactGraphql | null } }>(CREATE_CONTACT_MUTATION, {
        name: form.organization,
        email: form.email,
        company: '',
        phone: form.phone,
        ...contactApiMapping[need],
        message,
        privacyConsent: true,
        startedAt: Date.now() - 5000,
      });
      if (!response.createContact.contact) {
        throw new Error('Contact rejected');
      }
      const created = {
        ...mapContact(response.createContact.contact),
        confirmationUrl: `/ticket/${response.createContact.contact.secretToken}`,
      };
      ticket.value = created;
      return created;
    } catch {
      submitError.value = "La demande n’a pas pu être envoyée. Vos informations sont conservées : vous pouvez réessayer.";
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
      const response = await graphqlRequest<{ contactByToken: ContactGraphql }>(CONTACT_BY_TOKEN_QUERY, { token });
      ticket.value = mapContact(response.contactByToken);
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
      const response = await graphqlRequest<{ addContactMessage: { contact: ContactGraphql } }>(ADD_CONTACT_MESSAGE_MUTATION, {
        token: ticket.value.secretToken,
        message: reply.value,
        authorName: ticket.value.organization,
      });
      ticket.value = mapContact(response.addContactMessage.contact);
      reply.value = '';
    } catch {
      replyError.value = "Impossible d'ajouter ce message pour le moment.";
    } finally {
      isAddingReply.value = false;
    }
  };

  return { ticket, error, isLoading, reply, replyError, isAddingReply, load, addMessage };
};
