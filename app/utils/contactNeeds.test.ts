import { describe, expect, it } from 'vitest';
import { buildContactMessage, contactApiMapping, CONTACT_MESSAGE_LIMIT, resolveContactNeed } from './contactNeeds';

describe('Présélection et contrat historique du contact', () => {
  it.each(Object.keys(contactApiMapping))('accepte le code autorisé %s', value => {
    expect(resolveContactNeed(value)).toBe(value);
  });
  it.each([undefined, null, 42, {}, ['reparation'], 'constructor', '__proto__', 'symptome=secret', 'inconnu'])('refuse une valeur non autorisée %j', value => {
    expect(resolveContactNeed(value)).toBe('');
  });
  it('utilise uniquement les services et types historiques, sans envoyer le code public comme type API', () => {
    const services = ['materiel', 'maintenance_documentation', 'developpement', 'formation', 'autre'];
    const demands = ['diagnostic', 'partnership', 'transmission', 'refonte'];
    for (const entry of Object.values(contactApiMapping)) {
      expect(services).toContain(entry.serviceType);
      expect(demands).toContain(entry.demandType);
    }
    expect(contactApiMapping.reparation.serviceType).toBe('materiel');
    expect(contactApiMapping.reemploi.serviceType).toBe('materiel');
    expect(contactApiMapping.formation.serviceType).toBe('formation');
  });
  it('enrichit le besoin actif sans transmettre les détails d’un autre besoin', () => {
    const message = buildContactMessage({ need: 'reparation', message: 'Texte intact\nDeuxième ligne', deviceType: 'Ordinateur', model: 'Modèle connu', usage: 'Usage masqué', budget: 'Budget masqué' });
    expect(message).toContain('Ordinateur');
    expect(message).toContain('Modèle connu');
    expect(message.endsWith('Texte intact\nDeuxième ligne')).toBe(true);
    expect(message).not.toContain('Usage masqué');
    expect(message).not.toContain('Budget masqué');
  });
  it('ne tronque pas silencieusement un message dépassant la limite API', () => {
    const message = 'x'.repeat(CONTACT_MESSAGE_LIMIT + 1);
    expect(buildContactMessage({ need: 'autre', message, deviceType: '', model: '', usage: '', budget: '' })).toContain(message);
  });
});
