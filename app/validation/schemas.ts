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
  .refine((value) => namePattern.test(value), "Un prénom, c'est fait pour être lu par des humains, pas par une base de données — que des lettres, s'il te plaît");

const normalizedEmailSchema = z.string()
  .email("Ton email ressemble à s'y méprendre à un email raté, un petit @ quelque part ?")
  .refine((value) => value.length <= 254, '254 caractères maximum.')
  .refine((value) => !/\s/.test(value) && (value.match(/@/g) || []).length === 1, "Ton email ressemble à s'y méprendre à un email raté, un petit @ quelque part ?");

export const emailSchema = z.preprocess(
  (value) => typeof value === 'string' ? normalizeEmail(value) : value,
  normalizedEmailSchema,
);

export const frenchPhoneSchema = z.string()
  .transform(normalizePhoneDigits)
  .refine((value) => phoneInputPattern.test(value), 'Uniquement des chiffres, espaces et éventuellement +33.')
  .refine((value) => phoneStrictPattern.test(value), 'Ton téléphone doit ressembler à du 06 XX XX XX XX ou +33 6 XX XX XX XX');

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
