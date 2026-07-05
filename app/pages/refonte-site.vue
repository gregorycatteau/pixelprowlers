<template>
  <LandingPageContent :landing="landings['/refonte-site']" />
</template>

<script setup lang="ts">
import LandingPageContent from '~/components/sections/LandingPageContent.vue';
import { landings } from '~/utils/siteContent';
</script>
