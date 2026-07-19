import { describe, expect, it } from 'vitest';

import {
  contactDemandOptions,
  isContactDemandType,
  serviceTypeFromDemand,
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
