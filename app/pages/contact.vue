<template>
  <main class="ContactPage">
    <section class="ContactShell" aria-labelledby="contact-title">
      <LazyFormsContactForm :initial-need="initialNeed" />
    </section>
  </main>
</template>
<script setup lang="ts">
import { computed } from 'vue';
import { resolveContactNeed } from '~/utils/contactNeeds';
const route = useRoute();
const initialNeed = computed(() => resolveContactNeed(route.query.besoin));
useSeoMeta({ title: 'Contact : réparation, réemploi et services numériques | PixelProwlers', description: 'Décrivez votre panne, demandez du matériel reconditionné ou préparez un projet numérique avec PixelProwlers.', robots: 'index, follow', ogUrl: 'https://pixelprowlers.io/contact' });
useHead({ link: [{ rel: 'canonical', href: 'https://pixelprowlers.io/contact' }] });
</script>
<style scoped>
@reference "../assets/css/main.css";
.ContactPage { @apply bg-pxp-paper text-pxp-ink; }
.ContactShell { @apply mx-auto max-w-4xl px-4 py-8 md:px-8 md:py-10; }
</style>
