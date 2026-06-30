<template>
  <main class="bg-paper text-ink">
    <section class="page-hero">
      <div class="container-site max-w-4xl">
        <p class="eyebrow">Matériel</p>
        <h1>Matériel informatique fiable et durable</h1>
        <p>
          Réparation, maintenance, reconditionnement et conseil pour équiper votre entreprise avec discernement.
        </p>
      </div>
    </section>

    <section class="content-section">
      <div class="container-site">
        <div class="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
          <ServiceCard v-for="item in services" :key="item.title" v-bind="item" />
        </div>

        <div class="mt-12 grid gap-6 md:grid-cols-2 xl:grid-cols-4">
          <ServiceCard v-for="item in benefits" :key="item.title" v-bind="item" />
        </div>
      </div>
    </section>

    <section class="dark-cta">
      <div class="container-site text-center">
        <h2>Besoin d’une réparation ou d’un poste fiable ?</h2>
        <p>
          Diagnostic, conseil et réponse rapide pour éviter les achats inutiles.
        </p>
        <NuxtLink to="/contact" class="cta-primary mt-8 px-7 py-3">
          Nous contacter
        </NuxtLink>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
const services = [
  { title: 'Réparation et maintenance', description: 'Diagnostic clair, intervention rapide et suivi après réparation.', icon: 'hardware' },
  { title: 'Reconditionnement', description: 'Matériel testé, nettoyé, mis à jour et remis en circulation proprement.', icon: 'shield' },
  { title: 'Vente de matériel', description: 'Postes et composants sélectionnés pour durer dans un contexte professionnel.', icon: 'hardware' },
] as const;

const benefits = [
  { title: 'Économique', description: 'Réduire les coûts sans sacrifier la fiabilité.', icon: 'bolt' },
  { title: 'Responsable', description: 'Allonger la durée de vie du matériel existant.', icon: 'shield' },
  { title: 'Testé', description: 'Chaque poste est contrôlé avant remise en service.', icon: 'hardware' },
  { title: 'Support local', description: 'Un interlocuteur direct pour les décisions techniques.', icon: 'training' },
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

.dark-cta {
  @apply bg-night py-16 text-white md:py-20;
}

.dark-cta h2 {
  @apply mx-auto max-w-3xl font-heading text-3xl font-black md:text-4xl;
}

.dark-cta p {
  @apply mx-auto mt-4 max-w-2xl leading-7 text-white/75;
}
</style>
