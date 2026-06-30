<template>
  <main class="bg-paper text-ink">
    <section class="page-hero">
      <div class="container-site hero-grid">
        <div>
          <p class="eyebrow">Site maintenable</p>
          <h1>Un site sobre, sécurisé, maintenable.</h1>
          <p>
            Pour petites structures qui veulent un site fiable, compréhensible, documenté et cohérent
            avec leurs usages réels. Pas une vitrine fragile posée sur une pile d’outils oubliés.
          </p>
          <div class="hero-actions">
            <NuxtLink to="/contact" class="cta-primary px-7 py-3">Planifier un premier échange</NuxtLink>
            <NuxtLink to="/audit-site-web" class="cta-secondary-local">Faire vérifier l’existant</NuxtLink>
          </div>
        </div>

        <aside class="principle-panel" aria-labelledby="principle-title">
          <p class="panel-kicker">Principe</p>
          <h2 id="principle-title">Le bon outil est celui que votre équipe peut garder en main.</h2>
          <p>
            Linux, open source et sobriété ne sont pas des slogans : ce sont des choix de maintenance,
            de documentation, de maîtrise des coûts et de dépendances réduites.
          </p>
        </aside>
      </div>
    </section>

    <section class="content-section">
      <div class="container-site">
        <div class="section-heading">
          <p class="eyebrow">Ce qu’on construit</p>
          <h2>Une base simple pour durer.</h2>
          <p>
            Le but n’est pas d’empiler des fonctionnalités. Le but est que votre site reste utile,
            compréhensible et réparable quand l’équipe change, quand un prestataire part ou quand un
            outil vieillit.
          </p>
        </div>

        <div class="card-grid">
          <article v-for="item in foundations" :key="item.title" class="info-card">
            <h3>{{ item.title }}</h3>
            <p>{{ item.text }}</p>
          </article>
        </div>
      </div>
    </section>

    <section class="content-section alt">
      <div class="container-site split-grid">
        <div>
          <p class="eyebrow">Livrables</p>
          <h2>Ce qui reste après la mise en ligne.</h2>
          <ul class="check-list">
            <li v-for="item in deliverables" :key="item">{{ item }}</li>
          </ul>
        </div>

        <div>
          <p class="eyebrow">Cadre</p>
          <h2>Ce qu’on évite volontairement.</h2>
          <ul class="check-list muted-list">
            <li v-for="item in refusals" :key="item">{{ item }}</li>
          </ul>
        </div>
      </div>
    </section>

    <section class="proof-section">
      <div class="container-site proof-grid">
        <div>
          <p class="eyebrow light">Cas typiques</p>
          <h2>Quand cette offre est pertinente.</h2>
          <p>
            Réparer quand c’est fiable, remplacer quand c’est nécessaire. Une refonte n’a de sens que
            si elle réduit la fragilité, clarifie la maintenance ou rend l’équipe plus autonome.
          </p>
        </div>

        <div class="scenario-list">
          <article v-for="scenario in scenarios" :key="scenario.title" class="scenario-card">
            <h3>{{ scenario.title }}</h3>
            <p>{{ scenario.text }}</p>
          </article>
        </div>
      </div>
    </section>

    <section class="dark-cta">
      <div class="container-site text-center">
        <h2>Vous voulez un site qui reste exploitable après la livraison ?</h2>
        <p>
          On part de vos usages, de vos contraintes et de ce que votre équipe doit pouvoir comprendre.
        </p>
        <NuxtLink to="/contact" class="cta-primary mt-8 px-7 py-3">
          Planifier un premier échange
        </NuxtLink>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
usePixelSeo({
  title: 'Site sobre, sécurisé, maintenable | PixelProwlers',
  description: 'Créer ou refondre un site web sobre, sécurisé, documenté et maintenable pour petites structures, associations, TPE et collectifs.',
  path: '/developpement',
});

const foundations = [
  {
    title: 'Architecture lisible',
    text: 'Un site structuré pour être compris, maintenu et repris sans dépendre d’un seul prestataire.',
  },
  {
    title: 'Sécurité de base sérieuse',
    text: 'HTTPS, formulaires propres, dépendances limitées, mises à jour maîtrisées et surface d’attaque réduite.',
  },
  {
    title: 'Sobriété utile',
    text: 'Des pages rapides, des contenus clairs et des choix techniques qui évitent la surenchère inutile.',
  },
  {
    title: 'Documentation minimale',
    text: 'Accès, hébergement, procédures, sauvegardes et gestes de maintenance expliqués simplement.',
  },
] as const;

const deliverables = [
  'Un site ou socle technique adapté à vos usages réels.',
  'Une documentation claire des accès, outils et procédures.',
  'Une stratégie de sauvegarde compréhensible et testable.',
  'Un plan de maintenance proportionné à votre structure.',
  'Une passation pour que l’équipe sache quoi faire après.',
] as const;

const refusals = [
  'Pas de bling-bling qui complique la maintenance.',
  'Pas de dépendances inutiles pour paraître moderne.',
  'Pas de promesse de sécurité totale.',
  'Pas de site “vite fait” sans sauvegarde ni responsabilité.',
  'Pas de discours startup pour masquer une offre floue.',
] as const;

const scenarios = [
  {
    title: 'WordPress vieillissant',
    text: 'Plugins accumulés, thème ancien, sauvegardes incertaines et personne ne sait vraiment ce qui casse quoi.',
  },
  {
    title: 'Refonte nécessaire',
    text: 'Le site ne reflète plus l’activité, mais la priorité reste la clarté, la sécurité et la maintenabilité.',
  },
  {
    title: 'Transmission fragile',
    text: 'La personne qui connaît les accès part bientôt, ou l’organisation dépend d’un bénévole technique.',
  },
] as const;
</script>

<style scoped>
.page-hero {
  @apply border-b border-forest/15 bg-paper py-16 md:py-24;
}

.hero-grid {
  @apply grid gap-8 lg:grid-cols-[1.05fr_0.75fr] lg:items-center;
}

.eyebrow {
  @apply font-mono text-xs font-bold uppercase tracking-[0.24em] text-trust;
}

.eyebrow.light {
  @apply text-scan;
}

.page-hero h1 {
  @apply mt-5 max-w-4xl font-heading text-4xl font-black leading-[1.04] text-ink sm:text-5xl md:text-6xl;
}

.page-hero p:not(.eyebrow),
.section-heading p,
.proof-grid > div > p:not(.eyebrow) {
  @apply mt-6 max-w-3xl text-lg leading-8 text-muted md:text-xl;
}

.hero-actions {
  @apply mt-8 flex flex-col gap-3 sm:flex-row;
}

.cta-secondary-local {
  @apply inline-flex min-h-12 items-center justify-center rounded-lg border-2 border-trust px-7 py-3 text-center font-extrabold text-ink outline-none transition hover:border-scan hover:bg-scan/10 hover:text-forest focus-visible:ring-2 focus-visible:ring-scan focus-visible:ring-offset-2 focus-visible:ring-offset-paper;
}

.principle-panel {
  @apply rounded-lg border border-forest/15 bg-sand p-6 shadow-soft md:p-8;
}

.panel-kicker {
  @apply font-mono text-xs font-bold uppercase tracking-[0.22em] text-trust;
}

.principle-panel h2 {
  @apply mt-4 font-heading text-3xl font-black text-ink;
}

.principle-panel p {
  @apply mt-4 leading-7 text-muted;
}

.content-section {
  @apply bg-sand py-16 md:py-24;
}

.content-section.alt {
  @apply border-y border-forest/15 bg-paper;
}

.section-heading {
  @apply max-w-3xl;
}

.section-heading h2,
.split-grid h2,
.proof-grid h2 {
  @apply mt-4 font-heading text-3xl font-black text-ink md:text-4xl;
}

.card-grid {
  @apply mt-10 grid gap-5 md:grid-cols-2 xl:grid-cols-4;
}

.info-card {
  @apply rounded-lg border border-forest/15 bg-paper p-6 shadow-sm;
}

.info-card h3 {
  @apply font-heading text-2xl font-extrabold text-ink;
}

.info-card p {
  @apply mt-4 leading-7 text-muted;
}

.split-grid {
  @apply grid gap-10 lg:grid-cols-2;
}

.check-list {
  @apply mt-8 grid gap-3;
}

.check-list li {
  @apply rounded-lg border border-forest/15 bg-sand px-4 py-3 font-semibold leading-6 text-forest;
}

.muted-list li {
  @apply border-trust/15 bg-white/65 text-muted;
}

.proof-section {
  @apply bg-night py-16 text-white md:py-24;
}

.proof-grid {
  @apply grid gap-10 lg:grid-cols-[0.85fr_1.15fr] lg:items-start;
}

.proof-grid h2 {
  @apply text-white;
}

.proof-grid > div > p:not(.eyebrow) {
  @apply text-white/75;
}

.scenario-list {
  @apply grid gap-4;
}

.scenario-card {
  @apply rounded-lg border border-scan/20 bg-white/[0.055] p-5;
}

.scenario-card h3 {
  @apply font-heading text-2xl font-extrabold text-white;
}

.scenario-card p {
  @apply mt-3 leading-7 text-white/75;
}

.dark-cta {
  @apply bg-paper py-16 md:py-20;
}

.dark-cta h2 {
  @apply mx-auto max-w-3xl font-heading text-3xl font-black text-ink md:text-4xl;
}

.dark-cta p {
  @apply mx-auto mt-4 max-w-2xl leading-7 text-muted;
}
</style>
