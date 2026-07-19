import { toTypedSchema } from '@vee-validate/zod';
import {
  computed,
  onMounted,
  reactive,
  ref,
} from 'vue';
import { useForm } from 'vee-validate';

import { graphqlRequest } from '~/utils/graphql';

import {
  contactFormSchema,
  contactPhoneSchema,
  contactRequiredFieldStates,
  formatFrenchPhone,
  privacyAcknowledgementSchema,
  type ContactFormInput,
} from '~/validation/schemas';

export type ContactDemandType =
  | 'diagnostic'
  | 'urgency'
  | 'audit'
  | 'refonte'
  | 'transmission'
  | 'materiel'
  | 'partnership';

export type ContactStatus =
  | 'open'
  | 'in_progress'
  | 'waiting_customer'
  | 'resolved'
  | 'closed';

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

type ContactRequiredField = {
  key: string;
  label: string;
  valid: boolean;
};

export const contactDemandOptions: Array<{
  label: string;
  value: ContactDemandType;
}> = [
  {
    label: 'Je souhaite réaliser un pré-diagnostic',
    value: 'diagnostic',
  },
  {
    label: 'Je rencontre un incident ou une urgence',
    value: 'urgency',
  },
  {
    label: 'Je souhaite faire auditer un site',
    value: 'audit',
  },
  {
    label: 'Je souhaite réparer ou refondre un site',
    value: 'refonte',
  },
  {
    label: 'Je souhaite transmettre ou clarifier des accès',
    value: 'transmission',
  },
  {
    label: 'Réparation, reconditionnement ou migration Linux',
    value: 'materiel',
  },
  {
    label: 'Partenariat ou autre demande',
    value: 'partnership',
  },
];

/*
 * Liste blanche stricte des types de demande acceptés. Toute valeur qui
 * n’en fait pas partie (par exemple un paramètre d’URL) doit être ignorée
 * plutôt que transmise au formulaire ou à GraphQL.
 */
export const isContactDemandType = (
  value: unknown,
): value is ContactDemandType => (
  typeof value === 'string'
  && contactDemandOptions.some(
    (option) => option.value === value,
  )
);

/*
 * Résout un type de demande présélectionné depuis un paramètre de requête
 * (ex. Nuxt/Vue Router peut fournir une chaîne, `null`, `undefined` ou un
 * tableau en cas de paramètre répété). Toute valeur hors liste blanche —
 * y compris un tableau non résolu — renvoie `undefined` : elle n’est
 * jamais transmise telle quelle au formulaire ni à GraphQL.
 */
export const resolveDemandTypeFromQuery = (
  rawValue: unknown,
): ContactDemandType | undefined => {
  const value = Array.isArray(rawValue) ? rawValue[0] : rawValue;

  return isContactDemandType(value) ? value : undefined;
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
  mutation AddContactMessage(
    $token: String!
    $message: String!
    $authorName: String!
  ) {
    addContactMessage(
      token: $token
      message: $message
      authorName: $authorName
    ) {
      contact ${CONTACT_FIELDS}
    }
  }
`;

/*
 * Dérive le service_type backend à partir du type de demande choisi côté
 * client. Exportée pour être testée indépendamment du cycle de vie du
 * formulaire (vee-validate) : c’est ici, et uniquement ici, que la valeur
 * ServiceType.MATERIEL est produite pour la mutation GraphQL.
 */
export const serviceTypeFromDemand = (
  demandType: ContactDemandType | '',
) => {
  if (demandType === 'urgency') {
    return 'urgence';
  }

  if (demandType === 'audit') {
    return 'audit_site';
  }

  if (demandType === 'refonte') {
    return 'site_maintenable';
  }

  if (demandType === 'transmission') {
    return 'maintenance_documentation';
  }

  if (demandType === 'materiel') {
    return 'materiel';
  }

  /*
   * La valeur existante est conservée pour rester compatible avec
   * le classement attendu par le serveur.
   */
  if (demandType === 'diagnostic') {
    return 'audit_site';
  }

  return 'autre';
};

const mapContact = (
  contact: ContactGraphql,
): ContactTicket => ({
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

export const statusLabel = (
  status: ContactStatus,
) => ({
  open: 'Ouvert',
  in_progress: 'En cours',
  waiting_customer: 'En attente du client',
  resolved: 'Résolu',
  closed: 'Fermé',
}[status] || status);

export const useContactForm = (
  initialDemandType?: ContactDemandType,
) => {
  const {
    defineField,
    errors,
    meta,
    validate,
  } = useForm<ContactFormInput>({
    validationSchema: toTypedSchema(contactFormSchema),

    initialValues: {
      demandType: (
        isContactDemandType(initialDemandType)
          ? initialDemandType
          : ''
      ) as ContactDemandType,
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

  const form = reactive({
    demandType,
    prenom,
    nom,
    organization,
    email,
    phone,
    objet,
    methodeContact,
    message,
  });

  const privacyAcknowledged = ref(false);
  const privacyError = ref('');
  const submitError = ref('');
  const isSubmitting = ref(false);
  const formStartedAt = ref<number | null>(null);

  onMounted(() => {
    /*
     * Heure réelle d’affichage du formulaire.
     * Elle peut être utilisée par le serveur comme signal anti-robot.
     */
    formStartedAt.value = Date.now();
  });

  const requiredFields = computed<ContactRequiredField[]>(() => [
    ...contactRequiredFieldStates(form),

    {
      key: 'privacyAcknowledged',
      label: 'Information sur les données',
      valid: privacyAcknowledgementSchema.safeParse(
        privacyAcknowledged.value,
      ).success,
    },
  ]);

  const validFieldCount = computed(
    () => requiredFields.value.filter(
      (field) => field.valid,
    ).length,
  );

  const progressMessage = computed(() => {
    const remaining = (
      requiredFields.value.length
      - validFieldCount.value
    );

    if (remaining === 0) {
      return 'Tous les champs obligatoires sont validés. Vous pouvez envoyer votre demande.';
    }

    return `Il reste ${remaining} champ${remaining > 1 ? 's' : ''} obligatoire${remaining > 1 ? 's' : ''} à compléter.`;
  });

  const canSubmit = computed(() => (
    meta.value.dirty
    && validFieldCount.value === requiredFields.value.length
    && contactFormSchema.safeParse(form).success
    && privacyAcknowledgementSchema.safeParse(
      privacyAcknowledged.value,
    ).success
    && !isSubmitting.value
  ));

  const formatPhoneOnBlur = () => {
    const parsed = contactPhoneSchema.safeParse(
      form.phone,
    );

    if (parsed.success) {
      form.phone = formatFrenchPhone(parsed.data);
    }
  };

  const validatePrivacyAcknowledgement = () => {
    const result = privacyAcknowledgementSchema.safeParse(
      privacyAcknowledged.value,
    );

    privacyError.value = result.success
      ? ''
      : result.error.issues[0]?.message
        || 'Veuillez prendre connaissance des informations relatives à vos données.';

    return result.success;
  };

  const submit = async () => {
    if (isSubmitting.value) {
      return null;
    }

    submitError.value = '';

    const privacyIsValid = validatePrivacyAcknowledgement();

    if (!form.phone.trim()) {
      submitError.value =
        'Indiquez votre numéro de téléphone pour permettre la qualification et le suivi de votre demande.';
      return null;
    }

    if (!privacyIsValid) {
      submitError.value =
        'Vérifiez l’information relative à l’utilisation de vos données.';
      return null;
    }

    if (!canSubmit.value) {
      submitError.value =
        'Vérifiez les champs obligatoires avant d’envoyer votre demande.';
      return null;
    }

    if (formStartedAt.value === null) {
      submitError.value =
        'Le formulaire n’a pas été initialisé correctement. Rechargez la page avant de réessayer.';
      return null;
    }

    isSubmitting.value = true;

    try {
      const validation = await validate();

      const parsedForm = contactFormSchema.safeParse(
        form,
      );

      if (!validation.valid || !parsedForm.success) {
        submitError.value =
          'Vérifiez le formulaire : une information est manquante ou incorrecte.';
        return null;
      }

      const contact = parsedForm.data;

      const response = await graphqlRequest<{
        createContact: {
          success: boolean;
          numeroDossier: string;
          message: string;
        };
      }>(
        CREATE_CONTACT_MUTATION,
        {
          nom: contact.nom,
          prenom: contact.prenom,
          email: contact.email,
          company: contact.organization,
          telephone: contact.phone,
          objet: contact.objet,
          methodeContact: contact.methodeContact,
          serviceType: serviceTypeFromDemand(
            contact.demandType,
          ),
          demandType: contact.demandType,
          message: contact.message,

          /*
           * Le serveur utilise encore le nom historique
           * privacyConsent. La valeur signifie ici que la personne
           * a pris connaissance de la notice, et non qu’elle consent
           * à l’ensemble des traitements.
           */
          privacyConsent: privacyAcknowledged.value,

          /*
           * Envoi de la véritable heure d’ouverture du formulaire.
           */
          startedAt: formStartedAt.value,
        },
      );

      if (
        !response.createContact.success
        || !response.createContact.numeroDossier
      ) {
        throw new Error('contact_creation_rejected');
      }

      const created = {
        numeroDossier:
          response.createContact.numeroDossier,

        message:
          response.createContact.message,

        confirmationUrl:
          '/contact/confirmation',
      };

      /*
       * L’échec du stockage local ne doit pas transformer une
       * création réussie en échec ni provoquer un doublon.
       */
      try {
        window.sessionStorage.setItem(
          'pixelprowlers-contact-confirmation',
          JSON.stringify(created),
        );
      } catch {
        /*
         * Le ticket est déjà créé. La navigation vers la page de
         * confirmation reste donc autorisée.
         */
      }

      return created;
    } catch {
      submitError.value =
        'Impossible d’enregistrer votre demande pour le moment. Vous pouvez réessayer ou appeler PixelProwlers au 06 68 14 51 52.';

      return null;
    } finally {
      isSubmitting.value = false;
    }
  };

  return {
    form,
    errors,
    privacyAcknowledged,
    privacyError,
    submitError,
    isSubmitting,
    canSubmit,
    requiredFields,
    validFieldCount,
    progressMessage,
    formatPhoneOnBlur,
    validatePrivacyAcknowledgement,
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

  const load = async (
    token: string,
  ) => {
    if (!token) {
      ticket.value = null;
      error.value =
        'Ce lien de suivi est incomplet.';
      return;
    }

    isLoading.value = true;
    error.value = '';

    try {
      const response = await graphqlRequest<{
        contactByToken: ContactGraphql;
      }>(
        CONTACT_BY_TOKEN_QUERY,
        {
          token,
        },
      );

      ticket.value = mapContact(
        response.contactByToken,
      );
    } catch {
      ticket.value = null;
      error.value =
        'Ce lien de suivi n’est plus disponible.';
    } finally {
      isLoading.value = false;
    }
  };

  const addMessage = async () => {
    if (!ticket.value || isAddingReply.value) {
      return;
    }

    const normalizedReply = reply.value
      .normalize('NFC')
      .trim();

    if (normalizedReply.length < 2) {
      replyError.value =
        'Rédigez un message avant de l’envoyer.';
      return;
    }

    if (normalizedReply.length > 4000) {
      replyError.value =
        'Votre message ne peut pas dépasser 4000 caractères.';
      return;
    }

    isAddingReply.value = true;
    replyError.value = '';

    try {
      const response = await graphqlRequest<{
        addContactMessage: {
          contact: ContactGraphql;
        };
      }>(
        ADD_CONTACT_MESSAGE_MUTATION,
        {
          token: ticket.value.secretToken,
          message: normalizedReply,
          authorName: ticket.value.organization,
        },
      );

      ticket.value = mapContact(
        response.addContactMessage.contact,
      );

      reply.value = '';
    } catch {
      replyError.value =
        'Impossible d’ajouter ce message pour le moment.';
    } finally {
      isAddingReply.value = false;
    }
  };

  return {
    ticket,
    error,
    isLoading,
    reply,
    replyError,
    isAddingReply,
    load,
    addMessage,
  };
};