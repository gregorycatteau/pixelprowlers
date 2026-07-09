<template>
  <section class="urgency-section" aria-labelledby="urgency-form-title">
    <div class="article-container">
      <div class="security-warning" role="alert">
        <strong>Ne transmettez aucun secret.</strong>
        <span>
          Pas de mot de passe, token, clé privée, accès administrateur, cookie, sauvegarde ou information sensible.
          Si un accès devient nécessaire, on utilisera un canal adapté après qualification.
        </span>
      </div>

      <div v-if="result" class="urgency-success" role="status" aria-live="polite">
        <p class="eyebrow">Votre demande est prise en charge</p>
        <h2>Référence : {{ result.reference }}</h2>
        <p>Vous êtes en train de sécuriser votre situation. Un expert va analyser votre situation.</p>
        <p>Réponse sous 24h selon le niveau d’impact et le créneau indiqué. Conservez cette référence de dossier pour le suivi.</p>
        <p>
          Ne transmettez aucun mot de passe, token, clé privée ou accès administrateur. Les modalités
          d’intervention seront vues après un premier échange humain.
        </p>
        <AppButton variant="secondary" type="button" @click="reset">Déclarer une autre urgence</AppButton>
      </div>

      <form v-else class="urgency-form" @submit.prevent="submit">
        <input
          v-model="form.website"
          class="honeypot-field"
          type="text"
          name="website"
          tabindex="-1"
          autocomplete="off"
          aria-hidden="true"
        >

        <fieldset class="urgency-block">
          <legend id="urgency-form-title">1. Ce qui se passe</legend>
          <div class="choice-grid">
            <label v-for="option in urgencyProblemOptions" :key="option.value" class="radio-choice">
              <input v-model="form.problemType" required type="radio" name="problemType" :value="option.value">
              <span>{{ option.label }}</span>
            </label>
          </div>
        </fieldset>

        <fieldset class="urgency-block">
          <legend>2. Impact maintenant</legend>
          <div class="choice-grid">
            <label v-for="option in urgencyImpactOptions" :key="option.value" class="radio-choice">
              <input v-model="form.impactLevel" required type="radio" name="impactLevel" :value="option.value">
              <span>{{ option.label }}</span>
            </label>
          </div>
        </fieldset>

        <div class="urgency-block">
          <h2>3. Contexte rapide</h2>
          <div class="contact-grid contact-form-grid">
            <label class="text-field full-field">
              <span>URL concernée</span>
              <input
                v-model="form.affectedUrl"
                required
                type="url"
                maxlength="240"
                placeholder="https://pixelprowlers.io/page-qui-pose-probleme"
                autocomplete="url"
              >
            </label>
            <label class="text-field full-field">
              <span>Description courte</span>
              <textarea
                v-model="form.shortDescription"
                required
                maxlength="700"
                rows="5"
                placeholder="Exemple : la page d’accueil affiche une erreur 500 depuis ce matin, les visiteurs ne peuvent plus accéder au formulaire."
              ></textarea>
            </label>
            <label class="text-field full-field">
              <span>Depuis quand ?</span>
              <input
                v-model="form.sinceWhen"
                required
                type="text"
                maxlength="120"
                placeholder="Exemple : depuis 8h30 ce matin, ou depuis la mise à jour d’hier soir"
              >
            </label>
          </div>
        </div>

        <div class="urgency-block">
          <h2>4. Comment vous recontacter</h2>
          <div class="contact-grid contact-form-grid">
            <label class="text-field">
              <span>Nom</span>
              <input v-model="form.name" required type="text" maxlength="120" placeholder="Votre prénom et nom" autocomplete="name">
            </label>
            <label class="text-field">
              <span>Structure</span>
              <input v-model="form.organization" required type="text" maxlength="160" placeholder="Association, école, TPE, indépendant..." autocomplete="organization">
            </label>
            <label class="text-field">
              <span>Email</span>
              <input v-model="form.email" required type="email" maxlength="180" placeholder="vous@exemple.fr" autocomplete="email">
            </label>
            <label class="text-field">
              <span>Téléphone</span>
              <input v-model="form.phone" required type="tel" maxlength="40" placeholder="+33 6 12 34 56 78" autocomplete="tel">
            </label>
          </div>
        </div>

        <fieldset class="urgency-block">
          <legend>5. Préférence de rappel</legend>
          <div class="choice-grid compact">
            <label v-for="option in urgencyContactOptions" :key="option.value" class="radio-choice">
              <input v-model="form.contactPreference" required type="radio" name="contactPreference" :value="option.value">
              <span>{{ option.label }}</span>
            </label>
          </div>
          <label class="text-field callback-field">
            <span>Créneau de rappel</span>
            <input
              v-model="form.callbackSlot"
              required
              type="text"
              maxlength="160"
              placeholder="Exemple : aujourd’hui 14h-17h, ou demain matin"
            >
          </label>
        </fieldset>

        <fieldset class="urgency-block">
          <legend>6. Prochaine étape souhaitée</legend>
          <p class="urgency-block-intro">
            Ici, pas besoin d’estimer quoi que ce soit. L’objectif est d’abord de comprendre la situation,
            vérifier le niveau d’urgence et voir ensemble la meilleure suite à donner. Les modalités
            d’intervention seront abordées après un premier échange humain.
          </p>
          <div class="choice-grid">
            <label v-for="option in urgencyNextStepOptions" :key="option.value" class="radio-choice">
              <input v-model="form.expected_next_step" required type="radio" name="expected_next_step" :value="option.value">
              <span>{{ option.label }}</span>
            </label>
          </div>
        </fieldset>

        <div class="urgency-consents">
          <label class="check-choice">
            <input v-model="form.consentToContact" required type="checkbox">
            <span>J’accepte d’être recontacté par PixelProwlers à propos de cette urgence.</span>
          </label>
          <label class="check-choice">
            <input v-model="form.noSecretsConfirmed" required type="checkbox">
            <span>Je confirme ne transmettre aucun mot de passe, token, clé privée, accès administrateur ou information sensible.</span>
          </label>
        </div>

        <div class="form-actions">
          <AppButton variant="validate" type="submit" :disabled="!canSubmit || isSubmitting" :loading="isSubmitting">
            {{ isSubmitting ? 'Transmission...' : 'Prévenir PixelProwlers maintenant' }}
          </AppButton>
        </div>

        <p v-if="submitError" class="form-error" role="alert">{{ submitError }}</p>
        <p class="form-note">
          La prise en compte est immédiate. La réponse humaine dépend du niveau d’impact et du créneau indiqué.
        </p>
      </form>
    </div>
  </section>
</template>

<script setup lang="ts">
import AppButton from '~/components/ui/AppButton.vue';
import {
  urgencyContactOptions,
  urgencyImpactOptions,
  urgencyNextStepOptions,
  urgencyProblemOptions,
  useUrgency,
} from '~/composables/useUrgency';

const {
  form,
  result,
  submitError,
  isSubmitting,
  canSubmit,
  reset,
  submit,
} = useUrgency();
</script>

<style scoped>
@reference "../../assets/css/main.css";

.urgency-section {
  @apply bg-[#f7f4ea] py-14;
}

.security-warning {
  @apply mb-7 grid gap-2 rounded-lg border border-[#d93622]/25 bg-[#d93622]/10 p-4 text-[#7c2418];
}

.security-warning strong {
  @apply text-base font-black;
}

.urgency-block {
  @apply mt-7 border-0 p-0;
}

.urgency-block:first-of-type {
  @apply mt-0;
}

.urgency-block legend,
.urgency-block h2 {
  @apply mb-4 mt-0 text-[clamp(1.35rem,2.8vw,2rem)] font-black leading-tight text-[#17251d];
}

.urgency-block-intro {
  @apply mb-4 max-w-[720px] text-[1rem] font-bold leading-relaxed text-[#435046];
}

.choice-grid,
.urgency-consents {
  @apply grid gap-3;
}

.callback-field {
  @apply mt-5;
}

.honeypot-field {
  @apply absolute h-px w-px overflow-hidden border-0 p-0 opacity-0;
  left: -10000px;
}

.urgency-success h2 {
  @apply mt-3 text-[clamp(1.85rem,4vw,3rem)] leading-tight;
}

.urgency-success p:not(.eyebrow) {
  @apply mt-4 max-w-[720px] text-[1.05rem] leading-relaxed text-[#27322a];
}
</style>
