<template>
  <main class="seo-page bg-paper text-ink">
    <section class="article-hero">
      <div class="container-site hero-grid">
        <div>
          <p class="eyebrow">{{ eyebrow }}</p>
          <h1>{{ title }}</h1>
          <p class="hero-text">{{ intro }}</p>

          <div class="hero-actions">
            <NuxtLink :to="primaryCta.href" class="cta-primary px-7 py-3">
              {{ primaryCta.label }}
            </NuxtLink>
            <NuxtLink to="/audit-site-web" class="secondary-action">
              Faire vérifier mon site
            </NuxtLink>
          </div>
        </div>

        <aside class="summary-panel" aria-labelledby="summary-title">
          <p class="panel-kicker">À retenir</p>
          <h2 id="summary-title">{{ summaryTitle }}</h2>
          <p>{{ summary }}</p>
        </aside>
      </div>
    </section>

    <section class="article-section">
      <div class="container-site article-grid">
        <article class="article-content">
          <section aria-labelledby="symptoms-title">
            <p class="eyebrow">Symptômes</p>
            <h2 id="symptoms-title">Comment reconnaître le problème.</h2>
            <div class="point-grid">
              <article v-for="item in symptoms" :key="item.title" class="point-card">
                <h3>{{ item.title }}</h3>
                <p>{{ item.text }}</p>
              </article>
            </div>
          </section>

          <section aria-labelledby="risks-title">
            <p class="eyebrow">Risques concrets</p>
            <h2 id="risks-title">Ce qui finit par coûter du temps, de l’argent ou de l’énergie.</h2>
            <ul class="detail-list">
              <li v-for="risk in risks" :key="risk">{{ risk }}</li>
            </ul>
          </section>

          <section aria-labelledby="exposure-title">
            <p class="eyebrow">Ce qui est exploité</p>
            <h2 id="exposure-title">Ce qu’une panne, une erreur humaine ou un attaquant opportuniste utilise.</h2>
            <p>{{ exploitation }}</p>
            <p class="warning-note">
              Le but n’est pas de fournir une recette offensive. Le but est de rendre visibles les points faibles
              simples, fréquents et corrigeables.
            </p>
          </section>

          <section aria-labelledby="checklist-title">
            <p class="eyebrow">Checklist</p>
            <h2 id="checklist-title">Ce qu’il faut vérifier avant de décider.</h2>
            <ul class="check-list">
              <li v-for="item in checklist" :key="item">{{ item }}</li>
            </ul>
          </section>

          <section aria-labelledby="pixel-title">
            <p class="eyebrow">Accompagnement</p>
            <h2 id="pixel-title">Ce que PixelProwlers peut faire.</h2>
            <div class="point-grid">
              <article v-for="item in pixelActions" :key="item.title" class="point-card">
                <h3>{{ item.title }}</h3>
                <p>{{ item.text }}</p>
              </article>
            </div>
          </section>

          <section aria-labelledby="limits-title">
            <p class="eyebrow">Limites raisonnables</p>
            <h2 id="limits-title">Ce qu’il ne faut pas promettre.</h2>
            <ul class="detail-list muted">
              <li v-for="limit in limits" :key="limit">{{ limit }}</li>
            </ul>
          </section>
        </article>

        <aside class="article-sidebar" aria-labelledby="sidebar-title">
          <h2 id="sidebar-title">Liens utiles</h2>
          <nav aria-label="Liens internes recommandés">
            <NuxtLink v-for="link in internalLinks" :key="link.href" :to="link.href">
              {{ link.label }}
            </NuxtLink>
          </nav>
        </aside>
      </div>
    </section>

    <section class="final-cta">
      <div class="container-site final-grid">
        <div>
          <p class="eyebrow">Prochaine action</p>
          <h2>{{ finalTitle }}</h2>
          <p>{{ finalText }}</p>
        </div>
        <NuxtLink :to="finalCta.href" class="cta-primary px-7 py-3">
          {{ finalCta.label }}
        </NuxtLink>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
type ArticlePoint = {
  title: string;
  text: string;
};

type ArticleLink = {
  label: string;
  href: string;
};

defineProps<{
  eyebrow: string;
  title: string;
  intro: string;
  summaryTitle: string;
  summary: string;
  symptoms: readonly ArticlePoint[];
  risks: readonly string[];
  exploitation: string;
  checklist: readonly string[];
  pixelActions: readonly ArticlePoint[];
  limits: readonly string[];
  internalLinks: readonly ArticleLink[];
  primaryCta: ArticleLink;
  finalTitle: string;
  finalText: string;
  finalCta: ArticleLink;
}>();
</script>

<style scoped>
.article-hero {
  @apply border-b border-forest/15 bg-paper py-16 md:py-24;
}

.hero-grid {
  @apply grid gap-8 lg:grid-cols-[1.05fr_0.75fr] lg:items-center;
}

.eyebrow {
  @apply font-mono text-xs font-bold uppercase tracking-[0.24em] text-trust;
}

.article-hero h1 {
  @apply mt-5 max-w-4xl font-heading text-4xl font-black leading-[1.04] text-ink sm:text-5xl xl:text-6xl;
}

.hero-text {
  @apply mt-6 max-w-3xl text-lg leading-8 text-muted md:text-xl;
}

.hero-actions {
  @apply mt-8 flex flex-col gap-3 sm:flex-row;
}

.secondary-action {
  @apply inline-flex min-h-12 items-center justify-center rounded-lg border-2 border-trust px-7 py-3 text-center font-extrabold text-ink outline-none transition hover:border-scan hover:bg-scan/10 hover:text-forest focus-visible:ring-2 focus-visible:ring-scan focus-visible:ring-offset-2 focus-visible:ring-offset-paper;
}

.summary-panel {
  @apply rounded-lg border border-forest/15 bg-sand p-6 shadow-soft md:p-8;
}

.panel-kicker {
  @apply font-mono text-xs font-bold uppercase tracking-[0.22em] text-trust;
}

.summary-panel h2 {
  @apply mt-4 font-heading text-3xl font-black text-ink;
}

.summary-panel p {
  @apply mt-4 leading-7 text-muted;
}

.article-section {
  @apply bg-sand py-16 md:py-24;
}

.article-grid {
  @apply grid gap-8 lg:grid-cols-[minmax(0,1fr)_20rem] lg:items-start;
}

.article-content {
  @apply grid gap-12;
}

.article-content section {
  @apply rounded-lg border border-forest/15 bg-paper p-6 shadow-sm md:p-8;
}

.article-content h2 {
  @apply mt-4 max-w-4xl font-heading text-3xl font-black text-ink md:text-4xl;
}

.article-content p:not(.eyebrow) {
  @apply mt-5 max-w-4xl leading-8 text-muted;
}

.point-grid {
  @apply mt-8 grid gap-5 md:grid-cols-2;
}

.point-card {
  @apply rounded-lg border border-forest/15 bg-sand p-5;
}

.point-card h3 {
  @apply font-heading text-2xl font-extrabold text-ink;
}

.point-card p {
  @apply mt-3 leading-7 text-muted;
}

.detail-list,
.check-list {
  @apply mt-8 grid gap-3;
}

.detail-list li,
.check-list li {
  @apply rounded-lg border border-forest/15 bg-sand px-4 py-3 font-semibold leading-6 text-forest;
}

.detail-list.muted li {
  @apply border-trust/15 bg-white/65 text-muted;
}

.warning-note {
  @apply rounded-lg border border-trust/20 bg-sand px-5 py-4 font-semibold text-forest;
}

.article-sidebar {
  @apply rounded-lg border border-forest/15 bg-paper p-6 shadow-sm lg:sticky lg:top-28;
}

.article-sidebar h2 {
  @apply font-heading text-2xl font-black text-ink;
}

.article-sidebar nav {
  @apply mt-5 grid gap-3;
}

.article-sidebar a {
  @apply rounded-lg border border-forest/15 bg-sand px-4 py-3 text-sm font-bold leading-6 text-forest outline-none transition hover:border-scan hover:text-trust focus-visible:ring-2 focus-visible:ring-scan focus-visible:ring-offset-2 focus-visible:ring-offset-paper;
}

.final-cta {
  @apply bg-night py-16 text-white md:py-20;
}

.final-grid {
  @apply grid gap-8 md:grid-cols-[1fr_auto] md:items-center;
}

.final-cta .eyebrow {
  @apply text-scan;
}

.final-cta h2 {
  @apply mt-4 max-w-3xl font-heading text-3xl font-black md:text-4xl;
}

.final-cta p {
  @apply mt-4 max-w-2xl leading-7 text-white/75;
}
</style>
