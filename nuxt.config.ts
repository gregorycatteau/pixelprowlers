import { fileURLToPath } from 'node:url';

const mainCssPath = fileURLToPath(new URL('./app/assets/css/main.css', import.meta.url));

export default defineNuxtConfig({
  compatibilityDate: '2026-07-04',
  srcDir: 'app',
  css: [mainCssPath],
  runtimeConfig: {
    graphqlApiUrl: process.env.GRAPHQL_API_URL || 'http://pixelprowlers-django:8000/graphql/',
    public: {
      graphqlApiUrl: process.env.NUXT_PUBLIC_GRAPHQL_API_URL || '/graphql/',
    },
  },
  postcss: {
    plugins: {
      '@tailwindcss/postcss': {},
    },
  },
});
