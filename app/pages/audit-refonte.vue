<template>
  <div class="AuditRefontePage">
    <LandingPageContent :landing="auditRefonteLanding" />
    <RefonteAuditStepper />
  </div>
</template>

<script setup lang="ts">
import RefonteAuditStepper from '~/components/refonte/RefonteAuditStepper.vue';
import LandingPageContent from '~/components/sections/LandingPageContent.vue';
import { auditRefonteLanding } from '~/utils/siteContent';
</script>

<style scoped>
@reference "../assets/css/main.css";

.AuditRefontePage {
  @apply flex flex-col;
}
</style>
