import { describe, expect, it } from 'vitest';
import { useRepairJourney } from './useRepairJourney';
describe('Parcours avec budgets', () => {
  it('conserve les retours compatibles et invalide le changement de famille', () => {
    const j=useRepairJourney();j.chooseFamily('controller');j.chooseSymptom('drift');expect(j.step.value).toBe('precision');
    j.choosePrecision('two');expect(j.result.value.offers[0]?.id).toBe('controller-drift-two');
    j.step.value='device';j.chooseFamily('controller');expect(j.precision.value).toBe('two');
    j.chooseFamily('phone');expect(j.symptom.value).toBe('');expect(j.precision.value).toBe('');expect(j.model.value).toBe('');
  });
  it('recalcule les budgets et invalide les précisions incompatibles', () => {
    const j=useRepairJourney();j.chooseFamily('phone');j.chooseSymptom('screen');j.choosePrecision('oled');
    expect(j.result.value.offers[0]?.id).toBe('phone-screen-oled');
    j.chooseSymptom('battery');expect(j.precision.value).toBe('');expect(j.step.value).toBe('budget');
    expect(j.result.value.offers[0]?.id).toBe('phone-battery');expect(j.choosePrecision('oled')).toBe(false);
  });
  it('un modèle inconnu ne masque pas le budget et ne prouve aucune compatibilité', () => {
    const j=useRepairJourney();j.chooseFamily('laptop');j.chooseSymptom('slow');const ids=j.result.value.offers.map(o=>o.id);
    j.chooseModel('Modèle inconnu');expect(j.result.value.offers.map(o=>o.id)).toEqual(ids);
    j.chooseModel('x'.repeat(200));expect(j.model.value.length).toBe(120);
    j.reset();expect(j.family.value).toBe('');expect(j.model.value).toBe('');expect(j.step.value).toBe('device');
  });
  it('isole les visiteurs et refuse les codes incompatibles', () => {
    const a=useRepairJourney(),b=useRepairJourney();a.chooseFamily('console');expect(b.family.value).toBe('');
    expect(a.chooseSymptom('battery')).toBe(false);expect(a.chooseFamily('other')).toBe(false);
  });
});
