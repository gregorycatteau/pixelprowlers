<template>
  <SiteShell>
    <main class="diagnostic-page">
      <section class="diagnostic-hero" aria-labelledby="diagnostic-title">
        <div class="form-container">
          <p class="eyebrow">Diagnostic gratuit</p>
          <h1 id="diagnostic-title">Parlons de votre situation. Honnêtement.</h1>
          <p>5 minutes. 5 questions. Zéro pression.</p>
        </div>
      </section>
      <LazyDiagnosticForm />
    </main>
  </SiteShell>
</template>

<script setup lang="ts">
import SiteShell from '~/components/layout/SiteShell.vue';
</script>
