<template>
  <main class="contact-page">
    <section class="about-hero" aria-labelledby="contact-title">
      <div class="article-container">
        <p class="eyebrow">Contact</p>
        <h1 id="contact-title">Parlons-en.</h1>
        <p>Urgence, question ou partenariat : décrivez votre situation. Votre demande sera enregistrée avant qualification.</p>
      </div>
    </section>

    <section class="manifest-section" aria-labelledby="contact-form-title">
      <div class="article-container">
        <LazyFormsContactForm :initial-demand-type="preselectedDemandType" />
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { isContactDemandType } from '~/composables/useContact';

const route = useRoute();

/*
 * Présélection du type de demande depuis l’URL (ex. venant du CTA de
 * /reparation-informatique). Toute valeur hors liste blanche est ignorée
 * silencieusement : elle n’est jamais transmise telle quelle au formulaire.
 */
const preselectedDemandType = computed(() => {
  const raw = route.query.demande;
  const value = Array.isArray(raw) ? raw[0] : raw;

  return isContactDemandType(value) ? value : undefined;
});
</script>
