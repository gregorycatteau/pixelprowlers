<template>
  <section id="offres" class="offers-section" aria-labelledby="offers-title">
    <div class="container-site">
      <div class="section-heading">
        <p class="eyebrow">Offres principales</p>
        <h2 id="offers-title">Trois façons de remettre votre numérique au propre.</h2>
        <p>
          Avant d’ajouter des outils, on vérifie ce qui tient encore debout : site, accès, sauvegardes,
          documentation et capacité de l’équipe à garder la main.
        </p>
      </div>

      <div class="offers-grid">
        <article v-for="offer in offers" :key="offer.title" class="offer-card">
          <p class="offer-kicker">{{ offer.kicker }}</p>
          <h3>{{ offer.title }}</h3>
          <p>{{ offer.description }}</p>
          <ul>
            <li v-for="item in offer.points" :key="item">{{ item }}</li>
          </ul>
          <NuxtLink :to="offer.href" class="offer-link">{{ offer.cta }}</NuxtLink>
        </article>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const offers = [
  {
    kicker: 'Audit',
    title: 'Audit sécurité de site web',
    description: 'Pour savoir ce qui expose votre site, vos formulaires, vos accès et vos sauvegardes.',
    points: [
      'Un site sans sauvegarde testée n’est pas maintenu.',
      'Rapport lisible, priorités claires, actions réalistes.',
      'Pas de promesse de sécurité totale.',
    ],
    href: '/audit-site-web',
    cta: 'Faire vérifier mon site',
  },
  {
    kicker: 'Refonte utile',
    title: 'Site sobre, sécurisé, maintenable',
    description: 'Pour remplacer un site fragile par une base simple, rapide, documentée et durable.',
    points: [
      'Moins de dépendances inutiles.',
      'Architecture compréhensible et maintenable.',
      'Le bon outil est celui que votre équipe peut garder en main.',
    ],
    href: '/developpement',
    cta: 'Voir le site maintenable',
  },
  {
    kicker: 'Transmission',
    title: 'Maintenance, accès et documentation',
    description: 'Pour réduire la dépendance à une seule personne et remettre les procédures à plat.',
    points: [
      'Un accès partagé dans un tableur n’est pas une stratégie.',
      'Cartographie des comptes, outils et responsabilités.',
      'Comprendre assez pour décider, documenter assez pour ne pas dépendre.',
    ],
    href: '/contact',
    cta: 'Cartographier mes accès',
  },
] as const;
</script>

<style scoped>
.offers-section {
  @apply border-y border-forest/15 bg-sand py-16 md:py-24;
}

.section-heading {
  @apply max-w-3xl;
}

.eyebrow {
  @apply font-mono text-xs font-bold uppercase tracking-[0.24em] text-trust;
}

.section-heading h2 {
  @apply mt-4 font-heading text-3xl font-black text-ink md:text-5xl;
}

.section-heading p {
  @apply mt-5 text-lg leading-8 text-muted;
}

.offers-grid {
  @apply mt-10 grid gap-5 lg:grid-cols-3;
}

.offer-card {
  @apply flex h-full flex-col rounded-lg border border-forest/15 bg-paper p-6 shadow-sm transition hover:-translate-y-1 hover:border-trust/45 hover:shadow-soft;
}

.offer-kicker {
  @apply font-mono text-xs font-bold uppercase tracking-[0.2em] text-trust;
}

.offer-card h3 {
  @apply mt-4 font-heading text-2xl font-black leading-tight text-ink;
}

.offer-card p:not(.offer-kicker) {
  @apply mt-4 leading-7 text-muted;
}

.offer-card ul {
  @apply mt-5 grid gap-3;
}

.offer-card li {
  @apply rounded-lg border border-forest/10 bg-white/65 px-4 py-3 text-sm font-semibold leading-6 text-forest;
}

.offer-link {
  @apply mt-6 inline-flex min-h-12 items-center justify-center rounded-lg bg-action px-5 py-3 text-center font-extrabold text-white shadow-orange outline-none transition hover:bg-[#FF9F2D] focus-visible:ring-2 focus-visible:ring-action focus-visible:ring-offset-2 focus-visible:ring-offset-paper;
}
</style>
