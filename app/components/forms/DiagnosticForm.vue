<template>
  <section class="diagnostic-form-section" aria-labelledby="diagnostic-form-title">
    <div class="form-container">
      <div class="progress-row" aria-live="polite">
        <span>Étape {{ currentStep + 1 }} de {{ diagnosticSteps.length }}</span>
        <div class="progress-track" aria-hidden="true">
          <span :style="{ width: `${progressPercent}%` }"></span>
        </div>
      </div>

      <form class="diagnostic-form" @submit.prevent="submit">
        <fieldset v-if="activeStep?.type === 'radio'">
          <legend id="diagnostic-form-title">{{ activeStep.question }}</legend>
          <label v-for="option in activeStep.options" :key="option.value" class="radio-choice">
            <input v-model="answers[activeStep.id]" type="radio" :name="activeStep.id" :value="option.value">
            <span>{{ option.label }}</span>
          </label>
          <label v-if="answers[activeStep.id] === 'other'" class="text-field inline-field">
            <span>Précisez</span>
            <input v-model="answers.structureOther" type="text" autocomplete="organization">
          </label>
        </fieldset>

        <fieldset v-else>
          <legend id="diagnostic-form-title">{{ activeStep?.question }}</legend>
          <div class="contact-grid">
            <label class="text-field">
              <span>Prénom / Organisation</span>
              <input v-model="contact.name" required type="text" autocomplete="organization">
            </label>
            <label class="text-field">
              <span>Email</span>
              <input v-model="contact.email" required type="email" autocomplete="email">
            </label>
            <label class="text-field">
              <span>Téléphone <small>(optionnel)</small></span>
              <input v-model="contact.phone" type="tel" autocomplete="tel">
            </label>
            <label class="text-field full-field">
              <span>Problématique / Contexte</span>
              <textarea
                v-model="contact.message"
                required
                maxlength="240"
                rows="5"
                placeholder="Expliquez en quelques lignes ce qui vous inquiète ou ce que vous voulez vérifier."
              ></textarea>
            </label>
          </div>
        </fieldset>

        <div class="form-actions">
          <AppButton variant="secondary" type="button" :disabled="currentStep === 0" @click="previousStep">
            Retour
          </AppButton>
          <AppButton v-if="!isLastStep" variant="validate" type="button" :disabled="!canContinue" @click="nextStep">
            Continuer
          </AppButton>
          <AppButton v-else variant="validate" type="submit" :disabled="!canSubmit || isSubmitting" :loading="isSubmitting">
            {{ isSubmitting ? 'Analyse en cours...' : 'Voir par où commencer' }}
          </AppButton>
        </div>

        <p v-if="submitError" class="form-error">{{ submitError }}</p>
        <p class="form-note">
          On ne vous demande pas de mot de passe, pas d'accès privé, pas de fichier sensible.
        </p>
      </form>
    </div>
  </section>
</template>

<script setup lang="ts">
import AppButton from '~/components/ui/AppButton.vue';
import { diagnosticSteps, useDiagnostic } from '~/composables/useDiagnostic';

const {
  currentStep,
  answers,
  contact,
  activeStep,
  isLastStep,
  progressPercent,
  isSubmitting,
  submitError,
  canContinue,
  canSubmit,
  nextStep,
  previousStep,
  submit,
} = useDiagnostic();
</script>

<style scoped>
.diagnostic-form-section {
  padding: 48px 0 84px;
  background: #f7f4ea;
}

.progress-row {
  display: grid;
  gap: 10px;
  color: #2b4b39;
  font-size: 0.92rem;
  font-weight: 850;
}

.progress-track {
  height: 10px;
  overflow: hidden;
  border-radius: 999px;
  background: rgba(43, 112, 83, 0.14);
}

.progress-track span {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: #2b7053;
  transition: width 180ms ease;
}

.diagnostic-form {
  margin-top: 26px;
}

fieldset {
  margin: 0;
  padding: 0;
  border: 0;
}

legend {
  margin-bottom: 18px;
  color: #17251d;
  font-size: clamp(1.45rem, 3vw, 2.2rem);
  font-weight: 900;
  line-height: 1.1;
}

.inline-field {
  margin-top: 16px;
}
</style>
