<template>
  <form
    class="contact-form"
    aria-labelledby="contact-form-title"
    novalidate
    @submit.prevent="handleSubmit"
  >
    <fieldset>
      <legend id="contact-form-title">Votre demande</legend>

      <label
        v-for="option in contactDemandOptions"
        :key="option.value"
        class="radio-choice"
      >
        <input
          v-model="form.demandType"
          type="radio"
          name="demandType"
          :value="option.value"
          :aria-invalid="Boolean(errors.demandType)"
          :aria-describedby="errors.demandType ? 'demand-type-error' : undefined"
        >
        <span>{{ option.label }}</span>
      </label>

      <p
        v-if="errors.demandType"
        id="demand-type-error"
        class="form-error"
        role="alert"
      >
        {{ errors.demandType }}
      </p>
    </fieldset>

    <div class="contact-grid contact-form-grid">
      <label class="text-field">
        <span>Votre prénom</span>
        <input
          v-model="form.prenom"
          required
          maxlength="100"
          type="text"
          autocomplete="given-name"
          :aria-invalid="Boolean(errors.prenom)"
          :aria-describedby="errors.prenom ? 'prenom-error' : undefined"
        >
        <span
          v-if="errors.prenom"
          id="prenom-error"
          class="form-error"
          role="alert"
        >
          {{ errors.prenom }}
        </span>
      </label>

      <label class="text-field">
        <span>Votre nom</span>
        <input
          v-model="form.nom"
          required
          maxlength="100"
          type="text"
          autocomplete="family-name"
          :aria-invalid="Boolean(errors.nom)"
          :aria-describedby="errors.nom ? 'nom-error' : undefined"
        >
        <span
          v-if="errors.nom"
          id="nom-error"
          class="form-error"
          role="alert"
        >
          {{ errors.nom }}
        </span>
      </label>

      <label class="text-field">
        <span>Organisation ou statut</span>
        <small>
          Indiquez le nom de votre organisation ou « Particulier » si vous
          intervenez à titre personnel.
        </small>
        <input
          v-model="form.organization"
          required
          maxlength="180"
          type="text"
          autocomplete="organization"
          placeholder="Nom de l’organisation ou Particulier"
          :aria-invalid="Boolean(errors.organization)"
          :aria-describedby="
            errors.organization
              ? 'organization-help organization-error'
              : 'organization-help'
          "
        >
        <small id="organization-help">
          Cette information permet d’identifier correctement votre demande.
        </small>
        <span
          v-if="errors.organization"
          id="organization-error"
          class="form-error"
          role="alert"
        >
          {{ errors.organization }}
        </span>
      </label>

      <label class="text-field">
        <span>Votre adresse email</span>
        <input
          v-model="form.email"
          required
          maxlength="254"
          type="email"
          autocomplete="email"
          placeholder="vous@exemple.fr"
          :aria-invalid="Boolean(errors.email)"
          :aria-describedby="errors.email ? 'email-error' : undefined"
        >
        <span
          v-if="errors.email"
          id="email-error"
          class="form-error"
          role="alert"
        >
          {{ errors.email }}
        </span>
      </label>

      <label class="text-field">
        <span>Votre numéro de téléphone</span>
        <small>
          Obligatoire afin que nous puissions vous rappeler au sujet de cette
          demande.
        </small>
        <input
          v-model="form.phone"
          required
          maxlength="30"
          type="tel"
          inputmode="tel"
          autocomplete="tel"
          placeholder="06 12 34 56 78"
          :aria-invalid="Boolean(errors.phone)"
          :aria-describedby="
            errors.phone
              ? 'phone-help phone-error'
              : 'phone-help'
          "
          @blur="formatPhoneOnBlur"
        >
        <small id="phone-help">
          Numéro de mobile français au format 06, 07 ou +33.
        </small>
        <span
          v-if="errors.phone"
          id="phone-error"
          class="form-error"
          role="alert"
        >
          {{ errors.phone }}
        </span>
      </label>

      <label class="text-field full-field">
        <span>Objet</span>
        <input
          v-model="form.objet"
          required
          maxlength="200"
          type="text"
          placeholder="Objet de votre demande"
          :aria-invalid="Boolean(errors.objet)"
          :aria-describedby="errors.objet ? 'objet-error' : undefined"
        >
        <span
          v-if="errors.objet"
          id="objet-error"
          class="form-error"
          role="alert"
        >
          {{ errors.objet }}
        </span>
      </label>

      <fieldset class="full-field">
        <legend class="field-legend">Méthode de contact souhaitée</legend>

        <label class="radio-choice">
          <input
            v-model="form.methodeContact"
            type="radio"
            name="methodeContact"
            value="email"
            :aria-invalid="Boolean(errors.methodeContact)"
          >
          <span>Email</span>
        </label>

        <label class="radio-choice">
          <input
            v-model="form.methodeContact"
            type="radio"
            name="methodeContact"
            value="telephone"
            :aria-invalid="Boolean(errors.methodeContact)"
          >
          <span>Téléphone</span>
        </label>

        <label class="radio-choice">
          <input
            v-model="form.methodeContact"
            type="radio"
            name="methodeContact"
            value="les_deux"
            :aria-invalid="Boolean(errors.methodeContact)"
          >
          <span>Email et téléphone</span>
        </label>

        <p
          v-if="errors.methodeContact"
          class="form-error"
          role="alert"
        >
          {{ errors.methodeContact }}
        </p>
      </fieldset>

      <label class="text-field full-field">
        <span>Votre situation ou votre problématique</span>
        <textarea
          v-model="form.message"
          required
          minlength="20"
          maxlength="4000"
          rows="6"
          placeholder="Décrivez en quelques lignes ce qui vous amène ici."
          :aria-invalid="Boolean(errors.message)"
          :aria-describedby="errors.message ? 'message-error' : undefined"
        ></textarea>
        <span
          v-if="errors.message"
          id="message-error"
          class="form-error"
          role="alert"
        >
          {{ errors.message }}
        </span>
      </label>
    </div>

    <div class="privacy-notice">
      <label class="check-choice">
        <input
          v-model="privacyAcknowledged"
          required
          type="checkbox"
          :aria-invalid="Boolean(privacyError)"
          :aria-describedby="
            privacyError
              ? 'privacy-explanation privacy-error'
              : 'privacy-explanation'
          "
          @change="validatePrivacyAcknowledgement"
          @blur="validatePrivacyAcknowledgement"
        >
        <span>
          J’ai pris connaissance de la
          <NuxtLink to="/confidentialite">
            politique de confidentialité
          </NuxtLink>
          et des informations relatives au traitement de ma demande.
        </span>
      </label>

      <p id="privacy-explanation" class="privacy-explanation">
        Les informations saisies sont utilisées uniquement pour qualifier,
        traiter et suivre votre demande. Aucun mot de passe, accès
        administrateur, clé privée ou autre secret ne doit être transmis dans
        ce formulaire.
      </p>

      <p
        v-if="privacyError"
        id="privacy-error"
        class="form-error"
        role="alert"
      >
        {{ privacyError }}
      </p>
    </div>

    <aside
      class="contact-progress"
      aria-labelledby="contact-progress-title"
      aria-live="polite"
    >
      <h2 id="contact-progress-title">Préparation de votre demande</h2>

      <p>
        {{ validFieldCount }} champs sur {{ requiredFields.length }} validés
      </p>

      <ul>
        <li
          v-for="field in requiredFields"
          :key="field.key"
          :class="{ 'is-valid': field.valid }"
        >
          <span aria-hidden="true">
            {{ field.valid ? '✓' : '○' }}
          </span>
          <span>{{ field.label }}</span>
          <span class="sr-only">
            {{ field.valid ? 'validé' : 'à compléter' }}
          </span>
        </li>
      </ul>

      <p>{{ progressMessage }}</p>
    </aside>

    <div class="form-actions">
      <AppButton
        variant="validate"
        type="submit"
        :disabled="!canSubmit"
        :loading="isSubmitting"
      >
        {{ isSubmitting ? 'Transmission…' : 'Envoyer ma demande' }}
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
  </form>
</template>

<script setup lang="ts">
import AppButton from '~/components/ui/AppButton.vue';
import {
  contactDemandOptions,
  useContactForm,
} from '~/composables/useContact';

const router = useRouter();

const {
  form,
  errors,
  privacyAcknowledged,
  privacyError,
  submitError,
  isSubmitting,
  canSubmit,
  requiredFields,
  validFieldCount,
  progressMessage,
  formatPhoneOnBlur,
  validatePrivacyAcknowledgement,
  submit,
} = useContactForm();

const handleSubmit = async () => {
  const ticket = await submit();

  if (ticket) {
    await router.push(ticket.confirmationUrl);
  }
};
</script>

<style scoped>
fieldset {
  margin: 0;
  padding: 0;
  border: 0;
}

legend {
  margin-bottom: 1.125rem;
  color: #17251d;
  font-size: clamp(1.35rem, 2.8vw, 2rem);
  font-weight: 900;
  line-height: 1.12;
}

.field-legend {
  font-size: 1.15rem;
}

.privacy-notice {
  display: grid;
  gap: 0.75rem;
  margin-top: 1.5rem;
  padding: 1rem;
  border: 1px solid rgb(43 112 83 / 20%);
  border-radius: 0.75rem;
  background: rgb(255 255 255 / 85%);
}

.privacy-notice a {
  color: #215d47;
  font-weight: 800;
  text-decoration: underline;
  text-decoration-thickness: 0.1em;
  text-underline-offset: 0.18em;
}

.privacy-notice a:hover {
  color: #17251d;
}

.privacy-notice a:focus-visible {
  border-radius: 0.2rem;
  outline: 0.15rem solid #2b7053;
  outline-offset: 0.2rem;
}

.privacy-explanation {
  margin: 0;
  color: #435046;
  font-size: 0.9rem;
  line-height: 1.6;
}

.contact-progress {
  margin-top: 1.5rem;
  padding: 1rem;
  border: 1px solid rgb(43 112 83 / 20%);
  border-radius: 0.75rem;
  background: rgb(255 255 255 / 85%);
}

.contact-progress h2 {
  margin: 0;
  color: #17251d;
  font-size: 1.15rem;
  font-weight: 900;
}

.contact-progress ul {
  display: grid;
  gap: 0.4rem;
  margin: 0.75rem 0;
  padding: 0;
  list-style: none;
}

.contact-progress li {
  display: flex;
  gap: 0.5rem;
  color: #435046;
}

.contact-progress li.is-valid {
  color: #2b7053;
  font-weight: 800;
}

.submit-error {
  margin-top: 1rem;
}
</style>