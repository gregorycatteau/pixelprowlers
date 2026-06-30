<template>
  <main class="bg-paper text-ink">
    <section class="page-hero">
      <div class="container-site hero-grid">
        <div>
          <p class="eyebrow">Audit sécurité site web</p>
          <h1>Faites vérifier ce qui expose vraiment votre site.</h1>
          <p>
            Pour associations, TPE, indépendants et petites structures qui veulent savoir si leur site,
            leurs accès, leurs sauvegardes et leurs formulaires tiennent encore debout.
          </p>
          <div class="hero-actions">
            <NuxtLink to="/contact" class="cta-primary px-7 py-3">Faire vérifier mon site</NuxtLink>
            <NuxtLink to="/contact" class="cta-secondary-local">Décrire mon urgence</NuxtLink>
          </div>
        </div>

        <aside class="proof-panel" aria-labelledby="audit-proof-title">
          <p class="panel-kicker">Cadre clair</p>
          <h2 id="audit-proof-title">Un audit n’est pas une promesse magique.</h2>
          <p>
            Il rend visibles les failles fréquentes, les dépendances dangereuses et les corrections prioritaires.
            Pas de théâtre cyber, pas de “sécurité totale”.
          </p>
        </aside>
      </div>
    </section>

    <section class="content-section">
      <div class="container-site">
        <div class="section-heading">
          <p class="eyebrow">À vérifier</p>
          <h2>Les problèmes qu’on cherche en priorité.</h2>
        </div>

        <div class="card-grid">
          <article v-for="item in checks" :key="item.title" class="info-card">
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
          <h2>Ce que vous récupérez.</h2>
          <ul class="check-list">
            <li v-for="item in deliverables" :key="item">{{ item }}</li>
          </ul>
        </div>

        <div>
          <p class="eyebrow">Limites</p>
          <h2>Ce que l’audit ne garantit pas.</h2>
          <ul class="check-list muted-list">
            <li v-for="item in limits" :key="item">{{ item }}</li>
          </ul>
        </div>
      </div>
    </section>

    <section class="method-band">
      <div class="container-site">
        <div class="section-heading light">
          <p class="eyebrow light">Méthode</p>
          <h2>Observer, prioriser, corriger sans noyer l’équipe.</h2>
          <p>
            Avant d’ajouter des outils, on vérifie ce qui tient encore debout. Un site sans sauvegarde
            testée n’est pas maintenu. Un accès partagé dans un tableur n’est pas une stratégie.
          </p>
        </div>

        <div class="method-grid">
          <article v-for="step in steps" :key="step.title" class="method-card">
            <span>{{ step.number }}</span>
            <h3>{{ step.title }}</h3>
            <p>{{ step.text }}</p>
          </article>
        </div>
      </div>
    </section>

    <section class="final-cta">
      <div class="container-site text-center">
        <h2>Votre site mérite une lecture claire, pas un devis flou.</h2>
        <p>
          Décrivez la situation : URL, CMS, hébergeur, urgence, sauvegardes connues et accès disponibles.
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
  title: 'Audit sécurité de site web | PixelProwlers',
  description: 'Audit sécurité pour site associatif, TPE ou indépendant : accès, sauvegardes, CMS, hébergement, formulaires, priorités et limites claires.',
  path: '/audit-site-web',
});

const checks = [
  {
    title: 'Sauvegardes',
    text: 'Existence, fréquence, restauration testée et personne responsable.',
  },
  {
    title: 'Accès',
    text: 'Comptes administrateurs, mots de passe réutilisés, MFA et anciens intervenants.',
  },
  {
    title: 'CMS et mises à jour',
    text: 'WordPress, plugins, thèmes, versions oubliées et extensions inutiles.',
  },
  {
    title: 'Formulaires',
    text: 'Validation, spam, injections, rate limit et données envoyées par email.',
  },
  {
    title: 'Hébergement',
    text: 'HTTPS, configuration, sauvegardes hébergeur, accès FTP/SSH et séparation des droits.',
  },
  {
    title: 'Dépendance humaine',
    text: 'Ce qui bloque si la seule personne qui sait faire n’est plus disponible.',
  },
] as const;

const deliverables = [
  'Une synthèse lisible pour décideurs non techniques.',
  'Une liste de risques classés par priorité.',
  'Des corrections recommandées, réalistes et chiffrables.',
  'Les points à documenter pour ne plus dépendre d’une seule personne.',
  'Une proposition d’accompagnement si PixelProwlers est utile.',
] as const;

const limits = [
  'L’audit ne garantit pas qu’aucune faille n’existe.',
  'Il ne remplace pas un test d’intrusion complet.',
  'Il ne promet pas une récupération miracle après piratage.',
  'Il dépend des accès et informations disponibles.',
  'Il ne pousse pas une refonte si une correction simple suffit.',
] as const;

const steps = [
  { number: '01', title: 'Collecter', text: 'URL, CMS, hébergeur, accès disponibles, sauvegardes et contexte d’urgence.' },
  { number: '02', title: 'Observer', text: 'Contrôles non destructifs, revue des points visibles et questions ciblées.' },
  { number: '03', title: 'Prioriser', text: 'Ce qui expose, ce qui bloque, ce qui peut attendre sans gaspiller le budget.' },
  { number: '04', title: 'Transmettre', text: 'Rapport clair, plan d’action et documentation minimale pour garder la main.' },
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
.section-heading p {
  @apply mt-6 max-w-3xl text-lg leading-8 text-muted md:text-xl;
}

.hero-actions {
  @apply mt-8 flex flex-col gap-3 sm:flex-row;
}

.cta-secondary-local {
  @apply inline-flex min-h-12 items-center justify-center rounded-lg border-2 border-trust px-7 py-3 text-center font-extrabold text-ink outline-none transition hover:border-scan hover:bg-scan/10 hover:text-forest focus-visible:ring-2 focus-visible:ring-scan focus-visible:ring-offset-2 focus-visible:ring-offset-paper;
}

.proof-panel {
  @apply rounded-lg border border-forest/15 bg-sand p-6 shadow-soft md:p-8;
}

.panel-kicker {
  @apply font-mono text-xs font-bold uppercase tracking-[0.22em] text-trust;
}

.proof-panel h2 {
  @apply mt-4 font-heading text-3xl font-black text-ink;
}

.proof-panel p {
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
.split-grid h2 {
  @apply mt-4 font-heading text-3xl font-black text-ink md:text-4xl;
}

.card-grid {
  @apply mt-10 grid gap-5 md:grid-cols-2 xl:grid-cols-3;
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

.method-band {
  @apply bg-night py-16 text-white md:py-24;
}

.section-heading.light h2 {
  @apply text-white;
}

.section-heading.light p {
  @apply text-white/75;
}

.method-grid {
  @apply mt-10 grid gap-5 md:grid-cols-2 xl:grid-cols-4;
}

.method-card {
  @apply rounded-lg border border-scan/20 bg-white/[0.055] p-5;
}

.method-card span {
  @apply font-mono text-sm font-bold text-scan;
}

.method-card h3 {
  @apply mt-4 font-heading text-2xl font-extrabold text-white;
}

.method-card p {
  @apply mt-3 leading-7 text-white/75;
}

.final-cta {
  @apply bg-paper py-16 md:py-20;
}

.final-cta h2 {
  @apply mx-auto max-w-3xl font-heading text-3xl font-black text-ink md:text-4xl;
}

.final-cta p {
  @apply mx-auto mt-4 max-w-2xl leading-7 text-muted;
}
</style>
