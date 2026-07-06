<template>
  <section id="audit-refonte-parcours" class="RefonteStepperSection" aria-labelledby="refonte-stepper-title">
    <CitationScreen v-if="!hasStarted" @continue="hasStarted = true" />

    <RefonteIdentificationForm
      v-else-if="!hasIdentity"
      :is-submitting="isSubmitting"
      :error="createError"
      @submit="handleIdentitySubmit"
    />

    <div v-else class="RefonteStepperShell">
      <div class="RefonteStepperHeader">
        <div class="RefonteStepperTitleGroup">
          <p class="RefonteStepperKicker">{{ progressLabel }}</p>
          <h2 id="refonte-stepper-title" class="RefonteStepperTitle">{{ activeSeries.label }}</h2>
        </div>
      </div>

      <progress class="RefonteProgressBar" :value="progressPercent" max="100">{{ progressPercent }}%</progress>

      <form class="RefonteQuestionForm" @submit.prevent="submit">
        <RefonteQuestionField
          v-for="question in activeSeries.questions"
          :key="question.id"
          v-model="answers[question.id]"
          :question="question"
        />

        <div class="RefonteStepperActions">
          <AppButton variant="secondary" type="button" :disabled="currentSeriesIndex === 0" @click="previousSeries">
            Retour
          </AppButton>
          <AppButton v-if="!isLastSeries" variant="validate" type="button" :disabled="!canContinue" @click="nextSeries">
            Continuer
          </AppButton>
          <AppButton v-else variant="validate" type="submit" :disabled="!canSubmit || isSubmitting" :loading="isSubmitting">
            {{ isSubmitting ? 'Analyse lancée...' : "Lancer l'analyse refonte" }}
          </AppButton>
        </div>

        <p v-if="createError" class="RefonteStepperError" role="alert">{{ createError }}</p>
      </form>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import AppButton from '~/components/ui/AppButton.vue';
import CitationScreen from '~/components/audit/CitationScreen.vue';
import RefonteIdentificationForm from '~/components/refonte/RefonteIdentificationForm.vue';
import RefonteQuestionField from '~/components/refonte/RefonteQuestionField.vue';
import { useRefonteAudit } from '~/composables/useRefonteAudit';
import type { RefonteIdentity } from '~/validation/schemas';

const hasStarted = ref(false);

const {
  answers,
  currentSeriesIndex,
  activeSeries,
  isLastSeries,
  progressPercent,
  progressLabel,
  hasIdentity,
  canContinue,
  canSubmit,
  createError,
  isSubmitting,
  setIdentity,
  nextSeries,
  previousSeries,
  submit,
} = useRefonteAudit();

const handleIdentitySubmit = (identity: RefonteIdentity) => {
  setIdentity(identity);
};
</script>

<style scoped>
@reference "../../assets/css/main.css";

.RefonteStepperSection {
  @apply bg-[#efe8d6] py-16;
}

.RefonteStepperShell {
  @apply mx-auto grid w-[min(980px,calc(100%_-_32px))] gap-6;
}

.RefonteStepperHeader {
  @apply flex flex-col gap-4;
}

.RefonteStepperTitleGroup {
  @apply grid gap-2;
}

.RefonteStepperKicker {
  @apply text-sm font-black uppercase tracking-wide text-pxp-green;
}

.RefonteStepperTitle {
  @apply text-[clamp(1.8rem,3vw,2.7rem)] font-black leading-tight text-[#17251d];
}

.RefonteProgressBar {
  @apply h-3 w-full overflow-hidden rounded-full accent-pxp-green;
}

.RefonteQuestionForm {
  @apply grid gap-5;
}

.RefonteStepperActions {
  @apply flex flex-wrap gap-3;
}

.RefonteStepperError {
  @apply rounded-lg border border-[#d93622]/25 bg-[#d93622]/10 p-4 font-bold text-[#7c2418];
}
</style>
