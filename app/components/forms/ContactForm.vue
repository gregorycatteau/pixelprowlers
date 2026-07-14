<template>
  <form class="contact-form" @submit.prevent="handleSubmit">
    <fieldset>
      <legend id="contact-form-title">Votre demande</legend>
      <label v-for="option in contactDemandOptions" :key="option.value" class="radio-choice">
        <input v-model="form.demandType" type="radio" name="demandType" :value="option.value">
        <span>{{ option.label }}</span>
      </label>
      <p v-if="errors.demandType" class="form-error">{{ errors.demandType }}</p>
    </fieldset>

    <div class="contact-grid contact-form-grid">
      <label class="text-field">
        <span>Votre prénom</span>
        <input v-model="form.prenom" required maxlength="100" type="text" autocomplete="given-name">
        <span v-if="errors.prenom" class="form-error">{{ errors.prenom }}</span>
      </label>
      <label class="text-field">
        <span>Votre nom</span>
        <input v-model="form.nom" required maxlength="100" type="text" autocomplete="family-name">
        <span v-if="errors.nom" class="form-error">{{ errors.nom }}</span>
      </label>
      <label class="text-field">
        <span>Organisation ou statut</span>
        <small>Indique le nom de ton organisation ou « Particulier » si tu ne fais pas partie d’une organisation.</small>
        <input v-model="form.organization" required maxlength="180" type="text" autocomplete="organization" placeholder="Nom de l’organisation ou Particulier">
        <span v-if="errors.organization" class="form-error">{{ errors.organization }}</span>
      </label>
      <label class="text-field">
        <span>Votre email</span>
        <input v-model="form.email" required maxlength="254" type="email" placeholder="Pour qu'on vous recontacte" autocomplete="email">
        <span v-if="errors.email" class="form-error">{{ errors.email }}</span>
      </label>
      <label class="text-field">
        <span>Numéro de téléphone</span>
        <input v-model="form.phone" required maxlength="30" type="tel" placeholder="06 12 34 56 78" autocomplete="tel" @blur="formatPhoneOnBlur">
        <span v-if="errors.phone" class="form-error">{{ errors.phone }}</span>
      </label>
      <label class="text-field full-field">
        <span>Objet</span>
        <input v-model="form.objet" required maxlength="200" type="text" placeholder="Objet de votre demande">
        <span v-if="errors.objet" class="form-error">{{ errors.objet }}</span>
      </label>
      <fieldset class="full-field">
        <legend>Méthode de contact souhaitée</legend>
        <label class="radio-choice">
          <input v-model="form.methodeContact" type="radio" value="email">
          <span>Email</span>
        </label>
        <label class="radio-choice">
          <input v-model="form.methodeContact" type="radio" value="telephone">
          <span>Téléphone</span>
        </label>
        <label class="radio-choice">
          <input v-model="form.methodeContact" type="radio" value="les_deux">
          <span>Email et téléphone</span>
        </label>
        <p v-if="errors.methodeContact" class="form-error">{{ errors.methodeContact }}</p>
      </fieldset>
      <label class="text-field full-field">
        <span>Votre situation / problématique</span>
        <textarea
          v-model="form.message"
          required
          minlength="20"
          maxlength="4000"
          rows="6"
          placeholder="Décrivez en quelques lignes ce qui vous amène ici"
        ></textarea>
        <span v-if="errors.message" class="form-error">{{ errors.message }}</span>
      </label>
    </div>

    <aside class="contact-progress" aria-labelledby="contact-progress-title" aria-live="polite">
      <h2 id="contact-progress-title">Préparation du ticket</h2>
      <p>{{ validFieldCount }} champs sur {{ requiredFields.length }} validés</p>
      <ul>
        <li v-for="field in requiredFields" :key="field.key" :class="{ 'is-valid': field.valid }">
          <span aria-hidden="true">{{ field.valid ? '✓' : '○' }}</span>
          <span>{{ field.label }}</span>
          <span class="sr-only">{{ field.valid ? 'validé' : 'à compléter' }}</span>
        </li>
      </ul>
      <p>{{ progressMessage }}</p>
    </aside>

    <div class="form-actions">
      <AppButton variant="validate" type="submit" :disabled="!canSubmit" :loading="isSubmitting">
        {{ isSubmitting ? 'Ouverture...' : 'Ouvrir un ticket' }}
      </AppButton>
    </div>
    <p v-if="submitError" class="form-error" role="alert" aria-live="polite">{{ submitError }}</p>
  </form>
</template>

<script setup lang="ts">
import AppButton from '~/components/ui/AppButton.vue';
import { contactDemandOptions, useContactForm } from '~/composables/useContact';

const router = useRouter();
const {
  form,
  errors,
  submitError,
  isSubmitting,
  canSubmit,
  requiredFields,
  validFieldCount,
  progressMessage,
  formatPhoneOnBlur,
  submit,
} = useContactForm();

const handleSubmit = async () => {
  const ticket = await submit();

  if (ticket) {
    router.push(ticket.confirmationUrl);
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
  margin-bottom: 18px;
  color: #17251d;
  font-size: clamp(1.35rem, 2.8vw, 2rem);
  font-weight: 900;
  line-height: 1.12;
}

.contact-progress {
  margin-top: 1.5rem;
  padding: 1rem;
  border: 1px solid rgb(43 112 83 / 20%);
  border-radius: 0.75rem;
  background: rgb(255 255 255 / 85%);
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
</style>
