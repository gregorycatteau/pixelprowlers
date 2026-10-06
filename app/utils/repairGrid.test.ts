import { describe, expect, it } from 'vitest';
import { budgetLabel, estimateRepair, publishedRepairGrid, validEstimate, type RepairGrid } from './repairGrid';
/** Montants synthétiques réservés aux tests : jamais importés dans la configuration publiée. */
const fixture: RepairGrid = {
  version: 'TEST-SEULEMENT', date: '2000-01-01',
  models: { phone: [{ id: 'test-model', brand: 'Fictif', label: 'Modèle de test' }] },
  diagnostic: { kind: 'diagnostic', amount: 11, deduction: 'Règle fictive de test', includes: ['Examen fictif'], excludes: [] },
  rules: [
    { family: 'phone', symptom: 'screen', model: 'test-model', service: 'Intervention de test', identified: true, estimate: { kind: 'fixed', amount: 71, includes: [], excludes: [] } },
    { family: 'laptop', symptom: 'heat', service: 'Intervention de test', identified: true, estimate: { kind: 'range', min: 31, max: 51, includes: [], excludes: [] } },
  ],
};
describe('Grille et budget', () => {
  it('ne publie aucun montant non confirmé', () => {
    expect(publishedRepairGrid.rules).toEqual([]);
    expect(estimateRepair(publishedRepairGrid, 'phone', 'screen').estimate.kind).toBe('unavailable');
    expect(budgetLabel(publishedRepairGrid.diagnostic)).not.toMatch(/0.*€/);
  });
  it('distingue forfait, fourchette et diagnostic', () => {
    expect(estimateRepair(fixture, 'phone', 'screen', 'test-model').estimate.kind).toBe('fixed');
    expect(estimateRepair(fixture, 'laptop', 'heat').estimate.kind).toBe('range');
    expect(estimateRepair(fixture, 'phone', 'charge').estimate.kind).toBe('diagnostic');
    expect(budgetLabel(fixture.diagnostic)).toContain('TTC');
  });
  it('ne réutilise pas le forfait pour un modèle inconnu', () => {
    expect(estimateRepair(fixture, 'phone', 'screen', 'inconnu').estimate.kind).toBe('diagnostic');
  });
  it('refuse les familles inactives et symptômes incompatibles', () => {
    expect(estimateRepair(fixture, 'console', 'power').estimate.kind).toBe('unavailable');
    expect(estimateRepair(fixture, 'desktop', 'battery').estimate.kind).toBe('unavailable');
  });
  it('refuse les valeurs absentes et fourchettes incohérentes sans conversion en zéro', () => {
    expect(validEstimate({ kind: 'fixed', amount: undefined as unknown as number, includes: [], excludes: [] })).toBe(false);
    expect(validEstimate({ kind: 'range', min: 50, max: 10, includes: [], excludes: [] })).toBe(false);
    expect(validEstimate({ kind: 'fixed', amount: NaN, includes: [], excludes: [] })).toBe(false);
  });
});
