<template>
  <section class="audience-section" aria-labelledby="audience-title">
    <div class="container-site">
      <div class="section-heading">
        <p class="eyebrow">Cadre de collaboration</p>
        <h2 id="audience-title">Pour qui, et pas pour qui.</h2>
        <p>
          Le filtrage évite les malentendus : PixelProwlers est utile quand il faut du solide, du compréhensible et du durable.
        </p>
      </div>

      <div class="audience-grid">
        <article class="audience-card positive">
          <h3>Pour vous si...</h3>
          <ul>
            <li v-for="item in goodFits" :key="item">{{ item }}</li>
          </ul>
        </article>

        <article class="audience-card negative">
          <h3>Pas idéal si...</h3>
          <ul>
            <li v-for="item in badFits" :key="item">{{ item }}</li>
          </ul>
        </article>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const goodFits = [
  'Vous êtes une association, TPE, école, indépendant ou collectif avec un vrai besoin de fiabilité.',
  'Vous voulez comprendre ce qui est fait et pourquoi.',
  'Vous préférez réduire les risques concrets avant d’empiler des abonnements.',
  'Vous voulez que l’équipe gagne en autonomie grâce à la documentation et à la transmission.',
] as const;

const badFits = [
  'Vous voulez juste un site pas cher, vite fait, sans maintenance ni sauvegarde.',
  'Vous cherchez une promesse magique sans implication interne.',
  'Vous voulez multiplier les outils sans clarifier les usages.',
  'Vous voulez déléguer sans documenter ni transmettre.',
] as const;
</script>

<style scoped>
.audience-section {
  @apply bg-paper py-16 md:py-24;
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

.audience-grid {
  @apply mt-10 grid gap-5 lg:grid-cols-2;
}

.audience-card {
  @apply rounded-lg border p-6 shadow-sm;
}

.audience-card.positive {
  @apply border-forest/25 bg-sand;
}

.audience-card.negative {
  @apply border-trust/25 bg-white/65;
}

.audience-card h3 {
  @apply font-heading text-2xl font-extrabold text-ink;
}

.audience-card ul {
  @apply mt-5 space-y-3;
}

.audience-card li {
  @apply rounded-lg border border-forest/10 bg-paper px-4 py-3 leading-6 text-muted;
}
</style>
