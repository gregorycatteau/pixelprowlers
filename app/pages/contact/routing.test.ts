import { describe, expect, it } from 'vitest';

/*
 * Garde-fou contre la régression corrigée ici : Nuxt imbrique
 * automatiquement une page `pages/contact.vue` avec un dossier `contact/`
 * de même nom, sans offrir d'outlet <NuxtPage /> pour ses enfants — ce qui
 * faisait que /contact/confirmation rendait silencieusement /contact.
 * La page « index » du dossier doit rester la seule route parente.
 *
 * import.meta.glob (Vite) est utilisé plutôt que node:fs pour rester dans
 * le même environnement de résolution de modules que le reste de l'app.
 */
const contactSiblingFile = import.meta.glob('../contact.vue');
const contactIndexFile = import.meta.glob('./index.vue');
const confirmationFile = import.meta.glob('./confirmation.vue');

describe('contact route structure (/contact and /contact/confirmation)', () => {
  it('exposes contact as an index page inside the contact/ folder', () => {
    expect(Object.keys(contactIndexFile)).toHaveLength(1);
  });

  it('exposes confirmation as a sibling page, not nested under contact.vue', () => {
    expect(Object.keys(confirmationFile)).toHaveLength(1);
  });

  it('does not have a sibling contact.vue that would shadow the contact/ folder', () => {
    expect(Object.keys(contactSiblingFile)).toHaveLength(0);
  });
});
