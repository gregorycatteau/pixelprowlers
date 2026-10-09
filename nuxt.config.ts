import { fileURLToPath } from 'node:url';

const mainCssPath = fileURLToPath(new URL('./app/assets/css/main.css', import.meta.url));
const isProduction = process.env.NODE_ENV === 'production';
const defaultGraphqlApiUrl = isProduction ? '/graphql/' : 'http://127.0.0.1:8000/graphql/';

export default defineNuxtConfig({
  compatibilityDate: '2026-07-04',
  srcDir: 'app',
  css: [mainCssPath],
  app: {
    pageTransition: { name: 'page', mode: 'out-in' },
    head: {
      link: [
        { rel: 'icon', type: 'image/svg+xml', sizes: 'any', href: '/favicon.svg' },
        { rel: 'icon', type: 'image/x-icon', sizes: '16x16 32x32 48x48', href: '/favicon.ico' },
        { rel: 'icon', type: 'image/png', sizes: '96x96', href: '/favicon-96x96.png' },
        { rel: 'apple-touch-icon', sizes: '180x180', href: '/apple-touch-icon.png' },
      ],
    },
  },
  routeRules: {
    '/reparation-informatique/decrire-ma-panne': { redirect: '/contact?besoin=reparation' },
    '/ticket/**': { headers: { 'X-Robots-Tag': 'noindex, nofollow', 'Cache-Control': 'no-store', 'Referrer-Policy': 'no-referrer' } },
    '/audit-refonte/resultat': { headers: { 'X-Robots-Tag': 'noindex, nofollow', 'Cache-Control': 'no-store', 'Referrer-Policy': 'no-referrer' } },
    '/diagnostic-result/**': { headers: { 'X-Robots-Tag': 'noindex, nofollow', 'Cache-Control': 'no-store', 'Referrer-Policy': 'no-referrer' } },
  },
  runtimeConfig: {
    graphqlApiUrl: process.env.GRAPHQL_API_URL || defaultGraphqlApiUrl,
    public: {
      apiBaseUrl: process.env.NUXT_PUBLIC_API_BASE_URL || (isProduction ? '' : 'http://127.0.0.1:8000'),
      graphqlApiUrl: process.env.NUXT_PUBLIC_GRAPHQL_API_URL || defaultGraphqlApiUrl,
    },
  },
  postcss: {
    plugins: {
      '@tailwindcss/postcss': {},
    },
  },
});
