<template>
  <main class="diagnostic-page">
    <section
      class="diagnostic-hero"
      aria-labelledby="diagnostic-title"
    >
      <div class="form-container diagnostic-hero-content">
        <p class="eyebrow">
          Pré-diagnostic gratuit
        </p>

        <h1 id="diagnostic-title">
          Situez votre priorité numérique en quatre questions
        </h1>

        <p class="diagnostic-introduction">
          Décrivez votre situation pour obtenir immédiatement une
          orientation indicative sur votre site, vos accès et votre
          dépendance technique.
        </p>

        <div
          class="diagnostic-scope"
          aria-labelledby="diagnostic-scope-title"
        >
          <h2 id="diagnostic-scope-title">
            Ce que produit ce pré-diagnostic
          </h2>

          <ul>
            <li>Une première lecture fondée sur vos réponses</li>
            <li>Un niveau de priorité indicatif</li>
            <li>Une prochaine étape adaptée à la situation déclarée</li>
          </ul>
        </div>

        <div
          class="diagnostic-boundaries"
          aria-labelledby="diagnostic-boundaries-title"
        >
          <h2 id="diagnostic-boundaries-title">
            Un questionnaire sans accès à votre système
          </h2>

          <ul>
            <li>4 questions, environ 3 minutes</li>
            <li>Aucun mot de passe ni fichier sensible demandé</li>
            <li>Aucune vérification ou modification automatique</li>
          </ul>

          <p>
            Le résultat ne remplace pas un audit technique. Une
            qualification humaine reste nécessaire avant toute
            recommandation définitive ou intervention.
          </p>
        </div>
      </div>
    </section>

    <LazyFormsDiagnosticForm />
  </main>
</template>

<script setup lang="ts">
const runtimeConfig = useRuntimeConfig();

const siteUrl = String(
  runtimeConfig.public.siteUrl || 'https://pixelprowlers.io',
).replace(/\/+$/, '');

const canonicalUrl = `${siteUrl}/diagnostic-situation`;

const title = 'Pré-diagnostic de site web et accès | PixelProwlers';

const description = [
  'Évaluez en quatre questions la priorité liée à votre site,',
  'vos accès et votre dépendance technique.',
  'Résultat immédiat et indicatif.',
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
          'Maintenance de site web',
          'Sécurité des accès',
          'Dépendance numérique',
          'Continuité numérique',
        ],
      }),
    },
  ],
});
</script>

<style scoped>
@reference "../assets/css/main.css";

.diagnostic-page {
  @apply bg-pxp-paper text-pxp-ink;
}

.diagnostic-hero {
  @apply border-b border-pxp-green/15 bg-pxp-panel py-12 md:py-20;
}

.diagnostic-hero-content {
  @apply grid gap-6;
}

.diagnostic-hero h1 {
  @apply max-w-4xl text-4xl font-black leading-tight text-pxp-ink md:text-6xl;
}

.diagnostic-introduction {
  @apply max-w-3xl text-lg font-semibold leading-relaxed text-pxp-ink/80 md:text-xl;
}

.diagnostic-scope,
.diagnostic-boundaries {
  @apply rounded-xl border border-pxp-green/20 bg-white p-5 md:p-6;
}

.diagnostic-scope h2,
.diagnostic-boundaries h2 {
  @apply mb-3 text-xl font-black text-pxp-ink;
}

.diagnostic-scope ul,
.diagnostic-boundaries ul {
  @apply grid gap-2 pl-5;
  list-style: disc;
}

.diagnostic-scope li,
.diagnostic-boundaries li {
  @apply font-semibold leading-relaxed text-pxp-ink/80;
}

.diagnostic-boundaries {
  @apply bg-pxp-green/5;
}

.diagnostic-boundaries p {
  @apply mt-4 border-l-4 border-pxp-green pl-4 font-semibold leading-relaxed text-pxp-ink;
}

@media (min-width: 768px) {
  .diagnostic-scope,
  .diagnostic-boundaries {
    @apply max-w-4xl;
  }
}
</style>