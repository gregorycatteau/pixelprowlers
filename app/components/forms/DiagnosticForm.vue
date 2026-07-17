<template>
  <section
    class="diagnostic-form-section"
    aria-label="Pré-diagnostic de votre situation numérique"
  >
    <div class="form-container">
      <div
        class="session-notice"
        role="status"
        aria-live="polite"
      >
        {{ dossierStatus }}
      </div>

      <div
        v-if="!immediateResult"
        class="progress-row"
      >
        <span>
          Étape {{ currentStep + 1 }} sur {{ diagnosticSteps.length }}
        </span>

        <div
          class="progress-track"
          role="progressbar"
          aria-label="Progression du pré-diagnostic"
          aria-valuemin="1"
          :aria-valuemax="diagnosticSteps.length"
          :aria-valuenow="currentStep + 1"
        >
          <span :style="{ width: `${progressPercent}%` }"></span>
        </div>
      </div>

      <form
        v-if="!immediateResult"
        class="diagnostic-form"
        @submit.prevent="nextStep"
      >
        <fieldset>
          <legend id="diagnostic-form-title">
            {{ activeStep.question }}
          </legend>

          <label
            v-for="option in activeStep.options"
            :key="option.value"
            class="radio-choice"
          >
            <input
              v-model="answers[activeStep.id]"
              type="radio"
              :name="activeStep.id"
              :value="option.value"
              required
            >

            <span>{{ option.label }}</span>
          </label>

          <label
            v-if="answers[activeStep.id] === 'other'"
            class="text-field inline-field"
          >
            <span>Précisez votre situation</span>

            <input
              v-model="answers.structureOther"
              type="text"
              required
              minlength="2"
              maxlength="160"
              autocomplete="organization"
              placeholder="Décrivez brièvement votre structure"
            >
          </label>
        </fieldset>

        <div class="form-actions">
          <AppButton
            variant="secondary"
            type="button"
            :disabled="currentStep === 0"
            @click="previousStep"
          >
            Retour
          </AppButton>

          <AppButton
            variant="validate"
            type="submit"
            :disabled="!canContinue"
          >
            {{ isLastStep ? 'Afficher mon pré-diagnostic' : 'Continuer' }}
          </AppButton>
        </div>
      </form>

      <section
        v-else
        class="diagnostic-result-card"
        aria-labelledby="diagnostic-result-title"
      >
        <p class="result-kicker">
          Résultat indicatif du pré-diagnostic
        </p>

        <h2 id="diagnostic-result-title">
          {{ immediateResult.title }}
        </h2>

        <p class="result-disclaimer">
          Ce résultat repose uniquement sur vos réponses. Il ne constitue
          ni un audit technique, ni une garantie de sécurité, ni la
          confirmation d’un incident.
        </p>

        <p class="risk-line">
          Niveau de priorité indicatif :
          <strong>{{ immediateResult.riskLevel }}</strong>
        </p>

        <p class="context-line">
          {{ immediateResult.context }}
        </p>

        <p class="consequence-line">
          {{ immediateResult.consequence }}
        </p>

        <p class="urgency-line">
          {{ immediateResult.urgencyMessage }}
        </p>

        <p class="outcome-line">
          {{ immediateResult.outcomeMessage }}
        </p>

        <p class="recommendation">
          {{ immediateResult.recommendation }}
        </p>

        <p class="next-step-line">
          {{ immediateResult.nextStepReason }}
        </p>

        <ul class="plain-list">
          <li
            v-for="reason in immediateResult.reasons"
            :key="reason"
          >
            {{ reason }}
          </li>
        </ul>

        <div class="result-actions">
          <NuxtLink
            class="ButtonBase ButtonPrimary"
            :to="immediateResult.ctaHref"
          >
            {{ immediateResult.cta }}
          </NuxtLink>

          <NuxtLink
            v-if="immediateResult.ctaHref !== '/rendez-vous'"
            class="ButtonBase ButtonSecondary"
            to="/rendez-vous"
          >
            Demander un rendez-vous
          </NuxtLink>
        </div>

        <p class="cta-note">
          Le périmètre, les délais et les accès éventuellement nécessaires
          sont définis avant toute intervention.
        </p>

        <p class="selection-note">
          {{ immediateResult.selectionMessage }}
        </p>

        <div
          class="safety-block"
          aria-labelledby="diagnostic-safety-title"
        >
          <h3 id="diagnostic-safety-title">
            Un cadre clair avant toute intervention
          </h3>

          <ul class="plain-list good-list">
            <li>Aucun mot de passe n’est demandé dans ce formulaire</li>
            <li>Aucune modification n’est déclenchée par ce résultat</li>
            <li>Tout accès éventuel doit être défini et validé au préalable</li>
          </ul>
        </div>

        <form
          class="diagnostic-contact-form"
          novalidate
          @submit.prevent="submit"
        >
          <div>
            <h3>
              {{
                isSubmitting
                  ? 'Enregistrement de votre demande'
                  : 'Demander une qualification humaine'
              }}
            </h3>

            <p class="form-introduction">
              Laissez vos coordonnées pour transformer ce résultat
              indicatif en demande concrète. Tous les champs sont
              obligatoires.
            </p>

            <p class="phone-alternative">
              Vous préférez appeler directement ?
              <a href="tel:+33668145152">
                06 68 14 51 52
              </a>
            </p>
          </div>

          <div class="contact-grid">
            <label class="text-field">
              <span>Nom ou organisation</span>

              <input
                v-model="contact.name"
                required
                minlength="2"
                maxlength="160"
                type="text"
                autocomplete="organization"
                placeholder="Votre nom ou votre structure"
                :aria-invalid="Boolean(contactErrors.name)"
                :aria-describedby="
                  contactErrors.name
                    ? 'diagnostic-name-error'
                    : undefined
                "
              >

              <span
                v-if="contactErrors.name"
                id="diagnostic-name-error"
                class="form-error"
              >
                {{ contactErrors.name }}
              </span>
            </label>

            <label class="text-field">
              <span>Adresse email</span>

              <input
                v-model="contact.email"
                required
                maxlength="254"
                type="email"
                autocomplete="email"
                placeholder="vous@exemple.fr"
                :aria-invalid="Boolean(contactErrors.email)"
                :aria-describedby="
                  contactErrors.email
                    ? 'diagnostic-email-error'
                    : undefined
                "
              >

              <span
                v-if="contactErrors.email"
                id="diagnostic-email-error"
                class="form-error"
              >
                {{ contactErrors.email }}
              </span>
            </label>

            <label class="text-field">
              <span>Numéro de téléphone</span>

              <small id="diagnostic-phone-help">
                Obligatoire pour qualifier et suivre votre demande.
                Mobile français au format 06, 07 ou +33.
              </small>

              <input
                v-model="contact.phone"
                required
                maxlength="20"
                type="tel"
                inputmode="tel"
                autocomplete="tel"
                placeholder="06 12 34 56 78"
                :aria-invalid="Boolean(contactErrors.phone)"
                aria-describedby="diagnostic-phone-help diagnostic-phone-error"
                @blur="formatPhoneOnBlur"
              >

              <span
                v-if="contactErrors.phone"
                id="diagnostic-phone-error"
                class="form-error"
              >
                {{ contactErrors.phone }}
              </span>
            </label>

            <label class="text-field full-field">
              <span>Contexte utile</span>

              <small id="diagnostic-message-help">
                Décrivez le problème observé et son effet sur votre activité.
                Ne transmettez aucun mot de passe ni donnée sensible.
              </small>

              <textarea
                v-model="contact.message"
                required
                minlength="20"
                maxlength="1000"
                rows="6"
                placeholder="Décrivez brièvement ce que vous souhaitez faire vérifier."
                :aria-invalid="Boolean(contactErrors.message)"
                aria-describedby="diagnostic-message-help diagnostic-message-error"
              ></textarea>

              <span
                v-if="contactErrors.message"
                id="diagnostic-message-error"
                class="form-error"
              >
                {{ contactErrors.message }}
              </span>
            </label>
          </div>

          <PrivacyNotice
            notice-id="diagnostic-privacy-notice"
            title="Utilisation de vos données"
            purpose="Analyser vos réponses, qualifier votre demande, vous recontacter et assurer son suivi."
            legal-basis="Mesures précontractuelles prises à votre demande et intérêt légitime de PixelProwlers à organiser et sécuriser le traitement des demandes reçues."
            recipients="Grégory Catteau / PixelProwlers et, dans la limite nécessaire à leurs services, les prestataires techniques Hostinger et Brevo."
            retention="Douze mois à compter du dernier échange si aucune relation contractuelle n’est engagée. En cas de prestation, les données nécessaires au suivi et aux obligations légales sont conservées pendant les durées applicables."
            required-fields="Tous les champs de ce formulaire sont obligatoires. Sans ces informations, PixelProwlers ne pourra pas qualifier ni suivre la demande."
          />

          <label class="privacy-acknowledgement">
            <input
              v-model="contact.privacyAcknowledged"
              required
              type="checkbox"
              :aria-invalid="
                Boolean(contactErrors.privacyAcknowledged)
              "
              aria-describedby="diagnostic-privacy-notice diagnostic-privacy-error"
            >

            <span>
              Je confirme avoir pris connaissance des informations
              relatives à l’utilisation de mes données.
            </span>
          </label>

          <p
            v-if="contactErrors.privacyAcknowledged"
            id="diagnostic-privacy-error"
            class="form-error"
          >
            {{ contactErrors.privacyAcknowledged }}
          </p>

          <div class="form-actions">
            <AppButton
              variant="secondary"
              type="button"
              :disabled="isSubmitting"
              @click="previousStep"
            >
              Modifier mes réponses
            </AppButton>

            <AppButton
              variant="validate"
              type="submit"
              :disabled="isSubmitting"
              :loading="isSubmitting"
            >
              {{
                isSubmitting
                  ? 'Enregistrement...'
                  : 'Envoyer ma demande'
              }}
            </AppButton>
          </div>
        </form>

        <p
          v-if="submitError"
          class="form-error submit-error"
          role="alert"
          aria-live="assertive"
        >
          {{ submitError }}
        </p>

        <p class="form-note">
          Aucun mot de passe, accès privé ou fichier sensible ne doit être
          transmis dans ce formulaire.
        </p>
      </section>
    </div>
  </section>
</template>

<script setup lang="ts">
import PrivacyNotice from '~/components/legal/PrivacyNotice.vue';
import AppButton from '~/components/ui/AppButton.vue';

import {
  diagnosticSteps,
  useDiagnostic,
} from '~/composables/useDiagnostic';

const {
  currentStep,
  answers,
  contact,
  contactErrors,
  immediateResult,
  dossierStatus,
  activeStep,
  isLastStep,
  progressPercent,
  isSubmitting,
  submitError,
  canContinue,
  formatPhoneOnBlur,
  nextStep,
  previousStep,
  submit,
} = useDiagnostic();
</script>

<style scoped>
@reference "../../assets/css/main.css";

.diagnostic-form-section {
  @apply bg-pxp-paper py-12 md:py-20;
}

.progress-row {
  @apply grid gap-2 text-sm font-extrabold text-pxp-green;
}

.progress-track {
  @apply h-2.5 overflow-hidden rounded-full bg-pxp-green/15;
}

.progress-track span {
  @apply block h-full rounded-full bg-pxp-green;
  transition: width 180ms ease;
}

.diagnostic-form {
  @apply mt-7;
}

.session-notice {
  @apply mb-5 rounded-lg border border-pxp-green/20 bg-pxp-green/10 px-4 py-3 font-extrabold text-pxp-green;
}

fieldset {
  @apply m-0 border-0 p-0;
}

legend {
  @apply mb-5 text-2xl font-black leading-tight text-pxp-ink md:text-3xl;
}

.inline-field {
  @apply mt-4;
}

.diagnostic-result-card {
  @apply mt-7 grid gap-4 rounded-xl border border-pxp-green/15 bg-pxp-panel p-6 shadow-lg md:p-9;
}

.diagnostic-result-card h2 {
  @apply text-3xl font-black leading-tight text-pxp-ink md:text-4xl;
}

.result-kicker {
  @apply text-xs font-black uppercase tracking-widest text-pxp-green;
}

.result-disclaimer {
  @apply rounded-lg border border-pxp-green/20 bg-white p-4 text-sm font-semibold leading-relaxed text-pxp-ink;
}

.risk-line,
.context-line,
.consequence-line,
.urgency-line,
.outcome-line,
.recommendation,
.next-step-line {
  @apply text-base font-semibold leading-relaxed text-pxp-ink md:text-lg;
}

.context-line {
  @apply font-extrabold;
}

.consequence-line {
  @apply border-l-4 border-pxp-orange bg-pxp-orange/10 px-4 py-3;
}

.urgency-line {
  @apply rounded-lg border border-pxp-orange/25 bg-pxp-orange/10 px-4 py-3 font-black text-pxp-ink;
}

.outcome-line {
  @apply border-l-4 border-pxp-green bg-pxp-green/10 px-4 py-3 font-black text-pxp-ink;
}

.next-step-line {
  @apply font-extrabold text-pxp-green;
}

.risk-line strong {
  @apply uppercase;
}

.result-actions {
  @apply flex flex-wrap gap-3;
}

.cta-note,
.selection-note,
.form-introduction,
.phone-alternative,
.form-note {
  @apply text-sm font-semibold leading-relaxed text-pxp-ink/75;
}

.selection-note {
  @apply text-pxp-green;
}

.phone-alternative {
  @apply mt-2;
}

.phone-alternative a {
  @apply font-black text-pxp-green underline decoration-2 underline-offset-4;
}

.safety-block {
  @apply rounded-lg border border-pxp-green/20 bg-white p-5;
}

.safety-block h3 {
  @apply text-lg font-black text-pxp-ink;
}

.diagnostic-contact-form {
  @apply mt-4 grid gap-5 border-t border-pxp-green/15 pt-6;
}

.diagnostic-contact-form h3 {
  @apply text-2xl font-black text-pxp-ink;
}

.privacy-acknowledgement {
  @apply flex cursor-pointer items-start gap-3 rounded-lg border border-pxp-green/20 bg-white p-4 font-semibold leading-relaxed text-pxp-ink;
}

.privacy-acknowledgement input {
  @apply mt-1 h-5 w-5 shrink-0 accent-pxp-green;
}

.form-error {
  @apply text-sm font-bold text-pxp-orange;
}

.submit-error {
  @apply rounded-lg border border-pxp-orange/25 bg-pxp-orange/10 p-4;
}
</style>