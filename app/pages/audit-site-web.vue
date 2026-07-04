<template>
  <SiteShell>
    <LandingPageContent :landing="landings['/audit-site-web']" />
  </SiteShell>
</template>

<script setup lang="ts">
import SiteShell from '~/components/layout/SiteShell.vue';
import LandingPageContent from '~/components/sections/LandingPageContent.vue';
import { landings } from '~/utils/siteContent';
</script>
