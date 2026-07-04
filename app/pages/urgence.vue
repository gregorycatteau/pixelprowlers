<template>
  <SiteShell>
    <main class="urgency-page">
      <section class="urgency-hero" aria-labelledby="urgency-title">
        <div class="article-container">
          <p class="eyebrow">Urgence web</p>
          <h1 id="urgency-title">Votre site est en vrac ? On prend la demande maintenant.</h1>
          <p>Décrivez le problème en quelques blocs. Vous recevez une référence de dossier à conserver.</p>
        </div>
      </section>
      <LazyUrgencyForm />
    </main>
  </SiteShell>
</template>

<script setup lang="ts">
import SiteShell from '~/components/layout/SiteShell.vue';
</script>
