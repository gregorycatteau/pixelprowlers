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

// Les métadonnées de l’accueil donnent la priorité à la réparation et à la micro-soudure.
const title =
  'Pixelprowlers | Réparation informatique et micro-soudure en Médoc';

const description =
  'Réparation informatique et micro-soudure dans le Médoc. Estimez votre budget et échangez avec un atelier passionné. Matériel reconditionné et Linux.';

const heroContent = {
  eyebrow: 'Réparation informatique et micro-soudure dans le Médoc.',
  title: 'Avant de remplacer votre appareil, parlons réparation.',
  subtitle: 'Prise de charge endommagée, port HDMI abîmé, circuit électronique en panne : nous recherchons la cause et intervenons au composant lorsque c’est adapté.',
  ctaText: 'Estimer ma réparation',
  ctaLink: '/reparation-informatique#parcours-reparation',
  secondaryCtaText: 'Décrire ma panne directement',
  secondaryCtaLink: '/contact?besoin=reparation',
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
      '@type': 'Organization',
      '@id': `${siteUrl}/#organization`,
      name: 'PixelProwlers',
      legalName:
        'Monsieur Grégory Catteau – PixelProwlers',

      url: canonicalUrl,
      telephone: '+33668145152',

      address: {
        '@type': 'PostalAddress',
        name: 'Adresse administrative — modalités de prise en charge à convenir après contact',
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
    },
    {
      '@type': 'Service',
      '@id': `${siteUrl}/#reparation-medoc`,
      name: 'Réparation informatique et micro-soudure dans le Médoc',
      serviceType: 'Diagnostic et réparation informatique, réparation au composant et micro-soudure',
      url: `${siteUrl}/reparation-informatique`,
      provider: { '@id': `${siteUrl}/#organization` },
      areaServed: { '@type': 'Place', name: 'Médoc' },
    },
    {
      '@type': 'Service',
      '@id': `${siteUrl}/#reemploi-medoc`,
      name: 'Matériel informatique reconditionné et réemploi dans le Médoc',
      serviceType: 'Matériel informatique reconditionné selon disponibilités',
      url: `${siteUrl}/materiel-reconditionne`,
      provider: { '@id': `${siteUrl}/#organization` },
      areaServed: { '@type': 'Place', name: 'Médoc' },
    },
    {
      '@type': 'Service',
      '@id': `${siteUrl}/#services-numeriques`,
      name: 'Conseil, cybersécurité et développement',
      url: `${siteUrl}/services-numeriques`,
      provider: { '@id': `${siteUrl}/#organization` },
    },
    {
      '@type': 'Service',
      '@id': `${siteUrl}/#formation`,
      name: 'Formation et transmission numériques',
      url: `${siteUrl}/formations`,
      provider: { '@id': `${siteUrl}/#organization` },
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
