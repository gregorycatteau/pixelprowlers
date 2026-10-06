import { computed, ref } from 'vue';
import { deviceFamilies, symptomsByFamily, estimateRepair, publishedRepairGrid, type DeviceFamily, type RepairGrid } from '~/utils/repairGrid';
/** Chaque appel crée son propre état ; aucune donnée visiteur n’est partagée en SSR. */
export function useRepairJourney(grid: RepairGrid = publishedRepairGrid) {
  const family = ref<DeviceFamily | ''>('');
  const symptom = ref('');
  const model = ref('');
  const step = ref<'device' | 'problem' | 'budget'>('device');
  const result = computed(() => estimateRepair(grid, family.value, symptom.value, model.value));
  const models = computed(() => grid.models[family.value as DeviceFamily] ?? []);
  /** Un changement de famille invalide les choix dépendants, même si leurs codes se ressemblent. */
  function chooseFamily(value: DeviceFamily) {
    if (!deviceFamilies.some(f => f.id === value && f.active)) return false;
    if (family.value !== value) { symptom.value = ''; model.value = ''; }
    family.value = value; step.value = 'problem'; return true;
  }
  /** N’accepte que les observations proposées pour l’appareil actif. */
  function chooseSymptom(value: string) {
    if (!family.value || !symptomsByFamily[family.value].some(s => s.id === value)) return false;
    symptom.value = value; step.value = 'budget'; return true;
  }
  /** Un modèle inconnu suit les règles générales, sans réutiliser un tarif de modèle précis. */
  function chooseModel(value: string) { model.value = models.value.some(m => m.id === value) ? value : ''; }
  /** Réinitialise uniquement les choix du parcours ; les coordonnées ne sont pas stockées ici. */
  function reset() { family.value = ''; symptom.value = ''; model.value = ''; step.value = 'device'; }
  return { family, symptom, model, step, models, result, chooseFamily, chooseSymptom, chooseModel, reset };
}
