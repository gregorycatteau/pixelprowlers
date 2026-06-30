<template>
  <main class="bg-paper text-ink">
    <section class="page-hero">
      <div class="container-site max-w-4xl">
        <p class="eyebrow">Formations</p>
        <h1>Formations en hygiène numérique</h1>
        <p>
          Des sessions concrètes pour aider vos équipes à reconnaître les risques et adopter les bons réflexes.
        </p>
      </div>
    </section>

    <section class="content-section">
      <div class="container-site">
        <div class="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
          <ServiceCard v-for="item in formations" :key="item.title" v-bind="item" />
        </div>
      </div>
    </section>

    <section class="content-section alt">
      <div class="container-site">
        <h2>Formats et modalités</h2>
        <div class="mt-10 grid gap-6 md:grid-cols-3">
          <ServiceCard v-for="item in formats" :key="item.title" v-bind="item" />
        </div>
      </div>
    </section>

    <section class="dark-cta">
      <div class="container-site text-center">
        <h2>Formez vos équipes maintenant</h2>
        <p>
          Planifiez une session adaptée à votre niveau, vos risques et vos contraintes terrain.
        </p>
        <NuxtLink to="/contact" class="cta-primary mt-8 px-7 py-3">
          Planifier une formation
        </NuxtLink>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
const formations = [
  { title: 'Hygiène et sécurité numériques', description: 'Mots de passe, phishing, MFA, sauvegardes et réflexes quotidiens.', icon: 'shield' },
  { title: 'Conformité RGPD et CNIL', description: 'Comprendre les obligations et mettre en place des gestes réalistes.', icon: 'training' },
  { title: 'Gestion des incidents cyber', description: 'Réagir, contenir, communiquer et reprendre l’activité avec méthode.', icon: 'bolt' },
] as const;

const formats = [
  { title: 'Présentiel', description: 'Sur site avec vos équipes, vos cas concrets et vos outils.', icon: 'training' },
  { title: 'Distanciel', description: 'Sessions en ligne structurées, efficaces et faciles à planifier.', icon: 'code' },
  { title: 'Intra-entreprise', description: 'Contenu personnalisé pour vos priorités opérationnelles.', icon: 'shield' },
] as const;
</script>

<style scoped>
.page-hero {
  @apply border-b border-forest/15 bg-paper py-16 md:py-24;
}

.eyebrow {
  @apply font-mono text-xs font-bold uppercase tracking-[0.24em] text-trust;
}

.page-hero h1 {
  @apply mt-5 max-w-4xl font-heading text-4xl font-black leading-[1.04] text-ink sm:text-5xl md:text-6xl;
}

.page-hero p:not(.eyebrow) {
  @apply mt-6 max-w-3xl text-lg leading-8 text-muted md:text-xl;
}

.content-section {
  @apply bg-sand py-16 md:py-24;
}

.content-section.alt {
  @apply border-y border-forest/15 bg-paper;
}

.content-section h2 {
  @apply text-center font-heading text-3xl font-black text-ink md:text-4xl;
}

.dark-cta {
  @apply bg-night py-16 text-white md:py-20;
}

.dark-cta h2 {
  @apply font-heading text-3xl font-black md:text-4xl;
}

.dark-cta p {
  @apply mx-auto mt-4 max-w-2xl leading-7 text-white/75;
}
</style>
