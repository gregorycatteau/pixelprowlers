<template>
  <main class="urgency-page">
    <section class="urgency-hero" aria-labelledby="urgency-title">
      <div class="article-container">
        <p class="eyebrow">Urgence web</p>
        <h1 id="urgency-title">Votre site est bloqué ?</h1>
        <p>Un site inaccessible, un accès perdu ou une modification suspecte : décrivez l’incident pour préparer notre échange.</p>
      </div>
    </section>
    <LazyFormsUrgencyForm />
  </main>
</template>

<script setup lang="ts">
useSeoMeta({ title: 'Urgence web : site inaccessible ou incident | PixelProwlers', description: 'Signalez un site inaccessible, un accès perdu ou une modification suspecte pour qualifier une urgence web.', robots: 'index, follow', ogUrl: 'https://pixelprowlers.io/urgence' });
useHead({ link: [{ rel: 'canonical', href: 'https://pixelprowlers.io/urgence' }] });
</script>

<style scoped>
@reference "../assets/css/main.css";
.urgency-hero { @apply py-8 md:py-12; }
.article-container { @apply grid gap-4; }
h1 { @apply max-w-3xl text-4xl font-bold leading-tight md:text-5xl; }
.urgency-hero p:not(.eyebrow) { @apply max-w-3xl text-base font-normal leading-relaxed md:text-lg; }
</style>
