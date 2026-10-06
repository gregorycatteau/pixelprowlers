/** Grille publique : aucun montant n’est publié sans confirmation métier. */
export type DeviceFamily = 'laptop' | 'desktop' | 'phone' | 'tablet' | 'console' | 'controller' | 'other';
export type Estimate =
  | { kind: 'fixed'; amount: number; includes: string[]; excludes: string[] }
  | { kind: 'range'; min: number; max: number; includes: string[]; excludes: string[] }
  | { kind: 'diagnostic'; amount: number; deduction: string; includes: string[]; excludes: string[] }
  | { kind: 'unavailable'; reason: string };
export type RepairRule = { family: DeviceFamily; symptom: string; model?: string; service: string; identified: boolean; estimate: Estimate };
export type RepairGrid = { version: string; date: string; models: Partial<Record<DeviceFamily, { id: string; brand: string; label: string }[]>>; rules: RepairRule[]; diagnostic: Estimate };
export const deviceFamilies: readonly { id: DeviceFamily; label: string; active: boolean }[] = [
  { id: 'laptop', label: 'Ordinateur portable', active: true },
  { id: 'desktop', label: 'Ordinateur fixe', active: true },
  { id: 'phone', label: 'Téléphone', active: true },
  { id: 'tablet', label: 'Tablette', active: true },
  { id: 'console', label: 'Console', active: false },
  { id: 'controller', label: 'Manette', active: false },
  { id: 'other', label: 'Autre appareil', active: false },
];
export type Symptom = { id: string; label: string; electronic?: boolean };
const common: Symptom[] = [{ id: 'other', label: 'Autre problème' }, { id: 'unknown', label: 'Je ne sais pas' }];
const computer: Symptom[] = [
  { id: 'power', label: 'Ne démarre plus', electronic: true }, { id: 'heat', label: 'Chauffe ou fait du bruit' },
  { id: 'slow', label: 'Ralentit' }, { id: 'screen', label: 'Écran endommagé' },
  { id: 'charge', label: 'Ne charge plus', electronic: true }, { id: 'keyboard', label: 'Clavier défaillant' }, ...common,
];
const mobile: Symptom[] = [
  { id: 'screen', label: 'Écran cassé' }, { id: 'battery', label: 'Autonomie faible' },
  { id: 'charge', label: 'Ne charge plus', electronic: true }, { id: 'power', label: 'Ne s’allume plus', electronic: true },
  { id: 'sound', label: 'Problème de son' }, { id: 'liquid', label: 'Contact avec un liquide', electronic: true }, ...common,
];
export const symptomsByFamily: Record<DeviceFamily, readonly Symptom[]> = {
  laptop: computer, desktop: computer.filter(s => s.id !== 'charge'), phone: mobile, tablet: mobile,
  console: [{ id: 'power', label: 'Ne démarre plus', electronic: true }, { id: 'image', label: 'Aucune image' }, { id: 'heat', label: 'Surchauffe' }, { id: 'read', label: 'Problème de lecture' }, { id: 'connector', label: 'Connecteur endommagé', electronic: true }, ...common],
  controller: [{ id: 'drift', label: 'Joystick qui dérive' }, { id: 'button', label: 'Bouton défaillant' }, { id: 'charge', label: 'Ne charge plus', electronic: true }, { id: 'connection', label: 'Problème de connexion' }, ...common], other: common,
};
/** Périmètre issu de la page publiée f16e604 ; tarifs et modèles restent non qualifiés. */
export const publishedRepairGrid: RepairGrid = {
  version: 'reparation-20261006-v1-sans-tarifs', date: '2026-10-06', models: {}, rules: [],
  diagnostic: { kind: 'unavailable', reason: 'Le budget nécessite un diagnostic. Son coût sera précisé avant la prise en charge.' },
};
/** Vérifie les montants : une absence ou une valeur incohérente ne devient jamais zéro. */
export function validEstimate(estimate: Estimate): boolean {
  if (estimate.kind === 'unavailable') return true;
  const money = (value: number) => Number.isFinite(value) && value >= 0;
  return estimate.kind === 'range' ? money(estimate.min) && money(estimate.max) && estimate.max >= estimate.min : money(estimate.amount);
}
/** Recherche uniquement une règle compatible ; un modèle inconnu ne reçoit aucun tarif spécifique. */
export function estimateRepair(grid: RepairGrid, family: DeviceFamily | '', symptom: string, model = '') {
  const supported = deviceFamilies.some(f => f.id === family && f.active) && symptomsByFamily[family as DeviceFamily]?.some(s => s.id === symptom);
  if (!supported) return { estimate: { kind: 'unavailable', reason: 'Aucune estimation validée n’est disponible pour ce choix.' } as Estimate, service: 'Diagnostic de la panne', identified: false };
  const knownModel = grid.models[family as DeviceFamily]?.some(m => m.id === model);
  const rule = supported ? grid.rules.find(r => r.family === family && r.symptom === symptom && r.model === model && knownModel)
    ?? grid.rules.find(r => r.family === family && r.symptom === symptom && !r.model) : undefined;
  const candidate = rule?.estimate ?? grid.diagnostic;
  const estimate: Estimate = supported && validEstimate(candidate) ? candidate : { kind: 'unavailable', reason: 'Aucune estimation validée n’est disponible pour ce choix.' };
  return { estimate, service: rule?.service ?? 'Diagnostic de la panne', identified: Boolean(rule?.identified) };
}
/** Formate le repère TTC, sans déduire ni additionner de prestations. */
export function budgetLabel(estimate: Estimate): string {
  const euro = (amount: number) => new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' }).format(amount);
  if (!validEstimate(estimate)) return 'Estimation indisponible';
  if (estimate.kind === 'unavailable') return 'Estimation après diagnostic';
  if (estimate.kind === 'range') return `${euro(estimate.min)} à ${euro(estimate.max)} TTC`;
  return `${estimate.kind === 'diagnostic' ? 'Diagnostic : ' : ''}${euro(estimate.amount)} TTC`;
}
