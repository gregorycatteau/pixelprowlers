import { describe, expect, it } from 'vitest';
import {
  auditIdentitySchema,
  contactDemandTypeSchema,
  contactFormSchema,
  contactPhoneSchema,
  contactRequiredFieldStates,
  createAuditAnswersSchema,
  emailSchema,
  frenchPhoneSchema,
  humanNameSchema,
  isContactFormComplete,
  normalizeFrenchMobile,
  structureNameSchema,
} from './schemas';

describe('audit validation schemas', () => {
  it('accepts and normalizes valid identity data', () => {
    const result = auditIdentitySchema.parse({
      prenom: '  Élodie  ',
      nom: ' Martin-Dupont ',
      email: 'ELODIE@EXEMPLE.FR',
      telephone: '06 12 34 56 78',
      type_personne: 'association',
      nom_structure: 'Les Amis & Co.',
      consentement_rgpd: true,
    });

    expect(result.email).toBe('elodie@exemple.fr');
    expect(result.telephone).toBe('0612345678');
  });

  it('rejects injection attempts in human names', () => {
    expect(() => humanNameSchema.parse('<script>alert(1)</script>')).toThrow();
    expect(() => humanNameSchema.parse('Robert--;')).toThrow();
    expect(() => humanNameSchema.parse('Marie42')).toThrow();
  });

  it('rejects invalid emails', () => {
    expect(() => emailSchema.parse('bad@@example.com')).toThrow();
    expect(() => emailSchema.parse('bad email@example.com')).toThrow();
  });

  it('accepts strict French phones only', () => {
    expect(frenchPhoneSchema.parse('+33612345678')).toBe('+33612345678');
    expect(frenchPhoneSchema.parse('0612345678')).toBe('0612345678');
    expect(() => frenchPhoneSchema.parse('+1 555 123')).toThrow();
  });

  it('validates structure names with a whitelist', () => {
    expect(structureNameSchema.parse('PixelProwlers & Co.')).toBe('PixelProwlers & Co.');
    expect(() => structureNameSchema.parse('Corp ${process.env.SECRET}')).toThrow();
  });

  it('rejects manipulated audit answers', () => {
    const schema = createAuditAnswersSchema(['q1', 'q2']);

    expect(schema.parse({ q1: 0, q2: 10 })).toEqual({ q1: 0, q2: 10 });
    expect(() => schema.parse({ q1: 0.5, q2: 10 })).toThrow();
    expect(() => schema.parse({ q1: 11, q2: 10 })).toThrow();
    expect(() => schema.parse({ q1: 1, q2: 2, extra: 3 })).toThrow();
  });
});

describe('contact validation schema and progress', () => {
  const completeContact = {
    demandType: 'audit' as const,
    prenom: 'Alice',
    nom: 'Martin',
    organization: 'Association Exemple',
    email: 'alice@example.com',
    phone: '06 12 34 56 78',
    objet: 'Audit du site',
    methodeContact: 'email' as const,
    message: 'Nous souhaitons faire auditer notre site avant une refonte.',
  };

  it.each([
    ['0612345678', '0612345678'],
    ['06 12 34 56 78', '0612345678'],
    ['+33612345678', '0612345678'],
    ['+33 6 12 34 56 78', '0612345678'],
    ['0712345678', '0712345678'],
    ['07 12 34 56 78', '0712345678'],
    ['+33712345678', '0712345678'],
    ['+33 7 12 34 56 78', '0712345678'],
  ])('normalizes the accepted French mobile presentation %s', (input, canonical) => {
    expect(normalizeFrenchMobile(input)).toBe(canonical);
    expect(contactPhoneSchema.parse(input)).toBe(canonical);
  });

  it.each([
    '+32470123456',
    '+41791234567',
    '+34612345678',
    '0012345678',
    '33612345678',
    '06AB345678',
    '+33',
    '061234567',
    '06123456789',
    '0123456789',
    '',
    '   ',
    '0612345678\u0000',
    '0612345678\r\n',
  ])('rejects the unsupported phone presentation %s', (input) => {
    expect(normalizeFrenchMobile(input)).toBeNull();
    expect(contactPhoneSchema.safeParse(input).success).toBe(false);
  });

  it.each(['email', 'telephone', 'les_deux'] as const)('requires a phone when the preferred method is %s', (method) => {
    expect(contactFormSchema.safeParse({ ...completeContact, methodeContact: method, phone: '' }).success).toBe(false);
  });

  it('keeps the button-equivalent validity false when only the phone is missing', () => {
    expect(isContactFormComplete({ ...completeContact, phone: '' })).toBe(false);
    expect(isContactFormComplete(completeContact)).toBe(true);
    expect(isContactFormComplete({ ...completeContact, phone: '123' })).toBe(false);
  });

  it('provides only the canonical phone to the GraphQL payload data', () => {
    const parsed = contactFormSchema.parse({ ...completeContact, phone: '+33 6 12 34 56 78' });
    expect(parsed.phone).toBe('0612345678');
  });

  it('normalizes the required organization and accepts Particulier explicitly', () => {
    expect(contactFormSchema.parse({ ...completeContact, organization: '  Particulier  ' }).organization).toBe('Particulier');
    expect(contactFormSchema.parse({ ...completeContact, organization: '  E\u0301quipe Exemple  ' }).organization).toBe('Équipe Exemple');
    expect(contactFormSchema.safeParse({ ...completeContact, organization: '   ' }).success).toBe(false);
    expect(contactFormSchema.safeParse({ ...completeContact, organization: 'Exemple\r\nInjection' }).success).toBe(false);
    expect(contactFormSchema.safeParse({ ...completeContact, organization: 'Exemple\u0000' }).success).toBe(false);
  });

  it('marks phone complete, then immediately neutral again when it becomes invalid', () => {
    const missing = contactRequiredFieldStates({ ...completeContact, phone: '' });
    const valid = contactRequiredFieldStates(completeContact);
    const invalidAgain = contactRequiredFieldStates({ ...completeContact, phone: '123' });

    expect(missing).toHaveLength(9);
    expect(missing.find((field) => field.key === 'phone')?.valid).toBe(false);
    expect(valid.find((field) => field.key === 'phone')?.valid).toBe(true);
    expect(invalidAgain.find((field) => field.key === 'phone')?.valid).toBe(false);
  });

  it('accepts the materiel demand type end to end', () => {
    expect(contactDemandTypeSchema.safeParse('materiel').success).toBe(true);

    const materielContact = { ...completeContact, demandType: 'materiel' as const };
    expect(contactFormSchema.safeParse(materielContact).success).toBe(true);
    expect(isContactFormComplete(materielContact)).toBe(true);

    const states = contactRequiredFieldStates(materielContact);
    expect(states.find((field) => field.key === 'demandType')?.valid).toBe(true);
  });

  it('rejects a demand type outside the whitelist, such as an arbitrary URL parameter', () => {
    expect(contactDemandTypeSchema.safeParse('materiel-urgent').success).toBe(false);
    expect(contactDemandTypeSchema.safeParse('<script>').success).toBe(false);
    expect(contactFormSchema.safeParse({ ...completeContact, demandType: 'unknown' }).success).toBe(false);
  });
});
