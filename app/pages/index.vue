<template>
  <main>
    <HeroSection v-bind="heroContent" />
    <HomeSections />
  </main>
</template>

<script setup lang="ts">
import HeroSection from '~/components/Hero/HeroSection.vue';
import HomeSections from '~/components/sections/HomeSections.vue';

const runtimeConfig = useRuntimeConfig();

const siteUrl = String(
  runtimeConfig.public.siteUrl || 'https://pixelprowlers.io',
).replace(/\/+$/, '');

const canonicalUrl = `${siteUrl}/`;

const title =
  'Sites web maintenables et accès maîtrisés | PixelProwlers';

const description = [
  'PixelProwlers répare, sécurise et documente vos sites,',
  'vos accès et vos outils pour réduire votre dépendance',
  'numérique et préserver votre liberté de choix.',
].join(' ');

const heroContent = {
  eyebrow:
    'Numérique maintenable et transmissible',

  title:
    'Reprenez le contrôle de votre numérique.',

  secondaryTitle:
    'Des sites réparés, des accès sécurisés et une autonomie documentée.',

  subtitle: [
    'Nous réparons, sécurisons et documentons vos sites,',
    'vos accès et vos outils pour que votre activité ne dépende',
    'ni d’un prestataire opaque ni d’une plateforme qui décide',
    'à votre place.',
  ].join(' '),

  ctaText:
    'Faire le pré-diagnostic',

  ctaLink:
    '/diagnostic-situation',

  secondaryCtaText:
    'Décrire ma situation',

  secondaryCtaLink:
    '/contact',

  ctaNote: [
    '4 questions, environ 3 minutes.',
    'Résultat indicatif immédiat.',
    'Aucun accès demandé.',
  ].join(' '),

  trustItems: [
    'Aucune modification sans validation',
    'Interventions documentées',
    'Réversibilité privilégiée',
  ],
};

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

const structuredData = {
  '@context': 'https://schema.org',

  '@graph': [
    {
      '@type': 'WebSite',
      '@id': `${siteUrl}/#website`,
      name: 'PixelProwlers',
      url: canonicalUrl,
      inLanguage: 'fr-FR',
    },

    {
      '@type': 'ProfessionalService',
      '@id': `${siteUrl}/#organization`,
      name: 'PixelProwlers',
      legalName:
        'Monsieur Grégory Catteau – PixelProwlers',

      url: canonicalUrl,
      telephone: '+33668145152',

      areaServed: {
        '@type': 'Country',
        name: 'France',
      },

      address: {
        '@type': 'PostalAddress',
        streetAddress:
          'BP 10023, 102 rue Joseph et François Connord',

        postalCode: '33341',
        addressLocality: 'Lesparre Cedex',
        addressCountry: 'FR',
      },

      identifier: {
        '@type': 'PropertyValue',
        propertyID: 'SIREN',
        value: '520890336',
      },

      serviceType: [
        'Réparation de sites web',
        'Audit de sites web',
        'Sécurisation des accès',
        'Documentation et transmission',
        'Maintenance de sites web',
      ],
    },
  ],
};

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
      textContent: JSON.stringify(structuredData),
    },
  ],
});
</script>