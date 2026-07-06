<template>
  <main class="RefonteResultPage">
    <section class="RefonteResultHero" aria-labelledby="refonte-result-title">
      <p class="RefonteResultKicker">Audit refonte</p>
      <h1 id="refonte-result-title" class="RefonteResultTitle">Rapport technique en préparation.</h1>
      <p class="RefonteResultIntro">{{ statusLabel }}</p>
    </section>

    <section class="RefonteResultShell" aria-live="polite">
      <div v-if="!reference" class="RefonteResultPanel">
        <h2 class="RefontePanelTitle">Référence manquante</h2>
        <p class="RefontePanelText">Relancez le parcours depuis la page audit refonte.</p>
        <AppButton href="/audit-refonte">Retour au parcours</AppButton>
      </div>

      <div v-else-if="isLoading && !result" class="RefonteResultPanel">
        <h2 class="RefontePanelTitle">Récupération du dossier</h2>
        <p class="RefontePanelText">On cherche la référence {{ reference }}.</p>
      </div>

      <div v-else-if="error" class="RefonteResultPanel">
        <h2 class="RefontePanelTitle">Rapport indisponible</h2>
        <p class="RefontePanelText">{{ error }}</p>
        <AppButton href="/audit-refonte">Relancer un audit refonte</AppButton>
      </div>

      <template v-else-if="result">
        <section class="RefonteResultPanel">
          <p class="RefonteResultKicker">{{ result.reference }}</p>
          <h2 class="RefontePanelTitle">{{ result.site_url }}</h2>
          <p class="RefontePanelText">{{ statusLabel }}</p>
          <div class="RefonteStatusPill">{{ result.analysis_status }}</div>
        </section>

        <section class="RefonteResultGrid">
          <article class="RefonteResultPanel">
            <h2 class="RefontePanelTitle">Technique</h2>
            <dl class="RefonteMetricList">
              <div>
                <dt>HTTPS</dt>
                <dd>{{ result.technical_report?.https || 'non disponible' }}</dd>
              </div>
              <div>
                <dt>Statut HTTP</dt>
                <dd>{{ result.technical_report?.status_code || 'non disponible' }}</dd>
              </div>
              <div>
                <dt>Ressources en erreur</dt>
                <dd>{{ result.technical_report?.failed_requests?.length || 0 }}</dd>
              </div>
              <div>
                <dt>Ressources lentes</dt>
                <dd>{{ result.technical_report?.slow_resources?.length || 0 }}</dd>
              </div>
            </dl>
          </article>

          <article class="RefonteResultPanel">
            <h2 class="RefontePanelTitle">Balises essentielles</h2>
            <ul class="RefonteCheckList">
              <li v-for="item in metaItems" :key="item.label">
                <span class="RefonteCheckState">{{ item.ok ? 'OK' : 'À vérifier' }}</span>
                <span>{{ item.label }}</span>
              </li>
            </ul>
          </article>
        </section>

        <section class="RefonteResultPanel">
          <h2 class="RefontePanelTitle">Performance</h2>
          <p class="RefontePanelText">{{ pagespeedText }}</p>
          <div class="RefontePerformanceGrid">
            <article v-for="strategy in performanceItems" :key="strategy.label" class="RefontePerformanceCard">
              <h3>{{ strategy.label }}</h3>
              <p>Score : {{ strategy.score }}</p>
              <p>LCP : {{ strategy.lcp }}</p>
              <p>CLS : {{ strategy.cls }}</p>
              <p>INP/FID : {{ strategy.inp }}</p>
            </article>
          </div>
        </section>

        <section class="RefonteResultPanel">
          <h2 class="RefontePanelTitle">Heuristiques Nielsen</h2>
          <div class="RefonteHeuristicGrid">
            <article v-for="heuristic in result.heuristic_report" :key="heuristic.name" class="RefonteHeuristicCard">
              <span class="RefonteStatusPill">{{ heuristic.score }}</span>
              <h3>{{ heuristic.name }}</h3>
              <p>{{ heuristic.justification }}</p>
            </article>
          </div>
        </section>
      </template>
    </section>
  </main>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue';
import AppButton from '~/components/ui/AppButton.vue';
import type { RefonteAuditResult } from '~/composables/useRefonteAudit';
import {
  REFONTE_AUDIT_QUERY,
  graphqlErrorMessage,
  graphqlRequest,
  parseGraphqlJson,
} from '~/utils/graphql';

const route = useRoute();
const reference = computed(() => typeof route.query.reference === 'string' ? route.query.reference : '');
const result = ref<RefonteAuditResult | null>(null);
const isLoading = ref(false);
const error = ref('');
let intervalId: ReturnType<typeof window.setInterval> | null = null;

const isPending = computed(() => result.value?.analysis_status === 'en_cours');
const normalizeAnalysisStatus = (status: string): RefonteAuditResult['analysis_status'] => ({
  EN_COURS: 'en_cours',
  TERMINE: 'termine',
  ECHEC_PARTIEL: 'echec_partiel',
  NON_ANALYSABLE: 'non_analysable',
  ECHEC: 'echec',
}[status] || status.toLowerCase()) as RefonteAuditResult['analysis_status'];

const statusLabel = computed(() => {
  if (!result.value) return "L'analyse démarre dès que le questionnaire est reçu.";
  if (result.value.analysis_status === 'en_cours') return "Analyse en cours. Cette page se met à jour automatiquement.";
  if (result.value.analysis_status === 'termine') return "Analyse terminée. Le rapport est prêt.";
  if (result.value.analysis_status === 'echec_partiel') return "Analyse partielle : certaines métriques ne sont pas disponibles.";
  if (result.value.analysis_status === 'non_analysable') return result.value.analysis_error || "Le site n'a pas pu être analysé automatiquement.";
  return result.value.analysis_error || "L'analyse a échoué.";
});

const metaItems = computed(() => {
  const meta = result.value?.technical_report?.meta_tags || {};
  return [
    { label: 'Title', ok: Boolean(meta.title) },
    { label: 'Description', ok: Boolean(meta.description) },
    { label: 'Viewport', ok: Boolean(meta.viewport) },
    { label: 'Open Graph title', ok: Boolean(meta.og_title) },
    { label: 'Open Graph description', ok: Boolean(meta.og_description) },
    { label: 'Open Graph image', ok: Boolean(meta.og_image) },
  ];
});

const pagespeedText = computed(() => result.value?.pagespeed_report?.status === 'available'
  ? 'Métriques PageSpeed récupérées.'
  : result.value?.pagespeed_report?.reason || 'Métriques non disponibles.');

const performanceItems = computed(() => {
  const data = result.value?.pagespeed_report?.results || {};
  return ['mobile', 'desktop'].map((key) => ({
    label: key === 'mobile' ? 'Mobile' : 'Desktop',
    score: data[key]?.performance_score ?? 'non disponible',
    lcp: data[key]?.lcp ?? 'non disponible',
    cls: data[key]?.cls ?? 'non disponible',
    inp: data[key]?.inp ?? 'non disponible',
  }));
});

const fetchResult = async () => {
  if (!reference.value) return;
  isLoading.value = true;
  error.value = '';

  try {
    const response = await graphqlRequest<{
      refonteAudit: {
        reference: string;
        site_url: string;
        analysis_status: RefonteAuditResult['analysis_status'];
        technical_report: RefonteAuditResult['technical_report'] | string;
        pagespeed_report: RefonteAuditResult['pagespeed_report'] | string;
        heuristic_report: RefonteAuditResult['heuristic_report'] | string;
        analysis_error: string;
        date_creation: string;
        date_maj: string;
      } | null;
    }>(REFONTE_AUDIT_QUERY, {
      reference: reference.value,
    });

    const data = response.refonteAudit;

    result.value = data ? {
      reference: data.reference,
      site_url: data.site_url,
      analysis_status: normalizeAnalysisStatus(data.analysis_status),
      technical_report: parseGraphqlJson<RefonteAuditResult['technical_report']>(data.technical_report, {}),
      pagespeed_report: parseGraphqlJson<RefonteAuditResult['pagespeed_report']>(data.pagespeed_report, {}),
      heuristic_report: parseGraphqlJson<RefonteAuditResult['heuristic_report']>(data.heuristic_report, []),
      analysis_error: data.analysis_error,
      date_creation: data.date_creation,
      date_maj: data.date_maj,
    } : null;

    if (!isPending.value && intervalId) {
      window.clearInterval(intervalId);
      intervalId = null;
    }
  } catch (caughtError) {
    error.value = graphqlErrorMessage(caughtError, 'Impossible de récupérer ce rapport.');
  } finally {
    isLoading.value = false;
  }
};

onMounted(async () => {
  await fetchResult();
  if (reference.value && isPending.value) {
    intervalId = window.setInterval(fetchResult, 3000);
  }
});

onBeforeUnmount(() => {
  if (intervalId) window.clearInterval(intervalId);
});
</script>

<style scoped>
@reference "../../assets/css/main.css";

.RefonteResultPage {
  @apply min-h-screen bg-[#efe8d6] pb-16 text-[#17251d];
}

.RefonteResultHero,
.RefonteResultShell {
  @apply mx-auto w-[min(1120px,calc(100%_-_32px))];
}

.RefonteResultHero {
  @apply grid gap-4 py-14;
}

.RefonteResultKicker {
  @apply text-sm font-black uppercase tracking-wide text-[#2b7053];
}

.RefonteResultTitle {
  @apply max-w-[820px] text-[clamp(2.1rem,5vw,4.4rem)] font-black leading-tight;
}

.RefonteResultIntro,
.RefontePanelText {
  @apply max-w-[780px] text-base font-bold leading-relaxed text-[#435046];
}

.RefonteResultShell,
.RefonteResultPanel,
.RefonteMetricList,
.RefonteCheckList,
.RefonteHeuristicGrid,
.RefontePerformanceGrid {
  @apply grid gap-5;
}

.RefonteResultPanel {
  @apply rounded-lg border border-white/70 bg-[#fbfaf5]/90 p-6 shadow-[0_22px_60px_rgb(23_37_29/0.14)];
}

.RefonteResultGrid,
.RefontePerformanceGrid {
  @apply grid gap-5;
}

.RefontePanelTitle {
  @apply text-2xl font-black;
}

.RefonteStatusPill,
.RefonteCheckState {
  @apply inline-flex w-fit rounded-lg bg-[#2b7053] px-3 py-1 text-xs font-black uppercase tracking-wide text-white;
}

.RefonteMetricList div,
.RefonteCheckList li {
  @apply flex items-center justify-between gap-4 rounded-lg border border-[#2b7053]/12 bg-white p-3 font-bold;
}

.RefonteMetricList dt {
  @apply text-[#435046];
}

.RefonteMetricList dd {
  @apply text-right text-[#17251d];
}

.RefonteCheckList {
  @apply list-none p-0;
}

.RefonteHeuristicCard,
.RefontePerformanceCard {
  @apply grid gap-3 rounded-lg border border-[#2b7053]/12 bg-white p-4;
}

.RefonteHeuristicCard h3,
.RefontePerformanceCard h3 {
  @apply text-lg font-black;
}

.RefonteHeuristicCard p,
.RefontePerformanceCard p {
  @apply font-bold leading-relaxed text-[#435046];
}

@media (min-width: 760px) {
  .RefonteResultGrid,
  .RefontePerformanceGrid {
    @apply grid-cols-2;
  }

  .RefonteHeuristicGrid {
    @apply grid-cols-2;
  }
}
</style>
