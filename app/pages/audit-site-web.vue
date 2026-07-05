<template>
  <div class="AuditPage">
    <LandingPageContent :landing="landings['/audit-site-web']" />
    <AuditStepper />
  </div>
</template>

<script setup lang="ts">
import AuditStepper from '~/components/audit/AuditStepper.vue';
import LandingPageContent from '~/components/sections/LandingPageContent.vue';
import { landings } from '~/utils/siteContent';
</script>

<style scoped>
@reference "../assets/css/main.css";

.AuditPage {
  @apply flex flex-col;
}
</style>
