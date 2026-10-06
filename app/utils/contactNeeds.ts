/** Besoins publics : seuls ces codes non personnels sont autorisés dans l’URL. */
export const contactDemandOptions = [
  { value: 'reparation', label: 'Réparer un appareil.' },
  { value: 'reemploi', label: 'Trouver un ordinateur reconditionné.' },
  { value: 'conseil', label: 'Obtenir un conseil, une assistance ou une intervention de cybersécurité.' },
  { value: 'developpement', label: 'Créer ou améliorer un site ou une application.' },
  { value: 'formation', label: 'Organiser une formation.' },
  { value: 'autre', label: 'Autre demande.' },
] as const;
export type ContactNeed = typeof contactDemandOptions[number]['value'];

/** Sépare les besoins publics des valeurs historiques reconnues par Django. */
export const contactApiMapping = {
  reparation: { serviceType: 'materiel', demandType: 'diagnostic' },
  reemploi: { serviceType: 'materiel', demandType: 'partnership' },
  conseil: { serviceType: 'maintenance_documentation', demandType: 'transmission' },
  developpement: { serviceType: 'developpement', demandType: 'refonte' },
  formation: { serviceType: 'formation', demandType: 'transmission' },
  autre: { serviceType: 'autre', demandType: 'partnership' },
} as const;

/** Refuse les paramètres inconnus, répétés, objets et clés héritées. */
export const resolveContactNeed = (value: unknown): ContactNeed | '' => (
  typeof value === 'string' && Object.hasOwn(contactApiMapping, value)
    ? value as ContactNeed : ''
);

export const CONTACT_MESSAGE_LIMIT = 4000;
export type ContactDescription = {
  need: ContactNeed | '';
  message: string;
  deviceType: string;
  model: string;
  usage: string;
  budget: string;
  repairContext?: string;
};

/** Enrichit le message sans le tronquer ; seuls les détails du besoin actif partent à l’API. */
export const buildContactMessage = (form: ContactDescription): string => {
  const option = contactDemandOptions.find(item => item.value === form.need);
  const lines = option ? [`Besoin : ${option.label}`] : [];
  const details = form.need === 'reparation'
    ? [['Appareil', form.deviceType], ['Modèle', form.model]]
    : form.need === 'reemploi' ? [['Usage', form.usage], ['Budget', form.budget]] : [];
  for (const [label, value] of details) {
    if (value?.trim()) lines.push(`${label} : ${value.trim()}`);
  }
  if (form.need === 'reparation' && form.repairContext?.trim()) lines.push(form.repairContext.trim());
  lines.push('', form.message.trim());
  return lines.join('\n');
};
