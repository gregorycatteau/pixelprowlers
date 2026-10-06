<template>
  <main class="pillar-page">
    <section class="pillar-hero" aria-labelledby="formations-title">
      <div class="form-container pillar-hero-content">
        <p class="eyebrow">Formations</p>

        <h1 id="formations-title">
          Des ateliers pour être plus à l’aise avec vos outils.
        </h1>

        <p class="pillar-introduction">
          Des gestes à pratiquer pour choisir vos logiciels, protéger vos comptes et organiser votre travail.
        </p>

        <div class="pillar-actions">
          <AppButton href="/contact?besoin=formation">
            Préparer un atelier
          </AppButton>
        </div>

        <p class="cta-note">
          Dites-nous qui doit être formé et sur quoi. Nous construisons le
          contenu à partir de votre situation réelle, pas d’un programme
          standard.
        </p>
      </div>
    </section>

    <section class="pillar-section" aria-labelledby="formations-themes-title">
      <div class="article-container">
        <h2 id="formations-themes-title">Ce que vous saurez faire</h2>

        <div v-reveal class="pillar-card-grid">
          <article v-for="theme in themes" :key="theme.title" class="pillar-card">
            <h3>{{ theme.title }}</h3>
            <p>{{ theme.description }}</p>
          </article>
        </div>
      </div>
    </section>

    <section class="pillar-section pillar-section-alt" aria-labelledby="formations-formats-title">
      <div class="article-container">
        <h2 id="formations-formats-title">Formats possibles</h2>

        <p class="pillar-section-intro">
          Le format se décide avec vous, selon le nombre de personnes à
          former et leur disponibilité.
        </p>

        <ul v-reveal class="pillar-principles">
          <li v-for="format in formats" :key="format">
            {{ format }}
          </li>
        </ul>


      </div>
    </section>

    <section class="pillar-final" aria-labelledby="formations-final-title">
      <div class="article-container">
        <h2 id="formations-final-title">Un besoin de formation&nbsp;?</h2>

        <p>
          Décrivez qui doit être formé, sur quel sujet et dans quel contexte.
          Nous définissons ensemble un contenu adapté.
        </p>

        <div class="pillar-actions">
          <AppButton href="/contact?besoin=formation">
            Préparer un atelier
          </AppButton>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
import AppButton from '~/components/ui/AppButton.vue';

const runtimeConfig = useRuntimeConfig();

const themes = [
  {
    title: 'Logiciel libre et formats ouverts',
    description:
      'Choisir un logiciel libre et reconnaître un format de fichier réutilisable.',
  },
  {
    title: 'Sécurité informatique',
    description:
      'Activer un second facteur, vérifier une sauvegarde et reconnaître une tentative d’hameçonnage.',
  },
  {
    title: 'Hygiène numérique',
    description:
      'Organiser les comptes, les accès partagés et les fichiers pour les retrouver.',
  },
  {
    title: 'Autonomie et choix d’outils',
    description:
      'Lire une proposition technique et poser les questions utiles avant de choisir.',
  },
  {
    title: 'Usages responsables',
    description:
      'Identifier les possibilités de réemploi et limiter les dépendances évitables.',
  },
];

const formats = [
  'En présentiel, sur site, pour un groupe déjà constitué.',
  'À distance, pour des participants dispersés géographiquement.',
  'En format hybride, quand une partie de l’équipe seulement peut se déplacer.',
];

const siteUrl = String(
  runtimeConfig.public.siteUrl || 'https://pixelprowlers.io',
).replace(/\/+$/, '');

const canonicalUrl = `${siteUrl}/formations`;

const title = 'Formations : logiciel libre, sécurité et autonomie numérique | PixelProwlers';

const description = [
  'Formations PixelProwlers au logiciel libre, à la sécurité informatique,',
  'à l’hygiène numérique et à l’autonomie, pour comprendre et décider',
  'par soi-même.',
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
          'Logiciel libre',
          'Sécurité informatique',
          'Hygiène numérique',
          'Autonomie numérique',
        ],
      }),
    },
  ],
});
</script>

<style scoped>
@reference "../assets/css/main.css";

.pillar-page {
  @apply bg-pxp-paper text-pxp-ink;
}

.pillar-hero {
  @apply border-b border-pxp-green/15 bg-pxp-panel py-12 md:py-16;
}

.pillar-hero-content {
  @apply grid gap-5;
}

.pillar-hero h1 {
  @apply max-w-4xl text-4xl font-black leading-tight text-pxp-ink md:text-5xl;
}

.pillar-introduction {
  @apply max-w-3xl text-lg font-normal leading-relaxed text-pxp-ink/80;
}

.pillar-actions {
  @apply flex flex-wrap gap-3;
}

.cta-note {
  @apply max-w-3xl text-sm font-normal leading-relaxed text-pxp-ink/70;
}

.pillar-section {
  @apply py-12 md:py-16;
}

.pillar-section-alt {
  @apply border-t border-pxp-green/15 bg-pxp-panel;
}

.pillar-section h2 {
  @apply text-3xl font-black leading-tight text-pxp-ink;
}

.pillar-section-intro {
  @apply mt-3 max-w-3xl font-normal leading-relaxed text-pxp-ink/80;
}

.pillar-card-grid {
  @apply mt-8 grid gap-4 md:grid-cols-2;
}

.pillar-card {
  @apply grid content-start gap-2 rounded-xl border border-pxp-green/20 bg-white p-5 shadow-sm md:p-6;
}

.pillar-card h3 {
  @apply text-lg font-black text-pxp-ink;
}

.pillar-card p {
  @apply font-normal leading-relaxed text-pxp-ink/80;
}

.pillar-principles {
  @apply mt-6 grid gap-2 pl-5;
  list-style: disc;
}

.pillar-principles li {
  @apply font-normal leading-relaxed text-pxp-ink/80;
}

.pillar-boundary {
  @apply mt-6 max-w-3xl rounded-lg border-2 border-pxp-orange/50 bg-pxp-orange/10 p-4 font-normal leading-relaxed text-pxp-ink;
}

.pillar-final {
  @apply bg-pxp-ink py-12 text-white md:py-16;
}

.pillar-final h2 {
  @apply text-3xl font-black leading-tight md:text-4xl;
}

.pillar-final p {
  @apply mt-3 max-w-3xl font-normal leading-relaxed text-white/85;
}

.pillar-final .pillar-actions {
  @apply mt-6;
}
</style>
