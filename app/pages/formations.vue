<template>
  <main class="pillar-page">
    <section class="pillar-hero" aria-labelledby="formations-title">
      <div class="form-container pillar-hero-content">
        <p class="eyebrow">Formations</p>

        <h1 id="formations-title">
          Comprendre, choisir et reprendre la main sur ses outils
        </h1>

        <p class="pillar-introduction">
          Des formations pour décider par vous-même : comprendre ce qu’on
          vous propose, sécuriser vos usages quotidiens et réduire votre
          dépendance à un outil ou à une personne. Sans devenir
          informaticien.
        </p>

        <div class="pillar-actions">
          <AppButton href="/contact">
            Nous contacter pour une formation
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
        <h2 id="formations-themes-title">Les thèmes que nous couvrons</h2>

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

        <p class="pillar-boundary">
          Une formation transmet des repères et des méthodes. Elle ne
          remplace pas une intervention technique sur votre installation :
          si le besoin relève d’une réparation ou d’un audit, nous vous le
          dirons plutôt que de vous vendre une session.
        </p>
      </div>
    </section>

    <section class="pillar-final" aria-labelledby="formations-final-title">
      <div class="article-container">
        <h2 id="formations-final-title">Un besoin de formation&nbsp;?</h2>

        <p>
          Décrivez qui doit être formé, sur quel sujet et dans quel contexte.
          Nous vous répondons avec une proposition adaptée, ou nous vous
          orientons ailleurs si ce n’est pas notre domaine.
        </p>

        <div class="pillar-actions">
          <AppButton href="/contact">
            Nous contacter pour une formation
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
      'Comprendre ce qu’apporte le libre concrètement, ce qu’il coûte, et pourquoi le format d’un fichier décide de qui garde la main dessus.',
  },
  {
    title: 'Sécurité informatique',
    description:
      'Mots de passe, second facteur, sauvegardes, hameçonnage : les gestes qui évitent la majorité des incidents réels.',
  },
  {
    title: 'Hygiène numérique',
    description:
      'Mettre de l’ordre dans les comptes, les accès partagés et les fichiers, pour que l’activité ne repose pas sur la mémoire d’une seule personne.',
  },
  {
    title: 'Autonomie et choix d’outils',
    description:
      'Savoir lire une proposition technique, poser les bonnes questions et évaluer ce qu’un outil vous coûtera pour en sortir.',
  },
  {
    title: 'Usages responsables',
    description:
      'Prolonger la durée de vie du matériel, limiter les dépendances évitables et réduire l’empreinte de son informatique.',
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
  @apply max-w-3xl text-lg font-semibold leading-relaxed text-pxp-ink/80;
}

.pillar-actions {
  @apply flex flex-wrap gap-3;
}

.cta-note {
  @apply max-w-3xl text-sm font-semibold leading-relaxed text-pxp-ink/70;
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
  @apply mt-3 max-w-3xl font-semibold leading-relaxed text-pxp-ink/80;
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
  @apply font-semibold leading-relaxed text-pxp-ink/80;
}

.pillar-principles {
  @apply mt-6 grid gap-2 pl-5;
  list-style: disc;
}

.pillar-principles li {
  @apply font-semibold leading-relaxed text-pxp-ink/80;
}

.pillar-boundary {
  @apply mt-6 max-w-3xl rounded-lg border-2 border-pxp-orange/50 bg-pxp-orange/10 p-4 font-semibold leading-relaxed text-pxp-ink;
}

.pillar-final {
  @apply bg-pxp-blue py-16 text-white md:py-20;
}

.pillar-final h2 {
  @apply text-3xl font-black leading-tight md:text-4xl;
}

.pillar-final p {
  @apply mt-3 max-w-3xl font-semibold leading-relaxed text-white/85;
}

.pillar-final .pillar-actions {
  @apply mt-6;
}
</style>
