import { describe, expect, it } from 'vitest';
import { contextualCtaFor, activePillarHrefFor } from './navigation';
describe('Orientation de l’urgence web', () => {
  it.each(['/urgence', '/urgence/', '/urgence?origine=menu#haut'])('oriente %s vers le formulaire incident', path => {
    expect(contextualCtaFor(path)).toEqual({ label: 'Signaler un incident', href: '/urgence#urgence-formulaire' });
    expect(activePillarHrefFor(path)).toBeNull();
  });
  it('conserve le contact sans CTA et la réparation matérielle dans son parcours', () => {
    expect(contextualCtaFor('/contact?besoin=reparation')).toBeNull();
    expect(contextualCtaFor('/reparation-informatique')?.href).toBe('/reparation-informatique#parcours-reparation');
  });
});
