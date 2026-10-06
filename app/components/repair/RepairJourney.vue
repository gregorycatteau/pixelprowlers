<template>
  <section id="parcours-reparation" class="Journey" aria-labelledby="repair-title">
    <p class="eyebrow">Diagnostic · Micro-soudure</p>
    <h1 id="repair-title" tabindex="-1" class="pxp-font-display">Quel appareil souhaitez-vous réparer ?</h1>
    <p class="Intro">Choisissez votre appareil et ce qui ne fonctionne plus pour découvrir les possibilités de réparation et un premier repère de budget.</p>
    <nav class="Progress" aria-label="Étapes de la réparation">
      <button type="button" :disabled="pending" :aria-current="step === 'device' ? 'step' : undefined" @click="go('device')">1. Appareil</button>
      <span aria-hidden="true">→</span>
      <button type="button" :disabled="!family || pending" :aria-current="step === 'problem' ? 'step' : undefined" @click="go('problem')">2. Problème</button>
      <span aria-hidden="true">→</span>
      <button type="button" :disabled="!symptom || pending" :aria-current="step === 'budget' ? 'step' : undefined" @click="go('budget')">3. Budget</button>
    </nav>
    <div v-if="step === 'device'" class="DeviceGrid" role="group" aria-label="Votre appareil">
      <button v-for="device in activeFamilies" :key="device.id" type="button" class="DeviceCard" :aria-pressed="family === device.id" @click="selectDevice(device.id)"><DeviceIllustration :family="device.id"/><span>{{ device.label }}</span><small>{{ family === device.id ? 'Sélectionné' : 'Choisir cet appareil' }}</small></button>
    </div>
    <div v-if="step === 'problem'" class="ProblemPanel">
      <h2 ref="problemTitle" tabindex="-1">{{ familyLabel }} : que se passe-t-il ?</h2>
      <label v-if="models.length" class="ModelChoice">Modèle <select :value="model" @change="selectModel"><option value="">Je ne connais pas le modèle</option><option v-for="item in models" :key="item.id" :value="item.id">{{ item.brand }} {{ item.label }}</option></select></label>
      <div class="SymptomGrid" role="group" aria-label="Le problème observé"><button v-for="item in visibleSymptoms" :key="item.id" type="button" class="SymptomCard" :aria-pressed="symptom === item.id" @click="selectProblem(item.id)">{{ item.label }}<span aria-hidden="true">→</span></button></div>
      <button v-if="availableSymptoms.length > 6" type="button" class="TextButton" :aria-expanded="showMore" @click="showMore = !showMore">{{ showMore ? 'Réduire les choix' : 'Autres symptômes ou problème inconnu' }}</button>
    </div>
    <div v-if="step === 'budget'" class="BudgetPanel">
      <h2 ref="budgetTitle" tabindex="-1">Votre premier repère</h2>
      <p class="Summary">{{ familyLabel }} · {{ symptomLabel }}<template v-if="modelLabel"> · {{ modelLabel.brand }} {{ modelLabel.label }}</template></p>
      <p class="Service">{{ result.service }}</p>
      <p class="Budget pxp-font-display">{{ budgetLabel(result.estimate) }}</p>
      <p v-if="result.estimate.kind === 'unavailable'">{{ result.estimate.reason }}</p>
      <template v-else><p v-for="line in result.estimate.includes" :key="line">Inclus : {{ line }}</p><p v-for="line in result.estimate.excludes" :key="line">Hors estimation : {{ line }}</p><p v-if="result.estimate.kind === 'diagnostic'">{{ result.estimate.deduction }}</p></template>
      <p v-if="electronic" class="MicroNote">Une réparation au composant peut être envisagée. Nous recherchons l’origine de la panne pour déterminer si une intervention ciblée sur la carte électronique est adaptée.</p>
      <p class="Frame">Le diagnostic confirme l’intervention et son prix. Vous décidez avant la réparation.</p>
      <button type="button" class="RequestButton" :disabled="pending" @click="openRequest">{{ result.identified ? 'Demander cette réparation' : 'Demander un diagnostic' }}</button>
      <p class="GridVersion">Informations du {{ new Intl.DateTimeFormat('fr-FR', { dateStyle: 'long', timeZone: 'UTC' }).format(new Date(publishedRepairGrid.date)) }}</p>
    </div>
    <div v-show="step === 'budget' && requestOpen" ref="requestPanel" class="RequestPanel"><ContactForm initial-need="reparation" :repair-context="context" @pending="pending = $event"/></div>
    <div class="JourneyActions"><button v-if="family" type="button" class="TextButton" :disabled="pending" @click="restart">Recommencer les choix</button><NuxtLink to="/contact?besoin=reparation">Faire une demande directe</NuxtLink><NuxtLink to="/contact">Autre appareil ou question</NuxtLink></div>
  </section>
</template>
<script setup lang="ts">
import { computed, nextTick, ref } from 'vue';
import { useRepairJourney } from '~/composables/useRepairJourney';
import { deviceFamilies, symptomsByFamily, budgetLabel, publishedRepairGrid, type DeviceFamily } from '~/utils/repairGrid';
import ContactForm from '~/components/forms/ContactForm.vue';
import DeviceIllustration from './DeviceIllustration.vue';
const { family, symptom, model, step, models, result, chooseFamily, chooseSymptom, chooseModel, reset } = useRepairJourney();
const activeFamilies = deviceFamilies.filter(f => f.active);
const showMore = ref(false), requestOpen = ref(false), pending = ref(false);
const problemTitle = ref<HTMLElement | null>(null), budgetTitle = ref<HTMLElement | null>(null), requestPanel = ref<HTMLElement | null>(null);
const familyLabel = computed(() => deviceFamilies.find(f => f.id === family.value)?.label ?? '');
const availableSymptoms = computed(() => family.value ? symptomsByFamily[family.value] : []);
const visibleSymptoms = computed(() => showMore.value ? availableSymptoms.value : availableSymptoms.value.slice(0, 6));
const symptomLabel = computed(() => availableSymptoms.value.find(s => s.id === symptom.value)?.label ?? '');
const electronic = computed(() => availableSymptoms.value.find(s => s.id === symptom.value)?.electronic);
const modelLabel = computed(() => models.value.find(m => m.id === model.value));
const context = computed(() => ['Appareil : ' + familyLabel.value, ...(modelLabel.value ? ['Modèle : ' + modelLabel.value.brand + ' ' + modelLabel.value.label] : []), 'Symptôme : ' + symptomLabel.value, 'Prestation envisagée : ' + result.value.service, 'Repère présenté : ' + budgetLabel(result.value.estimate), ...(result.value.estimate.kind === 'unavailable' ? [result.value.estimate.reason] : []), 'Grille : ' + publishedRepairGrid.version + ' (' + publishedRepairGrid.date + ')'].join('\n'));
/** Replace le focus après chaque transition, sans modifier l’URL ni stocker les coordonnées. */
async function focusStep() { await nextTick(); (step.value === 'problem' ? problemTitle.value : step.value === 'budget' ? budgetTitle.value : document.getElementById('repair-title'))?.focus(); }
/** Les retours gardent les choix tant qu’ils restent compatibles. */
async function go(value: typeof step.value) { step.value = value; await focusStep(); }
async function selectDevice(value: DeviceFamily) { const changed = family.value !== value; chooseFamily(value); if (changed) { requestOpen.value = false; showMore.value = false; } await focusStep(); }
async function selectProblem(value: string) { chooseSymptom(value); await focusStep(); }
function selectModel(event: Event) { chooseModel((event.target as HTMLSelectElement).value); }
/** Affiche le formulaire seulement après le repère, puis place le focus dans la description. */
async function openRequest() { requestOpen.value = true; await nextTick(); requestPanel.value?.querySelector('textarea')?.focus(); }
async function restart() { reset(); requestOpen.value = false; showMore.value = false; await focusStep(); }
</script>
<style scoped>
@reference "../../assets/css/main.css";
.Journey { @apply grid gap-6 py-12 md:py-16; scroll-margin-top: 100px; }
h1 { @apply max-w-4xl text-5xl leading-none md:text-6xl; }
.Intro { @apply max-w-2xl text-lg leading-relaxed; }
.Progress { @apply flex flex-wrap items-center gap-2 border-y border-pxp-green/20 py-3 text-sm sm:gap-4; }
.Progress button { @apply min-h-11 px-1; }
.Progress [aria-current=step] { @apply font-bold text-pxp-green underline underline-offset-4; }
button:disabled { @apply cursor-default opacity-50; }
.DeviceGrid { @apply grid grid-cols-2 gap-3 lg:grid-cols-4; }
.DeviceCard { @apply grid min-w-0 gap-3 rounded-xl border border-pxp-green/25 bg-white p-4 text-left hover:border-pxp-green sm:p-6; }
.DeviceCard span { @apply text-lg font-semibold; }
.DeviceCard small { @apply text-xs text-pxp-green; }
[aria-pressed=true] { @apply border-pxp-green bg-pxp-green/10 ring-2 ring-pxp-green; }
.ProblemPanel { @apply grid gap-5; }
h2 { @apply text-2xl font-bold; }
.SymptomGrid { @apply grid gap-3 sm:grid-cols-2 lg:grid-cols-3; }
.SymptomCard { @apply flex min-h-16 items-center justify-between gap-3 rounded-lg border border-pxp-green/25 bg-white p-4 text-left hover:border-pxp-green; }
.BudgetPanel { @apply grid max-w-3xl gap-4 rounded-xl border border-pxp-green/30 bg-white p-5 sm:p-8; }
.Summary { @apply font-semibold; }
.Service { @apply text-pxp-green; }
.Budget { @apply text-4xl leading-tight; }
.MicroNote { @apply border-l-2 border-pxp-green pl-4 leading-relaxed; }
.Frame { @apply text-sm leading-relaxed; }
.RequestButton { @apply min-h-12 w-fit rounded-md bg-pxp-green px-5 py-3 font-semibold text-white hover:bg-pxp-ink; }
.GridVersion { @apply break-words text-xs; }
.RequestPanel { @apply max-w-3xl; }
.JourneyActions { @apply flex flex-wrap items-center gap-x-6 gap-y-2 text-sm; }
.TextButton, .JourneyActions a { @apply min-h-11 py-2 text-pxp-green underline underline-offset-4; }
.ModelChoice { @apply grid max-w-md gap-2; }
.ModelChoice select { @apply min-h-11 border border-pxp-green/30 bg-white p-2; }
button:focus-visible, a:focus-visible, select:focus-visible, h1:focus, h2:focus { @apply outline-2 outline-offset-4 outline-pxp-green; }
</style>
