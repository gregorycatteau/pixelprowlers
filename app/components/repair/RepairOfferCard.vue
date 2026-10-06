<template>
  <article class="OfferCard" :data-offer-id="offer.id">
    <p class="Kind" :class="{ Electronic: offer.estimate.kind === 'diagnostic', Fixed: offer.estimate.kind === 'fixed' }">{{ kindLabel }}</p>
    <h3>{{ offer.label }}</h3>
    <p class="Amount pxp-font-display">{{ budgetLabel(offer.estimate) }}</p>
    <p v-if="!offer.replacesPart" class="Scope">{{ offer.scope }}</p>
    <p class="Inclusion">{{ offer.replacesPart ? 'Pièce, pose et tests inclus. Prix confirmé après vérification du modèle.' : 'Intervention et tests inclus dans le périmètre présenté.' }}</p>
    <p v-if="offer.condition" class="Condition">{{ offer.condition }}</p>
    <p v-else-if="offer.quoteCases[0]" class="Condition">{{ offer.quoteCases[0] }}</p>
    <details><summary>Ce qui est inclus</summary><p>{{ offer.scope }}</p><p>Travail, tests et pièces prévues dans le périmètre ci-dessus. Transport et déplacement chiffrés séparément avant accord.</p><p v-for="line in offer.quoteCases" :key="line">{{ line }}</p></details>
  </article>
</template>
<script setup lang="ts">
import { computed } from 'vue';
import { budgetLabel, type RepairOffer } from '~/utils/repairGrid';
const props = defineProps<{ offer: RepairOffer }>();
const kindLabel = computed(() => props.offer.estimate.kind === 'range' ? 'Budget indicatif' : props.offer.estimate.kind === 'diagnostic' ? (props.offer.id === 'diagnostic-electronique' ? 'Diagnostic électronique' : 'Diagnostic') : 'Forfait');
</script>
<style scoped>
@reference "../../assets/css/main.css";
.OfferCard { @apply grid content-start gap-3 rounded-lg border border-pxp-green/25 bg-pxp-panel p-4 sm:p-5; }
.Kind { @apply w-fit rounded bg-pxp-green/10 px-2 py-1 text-xs font-semibold text-pxp-green; }
.Fixed { @apply bg-pxp-green text-white; }
.Electronic { @apply bg-pxp-ink text-white; }
h3 { @apply text-lg font-bold leading-tight; }
.Amount { @apply text-4xl leading-tight text-pxp-green; }
.Scope, .Inclusion, .Condition, details { @apply text-sm leading-relaxed; }
.Condition { @apply text-pxp-ink; }
summary { @apply min-h-11 cursor-pointer py-2 font-semibold underline underline-offset-4; }
details p { @apply mt-2; }
summary:focus-visible { @apply outline-2 outline-offset-2 outline-pxp-green; }
</style>
