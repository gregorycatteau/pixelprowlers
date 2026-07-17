import {
  computed,
  reactive,
  ref,
} from 'vue';

import { z } from 'zod';

import {
  CREATE_URGENCY_REQUEST_MUTATION,
  graphqlErrorMessage,
  graphqlRequest,
} from '~/utils/graphql';

import {
  contactPhoneSchema,
  emailSchema,
  siteUrlSchema,
  stripUnsafeInvisibleChars,
} from '~/validation/schemas';

const urgencyProblemValues = [
  'site_down',
  'suspected_hack',
  'broken_form',
  'email_dns_domain',
  'content_modified',
  'critical_error',
  'massive_slowdown',
  'other',
] as const;

const urgencyImpactValues = [
  'minor',
  'disrupted',
  'blocked',
  'security_data_risk',
] as const;

const urgencyContactPreferenceValues = [
  'email',
  'phone',
  'either',
] as const;

const urgencyExpectedNextStepValues = [
  'understand_first',
  'quick_callback',
  'secure_before_action',
  'prepare_intervention',
  'need_guidance',
] as const;

const clientEmailStatusValues = [
  'sent',
  'not_configured',
  'failed',
] as const;

export type UrgencyProblemType =
  typeof urgencyProblemValues[number];

export type UrgencyImpactLevel =
  typeof urgencyImpactValues[number];

export type UrgencyContactPreference =
  typeof urgencyContactPreferenceValues[number];

export type UrgencyExpectedNextStep =
  typeof urgencyExpectedNextStepValues[number];

export type UrgencyClientEmailStatus =
  typeof clientEmailStatusValues[number];

export type UrgencyResponse = {
  reference: string;
  status: 'open';
  clientEmailStatus: UrgencyClientEmailStatus;
  message: string;
};

type UrgencyOption<T extends string> = {
  label: string;
  value: T;
};

export const urgencyProblemOptions: Array<
  UrgencyOption<UrgencyProblemType>
> = [
  {
    label: 'Site inaccessible',
    value: 'site_down',
  },
  {
    label: 'Suspicion de compromission',
    value: 'suspected_hack',
  },
  {
    label: 'Formulaire devenu inutilisable',
    value: 'broken_form',
  },
  {
    label: 'Problème lié aux emails, au DNS ou au nom de domaine',
    value: 'email_dns_domain',
  },
  {
    label: 'Contenu modifié sans autorisation',
    value: 'content_modified',
  },
  {
    label: 'Erreur empêchant une fonction essentielle',
    value: 'critical_error',
  },
  {
    label: 'Ralentissement important',
    value: 'massive_slowdown',
  },
  {
    label: 'Autre situation',
    value: 'other',
  },
];

export const urgencyImpactOptions: Array<
  UrgencyOption<UrgencyImpactLevel>
> = [
  {
    label: 'Gêne limitée, activité maintenue',
    value: 'minor',
  },
  {
    label: 'Activité perturbée',
    value: 'disrupted',
  },
  {
    label: 'Activité actuellement bloquée',
    value: 'blocked',
  },
  {
    label: 'Risque possible pour la sécurité ou les données',
    value: 'security_data_risk',
  },
];

export const urgencyContactOptions: Array<
  UrgencyOption<UrgencyContactPreference>
> = [
  {
    label: 'Email en priorité',
    value: 'email',
  },
  {
    label: 'Téléphone en priorité',
    value: 'phone',
  },
  {
    label: 'Email ou téléphone',
    value: 'either',
  },
];

export const urgencyNextStepOptions: Array<
  UrgencyOption<UrgencyExpectedNextStep>
> = [
  {
    label: 'Je souhaite d’abord comprendre la situation',
    value: 'understand_first',
  },
  {
    label: 'Je souhaite être rappelé pour qualifier la situation',
    value: 'quick_callback',
  },
  {
    label: 'Je souhaite sécuriser la situation avant toute autre action',
    value: 'secure_before_action',
  },
  {
    label: 'Je souhaite préparer une intervention si elle est nécessaire',
    value: 'prepare_intervention',
  },
  {
    label: 'Je ne sais pas encore quelle suite choisir',
    value: 'need_guidance',
  },
];

const urgencyProblemSchema = z.enum(
  urgencyProblemValues,
  {
    errorMap: () => ({
      message: 'Sélectionnez la situation observée.',
    }),
  },
);

const urgencyImpactSchema = z.enum(
  urgencyImpactValues,
  {
    errorMap: () => ({
      message: 'Sélectionnez l’impact actuel.',
    }),
  },
);

const urgencyContactPreferenceSchema = z.enum(
  urgencyContactPreferenceValues,
  {
    errorMap: () => ({
      message: 'Indiquez comment vous souhaitez être recontacté.',
    }),
  },
);

const urgencyExpectedNextStepSchema = z.enum(
  urgencyExpectedNextStepValues,
  {
    errorMap: () => ({
      message: 'Indiquez la suite que vous souhaitez envisager.',
    }),
  },
);

const requiredUrgencyText = (
  label: string,
  minimumLength: number,
  maximumLength: number,
) => z.string()
  .transform(stripUnsafeInvisibleChars)
  .refine(
    (value) => value.length >= minimumLength,
    `${label} est obligatoire.`,
  )
  .refine(
    (value) => value.length <= maximumLength,
    `${maximumLength} caractères maximum.`,
  );

export const urgencyFormSchema = z.object({
  problemType: urgencyProblemSchema,
  impactLevel: urgencyImpactSchema,

  affectedUrl: siteUrlSchema,

  shortDescription: requiredUrgencyText(
    'La description de l’incident',
    20,
    700,
  ),

  sinceWhen: requiredUrgencyText(
    'La date ou la période de début',
    2,
    120,
  ),

  name: requiredUrgencyText(
    'Le prénom et le nom',
    2,
    120,
  ),

  organization: requiredUrgencyText(
    'L’organisation ou le statut',
    2,
    160,
  ),

  email: emailSchema,
  phone: contactPhoneSchema,

  contactPreference: urgencyContactPreferenceSchema,

  callbackSlot: requiredUrgencyText(
    'Le créneau de rappel',
    2,
    160,
  ),

  expected_next_step: urgencyExpectedNextStepSchema,

  /*
   * Le nom historique de la propriété est conservé pour rester
   * compatible avec la mutation GraphQL. Cette case représente
   * une demande de rappel et un accusé de lecture, pas un
   * consentement général au traitement des données.
   */
  consentToContact: z.literal(true, {
    errorMap: () => ({
      message:
        'Vous devez confirmer votre demande de rappel et la lecture des informations relatives à vos données.',
    }),
  }),

  noSecretsConfirmed: z.literal(true, {
    errorMap: () => ({
      message:
        'Vous devez confirmer qu’aucun secret ni accès sensible n’est transmis.',
    }),
  }),

  /*
   * Le champ doit rester vide. Il sert uniquement de piège
   * anti-robot et n’est jamais affiché aux visiteurs.
   */
  website: z.string()
    .max(0, 'La demande ne peut pas être transmise.'),
}).strict();

type UrgencyFormState = {
  problemType: UrgencyProblemType | '';
  impactLevel: UrgencyImpactLevel | '';
  affectedUrl: string;
  shortDescription: string;
  sinceWhen: string;
  name: string;
  organization: string;
  email: string;
  phone: string;
  contactPreference: UrgencyContactPreference | '';
  callbackSlot: string;
  expected_next_step: UrgencyExpectedNextStep | '';
  consentToContact: boolean;
  noSecretsConfirmed: boolean;
  website: string;
};

const createUrgencyForm = (): UrgencyFormState => ({
  problemType: '',
  impactLevel: '',
  affectedUrl: '',
  shortDescription: '',
  sinceWhen: '',
  name: '',
  organization: '',
  email: '',
  phone: '',
  contactPreference: '',
  callbackSlot: '',
  expected_next_step: '',
  consentToContact: false,
  noSecretsConfirmed: false,
  website: '',
});

const isClientEmailStatus = (
  value: unknown,
): value is UrgencyClientEmailStatus => (
  typeof value === 'string'
  && clientEmailStatusValues.some(
    (status) => status === value,
  )
);

export const useUrgency = () => {
  const form = reactive<UrgencyFormState>(
    createUrgencyForm(),
  );

  const result = ref<UrgencyResponse | null>(null);
  const submitError = ref('');
  const isSubmitting = ref(false);

  const canSubmit = computed(() => (
    urgencyFormSchema.safeParse(form).success
    && !isSubmitting.value
  ));

  const reset = () => {
    Object.assign(
      form,
      createUrgencyForm(),
    );

    result.value = null;
    submitError.value = '';
  };

  /*
   * Seules les informations nécessaires à la qualification sont
   * transmises. Aucun fichier ni accès technique n’est demandé.
   */
  const submit = async () => {
    if (isSubmitting.value) {
      return;
    }

    submitError.value = '';

    /*
     * Un champ honeypot rempli entraîne un abandon silencieux.
     * Il ne faut pas expliquer son fonctionnement au robot.
     */
    if (form.website.trim().length > 0) {
      return;
    }

    const validation = urgencyFormSchema.safeParse(
      form,
    );

    if (!validation.success) {
      submitError.value =
        validation.error.issues[0]?.message
        || 'Vérifiez les informations du formulaire avant de l’envoyer.';

      return;
    }

    isSubmitting.value = true;

    try {
      const normalizedForm = validation.data;

      const response = await graphqlRequest<{
        createUrgencyRequest: {
          reference: string | null;
          status: string | null;
          message: string | null;
          clientEmailStatus: string | null;
          ticket: {
            reference: string;
            status: string;
          } | null;
        };
      }>(
        CREATE_URGENCY_REQUEST_MUTATION,
        {
          affectedUrl: normalizedForm.affectedUrl,
          callbackSlot: normalizedForm.callbackSlot,

          /*
           * Nom conservé pour compatibilité avec l’API existante.
           */
          consentToContact:
            normalizedForm.consentToContact,

          contactPreference:
            normalizedForm.contactPreference,

          email: normalizedForm.email,

          expectedNextStep:
            normalizedForm.expected_next_step,

          impactLevel:
            normalizedForm.impactLevel,

          name:
            normalizedForm.name,

          noSecretsConfirmed:
            normalizedForm.noSecretsConfirmed,

          organization:
            normalizedForm.organization,

          phone:
            normalizedForm.phone,

          problemType:
            normalizedForm.problemType,

          shortDescription:
            normalizedForm.shortDescription,

          sinceWhen:
            normalizedForm.sinceWhen,

          website: '',
        },
      );

      const reference = (
        response.createUrgencyRequest.reference
        || response.createUrgencyRequest.ticket?.reference
        || ''
      ).trim();

      if (!reference) {
        throw new Error(
          'urgency_reference_missing',
        );
      }

      const emailStatus = (
        response.createUrgencyRequest.clientEmailStatus
      );

      result.value = {
        reference,
        status: 'open',

        clientEmailStatus: isClientEmailStatus(
          emailStatus,
        )
          ? emailStatus
          : 'not_configured',

        /*
         * Le message local évite d’afficher une ancienne promesse
         * de délai éventuellement renvoyée par le serveur.
         */
        message: 'Demande enregistrée.',
      };
    } catch (error) {
      submitError.value = graphqlErrorMessage(
        error,
        'Impossible d’enregistrer votre demande pour le moment. Vous pouvez réessayer ou appeler PixelProwlers au 06 68 14 51 52.',
      );
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