<template>
  <main class="repair-page">
    <section class="repair-hero" aria-labelledby="repair-title">
      <div class="container RepairHeroLayout">
        <div class="repair-hero-content">
          <p class="eyebrow">Diagnostic · Réparation au composant</p>

          <h1 id="repair-title" class="pxp-font-display">
            Réparer, même les composants.
          </h1>

          <p class="repair-introduction">
            PixelProwlers diagnostique, répare et reconditionne des
            ordinateurs, des téléphones et des tablettes, et accompagne la
            migration vers Linux lorsque le matériel et vos usages le
            permettent. Pour les associations, TPE, collectifs et particuliers
            accompagnés.
          </p>

          <div class="repair-actions">
            <AppButton href="/contact">
              Décrire ma panne
            </AppButton>

            <AppButton variant="secondary" href="/contact">
              Nous écrire directement
            </AppButton>
          </div>

          <p class="cta-note">Décrivez ce que vous observez dans le formulaire de contact. Aucun prix, délai ou engagement n’est fixé avant l’examen de votre matériel.</p>

        </div>
        <EditorialImage name="microscope" alt="Illustration de micro-soudure sur une carte électronique sous microscope" caption="travail de précision" priority sizes="(min-width: 1024px) 50vw, 100vw" />
      </div>
    </section>

    <section id="micro-soudure" class="repair-section MicroSection" aria-labelledby="micro-title">
      <div class="container MicroLayout">
        <EditorialImage name="composant" alt="Illustration d’un composant travaillé avec un fer à souder et une pince" caption="détail de réparation" />
        <div class="MicroCopy">
          <p class="eyebrow">Précision électronique</p>
          <h2 id="micro-title" class="pxp-font-display">La carte mère aussi peut se réparer.</h2>
          <p>Diagnostic des pannes de carte mère, réparation au niveau des composants et micro-soudure : un travail de précision sous microscope pour intervenir là où la panne se situe.</p>
          <p>Le diagnostic détermine si cette intervention est adaptée à votre appareil. Aucune réparation n’est garantie avant son examen.</p>
          <AppButton href="/contact">Décrire ma panne</AppButton>
        </div>
      </div>
    </section>
    <section class="repair-section" aria-labelledby="repair-security-title">
      <div class="container">
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
              Ne transmettez pas le code de déverrouillage de votre
              téléphone&nbsp;: il vous sera demandé de le déverrouiller
              vous-même, ou de le faire sur place.
            </li>
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
            <h3>Réparation de téléphones et de tablettes</h3>
            <p>
              Écran cassé, batterie qui ne tient plus, connecteur de charge
              capricieux, appareil tombé dans l’eau&nbsp;: les pannes mobiles
              suivent le même cadre que les autres — examen d’abord,
              proposition ensuite.
            </p>
            <p class="repair-card-note">
              Une batterie qui gonfle ou un appareil qui chauffe
              anormalement ne doivent plus être rechargés&nbsp;:
              <NuxtLink to="/contact">
                signalez-le dès la description de la panne</NuxtLink>.
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
          <li class="repair-journey-step-with-cta">
            <span class="repair-journey-index">01</span>
            <div class="repair-journey-step-content">
              <h3>Demande initiale</h3>
              <p>Vous décrivez votre matériel et votre besoin via le formulaire de contact.</p>
            </div>
            <NuxtLink
              to="/contact"
              class="repair-journey-cta"
              aria-label="Décrire ma panne : ouvrir le formulaire de contact"
            >
              <svg
                class="repair-journey-cta-icon"
                viewBox="0 0 24 24"
                fill="none"
                aria-hidden="true"
              >
                <path
                  d="M9 3.75h4.5a1.5 1.5 0 0 1 1.5 1.5v.75h.75A2.25 2.25 0 0 1 18 8.25v10.5A2.25 2.25 0 0 1 15.75 21h-7.5A2.25 2.25 0 0 1 6 18.75V8.25A2.25 2.25 0 0 1 8.25 6H9v-.75a1.5 1.5 0 0 1 1.5-1.5Z"
                  stroke="currentColor"
                  stroke-width="1.5"
                  stroke-linejoin="round"
                />
                <path
                  d="M9 12.75 11 14.75 15.25 10.5"
                  stroke="currentColor"
                  stroke-width="1.5"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
              <span>
                Décrire ma panne
                <small>Contact matériel</small>
              </span>
            </NuxtLink>
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
          <AppButton href="/contact">
            Décrire ma panne
          </AppButton>

          <AppButton variant="secondary" href="/contact">
            Nous écrire directement
          </AppButton>
        </div>

        <p class="cta-note">
          Le questionnaire commence par vous demander s’il s’agit d’un
          ordinateur ou d’un téléphone&nbsp;: les questions ne sont pas les
          mêmes.
        </p>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
import AppButton from '~/components/ui/AppButton.vue';
import EditorialImage from '~/components/sections/EditorialImage.vue';

const runtimeConfig = useRuntimeConfig();

const siteUrl = String(
  runtimeConfig.public.siteUrl || 'https://pixelprowlers.io',
).replace(/\/+$/, '');

const canonicalUrl = `${siteUrl}/reparation-informatique`;

const title =
  'Réparation au composant et micro-soudure | PixelProwlers';

const description = [
  'Diagnostic de carte mère, réparation au composant et micro-soudure.',
  'Réparation d’ordinateurs, de téléphones et de tablettes,',
  'reconditionnement, migration vers Linux lorsque c’est pertinent,',
  'sécurisation et documentation du poste. Pour associations, TPE,',
  'collectifs et particuliers accompagnés.',
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
          'Réparation au composant et micro-soudure',
          'Réparation de téléphones et tablettes',
          'Remplacement d’écran et de batterie',
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
  @apply border-b border-pxp-green/15 bg-pxp-panel py-10 md:py-16;
}

.repair-hero-content {
  @apply grid gap-6;
}

.repair-hero h1 {
  @apply max-w-4xl font-bold text-pxp-ink;
  font-size: clamp(3.5rem, 6vw, 5.5rem);
  line-height: 0.98;
}

.repair-introduction {
  @apply max-w-3xl text-lg font-semibold leading-relaxed text-pxp-ink/80 md:text-xl;
}

.repair-actions {
  @apply flex flex-wrap gap-3;
}

.repair-actions :deep(.ButtonPrimary) {
  @apply bg-pxp-green text-white shadow-none hover:bg-pxp-ink focus-visible:ring-pxp-green;
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
  @apply rounded-xl border border-pxp-green/20 bg-white p-5 shadow-sm md:p-6;
}

.repair-card h3 {
  @apply text-lg font-black text-pxp-ink;
}

.repair-card-note {
  @apply mt-3 border-t border-pxp-orange/30 pt-3 text-sm font-semibold leading-relaxed text-pxp-ink/75;
}

.repair-card-note a {
  @apply font-black text-pxp-green underline decoration-2 underline-offset-2;
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

.repair-journey-step-with-cta {
  @apply flex-wrap items-start gap-y-4;
}

.repair-journey-step-content {
  @apply min-w-0 flex-1;
}

/*
 * Lien composite (icône + intitulé + précision) : il ne passe pas par
 * .ButtonPrimary, qui centre un libellé sur une seule ligne. Il en reprend
 * en revanche le langage de mouvement et de focus unifié.
 */
.repair-journey-cta {
  @apply flex min-h-12 w-full shrink-0 items-center gap-3 rounded-md border-2 border-pxp-green bg-pxp-green px-4 py-3 font-black text-white active:scale-[0.98];
  transition:
    background-color var(--motion-feedback) var(--motion-ease-standard),
    border-color var(--motion-feedback) var(--motion-ease-standard),
    transform var(--motion-feedback) var(--motion-ease-standard);
}

.repair-journey-cta:hover {
  @apply bg-pxp-ink border-pxp-ink;
}

.repair-journey-cta:focus-visible {
  @apply outline-none ring-2 ring-pxp-orange ring-offset-2;
}

.repair-journey-cta-icon {
  @apply h-6 w-6 shrink-0;
}

.repair-journey-cta span {
  @apply grid text-left leading-tight;
}

.repair-journey-cta small {
  @apply text-xs font-semibold text-white/80;
}

@media (min-width: 768px) {
  .repair-journey-cta {
    @apply w-auto md:ml-auto;
  }
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

.RepairHeroLayout { @apply grid items-center gap-10 lg:grid-cols-2; }
.RepairHeroLayout :deep(figure) { @apply h-full min-h-80; }
.MicroSection { @apply bg-pxp-ink text-pxp-paper; }
.MicroLayout { @apply grid items-center gap-10 md:grid-cols-2; }
.MicroCopy { @apply grid gap-5; }
.MicroCopy h2 { @apply text-pxp-paper; }
.MicroCopy .eyebrow { @apply text-[#a8d5bd]; }
.MicroCopy p { @apply leading-relaxed; }
.MicroCopy :deep(.ButtonPrimary) { @apply w-fit bg-pxp-paper text-pxp-ink shadow-none hover:bg-white focus-visible:ring-white; }
</style>
