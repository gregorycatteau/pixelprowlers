<template>
  <main class="urgency-page">
    <section class="urgency-hero" aria-labelledby="urgency-title">
      <div class="article-container">
        <p class="eyebrow">Urgence web</p>
        <h1 id="urgency-title">Votre site est en vrac ? On prend la demande maintenant.</h1>
        <p>Décrivez le problème en quelques blocs. Vous recevez une référence de dossier à conserver.</p>
      </div>
    </section>
    <LazyFormsUrgencyForm />
  </main>
</template>

<script setup lang="ts">
useSeoMeta({ title: 'Urgence web : site inaccessible ou incident | PixelProwlers', description: 'Signalez un site inaccessible, un accès perdu ou une modification suspecte pour qualifier une urgence web.', robots: 'index, follow', ogUrl: 'https://pixelprowlers.io/urgence' });
useHead({ link: [{ rel: 'canonical', href: 'https://pixelprowlers.io/urgence' }] });
</script>
