<template>
  <section id="audit-parcours" class="AuditStepperSection" aria-labelledby="audit-stepper-title">
    <CitationScreen v-if="!hasStarted" @continue="hasStarted = true" />
    <AuditIdentificationForm
      v-else-if="!hasDossier"
      :is-submitting="isCreatingDossier"
      :error="createError"
      @submit="handleIdentitySubmit"
    />

    <div v-else-if="showDossierConfirmation" class="DossierConfirmation" role="status" aria-live="polite">
      <span class="ConfirmationCheck" aria-hidden="true"></span>
      <p class="ConfirmationKicker">Dossier créé</p>
      <p class="ConfirmationText">Le questionnaire arrive.</p>
    </div>

    <div v-else class="AuditStepperShell">
      <div class="AuditStepperHeader">
        <div class="AuditStepperTitleGroup">
          <p class="AuditStepperKicker">{{ progressLabel }}</p>
          <h2 id="audit-stepper-title" class="AuditStepperTitle">{{ activeSeries?.label }}</h2>
        </div>
        <AuditDossierBadge :numero-dossier="numeroDossier" />
      </div>

      <progress class="ProgressBar" :value="progressPercent" max="100">{{ progressPercent }}%</progress>

      <AuditResultSummary v-if="result" :result="result" />

      <form v-else class="QuestionForm" @submit.prevent="submitResponses">
        <AuditQuestionSlider
          v-for="question in activeSeries?.questions"
          :key="question.id"
          v-model="answers[question.id]"
          :question="question"
        />

        <div class="StepperActions">
          <AppButton variant="secondary" type="button" :disabled="currentSeriesIndex === 0" @click="previousSeries">
            Retour
          </AppButton>
          <AppButton v-if="!isLastSeries" variant="validate" type="button" @click="nextSeries">
            Continuer
          </AppButton>
          <AppButton v-else variant="validate" type="submit" :disabled="isSubmittingResponses" :loading="isSubmittingResponses">
            {{ isSubmittingResponses ? 'Transmission...' : 'Voir le résultat' }}
          </AppButton>
        </div>

        <p v-if="submitError" class="StepperError" role="alert">{{ submitError }}</p>
      </form>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import AppButton from '~/components/ui/AppButton.vue';
import AuditDossierBadge from '~/components/audit/AuditDossierBadge.vue';
import AuditIdentificationForm from '~/components/audit/AuditIdentificationForm.vue';
import AuditQuestionSlider from '~/components/audit/AuditQuestionSlider.vue';
import AuditResultSummary from '~/components/audit/AuditResultSummary.vue';
import CitationScreen from '~/components/audit/CitationScreen.vue';
import { useAudit } from '~/composables/useAudit';
import type { AuditIdentity } from '~/validation/schemas';

const hasStarted = ref(false);
const showDossierConfirmation = ref(false);

const {
  answers,
  numeroDossier,
  currentSeriesIndex,
  result,
  createError,
  submitError,
  isCreatingDossier,
  isSubmittingResponses,
  activeSeries,
  hasDossier,
  isLastSeries,
  progressLabel,
  progressPercent,
  createDossier,
  previousSeries,
  nextSeries,
  submitResponses,
} = useAudit();

const handleIdentitySubmit = async (identity: AuditIdentity) => {
  await createDossier(identity);

  if (!numeroDossier.value) {
    return;
  }

  showDossierConfirmation.value = true;
  window.setTimeout(() => {
    showDossierConfirmation.value = false;
  }, 950);
};
</script>

<style scoped>
@reference "../../assets/css/main.css";

.AuditStepperSection {
  @apply bg-[#efe8d6] py-16;
}

.AuditStepperShell {
  @apply mx-auto grid w-[min(980px,calc(100%_-_32px))] gap-6;
}

.AuditStepperHeader {
  @apply flex flex-col gap-4;
}

.AuditStepperTitleGroup {
  @apply grid gap-2;
}

.AuditStepperKicker {
  @apply text-sm font-black uppercase tracking-wide text-[#2b7053];
}

.AuditStepperTitle {
  @apply text-[clamp(1.8rem,3vw,2.7rem)] font-black leading-tight text-[#17251d];
}

.ProgressBar {
  @apply h-3 w-full overflow-hidden rounded-full accent-[#2b7053];
}

.QuestionForm {
  @apply grid gap-5;
}

.StepperActions {
  @apply flex flex-wrap gap-3;
}

.StepperError {
  @apply rounded-lg border border-[#d93622]/25 bg-[#d93622]/10 p-4 font-bold text-[#7c2418];
}

.DossierConfirmation {
  @apply mx-auto grid min-h-[280px] w-[min(680px,calc(100%_-_32px))] place-items-center gap-3 rounded-lg border border-[#2b7053]/15 bg-[#fbfaf5]/90 p-8 text-center shadow-[0_22px_60px_rgb(23_37_29/0.14)];
}

.ConfirmationCheck {
  @apply grid h-16 w-16 place-items-center rounded-full bg-[#2b7053] text-3xl font-black text-white shadow-[0_18px_35px_rgb(43_112_83/0.28)];
  animation: confirmation-pop 0.48s ease both;
}

.ConfirmationCheck::before {
  content: "✓";
}

.ConfirmationKicker {
  @apply text-sm font-black uppercase tracking-wide text-[#2b7053];
}

.ConfirmationText {
  @apply text-2xl font-black text-[#17251d];
}

@keyframes confirmation-pop {
  0% {
    opacity: 0;
    transform: scale(0.72);
  }

  70% {
    transform: scale(1.08);
  }

  100% {
    opacity: 1;
    transform: scale(1);
  }
}

@media (min-width: 760px) {
  .AuditStepperHeader {
    @apply flex-row items-center justify-between;
  }
}
</style>
