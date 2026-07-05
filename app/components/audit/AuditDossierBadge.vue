<template>
  <div class="DossierBadge" role="status" aria-live="polite">
    <span class="DossierBadgeLabel">Dossier audit</span>
    <strong class="DossierBadgeNumber">{{ numeroDossier }}</strong>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  numeroDossier: string;
}>();
</script>

<style scoped>
@reference "../../assets/css/main.css";

.DossierBadge {
  @apply inline-flex flex-wrap items-center gap-2 rounded-lg border border-[#2b7053]/20 bg-white px-4 py-2 text-[#17251d] shadow-sm;
}

.DossierBadgeLabel {
  @apply text-sm font-bold uppercase tracking-wide text-[#2b7053];
}

.DossierBadgeNumber {
  @apply text-base font-black;
}
</style>
