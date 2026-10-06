<template>
  <main class="ServicesPage">
    <section class="container Intro" aria-labelledby="services-title"><p class="eyebrow">Conseil · Cybersécurité · Développement</p><h1 id="services-title" class="pxp-font-display">Des outils qui vous simplifient le quotidien.</h1><p>Une difficulté à résoudre, des accès à clarifier ou un projet à construire : partons de vos usages.</p><AppButton href="/contact?besoin=conseil">Décrire ma situation</AppButton></section>
    <section id="conseil-cybersecurite" class="container Cards" aria-label="Conseil et cybersécurité">
      <article><h2>Résoudre une difficulté.</h2><p>Choisir un logiciel, comprendre une configuration ou débloquer un usage : avançons sur votre problème concret.</p><NuxtLink to="/contact?besoin=conseil">Demander conseil →</NuxtLink><NuxtLink to="/diagnostic-situation">Faire le bilan numérique →</NuxtLink></article>
      <article><h2>Sécuriser son activité.</h2><p>Examiner les accès, les sauvegardes et les points fragiles de votre site pour classer les actions utiles.</p><NuxtLink to="/audit-site-web">Examiner mon site →</NuxtLink><NuxtLink to="/transmission-acces">Clarifier mes accès →</NuxtLink></article>
    </section>
    <section id="developpement" class="container Development"><h2>Créer un site ou un outil.</h2><p>Présenter votre activité, suivre votre travail ou simplifier une tâche répétitive : définissons un outil maintenable, adapté à votre besoin.</p><div class="Links"><NuxtLink to="/refonte-site">Parler de mon site →</NuxtLink><NuxtLink to="/contact?besoin=developpement">Décrire mon projet d’application →</NuxtLink></div></section>
    <section class="container Agreement"><h2>Un cadre convenu ensemble.</h2><p>Les interventions de cybersécurité portent sur les systèmes autorisés. Nous définissons le périmètre, les accès et les actions avant toute modification.</p><NuxtLink to="/urgence">Un site bloqué ? Signaler un incident →</NuxtLink></section>
  </main>
</template>
<script setup lang="ts">
import AppButton from '~/components/ui/AppButton.vue';

const runtimeConfig = useRuntimeConfig();

/*
 * Page carrefour : elle oriente vers les pages spécialisées, qui gardent
 * leurs URL et leur contenu commercial. Elle ne les recopie pas, pour ne pas
 * se mettre en concurrence avec elles.
 */
const siteUrl = String(
  runtimeConfig.public.siteUrl || 'https://pixelprowlers.io',
).replace(/\/+$/, '');

const canonicalUrl = `${siteUrl}/services-numeriques`;

const title = 'Conseil, cybersécurité et développement web et logiciel | PixelProwlers';

const description = [
  'Conseil, assistance et cybersécurité dans un cadre autorisé.',
  'Développement de sites, applications et outils métier : des besoins',
  'définis ensemble, des données maîtrisées et une maintenance prévue.',
].join(' ');

useSeoMeta({
  title,
  description,
  robots: 'index, follow',

  ogType: 'website',
  ogTitle: title,
  ogDescription: description,
  ogUrl: canonicalUrl,
  ogSiteName: 'PixelProwlers',

  twitterCard: 'summary',
  twitterTitle: title,
  twitterDescription: description,
});

useHead({
  link: [
    {
      rel: 'canonical',
      href: canonicalUrl,
    },
  ],

  script: [
    {
      type: 'application/ld+json',
      textContent: JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'WebPage',
        name: title,
        description,
        url: canonicalUrl,
        isPartOf: {
          '@type': 'WebSite',
          name: 'PixelProwlers',
          url: siteUrl,
        },
        about: [
          'Conseil et assistance informatique',
          'Audit de sécurité de site web',
          'Transmission et sécurisation des accès',
          'Développement de sites, applications et outils métier',
          'Autonomie numérique',
        ],
      }),
    },
  ],
});
</script>

<style scoped>
@reference "../assets/css/main.css";
.ServicesPage { @apply bg-pxp-paper text-pxp-ink; }
.Intro { @apply grid gap-5 py-10 md:py-16; }
h1 { @apply max-w-4xl text-5xl leading-none md:text-6xl; }
h2 { @apply text-3xl font-bold; }
p { @apply max-w-3xl leading-relaxed; }
.Cards { @apply grid gap-8 py-8 md:grid-cols-2; }
.Cards article { @apply grid content-start gap-4 border-t border-pxp-green/25 pt-6; }
.Development, .Agreement { @apply grid gap-5 py-10; }
.Agreement { @apply border-t border-pxp-green/25 pb-16; }
.Links { @apply flex flex-wrap gap-x-8 gap-y-2; }
a { @apply inline-flex min-h-11 w-fit items-center text-pxp-green font-semibold underline underline-offset-4 focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-pxp-green; }
:deep(.ButtonPrimary) { @apply no-underline text-white; }
.Cards, .Development { @apply scroll-mt-32; }
</style>
