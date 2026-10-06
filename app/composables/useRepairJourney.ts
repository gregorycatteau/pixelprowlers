import { computed, ref } from 'vue';
import { deviceFamilies, symptomsByFamily, precisionOptions, resolveScenarios, publishedRepairGrid, type DeviceFamily, type RepairGrid } from '~/utils/repairGrid';
/** Chaque appel isole les choix et la saisie par visiteur, sans stockage persistant. */
export function useRepairJourney(grid: RepairGrid = publishedRepairGrid) {
  const family = ref<DeviceFamily | ''>(''), symptom = ref(''), precision = ref(''), model = ref('');
  const step = ref<'device' | 'problem' | 'precision' | 'budget'>('device');
  const options = computed(() => precisionOptions(family.value, symptom.value));
  const result = computed(() => resolveScenarios(grid, family.value, symptom.value, precision.value));
  /** Un changement de famille invalide les informations dépendantes ; un retour compatible les garde. */
  function chooseFamily(value: DeviceFamily) {
    if (!deviceFamilies.some(f => f.id === value && f.active)) return false;
    if (family.value !== value) { symptom.value = ''; precision.value = ''; model.value = ''; }
    family.value = value; step.value = 'problem'; return true;
  }
  /** Le symptôme mène au budget, ou à une seule précision utile avec une option inconnue. */
  function chooseSymptom(value: string) {
    if (!family.value || !symptomsByFamily[family.value].some(s => s.id === value)) return false;
    if (symptom.value !== value) precision.value = '';
    symptom.value = value; step.value = options.value.length && !precision.value ? 'precision' : 'budget'; return true;
  }
  /** Valide les codes de précision par allowlist et recalcule immédiatement les scénarios. */
  function choosePrecision(value: string) {
    if (!options.value.some(p => p.id === value)) return false;
    precision.value = value; step.value = 'budget'; return true;
  }
  /** Un modèle libre aide la demande, sans modifier un budget ni affirmer une compatibilité. */
  function chooseModel(value: string) { model.value = value.slice(0, 120); }
  /** Réinitialise explicitement les choix du parcours. */
  function reset() { family.value = ''; symptom.value = ''; precision.value = ''; model.value = ''; step.value = 'device'; }
  return { family, symptom, precision, model, step, options, result, chooseFamily, chooseSymptom, choosePrecision, chooseModel, reset };
}
