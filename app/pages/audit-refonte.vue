<template>
  <div v-if="route.path.replace(/\/$/, '') === '/audit-refonte'" class="AuditRefontePage">
    <LandingPageContent :landing="auditRefonteLanding" />
    <RefonteAuditStepper />
  </div>
  <NuxtPage v-else />
</template>

<script setup lang="ts">
const route = useRoute();
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
