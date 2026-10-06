<template>
  <form class="contact-form" novalidate @submit.prevent="handleSubmit">
    <header class="ContactIntro">
      <p class="eyebrow">Contact</p>
      <h1 id="contact-title" class="pxp-font-display">{{ heading }}</h1>
      <p>{{ form.need === 'reparation' ? 'Décrivez le symptôme : nous préciserons ensemble la suite.' : 'Quelques lignes suffisent pour préparer notre échange.' }}</p>
    </header>
    <div class="NeedSummary">
      <span>{{ selectedLabel || 'Choisissez votre demande' }}</span>
      <button ref="toggleButton" class="NeedToggle" type="button" :aria-expanded="selectorOpen" aria-controls="need-options" @click="selectorOpen = !selectorOpen">{{ selectorOpen ? 'Fermer les choix' : 'Changer de demande' }}</button>
    </div>
    <fieldset v-if="selectorOpen" id="need-options" @keydown.esc.prevent="closeSelector">
      <legend class="sr-only">Votre demande</legend>
      <div class="NeedGrid">
        <label v-for="option in contactDemandOptions" :key="option.value" class="radio-choice">
          <input v-model="form.need" type="radio" name="need" :value="option.value"><span>{{ shortLabels[option.value] }}</span>
        </label>
      </div>
      <button class="NeedClose" type="button" @click="closeSelector">Utiliser ce choix</button>
    </fieldset>
    <p v-if="attempted && !form.need" class="FieldError" role="alert">Choisissez le sujet de votre demande.</p>
    <div class="ContactFields">
      <div v-if="form.need === 'reparation'" class="FieldPair">
        <label class="text-field"><span>Appareil <small>(facultatif)</small></span><select v-model="form.deviceType"><option value="">Choisir</option><option>Ordinateur</option><option>Téléphone</option><option>Tablette</option><option>Autre</option></select></label>
        <label class="text-field"><span>Modèle <small>(facultatif)</small></span><input v-model="form.model" maxlength="120" placeholder="Marque et modèle"></label>
      </div>
      <div v-if="form.need === 'reemploi'" class="FieldPair">
        <label class="text-field"><span>Usage <small>(facultatif)</small></span><input v-model="form.usage" maxlength="200" placeholder="Quotidien, études, travail…"></label>
        <label class="text-field"><span>Budget <small>(facultatif)</small></span><input v-model="form.budget" maxlength="80" placeholder="Une fourchette suffit"></label>
      </div>
      <label class="text-field">
        <span>{{ form.need === 'reparation' ? 'Quel symptôme observez-vous ?' : 'Décrivez votre besoin' }}</span>
        <textarea v-model="form.message" required minlength="20" maxlength="500" rows="3" :aria-describedby="`description-help description-counter${showError('message') ? ' message-error' : ''}`" :aria-invalid="showError('message') || undefined" placeholder="Ce qui ne fonctionne plus, depuis quand…" @blur="touched.message = true"></textarea>
        <small id="description-help">{{ form.need === 'reparation' ? 'Décrivez la panne ; aucun mot de passe n’est nécessaire ici.' : 'Décrivez votre besoin ; aucun mot de passe n’est nécessaire ici.' }}</small>
        <small id="description-counter">{{ form.message.length }} / 500 caractères · minimum 20</small>
        <small v-if="showError('message')" id="message-error" class="FieldError">Décrivez votre situation en 20 à 500 caractères.</small>
      </label>
      <div class="FieldPair">
        <label class="text-field"><span>Votre nom</span><input v-model="form.organization" required autocomplete="name" maxlength="160" placeholder="Prénom et nom" :aria-describedby="showError('name') ? 'name-error' : undefined" :aria-invalid="showError('name') || undefined" @blur="touched.name = true"><small v-if="showError('name')" id="name-error" class="FieldError">Indiquez votre nom (160 caractères maximum).</small></label>
        <label class="text-field"><span>E-mail</span><input v-model="form.email" required type="email" autocomplete="email" maxlength="254" placeholder="vous@exemple.fr" :aria-describedby="showError('email') ? 'email-error' : undefined" :aria-invalid="showError('email') || undefined" @blur="touched.email = true"><small v-if="showError('email')" id="email-error" class="FieldError">Indiquez une adresse e-mail valide.</small></label>
      </div>
      <label class="text-field PhoneField"><span>Téléphone <small>(facultatif)</small></span><input v-model="form.phone" type="tel" autocomplete="tel" maxlength="40" placeholder="Votre numéro"></label>
    </div>
    <div class="form-actions"><AppButton variant="primary" type="submit" :disabled="isSubmitting" :loading="isSubmitting">{{ isSubmitting ? 'Envoi en cours…' : 'Envoyer ma demande' }}</AppButton></div>
    <p v-if="submitError" class="form-error" role="alert">{{ submitError }}</p>
    <p class="PrivacyNote">Vos coordonnées servent à traiter votre demande. <NuxtLink to="/confidentialite">Confidentialité</NuxtLink>.</p>
  </form>
</template>
<script setup lang="ts">
import { computed, nextTick, reactive, ref, watch } from 'vue';
import AppButton from '~/components/ui/AppButton.vue';
import { useContactForm } from '~/composables/useContact';
import { contactDemandOptions, resolveContactNeed, type ContactNeed } from '~/utils/contactNeeds';
import { isEmailLike } from '~/utils/formatDate';
const props = defineProps<{ initialNeed?: ContactNeed | '' }>();
const router = useRouter();
const { form, submitError, isSubmitting, canSubmit, submit } = useContactForm(props.initialNeed);
const selectorOpen = ref(!props.initialNeed);
const toggleButton = ref<HTMLButtonElement | null>(null);
const attempted = ref(false);
const touched = reactive({ name: false, email: false, message: false });
const shortLabels: Record<ContactNeed, string> = { reparation: 'Réparation', reemploi: 'Ordinateur reconditionné', conseil: 'Conseil et assistance', developpement: 'Développement', formation: 'Formation', autre: 'Autre' };
const headings: Record<ContactNeed, string> = { reparation: 'Quel appareil souhaitez-vous réparer ?', reemploi: 'Quel ordinateur vous conviendrait ?', conseil: 'Quelle difficulté souhaitez-vous résoudre ?', developpement: 'Quel projet souhaitez-vous créer ?', formation: 'Que souhaitez-vous apprendre ?', autre: 'Parlons de votre besoin.' };
const selectedLabel = computed(() => form.need ? shortLabels[form.need] : '');
const heading = computed(() => form.need ? headings[form.need] : 'Parlons de votre besoin.');
// Une navigation vers un autre besoin conserve toutes les saisies.
watch(() => props.initialNeed, value => { form.need = resolveContactNeed(value); selectorOpen.value = !form.need; });
/** Referme les choix et replace le focus sur leur bouton d’ouverture. */
const closeSelector = async () => { selectorOpen.value = false; await nextTick(); toggleButton.value?.focus(); };
/** Affiche une erreur après interaction, sans effacer les champs. */
const showError = (field: keyof typeof touched) => {
  if (!attempted.value && !touched[field]) return false;
  if (field === 'name') return !form.organization.trim() || form.organization.trim().length > 160;
  if (field === 'email') return !isEmailLike(form.email) || form.email.trim().length > 254;
  return form.message.trim().length < 20 || form.message.length > 500;
};
/** Ouvre le suivi uniquement lorsque l’API confirme l’enregistrement. */
const handleSubmit = async () => {
  attempted.value = true;
  if (!canSubmit.value) {
    await nextTick();
    (document.querySelector<HTMLElement>('.contact-form [aria-invalid="true"]') || toggleButton.value)?.focus();
    return;
  }
  const ticket = await submit();
  if (ticket) router.push(ticket.confirmationUrl);
};
</script>
<style scoped>
@reference "../../assets/css/main.css";
.contact-form { @apply grid gap-5; }
.ContactIntro { @apply grid gap-3; }
h1 { @apply text-3xl leading-tight sm:text-4xl md:text-5xl; }
.NeedSummary { @apply flex flex-wrap items-center justify-between gap-2 border-y border-pxp-green/20 py-3 text-sm; }
.NeedSummary > span { @apply font-semibold; }
.NeedToggle, .NeedClose { @apply min-h-11 text-pxp-green underline underline-offset-4; }
fieldset { @apply m-0 grid gap-2 border-0 p-0; }
.NeedGrid { @apply grid gap-2 sm:grid-cols-2; }
.radio-choice { @apply flex min-h-11 items-center gap-3 rounded border border-pxp-green/25 bg-white px-3 py-2 text-sm; }
.radio-choice input { @apply shrink-0 accent-pxp-green; }
.radio-choice:has(input:checked) { @apply border-pxp-green bg-pxp-panel; }
.ContactFields { @apply grid gap-4; }
.FieldPair { @apply grid gap-4 sm:grid-cols-2; }
.PhoneField { @apply sm:max-w-[calc(50%-8px)]; }
.text-field { @apply gap-1 font-normal; }
.text-field > span { @apply text-sm font-semibold; }
.text-field input, .text-field select, .text-field textarea { @apply w-full min-w-0 rounded border border-pxp-green/30 bg-white px-3 py-2 text-base text-pxp-ink; }
.text-field input, .text-field select { @apply h-11; }
.text-field textarea { @apply min-h-24; }
small { @apply text-xs leading-relaxed; }
.FieldError { @apply text-[#972c20]; }
input:focus-visible, select:focus-visible, textarea:focus-visible, button:focus-visible { @apply outline-2 outline-offset-2 outline-pxp-green; }
.form-actions { @apply m-0; }
.PrivacyNote { @apply text-xs leading-relaxed; }
.PrivacyNote a { @apply text-pxp-green underline underline-offset-4; }
</style>
