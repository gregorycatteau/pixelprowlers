import { describe, expect, it } from 'vitest';
import { useRepairJourney } from './useRepairJourney';
import type { RepairGrid } from '~/utils/repairGrid';
describe('État du parcours réparation', () => {
  it('conserve un retour compatible mais invalide un changement de famille', () => {
    const j = useRepairJourney(); j.chooseFamily('phone'); j.chooseSymptom('battery');
    j.step.value = 'device'; j.chooseFamily('phone'); expect(j.symptom.value).toBe('battery');
    j.chooseFamily('desktop'); expect(j.symptom.value).toBe(''); expect(j.model.value).toBe('');
    expect(j.chooseSymptom('battery')).toBe(false);
  });
  it('recalcule immédiatement et refuse les choix non couverts', () => {
    const j = useRepairJourney(); expect(j.chooseFamily('console')).toBe(false);
    j.chooseFamily('phone'); j.chooseSymptom('charge'); expect(j.result.value.estimate.kind).toBe('unavailable');
    j.chooseModel('inconnu'); expect(j.model.value).toBe('');
    j.reset(); expect(j.family.value).toBe(''); expect(j.symptom.value).toBe(''); expect(j.step.value).toBe('device');
  });
  it('isole deux visiteurs et ne partage pas les coordonnées', () => {
    const a = useRepairJourney(), b = useRepairJourney(); a.chooseFamily('laptop');
    expect(b.family.value).toBe(''); expect(Object.keys(a)).not.toContain('email');
  });
});

describe('Recalcul avec tarifs synthétiques exclusivement de test', () => {
  it('remplace le forfait par le diagnostic après changement de symptôme ou de modèle', () => {
    const grid: RepairGrid = { version: 'TEST', date: '2000-01-01', models: { phone: [{ id: 'fictif', brand: 'Test', label: 'Test' }] }, diagnostic: { kind: 'diagnostic', amount: 12, deduction: '', includes: [], excludes: [] }, rules: [{ family: 'phone', symptom: 'screen', model: 'fictif', service: 'Test', identified: true, estimate: { kind: 'fixed', amount: 72, includes: [], excludes: [] } }] };
    const j = useRepairJourney(grid); j.chooseFamily('phone'); j.chooseModel('fictif'); j.chooseSymptom('screen');
    expect(j.result.value.estimate.kind).toBe('fixed');
    j.chooseModel('inconnu'); expect(j.result.value.estimate.kind).toBe('diagnostic');
    j.chooseModel('fictif'); j.chooseSymptom('charge'); expect(j.result.value.estimate.kind).toBe('diagnostic');
  });
});
