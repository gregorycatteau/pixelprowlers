import { z } from 'zod';

const controlCharactersPattern = /[\u0000-\u001F\u007F-\u009F\u200B-\u200D\uFEFF]/g;
const htmlPattern = /[<>]/;
const sqlOrTemplatePattern = /(--|\/\*|\*\/|;|"|`|\$\{)/;
const namePattern = /^[\p{L}]+(?:[ '\-][\p{L}]+)*$/u;
const structurePattern = /^[\p{L}\p{N}][\p{L}\p{N} &.'\-]*[\p{L}\p{N}.]$/u;
const phoneInputPattern = /^[+\d\s]+$/;
const phoneStrictPattern = /^(?:\+33[1-9]\d{8}|0[1-9]\d{8})$/;

export const stripUnsafeInvisibleChars = (value: string) => (
  value
    .normalize('NFC')
    .replace(controlCharactersPattern, '')
    .replace(/\s+/g, ' ')
    .trim()
);

export const normalizeName = (value: string) => stripUnsafeInvisibleChars(value);
export const normalizeEmail = (value: string) => stripUnsafeInvisibleChars(value).toLowerCase();
export const normalizeStructureName = (value: string) => stripUnsafeInvisibleChars(value);
export const normalizePhoneDigits = (value: string) => stripUnsafeInvisibleChars(value).replace(/\s+/g, '');

export const formatFrenchPhone = (value: string) => {
  const normalized = normalizePhoneDigits(value);

  if (normalized.startsWith('+33')) {
    const local = `0${normalized.slice(3)}`;
    return `+33 ${local.slice(1).replace(/(\d)(?=(\d{2})+$)/g, '$1 ')}`;
  }

  return normalized.replace(/(\d{2})(?=\d)/g, '$1 ');
};

const rejectInjectionChars = (value: string) => (
  !htmlPattern.test(value)
  && !sqlOrTemplatePattern.test(value)
);

export const humanNameSchema = z.string()
  .transform(normalizeName)
  .refine((value) => value.length >= 2 && value.length <= 50, 'Entre 2 et 50 caractères.')
  .refine(rejectInjectionChars, 'Pas de balise, guillemet, point-virgule, commentaire SQL ou template.')
  .refine((value) => namePattern.test(value), 'Lettres, espaces, apostrophes et tirets uniquement.');

const normalizedEmailSchema = z.string()
  .email('Indiquez une adresse email valide.')
  .refine((value) => value.length <= 254, '254 caractères maximum.')
  .refine((value) => !/\s/.test(value) && (value.match(/@/g) || []).length === 1, 'Indiquez une adresse email valide.');

export const emailSchema = z.preprocess(
  (value) => typeof value === 'string' ? normalizeEmail(value) : value,
  normalizedEmailSchema,
);

export const frenchPhoneSchema = z.string()
  .transform(normalizePhoneDigits)
  .refine((value) => phoneInputPattern.test(value), 'Uniquement des chiffres, espaces et éventuellement +33.')
  .refine((value) => phoneStrictPattern.test(value), 'Indiquez un numéro au format 06 XX XX XX XX ou +33 6 XX XX XX XX.');

const frenchMobilePresentations = [
  /^0[67][0-9]{8}$/,
  /^0[67](?: [0-9]{2}){4}$/,
  /^\+33[67][0-9]{8}$/,
  /^\+33 [67](?: [0-9]{2}){4}$/,
];

export const normalizeFrenchMobile = (value: string): string | null => {
  if (typeof value !== 'string' || !frenchMobilePresentations.some((pattern) => pattern.test(value))) {
    return null;
  }
  const compact = value.replaceAll(' ', '');
  return compact.startsWith('+33') ? `0${compact.slice(3)}` : compact;
};

export const contactPhoneSchema = z.string()
  .superRefine((value, context) => {
    if (normalizeFrenchMobile(value)) {
      return;
    }
    const foreign = /^\+(?!33)|^00/.test(value);
    context.addIssue({
      code: z.ZodIssueCode.custom,
      message: foreign
        ? 'PixelProwlers intervient localement : indique un numéro de mobile français.'
        : 'Indique un numéro de mobile français valide, par exemple 06 12 34 56 78.',
    });
  })
  .transform((value) => normalizeFrenchMobile(value) as string);

export const contactDemandTypeSchema = z.enum([
  'diagnostic',
  'urgency',
  'audit',
  'refonte',
  'transmission',
  'partnership',
]);

export const contactMethodSchema = z.enum(['email', 'telephone', 'les_deux']);

const requiredContactText = (label: string, maxLength: number) => z.string()
  .transform((value) => value.normalize('NFC').trim())
  .refine((value) => value.length >= 2, `${label} est obligatoire.`)
  .refine((value) => value.length <= maxLength, `${maxLength} caractères maximum.`)
  .refine((value) => value.search(controlCharactersPattern) === -1, 'Vérifie ce champ : il semble manquer une information.');

export const contactFormSchema = z.object({
  demandType: contactDemandTypeSchema,
  prenom: requiredContactText('Le prénom', 100),
  nom: requiredContactText('Le nom', 100),
  organization: requiredContactText("L'organisation", 180),
  email: emailSchema,
  phone: contactPhoneSchema,
  objet: requiredContactText("L'objet", 200),
  methodeContact: contactMethodSchema,
  message: z.string()
    .transform((value) => value.normalize('NFC').trim())
    .refine((value) => value.length >= 20, 'Décris ta demande en au moins 20 caractères.')
    .refine((value) => value.length <= 4000, '4000 caractères maximum.')
    .refine((value) => !value.includes('\u0000'), 'Vérifie ce champ : il semble manquer une information.'),
}).strict();

export const contactRequiredFieldStates = (values: Partial<ContactFormInput>) => [
  { key: 'demandType', label: 'Type de demande', valid: contactDemandTypeSchema.safeParse(values.demandType).success },
  { key: 'prenom', label: 'Prénom', valid: contactFormSchema.shape.prenom.safeParse(values.prenom ?? '').success },
  { key: 'nom', label: 'Nom', valid: contactFormSchema.shape.nom.safeParse(values.nom ?? '').success },
  { key: 'organization', label: 'Organisation', valid: contactFormSchema.shape.organization.safeParse(values.organization ?? '').success },
  { key: 'email', label: 'Adresse email', valid: emailSchema.safeParse(values.email ?? '').success },
  { key: 'phone', label: 'Numéro de téléphone', valid: contactPhoneSchema.safeParse(values.phone ?? '').success },
  { key: 'methodeContact', label: 'Méthode de contact', valid: contactMethodSchema.safeParse(values.methodeContact).success },
  { key: 'objet', label: 'Objet de la demande', valid: contactFormSchema.shape.objet.safeParse(values.objet ?? '').success },
  { key: 'message', label: 'Message', valid: contactFormSchema.shape.message.safeParse(values.message ?? '').success },
] as const;

export const isContactFormComplete = (values: unknown) => contactFormSchema.safeParse(values).success;

export const personTypeSchema = z.enum(['individu', 'association', 'entreprise']);

export const structureNameSchema = z.string()
  .transform(normalizeStructureName)
  .refine((value) => value.length >= 2 && value.length <= 100, 'Entre 2 et 100 caractères.')
  .refine(rejectInjectionChars, 'Pas de balise, guillemet, point-virgule, commentaire SQL ou template.')
  .refine((value) => structurePattern.test(value), 'Lettres, chiffres, espaces, tirets, &, point et apostrophe uniquement.');

const auditIdentityBaseSchema = z.object({
  prenom: humanNameSchema,
  nom: humanNameSchema,
  email: emailSchema,
  telephone: frenchPhoneSchema,
  type_personne: personTypeSchema,
  nom_structure: z.string().transform(normalizeStructureName).optional(),
  consentement_rgpd: z.literal(true, {
    errorMap: () => ({ message: 'Le consentement RGPD est obligatoire.' }),
  }),
});

const applyStructureValidation = (
  value: z.infer<typeof auditIdentityBaseSchema>,
  context: z.RefinementCtx,
) => {
  if (value.type_personne !== 'individu') {
    const structure = structureNameSchema.safeParse(value.nom_structure || '');

    if (!structure.success) {
      for (const issue of structure.error.issues) {
        context.addIssue({ ...issue, path: ['nom_structure'] });
      }
      return;
    }

    value.nom_structure = structure.data;
  } else {
    value.nom_structure = '';
  }
};

export const auditIdentitySchema = auditIdentityBaseSchema.superRefine(applyStructureValidation);

const normalizedSiteUrlSchema = z.string()
  .url('Indique une URL complète, avec https:// ou http://.')
  .refine((value) => value.length <= 500, '500 caractères maximum.')
  .refine(rejectInjectionChars, 'Pas de balise, guillemet, point-virgule, commentaire SQL ou template.')
  .refine((value) => {
    try {
      return ['http:', 'https:'].includes(new URL(value).protocol);
    } catch {
      return false;
    }
  }, 'URL http ou https uniquement.');

export const siteUrlSchema = z.preprocess(
  (value) => typeof value === 'string' ? stripUnsafeInvisibleChars(value) : value,
  normalizedSiteUrlSchema,
);

export const refonteIdentitySchema = auditIdentityBaseSchema.extend({
  site_url: siteUrlSchema,
}).superRefine(applyStructureValidation);

export const auditAnswerSchema = z.number().int().min(0).max(10);

export const createAuditAnswersSchema = (questionIds: string[]) => z.object(
  Object.fromEntries(questionIds.map((id) => [id, auditAnswerSchema])),
).strict();

export type AuditIdentityInput = z.input<typeof auditIdentitySchema>;
export type AuditIdentity = z.output<typeof auditIdentitySchema>;
export type RefonteIdentityInput = z.input<typeof refonteIdentitySchema>;
export type RefonteIdentity = z.output<typeof refonteIdentitySchema>;
export type ContactFormInput = z.input<typeof contactFormSchema>;
export type ContactFormData = z.output<typeof contactFormSchema>;
