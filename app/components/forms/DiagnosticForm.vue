<template>
  <section class="diagnostic-form-section" aria-labelledby="diagnostic-form-title">
    <div class="form-container">
      <div class="session-notice" role="status">
        {{ dossierStatus }}
      </div>

      <div v-if="!immediateResult" class="progress-row" aria-live="polite">
        <span>Étape {{ currentStep + 1 }} de {{ diagnosticSteps.length }}</span>
        <div class="progress-track" aria-hidden="true">
          <span :style="{ width: `${progressPercent}%` }"></span>
        </div>
      </div>

      <form v-if="!immediateResult" class="diagnostic-form" @submit.prevent="nextStep">
        <fieldset>
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

        <div class="form-actions">
          <AppButton variant="secondary" type="button" :disabled="currentStep === 0" @click="previousStep">
            Retour
          </AppButton>
          <AppButton variant="validate" type="submit" :disabled="!canContinue">
            {{ isLastStep ? 'Obtenir un diagnostic clair' : 'Continuer' }}
          </AppButton>
        </div>
      </form>

      <div v-else class="diagnostic-result-card" role="status" aria-live="polite">
        <p class="result-kicker">Résultat immédiat</p>
        <h2>{{ immediateResult.title }}</h2>
        <p class="risk-line">Niveau de risque : <strong>{{ immediateResult.riskLevel }}</strong></p>
        <p class="context-line">{{ immediateResult.context }}</p>
        <p class="consequence-line">{{ immediateResult.consequence }}</p>
        <p class="urgency-line">{{ immediateResult.urgencyMessage }}</p>
        <p class="outcome-line">{{ immediateResult.outcomeMessage }}</p>
        <p class="recommendation">{{ immediateResult.recommendation }}</p>
        <p class="next-step-line">{{ immediateResult.nextStepReason }}</p>
        <ul class="plain-list">
          <li v-for="reason in immediateResult.reasons" :key="reason">{{ reason }}</li>
        </ul>

        <div class="result-actions">
          <NuxtLink class="ButtonBase ButtonPrimary" :to="immediateResult.ctaHref">
            {{ immediateResult.cta }}
          </NuxtLink>
          <NuxtLink class="ButtonBase ButtonSecondary" to="/rendez-vous">
            Être accompagné sur mon problème
          </NuxtLink>
        </div>
        <p class="cta-note">Réponse sous 24h. Sans engagement. Pas d’accès demandé sans validation.</p>
        <p class="selection-note">{{ immediateResult.selectionMessage }}</p>

        <div class="safety-block" aria-labelledby="diagnostic-safety-title">
          <h3 id="diagnostic-safety-title">Vos données restent cadrées</h3>
          <ul class="plain-list good-list">
            <li>Vous ne partagez jamais vos accès sans cadre clair</li>
            <li>Confidentialité stricte</li>
            <li>Aucune modification sans votre accord</li>
          </ul>
        </div>

        <form class="diagnostic-contact-form" @submit.prevent="submit">
          <h3>{{ isSubmitting ? 'Votre demande est prise en charge' : 'Recevoir le détail par email' }}</h3>
          <p v-if="isSubmitting" class="handoff-line">
            Vous êtes en train de sécuriser votre situation. Première étape vers la reprise de contrôle.
          </p>
          <div class="contact-grid">
            <label class="text-field">
              <span>Nom ou organisation</span>
              <input v-model="contact.name" required type="text" autocomplete="organization" placeholder="Votre nom ou structure">
            </label>
            <label class="text-field">
              <span>Email</span>
              <input v-model="contact.email" required type="email" autocomplete="email" placeholder="vous@exemple.fr">
            </label>
            <label class="text-field">
              <span>Téléphone <small>(optionnel)</small></span>
              <input v-model="contact.phone" type="tel" autocomplete="tel" placeholder="+33 6 12 34 56 78">
            </label>
            <label class="text-field full-field">
              <span>Contexte utile</span>
              <textarea
                v-model="contact.message"
                required
                maxlength="240"
                rows="5"
                placeholder="Décrivez brièvement ce que vous voulez vérifier."
              ></textarea>
            </label>
          </div>
          <div class="form-actions">
            <AppButton variant="secondary" type="button" @click="previousStep">
              Modifier mes réponses
            </AppButton>
            <AppButton variant="validate" type="submit" :disabled="!canSubmit || isSubmitting" :loading="isSubmitting">
              {{ isSubmitting ? 'Clarification en cours...' : 'Obtenir mon diagnostic clair' }}
            </AppButton>
          </div>
        </form>
        <p v-if="submitError" class="form-error">{{ submitError }}</p>
        <p class="form-note">
          On ne vous demande pas de mot de passe, pas d'accès privé, pas de fichier sensible.
        </p>
      </div>
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
  immediateResult,
  dossierStatus,
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

.session-notice {
  margin-bottom: 18px;
  border: 1px solid rgba(43, 112, 83, 0.18);
  border-radius: 8px;
  background: rgba(43, 112, 83, 0.08);
  padding: 12px 14px;
  color: #2b4b39;
  font-weight: 850;
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

.diagnostic-result-card {
  display: grid;
  gap: 16px;
  margin-top: 26px;
  border: 1px solid rgba(43, 112, 83, 0.14);
  border-radius: 8px;
  background: #fbfaf5;
  padding: clamp(22px, 4vw, 34px);
  box-shadow: 0 14px 38px rgba(23, 37, 29, 0.06);
}

.diagnostic-result-card h2 {
  color: #17251d;
  font-size: clamp(1.8rem, 4vw, 3rem);
  font-weight: 900;
  line-height: 1.05;
}

.result-kicker {
  color: #2b7053;
  font-size: 0.78rem;
  font-weight: 900;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.risk-line,
.context-line,
.consequence-line,
.urgency-line,
.outcome-line,
.recommendation,
.next-step-line {
  color: #27322a;
  font-size: 1.05rem;
  font-weight: 760;
  line-height: 1.55;
}

.context-line {
  color: #17251d;
  font-weight: 850;
}

.consequence-line {
  border-left: 4px solid #e95f24;
  background: rgba(233, 95, 36, 0.08);
  padding: 12px 14px;
}

.urgency-line {
  border: 1px solid rgba(233, 95, 36, 0.2);
  border-radius: 8px;
  background: rgba(233, 95, 36, 0.07);
  padding: 12px 14px;
  color: #7c3a18;
  font-weight: 900;
}

.outcome-line {
  border-left: 4px solid #2b7053;
  background: rgba(43, 112, 83, 0.08);
  padding: 12px 14px;
  color: #173f2e;
  font-weight: 900;
}

.next-step-line {
  color: #2b4b39;
  font-weight: 850;
}

.risk-line strong {
  text-transform: uppercase;
}

.diagnostic-contact-form {
  display: grid;
  gap: 18px;
  margin-top: 16px;
  border-top: 1px solid rgba(43, 112, 83, 0.14);
  padding-top: 22px;
}

.diagnostic-contact-form h3 {
  color: #17251d;
  font-size: 1.35rem;
  font-weight: 900;
}

.cta-note,
.selection-note,
.handoff-line {
  color: #596158;
  font-size: 0.96rem;
  font-weight: 800;
  line-height: 1.55;
}

.selection-note {
  color: #2b4b39;
}

.safety-block {
  border: 1px solid rgba(43, 112, 83, 0.14);
  border-radius: 8px;
  background: white;
  padding: 18px;
}

.safety-block h3 {
  color: #17251d;
  font-size: 1.15rem;
  font-weight: 900;
}
</style>
