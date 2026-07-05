<template>
  <section class="ResultSummary" aria-labelledby="audit-result-title">
    <div class="ResultHeader">
      <p class="ResultKicker">Résultat transmis</p>
      <h2 id="audit-result-title" class="ResultTitle">Votre dossier est complet.</h2>
      <p class="ResultIntro">
        Un consultant PixelProwlers reprendra votre dossier sous 48h avec une analyse détaillée et des recommandations personnalisées.
      </p>
    </div>

    <div class="ResultScorePanel">
      <span class="ResultScoreLabel">Score global</span>
      <strong class="ResultScoreValue">{{ normalizedGlobalScore }}/10</strong>
      <span class="ResultPriority">Pilier prioritaire : {{ result.pilier_faible }}</span>
    </div>

    <div class="PillarGrid">
      <article v-for="score in normalizedScores" :key="score.id" class="PillarScore">
        <h3 class="PillarTitle">{{ score.label }}</h3>
        <p class="PillarValue">{{ score.value }}/10</p>
      </article>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import type { AuditResult } from '~/composables/useAudit';

const props = defineProps<{
  result: AuditResult;
}>();

const formatScore = (value: string | number) => Number(value).toFixed(2).replace('.00', '');

const normalizedGlobalScore = computed(() => formatScore(props.result.score_global));
const normalizedScores = computed(() => Object.entries(props.result.scores_series).map(([id, score]) => ({
  id,
  label: score.label,
  value: formatScore(score.score),
})));
</script>

<style scoped>
@reference "../../assets/css/main.css";

.ResultSummary {
  @apply mx-auto grid w-[min(920px,calc(100%_-_32px))] gap-6 rounded-lg border border-[#2b7053]/15 bg-[#fbfaf5] p-6 shadow-sm;
}

.ResultHeader {
  @apply grid gap-3;
}

.ResultKicker {
  @apply text-sm font-black uppercase tracking-wide text-[#2b7053];
}

.ResultTitle {
  @apply text-[clamp(1.85rem,3vw,2.75rem)] font-black leading-tight text-[#17251d];
}

.ResultIntro {
  @apply max-w-[760px] text-base font-bold leading-relaxed text-[#435046];
}

.ResultScorePanel {
  @apply grid gap-2 rounded-lg bg-[#17251d] p-5 text-white;
}

.ResultScoreLabel,
.ResultPriority {
  @apply text-sm font-bold uppercase tracking-wide text-[#9ee7df];
}

.ResultScoreValue {
  @apply text-[clamp(2.2rem,5vw,4rem)] font-black leading-none;
}

.PillarGrid {
  @apply grid gap-4;
}

.PillarScore {
  @apply rounded-lg border border-[#2b7053]/15 bg-white p-4;
}

.PillarTitle {
  @apply text-base font-black text-[#17251d];
}

.PillarValue {
  @apply mt-2 text-2xl font-black text-[#2b7053];
}

@media (min-width: 760px) {
  .PillarGrid {
    @apply grid-cols-2;
  }
}
</style>
