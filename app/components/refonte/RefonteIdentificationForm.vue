<template>
  <section class="RefonteIdentificationSection" aria-labelledby="refonte-identification-title">
    <div class="RefonteIdentificationLayout">
      <div class="RefonteIdentificationPanel">
        <div class="RefonteIdentificationHeader">
          <p class="RefonteIdentificationKicker">Étape 1</p>
          <h2 id="refonte-identification-title" class="RefonteIdentificationTitle">On prépare l'analyse de refonte.</h2>
          <p class="RefonteIdentificationIntro">Vos coordonnées, l'URL du site actuel, puis le questionnaire démarre.</p>
        </div>

        <form class="RefonteIdentificationForm" @submit.prevent="submitForm">
          <div class="RefonteIdentificationGrid">
            <label class="RefonteTextField">
              <span class="RefonteFieldLabel">Prénom</span>
              <input v-model="prenom" required type="text" autocomplete="given-name" placeholder="Prénom">
              <span v-if="prenomError" class="RefonteFieldError">{{ prenomError }}</span>
            </label>

            <label class="RefonteTextField">
              <span class="RefonteFieldLabel">Nom</span>
              <input v-model="nom" required type="text" autocomplete="family-name" placeholder="Nom">
              <span v-if="nomError" class="RefonteFieldError">{{ nomError }}</span>
            </label>

            <label class="RefonteTextField">
              <span class="RefonteFieldLabel">Email</span>
              <input v-model="email" required type="email" autocomplete="email" placeholder="nom@exemple.fr">
              <span v-if="emailError" class="RefonteFieldError">{{ emailError }}</span>
            </label>

            <label class="RefonteTextField">
              <span class="RefonteFieldLabel">Téléphone</span>
              <input v-model="telephone" required type="tel" autocomplete="tel" placeholder="06 12 34 56 78">
              <span v-if="telephoneError" class="RefonteFieldError">{{ telephoneError }}</span>
            </label>
          </div>

          <label class="RefonteTextField">
            <span class="RefonteFieldLabel">URL du site actuel</span>
            <input v-model="siteUrl" required type="url" autocomplete="url" placeholder="https://votre-site.fr">
            <span v-if="siteUrlError" class="RefonteFieldError">{{ siteUrlError }}</span>
          </label>

          <fieldset class="RefontePersonTypeGroup">
            <legend class="RefonteFieldLabel">Type de personne</legend>
            <label v-for="option in personTypes" :key="option.value" class="RefonteRadioChoice">
              <input v-model="typePersonne" required type="radio" name="refontePersonType" :value="option.value">
              <span>{{ option.label }}</span>
            </label>
            <span v-if="typePersonneError" class="RefonteFieldError">{{ typePersonneError }}</span>
          </fieldset>

          <label v-if="needsStructure" class="RefonteTextField">
            <span class="RefonteFieldLabel">Nom de la structure</span>
            <input v-model="nomStructure" required type="text" autocomplete="organization" placeholder="Nom de votre structure">
            <span v-if="nomStructureError" class="RefonteFieldError">{{ nomStructureError }}</span>
          </label>

          <label class="RefonteConsentChoice">
            <input v-model="consentementRgpd" required type="checkbox">
            <span>J'accepte que ces informations soient utilisées pour traiter ma demande d'audit refonte.</span>
          </label>
          <span v-if="consentementRgpdError" class="RefonteFieldError">{{ consentementRgpdError }}</span>

          <AppButton variant="validate" type="submit" :disabled="!isValid || isSubmitting" :loading="isSubmitting">
            {{ isSubmitting ? 'Préparation...' : 'Continuer vers le questionnaire' }}
          </AppButton>

          <p v-if="error" class="RefonteFormError" role="alert">{{ error }}</p>
        </form>
      </div>

      <aside class="RefonteSidePanel" aria-label="Analyse prévue">
        <p class="RefonteSideKicker">Analyse technique</p>
        <ul class="RefonteSideList">
          <li>Balises essentielles et HTTPS</li>
          <li>Ressources en erreur ou lentes</li>
          <li>Core Web Vitals si PageSpeed est configuré</li>
          <li>Lecture heuristique Nielsen</li>
        </ul>
      </aside>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useField, useForm } from 'vee-validate';
import { toTypedSchema } from '@vee-validate/zod';
import AppButton from '~/components/ui/AppButton.vue';
import {
  refonteIdentitySchema,
  type RefonteIdentity,
  type RefonteIdentityInput,
} from '~/validation/schemas';
import type { AuditPersonType } from '~/composables/useAudit';

defineProps<{
  isSubmitting: boolean;
  error: string;
}>();

const emit = defineEmits<{
  submit: [identity: RefonteIdentity];
}>();

const personTypes: Array<{ label: string; value: AuditPersonType }> = [
  { label: 'Individu', value: 'individu' },
  { label: 'Association', value: 'association' },
  { label: 'Entreprise', value: 'entreprise' },
];

const { handleSubmit, meta } = useForm<RefonteIdentityInput>({
  validationSchema: toTypedSchema(refonteIdentitySchema),
  initialValues: {
    prenom: '',
    nom: '',
    email: '',
    telephone: '',
    type_personne: '' as AuditPersonType,
    nom_structure: '',
    site_url: '',
    consentement_rgpd: false,
  },
});

const { value: prenom, errorMessage: prenomError } = useField<string>('prenom');
const { value: nom, errorMessage: nomError } = useField<string>('nom');
const { value: email, errorMessage: emailError } = useField<string>('email');
const { value: telephone, errorMessage: telephoneError } = useField<string>('telephone');
const { value: typePersonne, errorMessage: typePersonneError } = useField<AuditPersonType | ''>('type_personne');
const { value: nomStructure, errorMessage: nomStructureError } = useField<string>('nom_structure');
const { value: siteUrl, errorMessage: siteUrlError } = useField<string>('site_url');
const { value: consentementRgpd, errorMessage: consentementRgpdError } = useField<boolean>('consentement_rgpd');

const needsStructure = computed(() => typePersonne.value === 'association' || typePersonne.value === 'entreprise');
const isValid = computed(() => meta.value.valid && consentementRgpd.value === true);

const submitForm = handleSubmit((values) => {
  emit('submit', values);
});
</script>

<style scoped>
@reference "../../assets/css/main.css";

.RefonteIdentificationSection {
  @apply bg-[#efe8d6] px-4 py-14;
}

.RefonteIdentificationLayout {
  @apply mx-auto grid w-[min(1120px,100%)] gap-6;
}

.RefonteIdentificationPanel,
.RefonteSidePanel {
  @apply rounded-lg border border-white/70 bg-pxp-panel/90 p-6 shadow-[0_22px_60px_rgb(23_37_29/0.14)] backdrop-blur-xl;
}

.RefonteIdentificationHeader,
.RefonteIdentificationForm,
.RefonteTextField,
.RefontePersonTypeGroup,
.RefonteSidePanel {
  @apply grid gap-3;
}

.RefonteIdentificationKicker,
.RefonteFieldLabel,
.RefonteSideKicker {
  @apply text-sm font-black uppercase tracking-wide text-pxp-green;
}

.RefonteIdentificationTitle {
  @apply text-[clamp(1.75rem,3vw,2.5rem)] font-black leading-tight text-pxp-ink;
}

.RefonteIdentificationIntro {
  @apply max-w-170 text-base font-bold leading-relaxed text-[#435046];
}

.RefonteIdentificationForm {
  @apply mt-6;
}

.RefonteIdentificationGrid {
  @apply grid gap-4;
}

.RefonteTextField input {
  @apply min-h-14 w-full min-w-0 rounded-lg border border-pxp-green/18 bg-white px-4 text-pxp-ink outline-none transition focus:border-pxp-green focus:ring-2 focus:ring-pxp-green/20;
}

.RefonteTextField input::placeholder {
  @apply text-xs font-bold text-[#435046]/55;
}

.RefonteRadioChoice,
.RefonteConsentChoice {
  @apply flex items-start gap-3 rounded-lg border border-pxp-green/15 bg-white/95 p-4 font-bold text-[#27322a];
}

.RefonteFieldError,
.RefonteFormError {
  @apply text-sm font-bold text-[#9f2d1c];
}

.RefonteFormError {
  @apply rounded-lg border border-[#d93622]/25 bg-[#d93622]/10 p-4;
}

.RefonteSideList {
  @apply grid gap-3 pl-5 text-sm font-bold leading-relaxed text-[#435046];
}

.RefonteSideList li {
  @apply list-disc;
}

@media (min-width: 780px) {
  .RefonteIdentificationLayout {
    @apply grid-cols-[minmax(0,1fr)_340px] items-start;
  }

  .RefonteIdentificationGrid {
    @apply grid-cols-2;
  }
}
</style>
