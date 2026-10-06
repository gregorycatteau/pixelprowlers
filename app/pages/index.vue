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

/*
 * Le titre nomme d'abord le métier d'atelier — réparer, vendre du
 * reconditionné — puis le volet numérique. L'ordre n'est pas cosmétique :
 * c'est la requête qui amène réellement les visiteurs, et le libellé
 * qu'ils reconnaissent dans une page de résultats.
 */
const title =
  'Réparation au composant, micro-soudure et réemploi | PixelProwlers';

const description = [
  'Diagnostic, réparation au composant et micro-soudure. Matériel',
  'reconditionné, conseil, cybersécurité, développement et formation',
  'pour prolonger les usages et garder la main sur vos outils.',
].join(' ');

const heroContent = {
  eyebrow: 'Réparation informatique · Micro-soudure',
  title: 'Avant de remplacer votre appareil, parlons réparation.',
  subtitle: 'Prise de charge endommagée, port HDMI abîmé, circuit électronique en panne : nous recherchons la cause et intervenons au composant lorsque c’est adapté.',
  ctaText: 'Estimer le budget de ma réparation',
  ctaLink: '/reparation-informatique#parcours-reparation',
  secondaryCtaText: 'Décrire ma panne directement',
  secondaryCtaLink: '/contact?besoin=reparation',
  ctaNote: 'Une proposition claire. Votre accord avant intervention.',
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

      /*
       * L'ordre reflète l'activité : le matériel d'abord. La liste
       * annonçait jusqu'ici cinq prestations web et aucune réparation
       * physique, ce que contredisait déjà le contenu du site.
       */
      serviceType: [
        'Réparation d’ordinateurs',
        'Réparation de téléphones et tablettes',
        'Vente de matériel informatique reconditionné',
        'Reconditionnement et réemploi de matériel',
        'Migration vers Linux',
        'Conseil et assistance informatique',
        'Cybersécurité dans un périmètre autorisé',
        'Audit et réparation de sites web',
        'Développement de sites, applications et outils métier',
        'Sécurisation des accès',
        'Documentation et transmission',
        'Formation et ateliers numériques',
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
