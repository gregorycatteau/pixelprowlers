<template>
  <form class="contact-form" @submit.prevent="handleSubmit">
    <fieldset>
      <legend id="contact-form-title">Votre demande</legend>
      <label v-for="option in contactDemandOptions" :key="option.value" class="radio-choice">
        <input v-model="form.demandType" type="radio" name="demandType" :value="option.value">
        <span>{{ option.label }}</span>
      </label>
    </fieldset>

    <div class="contact-grid contact-form-grid">
      <label class="text-field">
        <span>Votre prénom</span>
        <input v-model="form.prenom" required maxlength="100" type="text" autocomplete="given-name">
      </label>
      <label class="text-field">
        <span>Votre nom</span>
        <input v-model="form.nom" required maxlength="100" type="text" autocomplete="family-name">
      </label>
      <label class="text-field">
        <span>Votre organisation <small>(optionnel)</small></span>
        <input v-model="form.organization" maxlength="180" type="text" autocomplete="organization">
      </label>
      <label class="text-field">
        <span>Votre email</span>
        <input v-model="form.email" required type="email" placeholder="Pour qu'on vous recontacte" autocomplete="email">
      </label>
      <label class="text-field">
        <span>Téléphone <small>(obligatoire si rappel demandé)</small></span>
        <input v-model="form.phone" type="tel" placeholder="+33 6 ..." autocomplete="tel">
      </label>
      <label class="text-field full-field">
        <span>Objet</span>
        <input v-model="form.objet" required maxlength="200" type="text" placeholder="Objet de votre demande">
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
      </label>
    </div>

    <div class="form-actions">
      <AppButton variant="validate" type="submit" :disabled="!canSubmit || isSubmitting" :loading="isSubmitting">
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
const { form, submitError, isSubmitting, canSubmit, submit } = useContactForm();

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
</style>
