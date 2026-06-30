<template>
  <section id="methode" class="method-section" aria-labelledby="method-title">
    <div class="container-site method-grid">
      <div class="section-heading">
        <p class="eyebrow">Méthode</p>
        <h2 id="method-title">Avancer sans vous noyer dans la technique.</h2>
        <p>
          La méthode tient en quatre gestes simples : comprendre, rendre visible, décider, puis transmettre.
          Comprendre assez pour décider, documenter assez pour ne pas dépendre.
        </p>
      </div>

      <div class="steps" aria-label="Étapes d'accompagnement">
        <article v-for="step in steps" :key="step.title" class="step-card">
          <span>{{ step.number }}</span>
          <div>
            <h3>{{ step.title }}</h3>
            <p>{{ step.description }}</p>
          </div>
        </article>
      </div>

      <div class="deliverables-panel" aria-labelledby="deliverables-title">
        <h3 id="deliverables-title">Ce qui doit rester entre vos mains</h3>
        <ul>
          <li v-for="item in deliverables" :key="item">{{ item }}</li>
        </ul>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const steps = [
  {
    number: '01',
    title: 'Écouter',
    description: 'Comprendre vos usages, vos contraintes, vos budgets et les personnes impliquées.',
  },
  {
    number: '02',
    title: 'Cartographier',
    description: 'Repérer les sites, comptes, machines, documents, outils et dépendances critiques.',
  },
  {
    number: '03',
    title: 'Prioriser',
    description: 'Traiter d’abord ce qui réduit le plus de risque ou de friction pour l’équipe.',
  },
  {
    number: '04',
    title: 'Transmettre',
    description: 'Documenter, expliquer et former pour que vous gardiez la main après l’intervention.',
  },
] as const;

const deliverables = [
  'Une lecture claire des risques et priorités.',
  'Une cartographie des accès, outils et responsabilités.',
  'Des sauvegardes identifiées et, quand c’est possible, testées.',
  'Une documentation minimale exploitable par l’équipe.',
] as const;
</script>

<style scoped>
.method-section {
  @apply border-y border-forest/15 bg-sand py-16 md:py-24;
}

.method-grid {
  @apply grid gap-10 lg:grid-cols-[0.8fr_1fr_0.8fr] lg:items-start;
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

.steps {
  @apply grid gap-4;
}

.step-card {
  @apply grid gap-4 rounded-lg border border-forest/15 bg-paper p-5 shadow-sm transition hover:border-scan hover:shadow-soft sm:grid-cols-[4rem_1fr];
}

.step-card span {
  @apply flex h-14 w-14 items-center justify-center rounded-lg bg-forest font-mono text-sm font-bold text-white;
}

.step-card h3 {
  @apply font-heading text-2xl font-extrabold text-ink;
}

.step-card p {
  @apply mt-2 leading-7 text-muted;
}

.deliverables-panel {
  @apply rounded-lg border border-forest/15 bg-paper p-6 shadow-sm;
}

.deliverables-panel h3 {
  @apply font-heading text-2xl font-black text-ink;
}

.deliverables-panel ul {
  @apply mt-5 grid gap-3;
}

.deliverables-panel li {
  @apply rounded-lg border border-trust/15 bg-sand px-4 py-3 text-sm font-semibold leading-6 text-forest;
}
</style>
