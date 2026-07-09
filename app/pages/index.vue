<template>
  <HeroSection v-bind="heroContent" />
  <HomeSections :show-hero="false" />
</template>

<script setup lang="ts">
import HeroSection from '~/components/Hero/HeroSection.vue';
import HomeSections from '~/components/sections/HomeSections.vue';

const heroContent = {
  title: 'Votre site ralentit l’équipe.<span class="HeroTitleLine HeroTitleLineSecondary">On vous sort de la tempête en <span class="HeroTitleAccent">48h</span>.</span>',
  subtitle: 'Audit technique complet, refonte des performances et transmission sécurisée de vos accès. Même si votre tech n’est pas là demain.',
  ctaText: 'Obtenir un diagnostic clair',
  ctaLink: '/diagnostic-situation',
  ctaNote: 'Réponse sous 24h. Sans engagement. Pas d’accès demandé sans validation.',
};
</script>
