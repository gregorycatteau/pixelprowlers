import { describe, expect, it } from 'vitest';
import {
  auditIdentitySchema,
  createAuditAnswersSchema,
  emailSchema,
  frenchPhoneSchema,
  humanNameSchema,
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
