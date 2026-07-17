<template>
  <section
    class="urgency-section"
    aria-labelledby="urgency-form-title"
  >
    <div class="article-container">
      <aside
        class="security-warning"
        aria-labelledby="security-warning-title"
      >
        <strong id="security-warning-title">
          Ne transmettez aucun secret
        </strong>

        <p>
          N’indiquez aucun mot de passe, jeton d’accès, clé privée,
          cookie de session, accès administrateur, sauvegarde ou
          information sensible dans ce formulaire.
        </p>

        <p>
          Si un accès devient nécessaire, son périmètre et son mode de
          transmission seront définis avec vous après la qualification
          de la situation.
        </p>
      </aside>

      <div
        v-if="result"
        class="urgency-success"
        role="status"
        aria-live="polite"
      >
        <p class="eyebrow">
          Demande enregistrée
        </p>

        <h2>
          Référence de dossier&nbsp;: {{ result.reference }}
        </h2>

        <p>
          Votre déclaration a bien été enregistrée. Conservez cette
          référence pour identifier votre demande lors des prochains
          échanges.
        </p>

        <p>
          La situation doit maintenant être qualifiée afin de confirmer
          sa nature, son niveau de priorité et la suite qui peut lui être
          donnée.
        </p>

        <p>
          L’enregistrement ne constitue ni une promesse d’intervention
          immédiate ni un engagement sur un délai de résolution.
          Le périmètre, les délais et les éventuels accès nécessaires
          seront confirmés séparément.
        </p>

        <p>
          Ne transmettez aucun mot de passe, jeton d’accès, clé privée
          ou accès administrateur en dehors du cadre qui vous sera
          expressément indiqué.
        </p>

        <AppButton
          variant="secondary"
          type="button"
          @click="reset"
        >
          Déclarer un autre incident
        </AppButton>
      </div>

      <form
        v-else
        class="urgency-form"
        @submit.prevent="submit"
      >
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
          <legend id="urgency-form-title">
            1. Que se passe-t-il&nbsp;?
          </legend>

          <div class="choice-grid">
            <label
              v-for="option in urgencyProblemOptions"
              :key="option.value"
              class="radio-choice"
            >
              <input
                v-model="form.problemType"
                required
                type="radio"
                name="problemType"
                :value="option.value"
              >

              <span>{{ option.label }}</span>
            </label>
          </div>
        </fieldset>

        <fieldset class="urgency-block">
          <legend>
            2. Quel est l’impact actuel&nbsp;?
          </legend>

          <div class="choice-grid">
            <label
              v-for="option in urgencyImpactOptions"
              :key="option.value"
              class="radio-choice"
            >
              <input
                v-model="form.impactLevel"
                required
                type="radio"
                name="impactLevel"
                :value="option.value"
              >

              <span>{{ option.label }}</span>
            </label>
          </div>
        </fieldset>

        <div class="urgency-block">
          <h2>
            3. Donnez les éléments utiles
          </h2>

          <div class="contact-grid contact-form-grid">
            <label class="text-field full-field">
              <span>Adresse du site ou de la page concernée</span>

              <input
                v-model="form.affectedUrl"
                required
                type="url"
                maxlength="500"
                placeholder="https://votre-site.fr/page-concernee"
                autocomplete="url"
              >
            </label>

            <label class="text-field full-field">
              <span>Description de l’incident</span>

              <small id="urgency-description-help">
                Décrivez uniquement les faits observés et leur impact.
                Ne copiez aucun secret ni contenu sensible.
              </small>

              <textarea
                v-model="form.shortDescription"
                required
                minlength="20"
                maxlength="700"
                rows="5"
                aria-describedby="urgency-description-help"
                placeholder="Exemple : la page d’accueil affiche une erreur depuis ce matin et les visiteurs ne peuvent plus utiliser le formulaire."
              ></textarea>
            </label>

            <label class="text-field full-field">
              <span>Depuis quand observez-vous le problème&nbsp;?</span>

              <input
                v-model="form.sinceWhen"
                required
                type="text"
                maxlength="120"
                placeholder="Exemple : depuis 8 h 30 ce matin ou depuis la mise à jour d’hier soir"
              >
            </label>
          </div>
        </div>

        <div class="urgency-block">
          <h2>
            4. Comment vous recontacter
          </h2>

          <p class="urgency-block-intro">
            Le numéro de téléphone est obligatoire afin de permettre
            la qualification et le suivi de votre demande.
          </p>

          <div class="contact-grid contact-form-grid">
            <label class="text-field">
              <span>Prénom et nom</span>

              <input
                v-model="form.name"
                required
                minlength="2"
                maxlength="120"
                type="text"
                placeholder="Votre prénom et votre nom"
                autocomplete="name"
              >
            </label>

            <label class="text-field">
              <span>Organisation ou statut</span>

              <input
                v-model="form.organization"
                required
                minlength="2"
                maxlength="160"
                type="text"
                placeholder="Association, école, TPE, indépendant ou particulier"
                autocomplete="organization"
              >
            </label>

            <label class="text-field">
              <span>Adresse email</span>

              <input
                v-model="form.email"
                required
                type="email"
                maxlength="254"
                placeholder="vous@exemple.fr"
                autocomplete="email"
              >
            </label>

            <label class="text-field">
              <span>Numéro de téléphone</span>

              <small id="urgency-phone-help">
                Mobile français au format 06, 07 ou +33.
              </small>

              <input
                v-model="form.phone"
                required
                type="tel"
                inputmode="tel"
                maxlength="20"
                placeholder="06 12 34 56 78"
                autocomplete="tel"
                aria-describedby="urgency-phone-help"
              >
            </label>
          </div>
        </div>

        <fieldset class="urgency-block">
          <legend>
            5. Comment souhaitez-vous être recontacté&nbsp;?
          </legend>

          <div class="choice-grid compact">
            <label
              v-for="option in urgencyContactOptions"
              :key="option.value"
              class="radio-choice"
            >
              <input
                v-model="form.contactPreference"
                required
                type="radio"
                name="contactPreference"
                :value="option.value"
              >

              <span>{{ option.label }}</span>
            </label>
          </div>

          <label class="text-field callback-field">
            <span>Créneau pendant lequel vous êtes joignable</span>

            <input
              v-model="form.callbackSlot"
              required
              type="text"
              maxlength="160"
              placeholder="Exemple : aujourd’hui entre 14 h et 17 h ou demain matin"
            >
          </label>
        </fieldset>

        <fieldset class="urgency-block">
          <legend>
            6. Quelle suite souhaitez-vous envisager&nbsp;?
          </legend>

          <p class="urgency-block-intro">
            Cette réponse permet de comprendre votre attente. Elle ne
            constitue ni une commande ni un engagement d’intervention.
          </p>

          <div class="choice-grid">
            <label
              v-for="option in urgencyNextStepOptions"
              :key="option.value"
              class="radio-choice"
            >
              <input
                v-model="form.expected_next_step"
                required
                type="radio"
                name="expected_next_step"
                :value="option.value"
              >

              <span>{{ option.label }}</span>
            </label>
          </div>
        </fieldset>

        <PrivacyNotice
          notice-id="urgency-privacy-notice"
          title="Utilisation de vos données"
          purpose="Enregistrer l’incident déclaré, qualifier son impact, vous recontacter et assurer le suivi de votre demande."
          legal-basis="Mesures précontractuelles prises à votre demande et intérêt légitime de PixelProwlers à organiser, sécuriser et documenter le traitement des incidents signalés."
          recipients="Grégory Catteau / PixelProwlers et, dans la limite nécessaire à leurs services, les prestataires techniques Hostinger et Brevo."
          retention="Douze mois à compter du dernier échange si aucune relation contractuelle n’est engagée. En cas de prestation, les données nécessaires au suivi et aux obligations légales sont conservées pendant les durées applicables."
          required-fields="Tous les champs visibles de ce formulaire sont obligatoires. Sans ces informations, PixelProwlers ne pourra pas qualifier ni suivre la demande."
          show-security-reminder
        />

        <div class="urgency-acknowledgements">
          <label class="check-choice">
            <input
              v-model="form.consentToContact"
              required
              type="checkbox"
              aria-describedby="urgency-privacy-notice"
            >

            <span>
              Je demande à être recontacté par PixelProwlers au sujet
              de cet incident et je confirme avoir pris connaissance
              des informations relatives à mes données.
            </span>
          </label>

          <label class="check-choice">
            <input
              v-model="form.noSecretsConfirmed"
              required
              type="checkbox"
            >

            <span>
              Je confirme ne transmettre aucun mot de passe, jeton
              d’accès, clé privée, accès administrateur, sauvegarde
              ou information sensible.
            </span>
          </label>
        </div>

        <div class="form-actions">
          <AppButton
            variant="validate"
            type="submit"
            :disabled="!canSubmit || isSubmitting"
            :loading="isSubmitting"
          >
            {{
              isSubmitting
                ? 'Enregistrement...'
                : 'Enregistrer et transmettre la demande'
            }}
          </AppButton>
        </div>

        <p
          v-if="submitError"
          class="form-error submit-error"
          role="alert"
          aria-live="assertive"
        >
          {{ submitError }}
        </p>

        <p class="form-note">
          Après l’envoi, une référence de dossier vous est communiquée.
          La qualification humaine, les délais et les conditions
          d’intervention sont confirmés séparément.
        </p>
      </form>
    </div>
  </section>
</template>

<script setup lang="ts">
import PrivacyNotice from '~/components/legal/PrivacyNotice.vue';
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
  @apply bg-pxp-paper py-14 md:py-20;
}

.security-warning {
  @apply mb-7 grid gap-2 rounded-xl border border-pxp-orange/25 bg-pxp-orange/10 p-5 text-pxp-ink;
}

.security-warning strong {
  @apply text-lg font-black;
}

.security-warning p {
  @apply font-semibold leading-relaxed text-pxp-ink/80;
}

.urgency-form {
  @apply rounded-xl border border-pxp-green/15 bg-pxp-panel p-5 shadow-lg md:p-8;
}

.urgency-block {
  @apply mt-8 border-0 p-0;
}

.urgency-block:first-of-type {
  @apply mt-0;
}

.urgency-block legend,
.urgency-block h2 {
  @apply mb-4 mt-0 text-2xl font-black leading-tight text-pxp-ink md:text-3xl;
}

.urgency-block-intro {
  @apply mb-4 max-w-3xl text-base font-semibold leading-relaxed text-pxp-ink/75;
}

.choice-grid,
.urgency-acknowledgements {
  @apply grid gap-3;
}

.callback-field {
  @apply mt-5;
}

.honeypot-field {
  @apply absolute h-px w-px overflow-hidden border-0 p-0 opacity-0;
  left: -10000px;
}

.urgency-success {
  @apply rounded-xl border border-pxp-green/20 bg-pxp-panel p-6 shadow-lg md:p-8;
}

.urgency-success h2 {
  @apply mt-3 text-3xl font-black leading-tight text-pxp-ink md:text-4xl;
}

.urgency-success p:not(.eyebrow) {
  @apply mt-4 max-w-3xl font-semibold leading-relaxed text-pxp-ink/80;
}

.urgency-success .ButtonBase {
  @apply mt-6;
}

.urgency-acknowledgements {
  @apply mt-6;
}

.check-choice {
  @apply flex cursor-pointer items-start gap-3 rounded-lg border border-pxp-green/20 bg-white p-4 font-semibold leading-relaxed text-pxp-ink;
}

.check-choice input {
  @apply mt-1 h-5 w-5 shrink-0 accent-pxp-green;
}

.form-error {
  @apply text-sm font-bold text-pxp-orange;
}

.submit-error {
  @apply rounded-lg border border-pxp-orange/25 bg-pxp-orange/10 p-4;
}

.form-note {
  @apply text-sm font-semibold leading-relaxed text-pxp-ink/70;
}
</style>