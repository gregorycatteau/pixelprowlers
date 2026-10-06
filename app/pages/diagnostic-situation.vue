<template>
  <main class="diagnostic-page">
    <section class="diagnostic-hero" aria-labelledby="diagnostic-title">
      <div class="form-container">
        <p class="eyebrow">Diagnostic gratuit</p>
        <h1 id="diagnostic-title">Parlons de votre situation. Honnêtement.</h1>
        <p>{{ diagnosticSteps.length }} questions pour faire le point.</p>
      </div>
    </section>
    <LazyFormsDiagnosticForm />
  </main>
</template>

<script setup lang="ts">
import { diagnosticSteps } from '~/composables/useDiagnostic';
useSeoMeta({ title: 'Bilan numérique : faire le point | PixelProwlers', description: 'Quatre questions pour repérer les difficultés de votre site et de vos accès.', robots: 'index, follow', ogUrl: 'https://pixelprowlers.io/diagnostic-situation' });
useHead({ link: [{ rel: 'canonical', href: 'https://pixelprowlers.io/diagnostic-situation' }] });
</script>
