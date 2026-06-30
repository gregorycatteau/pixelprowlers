<template>
  <section id="diagnostic" class="mirror-section" aria-labelledby="mirror-title">
    <div class="container-site">
      <div class="section-heading">
        <p class="eyebrow">Diagnostic de départ</p>
        <h2 id="mirror-title">Vous reconnaissez une de ces situations ?</h2>
        <p>
          On commence par nommer ce qui fatigue l’équipe, puis on distingue ce qui est urgent, ce qui est risqué et ce qui peut attendre.
        </p>
      </div>

      <div class="problem-grid">
        <article v-for="problem in problems" :key="problem" class="problem-card">
          <span aria-hidden="true"></span>
          <h3>{{ problem }}</h3>
        </article>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const problems = [
  'Votre site ne reflète plus votre activité.',
  'Vos accès sont dispersés entre plusieurs personnes.',
  'Vos documents vivent entre mails, Drive perso et vieux PC.',
  'Votre matériel ralentit l’équipe.',
  'Vous dépendez d’un bénévole ou d’un prestataire unique.',
  'Vous voulez du sérieux sans usine à gaz.',
] as const;
</script>

<style scoped>
.mirror-section {
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

.problem-grid {
  @apply mt-10 grid gap-4 md:grid-cols-2 xl:grid-cols-3;
}

.problem-card {
  @apply rounded-lg border border-forest/15 bg-paper p-5 shadow-sm transition hover:-translate-y-1 hover:border-scan hover:shadow-soft;
}

.problem-card span {
  @apply mb-5 block h-1.5 w-12 rounded-full bg-scan;
}

.problem-card h3 {
  @apply font-heading text-xl font-extrabold leading-snug text-ink;
}
</style>
