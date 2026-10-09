<template>
  <section id="parcours-reparation" class="Journey" aria-labelledby="repair-title">
    <p class="eyebrow">Réparation informatique · Micro-soudure · Médoc</p>
    <h1 id="repair-title" tabindex="-1" class="pxp-font-display">Quel budget pour votre réparation ?</h1>
    <p class="Intro">Ordinateur, téléphone, tablette, console ou manette : choisissez votre appareil et ce que vous constatez pour estimer votre budget.</p>
    <nav class="Progress" aria-label="Étapes de la réparation">
      <button type="button" :disabled="pending" :aria-current="step === 'device' ? 'step' : undefined" @click="go('device')">1. Appareil</button>
      <span aria-hidden="true">→</span>
      <button type="button" :disabled="!family || pending" :aria-current="['problem', 'precision'].includes(step) ? 'step' : undefined" @click="go('problem')">2. Problème</button>
      <span aria-hidden="true">→</span>
      <button type="button" :disabled="!symptom || pending" :aria-current="step === 'budget' ? 'step' : undefined" @click="go('budget')">3. Budget</button>
    </nav>
    <div v-if="step === 'device'" class="DeviceGrid" role="group" aria-label="Votre appareil">
      <button v-for="device in activeFamilies" :key="device.id" type="button" class="DeviceCard" :aria-pressed="family === device.id" @click="selectDevice(device.id)"><DeviceIllustration :family="device.id"/><span>{{ device.label }}</span><small>{{ family === device.id ? 'Sélectionné' : 'Choisir cet appareil' }}</small></button>
    </div>
    <div v-if="step === 'problem'" class="ProblemPanel">
      <h2 ref="problemTitle" tabindex="-1">{{ familyLabel }} : que se passe-t-il ?</h2>
      <div class="SymptomGrid" role="group" aria-label="Le problème observé"><button v-for="item in visibleSymptoms" :key="item.id" type="button" class="SymptomCard" :aria-pressed="symptom === item.id" @click="selectProblem(item.id)">{{ item.label }}<span aria-hidden="true">→</span></button></div>
      <button v-if="availableSymptoms.length > 6" type="button" class="TextButton" :aria-expanded="showMore" @click="showMore = !showMore">{{ showMore ? 'Réduire les choix' : 'Autres symptômes ou problème inconnu' }}</button>
    </div>
    <div v-if="step === 'precision'" class="ProblemPanel">
      <h2 ref="precisionTitle" tabindex="-1">{{ precisionQuestion }}</h2>
      <div class="SymptomGrid" role="group" :aria-label="precisionQuestion"><button v-for="option in options" :key="option.id" type="button" class="SymptomCard" :aria-pressed="precision === option.id" @click="selectPrecision(option.id)">{{ option.label }}<span aria-hidden="true">→</span></button></div>
    </div>
    <div v-if="step === 'budget'" class="BudgetPanel">
      <h2 ref="budgetTitle" tabindex="-1">Votre budget possible</h2>
      <p class="Summary">{{ familyLabel }} · {{ symptomLabel }}<template v-if="precisionLabel"> · {{ precisionLabel }}</template></p>
      <p>{{ result.diagnosticFirst ? 'Le diagnostic permet de rechercher la cause avant de retenir une intervention.' : result.offers.length > 1 ? 'Ces scénarios sont des alternatives selon la cause : leurs montants ne s’additionnent pas.' : 'Cette intervention peut correspondre au problème observé ; la cause sera vérifiée.' }}</p>
      <div class="OfferGrid"><RepairOfferCard v-for="offer in result.offers" :key="offer.id" :offer="offer"/></div>
      <component :is="result.diagnosticFirst ? 'div' : 'details'" v-if="result.possible.length" class="Possible"><summary v-if="!result.diagnosticFirst">Autre possibilité après diagnostic</summary><h3 v-else>Interventions possibles après vérification</h3><p v-if="symptom === 'liquid'">Le traitement après contact avec un liquide peut être envisagé ; il ne garantit pas la remise en fonctionnement.</p><p v-else-if="family === 'console' && symptom === 'image'">Un défaut du circuit vidéo nécessite une investigation ; un port HDMI n’est pas automatiquement en cause.</p><div class="OfferGrid"><RepairOfferCard v-for="offer in result.possible" :key="offer.id" :offer="offer"/></div></component>
      <p class="PriceNote">{{ consumerPriceNote }} Transport et déplacement chiffrés séparément avant accord. Les budgets indicatifs sont des repères ; les cas hors périmètre passent sur devis.</p>
      <p v-if="electronic" class="MicroNote">Une réparation au composant peut être envisagée. Nous recherchons l’origine de la panne pour déterminer si une intervention ciblée sur la carte électronique est adaptée.</p>
      <div class="Deduction"><p>{{ diagnosticDeduction }}</p><details><summary>Diagnostic : périmètre et déduction</summary><p>Standard : {{ diagnostic.standard }} ; approfondi : {{ diagnostic.deep }}. Ils ne sont pas cumulés : passage à l’approfondi pour un supplément de {{ diagnostic.supplement }}, après accord.</p><p>Exemple : réparation totale {{ diagnostic.total }}, diagnostic payé {{ diagnostic.deep }}, reste à régler {{ diagnostic.remaining }}.</p><p>Si la réparation coûte moins que le diagnostic payé, la différence est remboursée ou fait l’objet d’un avoir convenu.</p><p>Les entretiens définis et le nettoyage de port à forfait n’exigent pas systématiquement un diagnostic séparé. Toute recherche au-delà du périmètre autorisé nécessite un accord complémentaire.</p></details></div>
      <p class="Frame">Le diagnostic confirme l’intervention et son prix. Vous décidez avant la réparation.</p>
      <div class="BudgetActions"><button type="button" class="RequestButton" :disabled="pending" @click="openRequest">{{ result.diagnosticFirst || result.offers.length > 1 ? 'Poursuivre ma demande' : 'Demander cette réparation' }}</button><button type="button" class="TextButton" :disabled="pending" @click="go('problem')">Modifier mes choix</button><button v-if="options.length" type="button" class="TextButton" :disabled="pending" @click="go('precision')">Modifier la précision</button></div>
      <p class="GridVersion">Informations du {{ new Intl.DateTimeFormat('fr-FR', { dateStyle: 'long', timeZone: 'UTC' }).format(new Date(publishedRepairGrid.date)) }}</p>
    </div>
    <div v-show="step === 'budget' && requestOpen" ref="requestPanel" class="RequestPanel"><label class="ModelChoice">Marque et modèle <small>(facultatif)</small><input :value="model" maxlength="120" placeholder="Je ne connais pas le modèle" @input="selectModel"><small>La référence aide à vérifier les pièces ; le budget ci-dessus reste indicatif.</small></label><ContactForm initial-need="reparation" :repair-context="context" @pending="pending = $event"/></div>
    <p v-if="step === 'device'" class="Orientation">{{ orientation?.label }} : {{ orientation ? budgetLabel(orientation.estimate).toLowerCase() : '' }}. Sans démontage ni recherche technique.</p>
    <details v-if="family" class="TariffCatalogue"><summary>Consulter les tarifs par appareil</summary><div class="OfferGrid"><RepairOfferCard v-for="offer in catalogue" :key="offer.id" :offer="offer"/></div></details>
    <div class="JourneyActions"><button v-if="family" type="button" class="TextButton" :disabled="pending" @click="restart">Recommencer les choix</button><NuxtLink to="/contact?besoin=reparation">Faire une demande directe</NuxtLink><NuxtLink to="/contact">Autre appareil ou question</NuxtLink></div>
  </section>
</template>
<script setup lang="ts">
import { computed, nextTick, ref } from 'vue';
import { useRepairJourney } from '~/composables/useRepairJourney';
import { deviceFamilies, symptomsByFamily, budgetLabel, publishedRepairGrid, offersForFamily, consumerPriceNote, diagnosticDeduction, diagnosticPresentation, type DeviceFamily } from '~/utils/repairGrid';
import ContactForm from '~/components/forms/ContactForm.vue';
import DeviceIllustration from './DeviceIllustration.vue';
import RepairOfferCard from './RepairOfferCard.vue';
const { family, symptom, precision, model, step, options, result, chooseFamily, chooseSymptom, choosePrecision, chooseModel, reset } = useRepairJourney();
const activeFamilies = deviceFamilies.filter(f => f.active);
const showMore = ref(false), requestOpen = ref(false), pending = ref(false);
const precisionTitle = ref<HTMLElement | null>(null);
const problemTitle = ref<HTMLElement | null>(null), budgetTitle = ref<HTMLElement | null>(null), requestPanel = ref<HTMLElement | null>(null);
const familyLabel = computed(() => deviceFamilies.find(f => f.id === family.value)?.label ?? '');
const availableSymptoms = computed(() => family.value ? symptomsByFamily[family.value] : []);
const visibleSymptoms = computed(() => showMore.value ? availableSymptoms.value : availableSymptoms.value.slice(0, 6));
const symptomLabel = computed(() => availableSymptoms.value.find(s => s.id === symptom.value)?.label ?? '');
const electronic = computed(() => availableSymptoms.value.find(s => s.id === symptom.value)?.electronic);
const precisionLabel = computed(() => options.value.find(o => o.id === precision.value)?.label ?? '');
const precisionQuestion = computed(() => family.value === 'controller' ? 'Combien de joysticks sont concernés ?' : family.value === 'console' ? 'Quelle famille de console ?' : symptom.value === 'screen' ? 'Quel type d’écran ?' : symptom.value === 'charge' ? 'Quel connecteur reconnaissez-vous ?' : 'Quel type de portable ?');
const diagnostic = diagnosticPresentation(publishedRepairGrid);
const orientation = publishedRepairGrid.offers.find(o => o.id === 'orientation');
const catalogue = computed(() => offersForFamily(publishedRepairGrid, family.value));
const context = computed(() => ['Appareil : ' + familyLabel.value, 'Symptôme : ' + symptomLabel.value, ...(precisionLabel.value ? ['Précision : ' + precisionLabel.value] : []), ...(model.value.trim() ? ['Modèle indiqué (compatibilité à vérifier) : ' + model.value.trim()] : []), 'Scénarios alternatifs présentés (non cumulés) :', ...[...result.value.offers, ...result.value.possible].map(o => o.label + ' : ' + budgetLabel(o.estimate) + ' — ' + o.scope), diagnosticDeduction, 'Grille : ' + publishedRepairGrid.version + ' (' + publishedRepairGrid.date + ')'].join('\n'));
/** Replace le focus après chaque transition, sans modifier l’URL ni stocker les coordonnées. */
async function focusStep() { await nextTick(); (step.value === 'precision' ? precisionTitle.value : step.value === 'problem' ? problemTitle.value : step.value === 'budget' ? budgetTitle.value : document.getElementById('repair-title'))?.focus(); }
/** Les retours gardent les choix tant qu’ils restent compatibles. */
async function go(value: typeof step.value) { step.value = value; await focusStep(); }
/** Change la famille et retire les choix devenus incompatibles. */
async function selectDevice(value: DeviceFamily) { const changed = family.value !== value; chooseFamily(value); if (changed) { requestOpen.value = false; showMore.value = false; } await focusStep(); }
/** Valide une observation et rejoint la précision ou le budget. */
async function selectProblem(value: string) { chooseSymptom(value); await focusStep(); }
/** La précision est un code public validé ; le modèle libre reste une information de contact. */
async function selectPrecision(value: string) { choosePrecision(value); await focusStep(); }
function selectModel(event: Event) { chooseModel((event.target as HTMLInputElement).value); }
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
.BudgetPanel { @apply grid gap-4 rounded-xl border border-pxp-green/30 bg-white p-5 sm:p-8; }
.Summary { @apply font-semibold; }
.Service { @apply text-pxp-green; }
.OfferGrid { @apply grid gap-4 md:grid-cols-2 xl:grid-cols-3; }
.Possible, .Deduction { @apply grid gap-3 border-t border-pxp-green/20 pt-4; }
.Possible h3 { @apply text-xl font-semibold; }
.BudgetActions { @apply flex flex-wrap items-center gap-4; }
.PriceNote, .Orientation { @apply text-sm leading-relaxed; }
.Deduction details, .TariffCatalogue { @apply text-sm leading-relaxed; }
summary { @apply min-h-11 cursor-pointer py-2 font-semibold underline underline-offset-4; }
.Deduction details p { @apply mt-3; }
.TariffCatalogue .OfferGrid { @apply mt-4; }
.Budget { @apply text-4xl leading-tight; }
.MicroNote { @apply border-l-2 border-pxp-green pl-4 leading-relaxed; }
.Frame { @apply text-sm leading-relaxed; }
.RequestButton { @apply min-h-12 w-fit rounded-md bg-pxp-green px-5 py-3 font-semibold text-white hover:bg-pxp-ink; }
.GridVersion { @apply break-words text-xs; }
.RequestPanel { @apply grid max-w-3xl gap-5; }
.JourneyActions { @apply flex flex-wrap items-center gap-x-6 gap-y-2 text-sm; }
.TextButton, .JourneyActions a { @apply min-h-11 py-2 text-pxp-green underline underline-offset-4; }
.ModelChoice { @apply grid max-w-md gap-2; }
.ModelChoice input { @apply min-h-11 border border-pxp-green/30 bg-white p-2; }
button:focus-visible, a:focus-visible, select:focus-visible, input:focus-visible, summary:focus-visible, h1:focus, h2:focus { @apply outline-2 outline-offset-4 outline-pxp-green; }
</style>
