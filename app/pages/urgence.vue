<template>
  <main class="urgency-page">
    <section
      class="urgency-hero"
      aria-labelledby="urgency-title"
    >
      <div class="article-container urgency-hero-content">
        <p class="eyebrow">
          Qualification d’un incident web
        </p>

        <h1 id="urgency-title">
          Un incident perturbe votre site&nbsp;?
          Décrivez ce qui se passe.
        </h1>

        <p class="urgency-introduction">
          Transmettez les faits observés et leur impact sur votre activité.
          Après l’envoi, votre demande est enregistrée et une référence
          de dossier vous est communiquée.
        </p>

        <div
          class="urgent-callout"
          aria-labelledby="urgent-callout-title"
        >
          <div>
            <h2 id="urgent-callout-title">
              Votre activité est actuellement bloquée&nbsp;?
            </h2>

            <p>
              Vous pouvez également appeler PixelProwlers pour signaler
              l’incident. L’appel ne remplace pas l’enregistrement des
              informations nécessaires à sa qualification.
            </p>
          </div>

          <a
            class="ButtonBase ButtonPrimary"
            href="tel:+33668145152"
          >
            Appeler le 06 68 14 51 52
          </a>
        </div>
      </div>
    </section>

    <section
      class="urgency-framework"
      aria-labelledby="urgency-framework-title"
    >
      <div class="article-container">
        <h2 id="urgency-framework-title">
          Avant d’envoyer votre demande
        </h2>

        <div v-reveal class="urgency-grid">
          <article class="urgency-card">
            <h3>Situations à signaler rapidement</h3>

            <ul>
              <li>Site inaccessible ou fortement dégradé</li>
              <li>Accès administrateur perdu ou détourné</li>
              <li>Modification suspecte ou contenu non autorisé</li>
              <li>Fonction essentielle devenue inutilisable</li>
              <li>Risque identifié pour des données ou des sauvegardes</li>
            </ul>
          </article>

          <article class="urgency-card">
            <h3>Demandes relevant d’un autre parcours</h3>

            <ul>
              <li>Refonte graphique ou nouvelle fonctionnalité</li>
              <li>Amélioration progressive des performances</li>
              <li>Audit préventif sans incident observé</li>
              <li>Référencement ou évolution éditoriale</li>
              <li>Projet de création encore en préparation</li>
            </ul>
          </article>
        </div>

        <div
          v-reveal
          class="qualification-process"
          aria-labelledby="qualification-process-title"
        >
          <h2 id="qualification-process-title">
            Comment votre demande est traitée
          </h2>

          <ol>
            <li>
              <strong>Enregistrement :</strong>
              les faits, leur impact et vos coordonnées sont associés
              à une référence de dossier.
            </li>

            <li>
              <strong>Qualification humaine :</strong>
              la situation est examinée afin de distinguer un incident
              actif, un dysfonctionnement et une demande non urgente.
            </li>

            <li>
              <strong>Cadre d’intervention :</strong>
              le périmètre, les accès éventuellement nécessaires,
              les délais et les conditions sont validés avec vous
              avant toute action.
            </li>
          </ol>
        </div>

        <p class="urgency-boundary">
          L’envoi du formulaire ne vaut ni acceptation d’intervention
          ni promesse de résolution immédiate. Aucun mot de passe,
          accès privé ou fichier sensible ne doit être transmis dans
          la description de l’incident.
        </p>
      </div>
    </section>

    <LazyFormsUrgencyForm />
  </main>
</template>

<script setup lang="ts">
const runtimeConfig = useRuntimeConfig();

const siteUrl = String(
  runtimeConfig.public.siteUrl || 'https://pixelprowlers.io',
).replace(/\/+$/, '');

const canonicalUrl = `${siteUrl}/urgence`;

const title = 'Incident ou urgence sur un site web | PixelProwlers';

const description = [
  'Signalez un site inaccessible, un accès perdu ou une anomalie',
  'suspecte. La situation est enregistrée puis qualifiée avant',
  'toute intervention.',
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
          'Incident de site web',
          'Perte d’accès administrateur',
          'Dysfonctionnement de site web',
          'Qualification de sécurité',
        ],
      }),
    },
  ],
});
</script>

<style scoped>
@reference "../assets/css/main.css";

.urgency-page {
  @apply bg-pxp-paper text-pxp-ink;
}

.urgency-hero {
  @apply border-b border-pxp-orange/20 bg-pxp-panel py-12 md:py-20;
}

.urgency-hero-content {
  @apply grid gap-6;
}

.urgency-hero h1 {
  @apply max-w-4xl text-4xl font-black leading-tight text-pxp-ink md:text-6xl;
}

.urgency-introduction {
  @apply max-w-3xl text-lg font-semibold leading-relaxed text-pxp-ink/80 md:text-xl;
}

.urgent-callout {
  @apply flex flex-col gap-5 rounded-xl border border-pxp-orange/25 bg-pxp-orange/10 p-5 md:flex-row md:items-center md:justify-between md:p-6;
}

.urgent-callout h2 {
  @apply text-xl font-black text-pxp-ink;
}

.urgent-callout p {
  @apply mt-2 max-w-3xl font-semibold leading-relaxed text-pxp-ink/80;
}

.urgent-callout .ButtonBase {
  @apply shrink-0;
}

.urgency-framework {
  @apply py-12 md:py-16;
}

.urgency-framework > .article-container {
  @apply grid gap-8;
}

.urgency-framework h2 {
  @apply text-2xl font-black text-pxp-ink md:text-3xl;
}

.urgency-grid {
  @apply grid gap-5 md:grid-cols-2;
}

.urgency-card {
  @apply rounded-xl border border-pxp-green/20 bg-white p-5 shadow-sm md:p-6;
}

.urgency-card h3 {
  @apply mb-4 text-xl font-black text-pxp-ink;
}

.urgency-card ul {
  @apply grid gap-3 pl-5;
  list-style: disc;
}

.urgency-card li {
  @apply font-semibold leading-relaxed text-pxp-ink/80;
}

.qualification-process {
  @apply rounded-xl border border-pxp-green/20 bg-pxp-green/5 p-5 md:p-6;
}

.qualification-process h2 {
  @apply mb-5;
}

.qualification-process ol {
  @apply grid gap-4 pl-5;
  list-style: decimal;
}

.qualification-process li {
  @apply pl-2 font-semibold leading-relaxed text-pxp-ink/80;
}

.qualification-process strong {
  @apply text-pxp-ink;
}

.urgency-boundary {
  @apply border-l-4 border-pxp-orange bg-pxp-orange/10 px-4 py-3 font-semibold leading-relaxed text-pxp-ink;
}
</style>