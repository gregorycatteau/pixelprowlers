import { fileURLToPath } from 'node:url';

const mainCssPath = fileURLToPath(new URL('./app/assets/css/main.css', import.meta.url));
const isProduction = process.env.NODE_ENV === 'production';
const defaultGraphqlApiUrl = isProduction ? '/graphql/' : 'http://127.0.0.1:8000/graphql/';

export default defineNuxtConfig({
  compatibilityDate: '2026-07-04',
  srcDir: 'app',
  css: [mainCssPath],
  runtimeConfig: {
    graphqlApiUrl: process.env.GRAPHQL_API_URL || defaultGraphqlApiUrl,
    public: {
      apiBaseUrl: process.env.NUXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000',
      graphqlApiUrl: process.env.NUXT_PUBLIC_GRAPHQL_API_URL || `${process.env.NUXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000'}/graphql/`,
    },
  },
  postcss: {
    plugins: {
      '@tailwindcss/postcss': {},
    },
  },
});
