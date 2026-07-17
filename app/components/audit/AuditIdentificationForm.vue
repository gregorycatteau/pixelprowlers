<template>
  <section class="IdentificationSection" aria-labelledby="audit-identification-title">
    <div class="IdentificationLayout">
      <div class="IdentificationPanel">
        <div class="IdentificationHeader">
          <p class="IdentificationKicker">Étape 0</p>
          <h2 id="audit-identification-title" class="IdentificationTitle">On prépare ton dossier.</h2>
          <p class="IdentificationIntro">Quelques coordonnées, un numéro de dossier, puis le diagnostic commence.</p>
        </div>

        <form class="IdentificationForm" @submit.prevent="submitForm">
          <div class="IdentificationGrid">
            <label class="TextField" :class="{ DisabledField: !isFieldEnabled('prenom'), ValidField: isFieldValid('prenom') }">
              <span class="FieldLabel">Prénom</span>
              <span class="FieldInputShell">
                <span class="FieldIcon FieldIconUser" aria-hidden="true"></span>
                <input
                  id="audit-prenom"
                  ref="prenomInput"
                  v-model="prenom"
                  required
                  :disabled="!isFieldEnabled('prenom')"
                  type="text"
                  maxlength="50"
                  placeholder="Votre prénom"
                  autocomplete="given-name"
                  @blur="normalizeField('prenom')"
                >
              </span>
              <span v-if="prenomError" class="FieldError">{{ prenomError }}</span>
            </label>

            <label class="TextField" :class="{ DisabledField: !isFieldEnabled('nom'), ValidField: isFieldValid('nom') }">
              <span class="FieldLabel">Nom</span>
              <span class="FieldInputShell">
                <span class="FieldIcon FieldIconBadge" aria-hidden="true"></span>
                <input
                  id="audit-nom"
                  ref="nomInput"
                  v-model="nom"
                  required
                  :disabled="!isFieldEnabled('nom')"
                  type="text"
                  maxlength="50"
                  placeholder="Votre nom"
                  autocomplete="family-name"
                  @blur="normalizeField('nom')"
                >
              </span>
              <span v-if="nomError" class="FieldError">{{ nomError }}</span>
            </label>

            <label class="TextField" :class="{ DisabledField: !isFieldEnabled('email'), ValidField: isFieldValid('email') }">
              <span class="FieldLabel">Email</span>
              <span class="FieldInputShell">
                <span class="FieldIcon FieldIconMail" aria-hidden="true"></span>
                <input
                  id="audit-email"
                  ref="emailInput"
                  v-model="email"
                  required
                  :disabled="!isFieldEnabled('email')"
                  type="email"
                  maxlength="254"
                  placeholder="vous@exemple.fr"
                  autocomplete="email"
                  @blur="normalizeField('email')"
                >
              </span>
              <span v-if="emailError" class="FieldError">{{ emailError }}</span>
            </label>

            <label class="TextField" :class="{ DisabledField: !isFieldEnabled('telephone'), ValidField: isFieldValid('telephone') }">
              <span class="FieldLabel">Téléphone</span>
              <span class="FieldInputShell">
                <span class="FieldIcon FieldIconPhone" aria-hidden="true"></span>
                <input
                  id="audit-telephone"
                  ref="telephoneInput"
                  v-model="telephone"
                  required
                  :disabled="!isFieldEnabled('telephone')"
                  type="tel"
                  maxlength="24"
                  placeholder="+33 6 12 34 56 78"
                  autocomplete="tel"
                  @blur="normalizeField('telephone')"
                >
              </span>
              <span v-if="telephoneError" class="FieldError">{{ telephoneError }}</span>
            </label>
          </div>

          <fieldset class="PersonTypeGroup" :class="{ DisabledField: !isFieldEnabled('type_personne') }">
            <legend class="GroupLegend">Type de personne</legend>
            <label v-for="option in personTypes" :key="option.value" class="RadioChoice">
              <input
                v-model="typePersonne"
                required
                :disabled="!isFieldEnabled('type_personne')"
                type="radio"
                name="auditPersonType"
                :value="option.value"
              >
              <span class="RadioIcon" :class="option.icon" aria-hidden="true"></span>
              <span class="RadioLabel">{{ option.label }}</span>
            </label>
            <span v-if="typePersonneError" class="FieldError">{{ typePersonneError }}</span>
          </fieldset>

          <Transition name="StructureReveal">
            <label v-if="needsStructure" class="TextField" :class="{ DisabledField: !isFieldEnabled('nom_structure'), ValidField: isFieldValid('nom_structure') }">
              <span class="FieldLabel">Nom de la structure</span>
              <span class="FieldInputShell">
                <span class="FieldIcon FieldIconBuilding" aria-hidden="true"></span>
                <input
                  id="audit-nom-structure"
                  ref="nomStructureInput"
                  v-model="nomStructure"
                  required
                  :disabled="!isFieldEnabled('nom_structure')"
                  type="text"
                  maxlength="100"
                  placeholder="Nom de votre structure"
                  autocomplete="organization"
                  @blur="normalizeField('nom_structure')"
                >
              </span>
              <span v-if="nomStructureError" class="FieldError">{{ nomStructureError }}</span>
            </label>
          </Transition>

          <label class="ConsentChoice" :class="{ DisabledField: !isFieldEnabled('consentement_rgpd') }">
            <input
              v-model="consentementRgpd"
              required
              :disabled="!isFieldEnabled('consentement_rgpd')"
              type="checkbox"
            >
            <span class="ConsentLabel">
              J'accepte que ces informations soient utilisées dans le cadre du traitement de ma demande d'audit.
            </span>
          </label>
          <span v-if="consentementRgpdError" class="FieldError">{{ consentementRgpdError }}</span>

          <div class="IdentificationActions">
            <AppButton variant="validate" type="submit" :disabled="!isComplete || isSubmitting" :loading="isSubmitting">
              {{ isSubmitting ? 'Première étape vers la reprise de contrôle...' : 'Faire analyser mon site' }}
            </AppButton>
          </div>

          <p class="PostActionNote">
            Votre demande sera enregistrée avant qualification. Sans engagement. Aucun accès ne sera demandé sans validation.
          </p>

          <p class="PrivacyNote">
            <span class="PrivacyIcon" aria-hidden="true"></span>
            Confidentialité stricte. Vous ne partagez jamais vos accès sans cadre clair. Aucune modification sans votre accord.
          </p>

          <p v-if="error" class="FormError" role="alert">{{ error }}</p>
        </form>
      </div>

      <AuditChecklist :items="checklistItems" @focus-item="focusField" />
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, nextTick, ref } from 'vue';
import { useField, useForm } from 'vee-validate';
import { toTypedSchema } from '@vee-validate/zod';
import AuditChecklist from '~/components/audit/AuditChecklist.vue';
import AppButton from '~/components/ui/AppButton.vue';
import type { AuditPersonType } from '~/composables/useAudit';
import {
  auditIdentitySchema,
  emailSchema,
  formatFrenchPhone,
  frenchPhoneSchema,
  humanNameSchema,
  normalizeEmail,
  normalizeName,
  normalizeStructureName,
  personTypeSchema,
  structureNameSchema,
  type AuditIdentity,
  type AuditIdentityInput,
} from '~/validation/schemas';

defineProps<{
  isSubmitting: boolean;
  error: string;
}>();

const emit = defineEmits<{
  submit: [identity: AuditIdentity];
}>();

const personTypes: Array<{ label: string; value: AuditPersonType; icon: string }> = [
  { label: 'Individu', value: 'individu', icon: 'RadioIconPerson' },
  { label: 'Association', value: 'association', icon: 'RadioIconHeart' },
  { label: 'Entreprise', value: 'entreprise', icon: 'RadioIconCompany' },
];

const prenomInput = ref<HTMLInputElement | null>(null);
const nomInput = ref<HTMLInputElement | null>(null);
const emailInput = ref<HTMLInputElement | null>(null);
const telephoneInput = ref<HTMLInputElement | null>(null);
const nomStructureInput = ref<HTMLInputElement | null>(null);

const { handleSubmit } = useForm<AuditIdentityInput>({
  validationSchema: toTypedSchema(auditIdentitySchema),
  initialValues: {
    prenom: '',
    nom: '',
    email: '',
    telephone: '',
    type_personne: '' as AuditPersonType,
    nom_structure: '',
    consentement_rgpd: false,
  },
});

const { value: prenom, errorMessage: prenomError } = useField<string>('prenom');
const { value: nom, errorMessage: nomError } = useField<string>('nom');
const { value: email, errorMessage: emailError } = useField<string>('email');
const { value: telephone, errorMessage: telephoneError } = useField<string>('telephone');
const { value: typePersonne, errorMessage: typePersonneError } = useField<AuditPersonType | ''>('type_personne');
const { value: nomStructure, errorMessage: nomStructureError } = useField<string>('nom_structure');
const { value: consentementRgpd, errorMessage: consentementRgpdError } = useField<boolean>('consentement_rgpd');

const needsStructure = computed(() => typePersonne.value === 'association' || typePersonne.value === 'entreprise');
const baseFieldOrder = computed(() => [
  'prenom',
  'nom',
  'email',
  'telephone',
  'type_personne',
  ...(needsStructure.value ? ['nom_structure'] : []),
  'consentement_rgpd',
]);

const fieldValidators = {
  prenom: () => humanNameSchema.safeParse(prenom.value).success,
  nom: () => humanNameSchema.safeParse(nom.value).success,
  email: () => emailSchema.safeParse(email.value).success,
  telephone: () => frenchPhoneSchema.safeParse(telephone.value).success,
  type_personne: () => personTypeSchema.safeParse(typePersonne.value).success,
  nom_structure: () => !needsStructure.value || structureNameSchema.safeParse(nomStructure.value).success,
  consentement_rgpd: () => consentementRgpd.value === true,
} as const;

type FieldId = keyof typeof fieldValidators;

const isFieldValid = (field: string) => fieldValidators[field as FieldId]?.() || false;
const isFieldEnabled = (field: string) => {
  const index = baseFieldOrder.value.indexOf(field);

  if (index <= 0) {
    return true;
  }

  return baseFieldOrder.value.slice(0, index).every(isFieldValid);
};

const isComplete = computed(() => baseFieldOrder.value.every(isFieldValid));
const checklistItems = computed(() => [
  { id: 'prenom', label: 'Prénom', valid: isFieldValid('prenom') },
  { id: 'nom', label: 'Nom', valid: isFieldValid('nom') },
  { id: 'email', label: 'Email', valid: isFieldValid('email') },
  { id: 'telephone', label: 'Téléphone', valid: isFieldValid('telephone') },
  { id: 'type_personne', label: 'Type', valid: isFieldValid('type_personne') },
  ...(needsStructure.value ? [{ id: 'nom_structure', label: 'Structure', valid: isFieldValid('nom_structure') }] : []),
  { id: 'consentement_rgpd', label: 'Consentement', valid: isFieldValid('consentement_rgpd') },
]);

const inputRefs = {
  prenom: prenomInput,
  nom: nomInput,
  email: emailInput,
  telephone: telephoneInput,
  nom_structure: nomStructureInput,
};

const focusField = async (field: string) => {
  await nextTick();
  inputRefs[field as keyof typeof inputRefs]?.value?.scrollIntoView({ behavior: 'smooth', block: 'center' });
  inputRefs[field as keyof typeof inputRefs]?.value?.focus();
};

const normalizeField = (field: string) => {
  if (field === 'prenom') prenom.value = normalizeName(prenom.value || '');
  if (field === 'nom') nom.value = normalizeName(nom.value || '');
  if (field === 'email') email.value = normalizeEmail(email.value || '');
  if (field === 'telephone') telephone.value = formatFrenchPhone(telephone.value || '');
  if (field === 'nom_structure') nomStructure.value = normalizeStructureName(nomStructure.value || '');
};

const submitForm = handleSubmit((values) => {
  emit('submit', values);
});
</script>

<style scoped>
@reference "../../assets/css/main.css";

.IdentificationSection {
  @apply bg-[#efe8d6] px-4 py-14;
}

.IdentificationLayout {
  @apply mx-auto grid w-[min(1120px,100%)] gap-6;
}

.IdentificationPanel {
  @apply rounded-lg border border-white/70 bg-[#fbfaf5]/85 p-6 shadow-[0_22px_60px_rgb(23_37_29/0.14)] backdrop-blur-xl;
}

.IdentificationHeader {
  @apply grid gap-3;
}

.IdentificationKicker {
  @apply text-sm font-black uppercase tracking-wide text-[#2b7053];
}

.IdentificationTitle {
  @apply text-[clamp(1.75rem,3vw,2.5rem)] font-black leading-tight text-[#17251d];
}

.IdentificationIntro {
  @apply max-w-[680px] text-base font-bold leading-relaxed text-[#435046];
}

.IdentificationForm {
  @apply mt-8 grid gap-6;
}

.IdentificationGrid {
  @apply grid gap-4;
}

.TextField {
  @apply grid gap-2 font-bold text-[#27322a];
}

.FieldInputShell {
  @apply grid min-h-14 grid-cols-[2.75rem_minmax(0,1fr)] items-center rounded-lg border border-[#2b7053]/18 bg-white/95 shadow-[inset_0_1px_0_rgb(255_255_255/0.75)] transition;
}

.TextField input {
  @apply min-h-14 w-full min-w-0 bg-transparent px-3 text-[#17251d] outline-none;
}

.TextField input::placeholder {
  @apply text-[0.62rem] font-bold text-[#435046]/55;
}

.TextField:focus-within .FieldInputShell {
  @apply border-[#2b7053] ring-2 ring-[#2b7053]/20;
}

.ValidField .FieldInputShell {
  @apply border-[#2b7053]/50 bg-[#f7fff9];
}

.ValidField .FieldInputShell::after {
  @apply mr-4 text-sm font-black text-[#2b7053];
  content: "✓";
}

.FieldIcon {
  @apply mx-auto inline-flex h-6 w-6 items-center justify-center rounded-full bg-[#2b7053]/10 text-sm font-black text-[#2b7053];
}

.FieldIconUser::before {
  content: "P";
}

.FieldIconBadge::before {
  content: "N";
}

.FieldIconMail::before {
  content: "@";
}

.FieldIconPhone::before {
  content: "T";
}

.FieldIconBuilding::before {
  content: "S";
}

.FieldLabel,
.GroupLegend {
  @apply text-sm font-black uppercase tracking-wide text-[#2b7053];
}

.PersonTypeGroup {
  @apply grid gap-3 border-0 p-0;
}

.RadioChoice {
  @apply flex items-center gap-3 rounded-lg border border-[#2b7053]/15 bg-white/95 p-4 font-bold text-[#27322a] shadow-[0_8px_24px_rgb(23_37_29/0.06)] transition hover:-translate-y-0.5 hover:border-[#2b7053]/45;
}

.ConsentChoice {
  @apply flex items-start gap-3 rounded-lg border border-[#2b7053]/15 bg-white/95 p-4 font-bold text-[#27322a];
}

.RadioChoice input,
.ConsentChoice input {
  @apply sr-only;
}

.RadioIcon {
  @apply inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-lg border border-[#2b7053]/20 bg-[#2b7053]/8 text-sm font-black text-[#2b7053] transition;
}

.RadioIconPerson::before {
  content: "I";
}

.RadioIconHeart::before {
  content: "A";
}

.RadioIconCompany::before {
  content: "E";
}

.RadioChoice input:checked + .RadioIcon {
  @apply border-[#2b7053] bg-[#2b7053] text-white shadow-[0_10px_24px_rgb(43_112_83/0.22)];
}

.RadioChoice:has(input:checked) {
  @apply border-[#2b7053]/55 bg-[#f7fff9];
}

.ConsentChoice input + .ConsentLabel::before {
  @apply mr-3 inline-flex h-5 w-5 items-center justify-center rounded-md border-2 border-[#2b7053]/35 align-middle text-sm font-black text-white transition;
  content: "";
}

.ConsentChoice input:checked + .ConsentLabel::before {
  @apply border-[#2b7053] bg-[#2b7053];
  content: "✓";
}

.RadioLabel,
.ConsentLabel {
  @apply leading-relaxed;
}

.IdentificationActions {
  @apply flex flex-wrap gap-3;
}

.PrivacyNote {
  @apply flex items-center gap-2 text-sm font-bold text-[#435046];
}

.PostActionNote {
  @apply text-sm font-black leading-relaxed text-[#2b7053];
}

.PrivacyIcon {
  @apply inline-flex h-6 w-6 items-center justify-center rounded-lg bg-[#2b7053]/10 text-xs font-black text-[#2b7053];
}

.PrivacyIcon::before {
  content: "✓";
}

.FormError {
  @apply rounded-lg border border-[#d93622]/25 bg-[#d93622]/10 p-4 font-bold text-[#7c2418];
}

.FieldError {
  @apply text-sm font-bold text-[#7c2418];
}

.DisabledField {
  @apply opacity-50;
}

.DisabledField input {
  @apply cursor-not-allowed bg-[#f4f0e3];
}

.StructureReveal-enter-active,
.StructureReveal-leave-active {
  @apply transition duration-300;
}

.StructureReveal-enter-from,
.StructureReveal-leave-to {
  @apply -translate-y-2 opacity-0;
}

@media (min-width: 720px) {
  .IdentificationGrid {
    @apply grid-cols-2;
  }

  .PersonTypeGroup {
    @apply grid-cols-3;
  }
}

@media (min-width: 980px) {
  .IdentificationLayout {
    @apply grid-cols-[minmax(0,1fr)_280px] items-start;
  }
}
</style>
