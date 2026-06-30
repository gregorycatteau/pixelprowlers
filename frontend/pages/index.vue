<template>
  <main class="home-page">
    <HeroSection />
    <CoreOffers />
    <ProblemMirror />
    <RiskMap />
    <MethodSection />
    <AudienceFilter />
    <FinalCta />
  </main>
</template>

<script setup lang="ts">
usePixelSeo({
  title: 'PixelProwlers | Sécurité concrète et sites maintenables',
  description: 'Audit sécurité de site web, sites sobres maintenables, documentation et autonomie numérique pour associations, TPE, indépendants et collectifs.',
  path: '/',
});
</script>

<style scoped>
.home-page {
  @apply bg-paper text-ink;
}
</style>
