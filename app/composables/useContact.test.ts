import { describe, expect, it } from 'vitest';

import {
  CONTACT_CONFIRMATION_STORAGE_KEY,
  contactDemandOptions,
  isContactDemandType,
  parseStoredContactConfirmation,
  resolveDemandTypeFromQuery,
  serviceTypeFromDemand,
  useContactForm,
} from './useContact';

describe('materiel demand type contract', () => {
  it('exposes a materiel option covering repair, refurbishment and Linux migration', () => {
    const option = contactDemandOptions.find(
      (item) => item.value === 'materiel',
    );

    expect(option).toBeDefined();
    expect(option?.label).toBe(
      'Réparation, reconditionnement ou migration Linux',
    );
  });

  it('maps the materiel demand type to the existing ServiceType.MATERIEL value', () => {
    expect(serviceTypeFromDemand('materiel')).toBe('materiel');
  });

  it('accepts materiel and rejects unknown values through the whitelist', () => {
    expect(isContactDemandType('materiel')).toBe(true);
    expect(isContactDemandType('unknown-value')).toBe(false);
    expect(isContactDemandType(undefined)).toBe(false);
    expect(isContactDemandType('')).toBe(false);
  });

  it('does not regress the mapping of the other existing demand types', () => {
    expect(serviceTypeFromDemand('urgency')).toBe('urgence');
    expect(serviceTypeFromDemand('audit')).toBe('audit_site');
    expect(serviceTypeFromDemand('refonte')).toBe('site_maintenable');
    expect(serviceTypeFromDemand('transmission')).toBe('maintenance_documentation');
    expect(serviceTypeFromDemand('diagnostic')).toBe('audit_site');
    expect(serviceTypeFromDemand('partnership')).toBe('autre');
  });

  it('does not regress the presence of the other existing demand options', () => {
    const values = contactDemandOptions.map((option) => option.value);

    expect(values).toEqual([
      'diagnostic',
      'urgency',
      'audit',
      'refonte',
      'transmission',
      'materiel',
      'partnership',
    ]);
  });
});

describe('/contact?demande= preselection (resolveDemandTypeFromQuery)', () => {
  it('preselects materiel from the query string used by the /reparation-informatique CTA', () => {
    expect(resolveDemandTypeFromQuery('materiel')).toBe('materiel');
  });

  it('preselects the other existing values the same way', () => {
    expect(resolveDemandTypeFromQuery('urgency')).toBe('urgency');
    expect(resolveDemandTypeFromQuery('audit')).toBe('audit');
  });

  it('ignores an unknown value instead of forwarding it', () => {
    expect(resolveDemandTypeFromQuery('materiel-urgent')).toBeUndefined();
    expect(resolveDemandTypeFromQuery('<script>alert(1)</script>')).toBeUndefined();
    expect(resolveDemandTypeFromQuery('')).toBeUndefined();
  });

  it('ignores absent, null or non-string values without throwing', () => {
    expect(resolveDemandTypeFromQuery(undefined)).toBeUndefined();
    expect(resolveDemandTypeFromQuery(null)).toBeUndefined();
    expect(resolveDemandTypeFromQuery(42)).toBeUndefined();
  });

  it('only reads the first entry of a repeated query parameter, and still whitelists it', () => {
    expect(resolveDemandTypeFromQuery(['materiel', 'audit'])).toBe('materiel');
    expect(resolveDemandTypeFromQuery(['unknown', 'materiel'])).toBeUndefined();
    expect(resolveDemandTypeFromQuery([])).toBeUndefined();
  });
});

describe('useContactForm preselection (ContactForm.vue initial-demand-type prop)', () => {
  it('initializes the reactive form with the whitelisted preselected value', () => {
    const { form } = useContactForm('materiel');

    expect(form.demandType).toBe('materiel');
  });

  it('lets the user change the preselected radio afterwards', () => {
    const { form } = useContactForm('materiel');

    form.demandType = 'audit';

    expect(form.demandType).toBe('audit');
  });

  it('falls back to no preselection when no initial value is given, as before', () => {
    const { form } = useContactForm();

    expect(form.demandType).toBe('');
  });

  it('ignores an initial value outside the whitelist as a defense-in-depth check', () => {
    const { form } = useContactForm('not-a-real-demand-type' as never);

    expect(form.demandType).toBe('');
  });
});

describe('contact confirmation storage contract (/contact/confirmation)', () => {
  it('accepts a validly shaped stored confirmation', () => {
    const raw = JSON.stringify({
      numeroDossier: '20072026001',
      message: 'Votre demande a bien été enregistrée.',
    });

    expect(parseStoredContactConfirmation(raw)).toEqual({
      numeroDossier: '20072026001',
      message: 'Votre demande a bien été enregistrée.',
    });
  });

  it('rejects when sessionStorage has nothing (direct access without context)', () => {
    expect(parseStoredContactConfirmation(null)).toBeNull();
  });

  it('rejects a dossier number that is not exactly 11 digits', () => {
    const raw = JSON.stringify({ numeroDossier: '123', message: 'x' });
    expect(parseStoredContactConfirmation(raw)).toBeNull();
  });

  it('rejects malformed JSON without throwing', () => {
    expect(() => parseStoredContactConfirmation('not-json{')).not.toThrow();
    expect(parseStoredContactConfirmation('not-json{')).toBeNull();
  });

  it('rejects a payload missing the message', () => {
    const raw = JSON.stringify({ numeroDossier: '20072026001' });
    expect(parseStoredContactConfirmation(raw)).toBeNull();
  });

  it('never derives the confirmation from the URL: the storage key is the only source', () => {
    expect(CONTACT_CONFIRMATION_STORAGE_KEY).toBe('pixelprowlers-contact-confirmation');
  });
});
