<template>
  <section class="hero-section" aria-labelledby="hero-title">
    <div class="container-site hero-grid">
      <div class="hero-copy">
        <p class="eyebrow">Sécurité concrète pour petites structures</p>
        <h1 id="hero-title" class="hero-title">
          Sites, accès, sauvegardes : reprenez la main sans vous faire avaler par la technique.
        </h1>
        <p class="hero-text">
          PixelProwlers aide les associations, TPE, indépendants et écoles alternatives à sécuriser,
          maintenir et documenter leur numérique avec une culture Linux, open source et sobriété utile.
        </p>

        <div class="hero-actions" aria-label="Actions principales">
          <NuxtLink to="/audit-site-web" class="primary-action">Faire vérifier mon site</NuxtLink>
          <NuxtLink to="/contact" class="secondary-action">Décrire mon urgence</NuxtLink>
        </div>

        <ul class="proof-list" aria-label="Ce que PixelProwlers privilégie">
          <li>Audit site web</li>
          <li>Site maintenable</li>
          <li>Transmission</li>
        </ul>
      </div>

      <aside class="diagnostic-panel" aria-labelledby="diagnostic-title">
        <p class="panel-kicker">Première lecture</p>
        <h2 id="diagnostic-title" class="panel-title">On vérifie les points de rupture.</h2>

        <div class="question-list">
          <article v-for="item in diagnosticItems" :key="item.title" class="question-card">
            <span class="question-icon" aria-hidden="true">{{ item.number }}</span>
            <div>
              <h3>{{ item.title }}</h3>
              <p>{{ item.text }}</p>
            </div>
          </article>
        </div>

        <p class="panel-objective">Objectif : décider quoi corriger maintenant, quoi documenter, quoi laisser tranquille.</p>
      </aside>
    </div>
  </section>
</template>

<script setup lang="ts">
const diagnosticItems = [
  {
    number: '1',
    title: 'Qui a les clés ?',
    text: 'Comptes admin, mails, hébergement, prestataire, bénévole.',
  },
  {
    number: '2',
    title: 'Qu’est-ce qui est sauvegardé ?',
    text: 'Copies réelles, restauration testée, fréquence, propriétaire.',
  },
  {
    number: '3',
    title: 'Qu’est-ce qui casse en premier ?',
    text: 'Site, formulaire, machine, plugin oublié, mot de passe réutilisé.',
  },
] as const;
</script>

<style scoped>
.hero-section {
  @apply bg-paper py-16 md:py-24;
}

.hero-grid {
  @apply grid items-center gap-10 lg:grid-cols-[1.05fr_0.95fr];
}

.hero-copy {
  @apply max-w-[22.5rem] lg:max-w-4xl;
}

.eyebrow {
  @apply font-mono text-xs font-bold uppercase tracking-[0.24em] text-trust;
}

.hero-title {
  @apply mt-5 max-w-[22.5rem] font-heading text-3xl font-black leading-[1.04] tracking-[0.02em] text-ink sm:text-4xl lg:max-w-5xl lg:text-6xl;
}

.hero-text {
  @apply mt-6 max-w-[22.5rem] text-base leading-8 text-muted lg:max-w-3xl lg:text-xl;
}

.hero-actions {
  @apply mt-8 flex flex-col gap-3 sm:flex-row;
}

.primary-action {
  @apply inline-flex min-h-12 items-center justify-center rounded-lg bg-action px-6 py-3 text-center font-extrabold text-white shadow-orange outline-none transition hover:bg-[#FF9F2D] focus-visible:ring-2 focus-visible:ring-action focus-visible:ring-offset-2 focus-visible:ring-offset-paper;
}

.secondary-action {
  @apply inline-flex min-h-12 items-center justify-center rounded-lg border-2 border-trust px-6 py-3 text-center font-extrabold text-ink outline-none transition hover:border-scan hover:bg-scan/10 hover:text-forest focus-visible:ring-2 focus-visible:ring-scan focus-visible:ring-offset-2 focus-visible:ring-offset-paper;
}

.proof-list {
  @apply mt-8 flex flex-wrap gap-2 text-sm font-bold text-forest;
}

.proof-list li {
  @apply rounded-full border border-forest/20 bg-white/60 px-4 py-2;
}

.diagnostic-panel {
  @apply relative max-w-[22.5rem] overflow-hidden rounded-lg border border-trust/20 bg-sand p-6 shadow-soft lg:max-w-none lg:p-7;
}

.diagnostic-panel::before {
  @apply absolute inset-0 opacity-25 content-[''];
  background-image:
    linear-gradient(rgba(44, 125, 160, 0.10) 1px, transparent 1px),
    linear-gradient(90deg, rgba(44, 125, 160, 0.10) 1px, transparent 1px);
  background-size: 32px 32px;
}

.panel-kicker {
  @apply relative z-10 font-mono text-xs font-bold uppercase tracking-[0.22em] text-trust;
}

.panel-title {
  @apply relative z-10 mt-3 font-heading text-3xl font-black text-ink;
}

.question-list {
  @apply relative z-10 mt-6 grid gap-4;
}

.question-card {
  @apply grid grid-cols-[2.25rem_1fr] gap-4 rounded-lg border border-trust/15 bg-paper/90 p-4 transition hover:-translate-y-0.5 hover:border-trust/45 hover:bg-paper;
}

.question-icon {
  @apply flex h-9 w-9 items-center justify-center rounded-full bg-trust font-mono text-sm font-bold text-white;
}

.question-card h3 {
  @apply font-heading text-xl font-extrabold text-ink;
}

.question-card p {
  @apply mt-2 text-sm leading-6 text-muted;
}

.panel-objective {
  @apply relative z-10 mt-6 rounded-lg bg-trust/10 px-4 py-3 text-sm font-extrabold text-forest;
}
</style>
