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
useSeoMeta({ title: 'Audit de site web : accès, sauvegardes et sécurité | PixelProwlers', description: 'Examiner les accès, la sécurité, les sauvegardes et les performances pour prioriser les actions.', robots: 'index, follow', ogUrl: 'https://pixelprowlers.io/audit-site-web' });
useHead({ link: [{ rel: 'canonical', href: 'https://pixelprowlers.io/audit-site-web' }] });
</script>

<style scoped>
@reference "../assets/css/main.css";

.AuditPage {
  @apply flex flex-col;
}
</style>
