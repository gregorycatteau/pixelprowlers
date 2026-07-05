<template>
  <LandingPageContent :landing="landings['/transmission-acces']" />
</template>

<script setup lang="ts">
import LandingPageContent from '~/components/sections/LandingPageContent.vue';
import { landings } from '~/utils/siteContent';
</script>
