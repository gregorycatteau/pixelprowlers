import { fileURLToPath } from 'node:url';

const mainCssPath = fileURLToPath(new URL('./app/assets/css/main.css', import.meta.url));

export default defineNuxtConfig({
  compatibilityDate: '2026-07-04',
  srcDir: 'app',
  css: [mainCssPath],
  postcss: {
    plugins: {
      '@tailwindcss/postcss': {},
    },
  },
});
