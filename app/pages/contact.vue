<template>
  <main class="contact-page">
    <section class="about-hero" aria-labelledby="contact-title">
      <div class="article-container">
        <p class="eyebrow">Contact</p>
        <h1 id="contact-title">Parlons-en.</h1>
        <p>Une réparation, du matériel reconditionné ou un besoin numérique : décrivez votre situation. Nous vous aidons à préciser la suite.</p>
      </div>
    </section>

    <section class="manifest-section" aria-labelledby="contact-form-title">
      <div class="article-container">
        <RepairHandoff compact />
        <LazyFormsContactForm :initial-need="initialNeed" />
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import RepairHandoff from '~/components/sections/RepairHandoff.vue';
import { resolveContactNeed } from '~/utils/contactNeeds';
const route = useRoute();
const initialNeed = computed(() => resolveContactNeed(route.query.besoin));
useSeoMeta({ title: 'Contact : réparation, réemploi et services numériques | PixelProwlers', description: 'Décrivez votre panne, demandez du matériel reconditionné ou préparez un projet numérique avec PixelProwlers.', robots: 'index, follow', ogUrl: 'https://pixelprowlers.io/contact' });
useHead({ link: [{ rel: 'canonical', href: 'https://pixelprowlers.io/contact' }] });
</script>

<style scoped>
@reference "../assets/css/main.css";
.manifest-section .article-container { @apply grid gap-8; }
</style>
