<template>
  <main class="ContactPage">
    <section class="ContactShell" aria-labelledby="contact-title">
      <p class="LocalNote">Une réparation ou du matériel reconditionné dans le Médoc ? Décrivez votre besoin ; nous préciserons ensemble les modalités de prise en charge.</p>
      <LazyFormsContactForm :initial-need="initialNeed" />
    </section>
  </main>
</template>
<script setup lang="ts">
import { computed } from 'vue';
import { resolveContactNeed } from '~/utils/contactNeeds';
const route = useRoute();
const initialNeed = computed(() => resolveContactNeed(route.query.besoin));
useSeoMeta({ title: 'Contact : réparation dans le Médoc et projets numériques | PixelProwlers', description: 'Contactez PixelProwlers pour une réparation ou du matériel reconditionné dans le Médoc, un conseil ou un projet numérique.', robots: 'index, follow', ogUrl: 'https://pixelprowlers.io/contact' });
useHead({ link: [{ rel: 'canonical', href: 'https://pixelprowlers.io/contact' }] });
</script>
<style scoped>
@reference "../assets/css/main.css";
.LocalNote { @apply mb-6 max-w-2xl text-base leading-relaxed; }
.ContactPage { @apply bg-pxp-paper text-pxp-ink; }
.ContactShell { @apply mx-auto max-w-4xl px-4 py-8 md:px-8 md:py-10; }
</style>
