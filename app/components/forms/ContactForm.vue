<template>
  <form class="contact-form" @submit.prevent="handleSubmit">
    <fieldset>
      <legend id="contact-form-title">Votre demande</legend>
      <label v-for="option in contactDemandOptions" :key="option.value" class="radio-choice">
        <input v-model="form.need" type="radio" name="need" :value="option.value">
        <span>{{ option.label }}</span>
      </label>
    </fieldset>

    <div class="contact-grid contact-form-grid">
      <label class="text-field">
        <span>Votre prénom / organisation</span>
        <input v-model="form.organization" required type="text" placeholder="Vous êtes ?" autocomplete="organization" maxlength="160">
      </label>
      <label class="text-field">
        <span>Votre email</span>
        <input v-model="form.email" required type="email" placeholder="Pour qu'on vous recontacte" autocomplete="email" maxlength="254">
      </label>
      <label class="text-field">
        <span>Téléphone <small>(optionnel)</small></span>
        <input v-model="form.phone" type="tel" placeholder="+33 6 ..." autocomplete="tel" maxlength="40">
      </label>
      <template v-if="form.need === 'reparation'">
        <label class="text-field"><span>Type d’appareil <small>(optionnel)</small></span><select v-model="form.deviceType"><option value="">Choisir</option><option>Ordinateur</option><option>Téléphone</option><option>Tablette</option><option>Autre</option></select></label>
        <label class="text-field"><span>Modèle, si vous le connaissez <small>(optionnel)</small></span><input v-model="form.model" maxlength="120" placeholder="Marque et modèle"></label>
      </template>
      <template v-if="form.need === 'reemploi'">
        <label class="text-field"><span>Usage prévu <small>(optionnel)</small></span><input v-model="form.usage" maxlength="200" placeholder="Bureautique, études, création…"></label>
        <label class="text-field"><span>Budget envisagé <small>(optionnel)</small></span><input v-model="form.budget" maxlength="80" placeholder="Une fourchette suffit"></label>
      </template>
      <label class="text-field full-field">
        <span>{{ form.need === 'reparation' ? 'Quel symptôme observez-vous ?' : 'Décrivez votre besoin' }}</span>
        <textarea
          v-model="form.message"
          required
          minlength="20"
          maxlength="500"
          aria-describedby="description-help description-security"
          rows="6"
          placeholder="Décrivez en quelques lignes ce qui vous amène ici"
        ></textarea>
        <small id="description-help">20 à 500 caractères. Décrivez ce que vous observez, sans chercher à identifier la cause.</small>
        <small id="description-security">Ne transmettez aucun mot de passe, code de déverrouillage ou clé de récupération.</small>
      </label>
    </div>

    <div class="form-actions">
      <AppButton variant="validate" type="submit" :disabled="!canSubmit || isSubmitting" :loading="isSubmitting">
        {{ isSubmitting ? 'Envoi en cours…' : 'Envoyer ma demande' }}
      </AppButton>
    </div>
    <p class="PrivacyNote">Vos coordonnées servent à traiter votre demande. <NuxtLink to="/confidentialite">Consulter la confidentialité</NuxtLink>.</p>
    <p v-if="submitError" class="form-error" role="alert">{{ submitError }}</p>
  </form>
</template>

<script setup lang="ts">
import AppButton from '~/components/ui/AppButton.vue';
import { watch } from 'vue';
import { useContactForm } from '~/composables/useContact';
import { contactDemandOptions, resolveContactNeed, type ContactNeed } from '~/utils/contactNeeds';
const props = defineProps<{ initialNeed?: ContactNeed | '' }>();

const router = useRouter();
const { form, submitError, isSubmitting, canSubmit, submit } = useContactForm(props.initialNeed);
// Une navigation vers un autre besoin conserve les coordonnées et la description.
watch(() => props.initialNeed, value => { form.need = resolveContactNeed(value); });

/** Ouvre le suivi uniquement lorsque l’API confirme l’enregistrement. */
const handleSubmit = async () => {
  const ticket = await submit();

  if (ticket) {
    router.push(ticket.confirmationUrl);
  }
};
</script>

<style scoped>
@reference "../../assets/css/main.css";
fieldset { @apply m-0 grid gap-3 border-0 p-0; }
legend { @apply mb-5 text-2xl font-bold text-pxp-ink; }
.radio-choice { @apply flex items-start gap-3 rounded-lg border border-pxp-green/25 bg-white p-4; }
.radio-choice input { @apply mt-1 shrink-0 accent-pxp-green; }
.radio-choice:has(input:checked) { @apply border-pxp-green bg-pxp-paper; }
input:focus-visible, select:focus-visible, textarea:focus-visible { @apply outline-2 outline-offset-2 outline-pxp-green; }
.PrivacyNote { @apply mt-4 text-sm leading-relaxed; }
.PrivacyNote a { @apply text-pxp-green underline underline-offset-4; }
#description-security { @apply text-pxp-ink font-semibold; }
:deep(.ButtonValidate) { @apply border-pxp-green text-pxp-green focus-visible:ring-pxp-green; }
</style>
