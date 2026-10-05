import { fileURLToPath } from 'node:url';
import { defineConfig } from 'vitest/config';

/*
 * Résout l’alias `~` (et `@`, équivalent) vers le dossier `app`, comme le
 * fait Nuxt via `srcDir: 'app'` dans nuxt.config.ts. Nécessaire pour tester
 * les composables en dehors du runtime Nuxt.
 */
const appDir = fileURLToPath(new URL('./app', import.meta.url));

export default defineConfig({
  resolve: {
    alias: {
      '~': appDir,
      '@': appDir,
    },
  },
});
