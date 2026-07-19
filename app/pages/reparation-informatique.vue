<template>
  <main class="repair-page">
    <section class="repair-hero" aria-labelledby="repair-title">
      <div class="form-container repair-hero-content">
        <p class="eyebrow">Réparation, reconditionnement &amp; Linux</p>

        <h1 id="repair-title">
          Prolonger la vie de votre matériel informatique, en confiance
        </h1>

        <p class="repair-introduction">
          PixelProwlers diagnostique, répare et reconditionne des
          ordinateurs, et accompagne la migration vers Linux lorsque le
          matériel et vos usages le permettent. Pour les associations, TPE,
          collectifs et particuliers accompagnés.
        </p>

        <div class="repair-actions">
          <AppButton href="/contact?demande=materiel">
            Demander une qualification matérielle
          </AppButton>
        </div>

        <p class="cta-note">
          Cette demande permet une première qualification de votre
          situation. Aucun prix, délai ou engagement n’est fixé avant
          l’échange.
        </p>

        <div
          class="repair-security"
          aria-labelledby="repair-security-title"
        >
          <h2 id="repair-security-title">
            Avant d’envoyer votre demande
          </h2>

          <ul>
            <li>Ne transmettez aucun mot de passe dans le formulaire.</li>
            <li>
              Ne transmettez aucune clé de récupération ni aucun code
              d’authentification à plusieurs facteurs (MFA).
            </li>
            <li>
              Ne détaillez pas les données personnelles contenues sur votre
              support dans le formulaire.
            </li>
            <li>
              Les modalités d’un éventuel accès à votre appareil seront
              définies séparément, avec votre accord explicite.
            </li>
            <li>
              Une sauvegarde préalable pourra vous être recommandée selon la
              nature de l’intervention.
            </li>
          </ul>
        </div>
      </div>
    </section>

    <section
      class="repair-section"
      aria-labelledby="repair-offer-title"
    >
      <div class="article-container">
        <h2 id="repair-offer-title">Ce que couvre cette offre</h2>

        <div v-reveal class="repair-card-grid">
          <article class="repair-card">
            <h3>Diagnostic et réparation d’ordinateurs</h3>
            <p>
              Identification précise de la panne ou du ralentissement avant
              toute intervention, puis réparation de ce qui peut
              raisonnablement l’être.
            </p>
          </article>

          <article class="repair-card">
            <h3>Reconditionnement et prolongation de vie</h3>
            <p>
              Quand une réparation ponctuelle ne suffit pas, remise en état
              d’usage du matériel : nettoyage, vérifications complètes,
              pièces réutilisables lorsque c’est pertinent.
            </p>
          </article>

          <article class="repair-card">
            <h3>Migration vers Linux</h3>
            <p>
              Lorsque le matériel et vos usages le permettent, installation
              et configuration d’un système Linux sobre, en remplacement ou
              en complément de l’existant.
            </p>
          </article>

          <article class="repair-card">
            <h3>Sécurisation et documentation du poste</h3>
            <p>
              Le poste restitué est accompagné d’une explication claire de
              ce qui a été fait, pour que vous restiez en mesure de le
              comprendre et de le maintenir.
            </p>
          </article>

          <article class="repair-card">
            <h3>Réemploi ou orientation adaptée</h3>
            <p>
              Quand la réparation n’est pas raisonnable, nous vous
              l’expliquons clairement et vous orientons vers une filière de
              réemploi ou de traitement adaptée.
            </p>
          </article>
        </div>
      </div>
    </section>

    <section
      class="repair-section repair-section-alt"
      aria-labelledby="repair-benefits-title"
    >
      <div class="article-container">
        <h2 id="repair-benefits-title">
          Pourquoi réparer plutôt que remplacer
        </h2>

        <ul v-reveal class="repair-benefits">
          <li>Prolonger la vie de votre matériel plutôt que le remplacer par défaut.</li>
          <li>Retrouver un poste réellement utilisable pour vos usages du quotidien.</li>
          <li>Réduire votre dépendance à un éditeur ou à un cycle de renouvellement imposé.</li>
          <li>Garder la maîtrise de vos données pendant toute l’intervention.</li>
          <li>Repartir avec un système documenté, que vous pouvez comprendre et maintenir.</li>
          <li>Éviter un remplacement prématuré quand une réparation raisonnable suffit.</li>
        </ul>

        <p class="repair-disclaimer">
          Certains matériels sont trop anciens, trop endommagés ou
          incompatibles avec les usages visés. Nous vous le disons
          clairement dès la qualification, avant toute réparation,
          reconditionnement ou migration : aucune réparation ni compatibilité
          Linux n’est garantie à l’avance.
        </p>
      </div>
    </section>

    <section
      class="repair-section"
      aria-labelledby="repair-journey-title"
    >
      <div class="article-container">
        <h2 id="repair-journey-title">Comment se déroule une demande</h2>

        <ol v-reveal class="repair-journey">
          <li>
            <span class="repair-journey-index">01</span>
            <div>
              <h3>Demande initiale</h3>
              <p>Vous décrivez votre matériel et votre besoin via le formulaire de contact.</p>
            </div>
          </li>

          <li>
            <span class="repair-journey-index">02</span>
            <div>
              <h3>Qualification du besoin</h3>
              <p>Nous clarifions la situation avec vous : usage visé, contraintes, urgence.</p>
            </div>
          </li>

          <li>
            <span class="repair-journey-index">03</span>
            <div>
              <h3>Diagnostic</h3>
              <p>Le matériel est examiné pour identifier précisément ce qui doit être traité.</p>
            </div>
          </li>

          <li>
            <span class="repair-journey-index">04</span>
            <div>
              <h3>Proposition avant intervention</h3>
              <p>Vous recevez une proposition claire avant toute action sur votre matériel.</p>
            </div>
          </li>

          <li>
            <span class="repair-journey-index">05</span>
            <div>
              <h3>Intervention autorisée</h3>
              <p>Nous n’intervenons qu’après votre accord explicite.</p>
            </div>
          </li>

          <li>
            <span class="repair-journey-index">06</span>
            <div>
              <h3>Tests et restitution documentée</h3>
              <p>Le matériel est testé puis restitué avec une explication de ce qui a été fait.</p>
            </div>
          </li>
        </ol>
      </div>
    </section>

    <section class="repair-final" aria-labelledby="repair-final-title">
      <div class="article-container">
        <h2 id="repair-final-title">Vous avez un ordinateur à faire vérifier ?</h2>

        <p>
          Décrivez votre matériel et votre besoin : nous qualifions votre
          demande avant toute intervention.
        </p>

        <div class="repair-actions">
          <AppButton href="/contact?demande=materiel">
            Demander une qualification matérielle
          </AppButton>

          <AppButton variant="secondary" href="/contact">
            Contacter PixelProwlers
          </AppButton>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
import AppButton from '~/components/ui/AppButton.vue';

const runtimeConfig = useRuntimeConfig();

const siteUrl = String(
  runtimeConfig.public.siteUrl || 'https://pixelprowlers.io',
).replace(/\/+$/, '');

const canonicalUrl = `${siteUrl}/reparation-informatique`;

const title =
  'Réparation, reconditionnement et migration Linux | PixelProwlers';

const description = [
  'Diagnostic et réparation d’ordinateurs, reconditionnement,',
  'migration vers Linux lorsque c’est pertinent, sécurisation et',
  'documentation du poste. Pour associations, TPE, collectifs et',
  'particuliers accompagnés.',
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
          'Réparation informatique',
          'Reconditionnement de matériel',
          'Migration vers Linux',
          'Sécurisation de poste',
          'Réemploi numérique',
        ],
      }),
    },
  ],
});
</script>

<style scoped>
@reference "../assets/css/main.css";

.repair-page {
  @apply bg-pxp-paper text-pxp-ink;
}

.repair-hero {
  @apply border-b border-pxp-green/15 bg-pxp-panel py-12 md:py-20;
}

.repair-hero-content {
  @apply grid gap-6;
}

.repair-hero h1 {
  @apply max-w-4xl text-4xl font-black leading-tight text-pxp-ink md:text-6xl;
}

.repair-introduction {
  @apply max-w-3xl text-lg font-semibold leading-relaxed text-pxp-ink/80 md:text-xl;
}

.repair-actions {
  @apply flex flex-wrap gap-3;
}

.cta-note {
  @apply max-w-2xl text-sm font-semibold leading-relaxed text-pxp-ink/70;
}

.repair-security {
  @apply rounded-xl border-2 border-pxp-orange/40 bg-white p-5 md:p-6;
}

.repair-security h2 {
  @apply mb-3 text-xl font-black text-pxp-ink;
}

.repair-security ul {
  @apply grid gap-2 pl-5;
  list-style: disc;
}

.repair-security li {
  @apply font-semibold leading-relaxed text-pxp-ink/80;
}

@media (min-width: 768px) {
  .repair-security {
    @apply max-w-4xl;
  }
}

.repair-section {
  @apply py-14 md:py-20;
}

.repair-section-alt {
  @apply border-y border-pxp-green/15 bg-pxp-panel;
}

.repair-section h2 {
  @apply text-3xl font-black leading-tight text-pxp-ink md:text-4xl;
}

.repair-card-grid {
  @apply mt-8 grid gap-5 md:grid-cols-2;
}

.repair-card {
  @apply rounded-xl border border-pxp-green/20 bg-white p-5 md:p-6;
}

.repair-card h3 {
  @apply text-lg font-black text-pxp-ink;
}

.repair-card p {
  @apply mt-2 font-semibold leading-relaxed text-pxp-ink/80;
}

.repair-benefits {
  @apply mt-8 grid gap-2 pl-5;
  list-style: disc;
}

.repair-benefits li {
  @apply font-semibold leading-relaxed text-pxp-ink/80;
}

.repair-disclaimer {
  @apply mt-6 max-w-3xl border-l-4 border-pxp-orange pl-4 font-semibold leading-relaxed text-pxp-ink;
}

.repair-journey {
  @apply mt-8 grid gap-4;
  list-style: none;
  padding: 0;
}

.repair-journey li {
  @apply flex items-start gap-4 rounded-xl border border-pxp-green/20 bg-white p-5;
}

.repair-journey-index {
  @apply shrink-0 text-2xl font-black text-pxp-green;
}

.repair-journey h3 {
  @apply text-lg font-black text-pxp-ink;
}

.repair-journey p {
  @apply mt-1 font-semibold leading-relaxed text-pxp-ink/80;
}

.repair-final {
  @apply bg-pxp-blue py-16 text-white md:py-20;
}

.repair-final h2 {
  @apply max-w-3xl text-3xl font-black leading-tight md:text-4xl;
}

.repair-final p {
  @apply mt-4 max-w-2xl text-lg font-semibold leading-relaxed text-white/80;
}

.repair-final .repair-actions {
  @apply mt-8;
}

.repair-final :deep(.ButtonSecondary) {
  border-color: rgba(255, 255, 255, 0.64);
  color: white;
  background: transparent;
}
</style>
