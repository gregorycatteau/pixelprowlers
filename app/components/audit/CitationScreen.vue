<template>
  <section class="CitationScreen" aria-labelledby="citation-screen-title">
    <div class="CitationBackdrop" aria-hidden="true"></div>
    <div class="CitationPanel">
      <p class="CitationKicker">Avant que tu ne répondes, prends le temps de lire ceci :</p>
      <blockquote class="CitationBlock">
        <p id="citation-screen-title" class="CitationText">{{ citationText }}</p>
        <footer class="CitationFooter">
          <span class="CitationAuthor">{{ citationAuthor }}</span>
          <span v-if="citationSource" class="CitationSource">{{ citationSource }}</span>
        </footer>
      </blockquote>
      <div class="CitationActions">
        <AppButton variant="validate" size="lg" type="button" @click="$emit('continue')">
          Continuer vers mon audit
        </AppButton>
        <button class="AnotherCitationButton" type="button" :disabled="isLoading" @click="fetchCitation">
          {{ isLoading ? 'Tirage...' : 'Une autre citation' }}
        </button>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import AppButton from '~/components/ui/AppButton.vue';

type Citation = {
  id: number;
  numero?: number;
  texte: string;
  auteur: string;
  source?: string;
};

defineEmits<{
  continue: [];
}>();

const citation = ref<Citation | null>(null);
const isLoading = ref(false);
const citationText = computed(() => citation.value?.texte || "Il n'est jamais trop tard pour remettre de l'ordre dans ce qui compte.");
const citationAuthor = computed(() => citation.value?.auteur || 'PixelProwlers');
const citationSource = computed(() => citation.value?.source || '');

const fetchCitation = async () => {
  if (isLoading.value) {
    return;
  }

  isLoading.value = true;

  try {
    const lastCitationId = window.localStorage.getItem('pixelprowlers:lastCitationId') || '';
    citation.value = await $fetch<Citation>('/api/citations/random', {
      query: lastCitationId ? { exclude_id: lastCitationId } : undefined,
    });

    if (citation.value.id) {
      window.localStorage.setItem('pixelprowlers:lastCitationId', String(citation.value.id));
    }
  } finally {
    isLoading.value = false;
  }
};

onMounted(fetchCitation);
</script>

<style scoped>
@reference "../../assets/css/main.css";

.CitationScreen {
  @apply relative isolate overflow-hidden bg-[#17251d] px-4 py-16 text-white;
}

.CitationBackdrop {
  @apply pointer-events-none absolute inset-0 -z-10 opacity-80;
  background:
    radial-gradient(circle at 18% 18%, rgb(103 192 142 / 0.45), transparent 30%),
    radial-gradient(circle at 78% 22%, rgb(237 193 96 / 0.35), transparent 28%),
    linear-gradient(135deg, #17251d 0%, #244332 48%, #5f4f2d 100%);
  animation: citation-ambient 14s ease-in-out infinite alternate;
}

.CitationBackdrop::after {
  @apply absolute inset-0;
  content: "";
  background-image:
    radial-gradient(circle, rgb(255 255 255 / 0.22) 1px, transparent 1px),
    radial-gradient(circle, rgb(255 255 255 / 0.14) 1px, transparent 1px);
  background-position: 0 0, 18px 22px;
  background-size: 52px 52px, 74px 74px;
  mask-image: linear-gradient(to bottom, transparent, black 20%, black 80%, transparent);
}

.CitationPanel {
  @apply mx-auto grid w-[min(960px,100%)] gap-8 rounded-lg border border-white/20 bg-white/12 p-7 shadow-[0_24px_70px_rgb(0_0_0/0.22)] backdrop-blur-xl;
}

.CitationKicker {
  @apply text-sm font-black uppercase tracking-wide text-[#f3d38a];
  animation: citation-fade-up 0.7s ease both;
}

.CitationBlock {
  @apply relative m-0 grid gap-5 pl-2;
}

.CitationBlock::before {
  @apply absolute -left-2 -top-8 text-[7rem] font-black leading-none text-white/15;
  content: "“";
}

.CitationText {
  @apply max-w-[900px] text-[clamp(2rem,5vw,4.4rem)] font-black leading-[1.04];
  animation: citation-fade-up 0.9s 0.12s ease both;
}

.CitationFooter {
  @apply flex flex-wrap gap-3 text-base font-bold text-white/75;
  animation: citation-fade-up 0.9s 0.22s ease both;
}

.CitationAuthor {
  @apply text-[#f3d38a];
}

.CitationSource::before {
  content: "- ";
}

.CitationActions {
  @apply flex flex-wrap items-center gap-4;
  animation: citation-fade-up 0.9s 0.32s ease both;
}

.AnotherCitationButton {
  @apply rounded-full border border-white/30 bg-white/10 px-5 py-3 text-sm font-black uppercase tracking-wide text-white transition hover:-translate-y-0.5 hover:bg-white/20 disabled:cursor-wait disabled:opacity-60;
}

@keyframes citation-ambient {
  from {
    transform: scale(1);
    filter: saturate(0.95);
  }

  to {
    transform: scale(1.04);
    filter: saturate(1.18);
  }
}

@keyframes citation-fade-up {
  from {
    opacity: 0;
    transform: translateY(18px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (min-width: 760px) {
  .CitationScreen {
    @apply py-24;
  }

  .CitationPanel {
    @apply p-10;
  }
}
</style>
