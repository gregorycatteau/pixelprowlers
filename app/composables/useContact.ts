import { toTypedSchema } from '@vee-validate/zod';
import { computed, reactive, ref } from 'vue';
import { useForm } from 'vee-validate';
import { graphqlRequest } from '~/utils/graphql';
import {
  contactFormSchema,
  contactRequiredFieldStates,
  contactPhoneSchema,
  isContactFormComplete,
  type ContactFormInput,
} from '~/validation/schemas';
import { formatFrenchPhone } from '~/validation/schemas';

export type ContactDemandType = 'diagnostic' | 'urgency' | 'audit' | 'refonte' | 'transmission' | 'partnership';
export type ContactStatus = 'open' | 'in_progress' | 'waiting_customer' | 'resolved' | 'closed';

export type ContactTicket = {
  ticketId: string;
  numeroDossier: string;
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

type ContactGraphql = {
  ticketId: string;
  numeroDossier: string;
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
  createdAt: string;
  updatedAt: string;
};

const CONTACT_FIELDS = /* GraphQL */ `
  {
    ticketId
    numeroDossier
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
    createdAt
    updatedAt
  }
`;

const CREATE_CONTACT_MUTATION = /* GraphQL */ `
  mutation CreateContact(
    $nom: String!
    $prenom: String!
    $email: String!
    $company: String!
    $telephone: String!
    $objet: String!
    $methodeContact: String!
    $serviceType: String!
    $demandType: String!
    $message: String!
    $privacyConsent: Boolean
    $startedAt: Float
  ) {
    createContact(
      nom: $nom
      prenom: $prenom
      email: $email
      company: $company
      telephone: $telephone
      objet: $objet
      methodeContact: $methodeContact
      serviceType: $serviceType
      demandType: $demandType
      message: $message
      privacyConsent: $privacyConsent
      startedAt: $startedAt
    ) {
      success
      numeroDossier
      message
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

const serviceTypeFromDemand = (demandType: ContactDemandType | '') => {
  if (demandType === 'urgency') return 'urgence';
  if (demandType === 'audit') return 'audit_site';
  if (demandType === 'refonte') return 'site_maintenable';
  if (demandType === 'transmission') return 'maintenance_documentation';
  if (demandType === 'diagnostic') return 'audit_site';
  return 'autre';
};

const mapContact = (contact: ContactGraphql): ContactTicket => ({
  ticketId: contact.ticketId,
  numeroDossier: contact.numeroDossier,
  secretToken: contact.secretToken,
  organization: contact.company || contact.name,
  email: contact.email,
  phone: contact.phone || '',
  demandType: contact.demandType || 'partnership',
  demandLabel: contact.demandLabel,
  message: contact.message,
  status: contact.status,
  messages: contact.messages || [],
  createdAt: contact.createdAt,
  updatedAt: contact.updatedAt,
});

export const statusLabel = (status: ContactStatus) => ({
  open: 'Ouvert',
  in_progress: 'En cours',
  waiting_customer: 'En attente client',
  resolved: 'Résolu',
  closed: 'Fermé',
}[status] || status);

export const useContactForm = () => {
  const { defineField, errors, meta, validate } = useForm<ContactFormInput>({
    validationSchema: toTypedSchema(contactFormSchema),
    initialValues: {
      demandType: '' as ContactDemandType,
      prenom: '',
      nom: '',
      organization: '',
      email: '',
      phone: '',
      objet: '',
      methodeContact: '' as ContactFormInput['methodeContact'],
      message: '',
    },
  });
  const [demandType] = defineField('demandType');
  const [prenom] = defineField('prenom');
  const [nom] = defineField('nom');
  const [organization] = defineField('organization');
  const [email] = defineField('email');
  const [phone] = defineField('phone');
  const [objet] = defineField('objet');
  const [methodeContact] = defineField('methodeContact');
  const [message] = defineField('message');
  const form = reactive({ demandType, prenom, nom, organization, email, phone, objet, methodeContact, message });
  const submitError = ref('');
  const isSubmitting = ref(false);

  const requiredFields = computed(() => contactRequiredFieldStates(form));
  const validFieldCount = computed(() => requiredFields.value.filter((field) => field.valid).length);
  const progressMessage = computed(() => {
    const remaining = requiredFields.value.length - validFieldCount.value;
    return remaining === 0
      ? 'Tout est prêt. Tu peux ouvrir ton ticket.'
      : `Encore ${remaining} champ${remaining > 1 ? 's' : ''} à compléter avant de pouvoir ouvrir ton ticket.`;
  });
  const canSubmit = computed(() => (
    meta.value.dirty
    && validFieldCount.value === requiredFields.value.length
    && isContactFormComplete(form)
    && !isSubmitting.value
  ));

  const formatPhoneOnBlur = () => {
    const parsed = contactPhoneSchema.safeParse(form.phone);
    if (parsed.success) {
      form.phone = formatFrenchPhone(parsed.data);
    }
  };

  const submit = async () => {
    if (!canSubmit.value || isSubmitting.value) {
      submitError.value = form.phone.trim()
        ? 'Vérifie les champs incomplets avant de pouvoir ouvrir ton ticket.'
        : 'Indique ton numéro de téléphone pour que nous puissions identifier et suivre correctement ta demande.';
      return null;
    }

    const validation = await validate();
    const parsedForm = contactFormSchema.safeParse(form);
    if (!validation.valid || !parsedForm.success) {
      submitError.value = 'Vérifie ce formulaire : il semble manquer une information.';
      return null;
    }
    const contact = parsedForm.data;

    isSubmitting.value = true;
    submitError.value = '';

    try {
      const response = await graphqlRequest<{ createContact: { success: boolean; numeroDossier: string; message: string } }>(CREATE_CONTACT_MUTATION, {
        nom: contact.nom,
        prenom: contact.prenom,
        email: contact.email,
        company: contact.organization,
        telephone: contact.phone,
        objet: contact.objet,
        methodeContact: contact.methodeContact,
        serviceType: serviceTypeFromDemand(contact.demandType),
        demandType: contact.demandType,
        message: contact.message,
        privacyConsent: true,
        startedAt: Date.now() - 5000,
      });
      if (!response.createContact.success || !response.createContact.numeroDossier) {
        throw new Error('Contact rejected');
      }
      const created = {
        numeroDossier: response.createContact.numeroDossier,
        message: response.createContact.message,
        confirmationUrl: '/contact/confirmation',
      };
      sessionStorage.setItem('pixelprowlers-contact-confirmation', JSON.stringify(created));
      return created;
    } catch {
      submitError.value = "Impossible d'ouvrir le ticket pour le moment. Vous pouvez réessayer dans quelques instants.";
      return null;
    } finally {
      isSubmitting.value = false;
    }
  };

  return {
    form,
    errors,
    submitError,
    isSubmitting,
    canSubmit,
    requiredFields,
    validFieldCount,
    progressMessage,
    formatPhoneOnBlur,
    submit,
  };
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
