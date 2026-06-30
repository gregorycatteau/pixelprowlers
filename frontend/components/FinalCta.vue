<template>
  <section class="final-section" aria-labelledby="final-title">
    <div class="container-site">
      <div class="final-card">
        <p class="eyebrow">Premier échange</p>
        <h2 id="final-title">On fait le point sur votre situation ?</h2>
        <p>
          On clarifie le besoin, les risques et le plan d’action avant de parler solution.
        </p>
        <NuxtLink to="/contact" class="final-action">Démarrer l’échange</NuxtLink>
      </div>
    </div>
  </section>
</template>

<style scoped>
.final-section {
  @apply bg-paper pb-16 md:pb-24;
}

.final-card {
  @apply rounded-lg bg-night p-6 text-white shadow-soft md:p-10;
}

.eyebrow {
  @apply font-mono text-xs font-bold uppercase tracking-[0.24em] text-scan;
}

.final-card h2 {
  @apply mt-4 max-w-3xl font-heading text-3xl font-black md:text-5xl;
}

.final-card p {
  @apply mt-5 max-w-2xl text-lg leading-8 text-white/75;
}

.final-action {
  @apply mt-8 inline-flex min-h-12 items-center justify-center rounded-lg bg-action px-6 py-3 text-center font-extrabold text-white shadow-orange outline-none transition hover:bg-[#FF9F2D] focus-visible:ring-2 focus-visible:ring-action focus-visible:ring-offset-2 focus-visible:ring-offset-night;
}
</style>
