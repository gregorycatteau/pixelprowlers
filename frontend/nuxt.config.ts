export default defineNuxtConfig({
  devtools: { enabled: true },

  css: ['~/assets/css/main.css'],

  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  },

  // Modules
  modules: [
    '@nuxtjs/tailwindcss',
  ],

  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_URL || 'http://localhost:8001',
    },
  },

  app: {
    head: {
      title: 'PixelProwlers | Sites sobres, sécurité concrète et autonomie numérique',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { 
          name: 'description', 
          content: 'Audit sécurité de site web, sites sobres maintenables, documentation, Linux, open source et reconditionné sérieux pour petites structures utiles.' 
        },
        { 
          name: 'keywords', 
          content: 'audit sécurité site web, site sobre, maintenance WordPress, open source, Linux, matériel reconditionné' 
        },
        { property: 'og:type', content: 'website' },
        { property: 'og:title', content: 'PixelProwlers | Sites sobres, sécurité concrète et autonomie numérique' },
        { 
          property: 'og:description',
          content: 'Audit sécurité, sites maintenables, documentation et accompagnement numérique pour associations, TPE, indépendants et collectifs.' 
        },
        { property: 'og:url', content: 'https://pixelprowlers.io/' },
        { property: 'og:image', content: 'https://pixelprowlers.io/og-pixelprowlers.png' },
        { property: 'og:site_name', content: 'PixelProwlers' },
        { name: 'twitter:card', content: 'summary_large_image' },
        { name: 'twitter:title', content: 'PixelProwlers | Sites sobres, sécurité concrète et autonomie numérique' },
        {
          name: 'twitter:description',
          content: 'Audit sécurité, sites maintenables, documentation et accompagnement numérique pour associations, TPE, indépendants et collectifs.'
        },
        { name: 'twitter:image', content: 'https://pixelprowlers.io/og-pixelprowlers.png' },
      ],
      link: [
        { rel: 'icon', type: 'image/png', href: '/logo-nav.png' },
      ],
    },
  },

  compatibilityDate: '2024-12-31',
});
