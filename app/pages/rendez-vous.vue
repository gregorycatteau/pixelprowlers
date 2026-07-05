<template>
  <main class="RdvPage">
    <section class="RdvHero" aria-labelledby="rdv-title">
      <p class="RdvKicker">Prendre rendez-vous</p>
      <h1 id="rdv-title" class="RdvTitle">Choisis le bon moment, on s'occupe du reste.</h1>
      <p class="RdvIntro">Un créneau clair, un motif précis, et un rappel avant l'échange.</p>
    </section>

    <section class="RdvLayout" aria-label="Réservation de rendez-vous">
      <section class="CalendarPanel" aria-labelledby="calendar-title">
        <div class="CalendarHeader">
          <button class="CalendarNav" type="button" aria-label="Mois précédent" @click="moveMonth(-1)">‹</button>
          <h2 id="calendar-title" class="CalendarTitle">{{ monthLabel }}</h2>
          <button class="CalendarNav" type="button" aria-label="Mois suivant" @click="moveMonth(1)">›</button>
        </div>

        <div class="CalendarWeekdays" aria-hidden="true">
          <span v-for="day in weekdays" :key="day" class="WeekdayLabel">{{ day }}</span>
        </div>

        <div class="CalendarGrid">
          <button
            v-for="day in calendarCells"
            :key="day.key"
            class="CalendarDay"
            :class="[day.statusClass, { SelectedDay: day.iso === selectedDate }]"
            type="button"
            :disabled="!day.inMonth"
            @click="selectDate(day.iso)"
          >
            <span class="DayNumber">{{ day.label }}</span>
            <span class="DayStatus">{{ day.statusLabel }}</span>
          </button>
        </div>

        <div class="CalendarLegend">
          <span class="LegendItem LegendFree">Libre</span>
          <span class="LegendItem LegendAudit">Audit</span>
          <span class="LegendItem LegendIntervention">Intervention</span>
          <span class="LegendItem LegendClosed">Fermé</span>
        </div>
      </section>

      <section class="BookingPanel" aria-labelledby="booking-title">
        <div v-if="confirmation" class="BookingConfirmation" role="status" aria-live="polite">
          <span class="ConfirmationBadge" aria-hidden="true"></span>
          <h2 id="booking-title" class="BookingTitle">Créneau réservé.</h2>
          <p class="BookingIntro">
            {{ confirmationDate }} · {{ confirmationSlot }} · {{ confirmation.motif.nom }}
          </p>
          <p class="ReminderText">Vous recevrez un rappel la veille et 1h avant votre RDV.</p>
        </div>

        <form v-else class="BookingForm" @submit.prevent="submitBooking">
          <div class="BookingHeader">
            <p class="RdvKicker">Votre échange</p>
            <h2 id="booking-title" class="BookingTitle">Réserver un créneau</h2>
          </div>

          <label class="BookingField">
            <span class="BookingLabel">Motif</span>
            <select v-model="selectedMotifId" required class="BookingSelect">
              <option value="">Choisir le motif</option>
              <option v-for="motif in motifs" :key="motif.id" :value="motif.id">{{ motif.nom }}</option>
            </select>
          </label>

          <label class="UrgencyChoice">
            <input v-model="isUrgent" type="checkbox">
            <span>C'est urgent</span>
          </label>
          <p v-if="isUrgent" class="UrgencyNote">Un tarif d'urgence peut s'appliquer. Vous serez recontacté pour confirmation du tarif.</p>

          <div class="SlotsBlock">
            <p class="BookingLabel">Créneaux disponibles le {{ selectedDateLabel }}</p>
            <p v-if="!selectedMotifId" class="EmptyState">Choisissez un motif pour afficher les créneaux.</p>
            <p v-else-if="isLoadingSlots" class="EmptyState">Chargement des créneaux...</p>
            <p v-else-if="daySlots.length === 0" class="EmptyState">Aucun créneau disponible ce jour-là.</p>
            <div v-else class="SlotsGrid">
              <button
                v-for="slot in daySlots"
                :key="slotKey(slot)"
                type="button"
                class="SlotButton"
                :class="{ SelectedSlot: selectedSlot && slotKey(selectedSlot) === slotKey(slot) }"
                @click="selectedSlot = slot"
              >
                {{ slot.label }}
              </button>
            </div>
          </div>

          <div class="BookingGrid">
            <label class="BookingField">
              <span class="BookingLabel">Prénom</span>
              <input v-model="form.prenom" required class="BookingInput" type="text" autocomplete="given-name" placeholder="Prénom utilisé au téléphone">
            </label>
            <label class="BookingField">
              <span class="BookingLabel">Nom</span>
              <input v-model="form.nom" required class="BookingInput" type="text" autocomplete="family-name" placeholder="Pour éviter les homonymes">
            </label>
            <label class="BookingField">
              <span class="BookingLabel">Email</span>
              <input v-model="form.email" required class="BookingInput" type="email" autocomplete="email" placeholder="Invitation et rappels">
            </label>
            <label class="BookingField">
              <span class="BookingLabel">Téléphone</span>
              <input v-model="form.telephone" required class="BookingInput" type="tel" autocomplete="tel" placeholder="Numéro utile pour le rappel">
            </label>
          </div>

          <fieldset class="ReasonsGroup">
            <legend class="BookingLabel">Raisons de l'appel</legend>
            <label v-for="raison in raisons" :key="raison.id" class="ReasonChoice">
              <input v-model="form.raisonIds" type="checkbox" :value="raison.id">
              <span>{{ raison.nom }}</span>
            </label>
          </fieldset>

          <label class="BookingField">
            <span class="BookingLabel">Message</span>
            <textarea v-model="form.message" class="BookingTextarea" rows="4" placeholder="Le contexte utile avant qu'on se parle"></textarea>
          </label>

          <AppButton variant="validate" type="submit" :disabled="!canSubmit || isSubmitting" :loading="isSubmitting">
            {{ isSubmitting ? 'Réservation...' : 'Je réserve mon créneau' }}
          </AppButton>

          <p v-if="bookingError" class="BookingError" role="alert">{{ bookingError }}</p>
        </form>
      </section>
    </section>
  </main>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue';
import AppButton from '~/components/ui/AppButton.vue';

type Motif = { id: number; nom: string; duree_minutes: number; creneau_type: string };
type Raison = { id: number; nom: string };
type DayState = { date: string; statut: string };
type Slot = { date: string; heure_debut: string; heure_fin: string; label: string };
type BookingResponse = {
  motif: Motif;
  creneaux: Array<{ date: string; heure_debut: string; heure_fin: string }>;
};

const weekdays = ['L', 'M', 'M', 'J', 'V', 'S', 'D'];
const today = new Date();
const currentMonth = ref(new Date(today.getFullYear(), today.getMonth(), 1));
const selectedDate = ref(toIsoDate(today));
const selectedMotifId = ref<number | ''>('');
const selectedSlot = ref<Slot | null>(null);
const isUrgent = ref(false);
const motifs = ref<Motif[]>([]);
const raisons = ref<Raison[]>([]);
const monthStates = ref<DayState[]>([]);
const slots = ref<Slot[]>([]);
const isLoadingSlots = ref(false);
const isSubmitting = ref(false);
const bookingError = ref('');
const confirmation = ref<BookingResponse | null>(null);
const form = reactive({
  prenom: '',
  nom: '',
  email: '',
  telephone: '',
  raisonIds: [] as number[],
  message: '',
});

const monthLabel = computed(() => new Intl.DateTimeFormat('fr-FR', { month: 'long', year: 'numeric' }).format(currentMonth.value));
const selectedDateLabel = computed(() => new Intl.DateTimeFormat('fr-FR', { day: '2-digit', month: 'long' }).format(new Date(selectedDate.value)));
const selectedMotif = computed(() => motifs.value.find((motif) => motif.id === Number(selectedMotifId.value)));
const daySlots = computed(() => slots.value.filter((slot) => slot.date === selectedDate.value));
const canSubmit = computed(() => Boolean(selectedMotif.value && selectedSlot.value && form.prenom && form.nom && form.email && form.telephone));
const confirmationDate = computed(() => confirmation.value?.creneaux[0] ? new Intl.DateTimeFormat('fr-FR', { day: '2-digit', month: 'long', year: 'numeric' }).format(new Date(confirmation.value.creneaux[0].date)) : '');
const confirmationSlot = computed(() => confirmation.value?.creneaux[0] ? `${confirmation.value.creneaux[0].heure_debut} - ${confirmation.value.creneaux[0].heure_fin}` : '');

const calendarCells = computed(() => {
  const first = currentMonth.value;
  const startOffset = (first.getDay() + 6) % 7;
  const cells = [];
  const states = new Map(monthStates.value.map((day) => [day.date, day.statut]));

  for (let index = 0; index < 42; index += 1) {
    const date = new Date(first.getFullYear(), first.getMonth(), index - startOffset + 1);
    const iso = toIsoDate(date);
    const inMonth = date.getMonth() === first.getMonth();
    const status = states.get(iso) || 'ferme';
    cells.push({
      key: iso,
      iso,
      inMonth,
      label: String(date.getDate()),
      statusLabel: statusLabel(status),
      statusClass: `DayStatus${status}`,
    });
  }
  return cells;
});

watch(currentMonth, loadMonth, { immediate: true });
watch([selectedMotifId, isUrgent], loadSlots);
watch(selectedDate, () => {
  selectedSlot.value = null;
  if (selectedMotifId.value) loadSlots();
});

onMounted(async () => {
  const [motifData, raisonData] = await Promise.all([
    $fetch<Motif[]>('/api/motifs'),
    $fetch<Raison[]>('/api/raisons-appel'),
  ]);
  motifs.value = motifData;
  raisons.value = raisonData;
});

function toIsoDate(value: Date) {
  const year = value.getFullYear();
  const month = String(value.getMonth() + 1).padStart(2, '0');
  const day = String(value.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

function statusLabel(status: string) {
  return {
    libre: 'Libre',
    partiel: 'Partiel',
    complet: 'Complet',
    audit: 'Audit',
    intervention: 'Intervention',
    ferme: 'Fermé',
  }[status] || 'Fermé';
}

function moveMonth(delta: number) {
  currentMonth.value = new Date(currentMonth.value.getFullYear(), currentMonth.value.getMonth() + delta, 1);
}

function selectDate(iso: string) {
  selectedDate.value = iso;
}

function slotKey(slot: Slot) {
  return `${slot.date}-${slot.heure_debut}-${slot.heure_fin}`;
}

async function loadMonth() {
  const response = await $fetch<{ results: DayState[] }>('/api/calendrier/mois', {
    query: {
      annee: currentMonth.value.getFullYear(),
      mois: currentMonth.value.getMonth() + 1,
    },
  });
  monthStates.value = response.results;
}

async function loadSlots() {
  selectedSlot.value = null;
  if (!selectedMotifId.value) {
    slots.value = [];
    return;
  }
  isLoadingSlots.value = true;
  try {
    const start = selectedDate.value;
    const endDate = new Date(selectedDate.value);
    endDate.setDate(endDate.getDate() + 14);
    const response = await $fetch<{ results: Slot[] }>('/api/creneaux/disponibles', {
      query: {
        motif: selectedMotifId.value,
        date_debut: start,
        date_fin: toIsoDate(endDate),
        urgence: isUrgent.value ? '1' : '0',
      },
    });
    slots.value = response.results;
  } finally {
    isLoadingSlots.value = false;
  }
}

async function submitBooking() {
  if (!selectedSlot.value || !selectedMotif.value) return;
  isSubmitting.value = true;
  bookingError.value = '';
  try {
    confirmation.value = await $fetch<BookingResponse>('/api/rdv/reserver', {
      method: 'POST',
      body: {
        motif_id: selectedMotif.value.id,
        date: selectedSlot.value.date,
        heure_debut: selectedSlot.value.heure_debut,
        heure_fin: selectedSlot.value.heure_fin,
        urgence: isUrgent.value,
        prenom: form.prenom,
        nom: form.nom,
        email: form.email,
        telephone: form.telephone,
        raison_ids: form.raisonIds,
        message: form.message,
      },
    });
    await loadMonth();
  } catch (error) {
    bookingError.value = typeof error === 'object' && error && 'statusMessage' in error
      ? String(error.statusMessage)
      : 'Impossible de réserver ce créneau pour le moment.';
  } finally {
    isSubmitting.value = false;
  }
}
</script>

<style scoped>
@reference "../assets/css/main.css";

.RdvPage {
  @apply overflow-x-hidden bg-[#efe8d6] text-[#17251d];
}

.RdvHero,
.RdvLayout {
  @apply mx-auto w-[min(1180px,calc(100%_-_32px))] max-w-full;
}

.RdvHero {
  @apply grid gap-4 py-14;
}

.RdvKicker,
.BookingLabel {
  @apply text-sm font-black uppercase tracking-wide text-[#2b7053];
}

.RdvTitle {
  @apply max-w-[850px] text-[clamp(2.2rem,5vw,4.5rem)] font-black leading-tight;
}

.RdvIntro,
.BookingIntro,
.ReminderText,
.EmptyState {
  @apply max-w-[760px] text-base font-bold leading-relaxed text-[#435046];
}

.RdvLayout {
  @apply grid min-w-0 gap-6 pb-16;
}

.CalendarPanel,
.BookingPanel {
  @apply min-w-0 rounded-lg border border-white/70 bg-[#fbfaf5]/90 p-4 shadow-[0_22px_60px_rgb(23_37_29/0.14)] backdrop-blur-xl;
}

.BookingPanel {
  container-type: inline-size;
}

.CalendarHeader {
  @apply mb-5 flex min-w-0 items-center justify-between gap-3;
}

.CalendarTitle,
.BookingTitle {
  @apply min-w-0 text-2xl font-black capitalize;
}

.CalendarNav {
  @apply grid h-11 w-11 place-items-center rounded-lg border border-[#2b7053]/20 bg-white text-2xl font-black text-[#2b7053] transition hover:bg-[#2b7053] hover:text-white;
}

.CalendarWeekdays,
.CalendarGrid {
  @apply grid w-full min-w-0 grid-cols-7 gap-[3px];
}

.WeekdayLabel {
  @apply py-2 text-center text-xs font-black uppercase text-[#435046]/70;
}

.CalendarDay {
  @apply grid min-h-[48px] min-w-0 content-start overflow-hidden rounded-lg border border-[#2b7053]/10 bg-white p-1 text-left transition hover:-translate-y-0.5 hover:border-[#2b7053]/40;
}

.CalendarDay:disabled {
  @apply cursor-not-allowed opacity-35 hover:translate-y-0;
}

.DayNumber {
  @apply text-base font-black;
}

.DayStatus {
  @apply hidden text-[0.47rem] font-black uppercase tracking-normal;
}

.DayStatuslibre {
  @apply bg-[#f7fff9];
}

.DayStatuspartiel,
.DayStatusaudit {
  @apply bg-[#fff4d6];
}

.DayStatusintervention {
  @apply bg-[#ffe2dc];
}

.DayStatusferme,
.DayStatuscomplet {
  @apply bg-[#ece8dc];
}

.SelectedDay {
  @apply border-[#2b7053] ring-2 ring-[#2b7053]/20;
}

.CalendarLegend {
  @apply mt-5 flex flex-wrap gap-2;
}

.LegendItem {
  @apply rounded-lg px-3 py-2 text-xs font-black uppercase tracking-wide;
}

.LegendFree {
  @apply bg-[#f7fff9] text-[#2b7053];
}

.LegendAudit {
  @apply bg-[#fff4d6] text-[#8a5a00];
}

.LegendIntervention {
  @apply bg-[#ffe2dc] text-[#9f2d1c];
}

.LegendClosed {
  @apply bg-[#ece8dc] text-[#5b5b55];
}

.BookingForm,
.BookingConfirmation,
.BookingHeader,
.SlotsBlock,
.ReasonsGroup,
.BookingField {
  @apply grid gap-3;
}

.BookingGrid {
  @apply grid gap-4;
}

.BookingInput,
.BookingSelect,
.BookingTextarea {
  @apply w-full min-w-0 rounded-lg border border-[#2b7053]/18 bg-white text-[#17251d] outline-none transition focus:border-[#2b7053] focus:ring-2 focus:ring-[#2b7053]/20;
  box-sizing: border-box;
}

.BookingInput,
.BookingSelect {
  @apply min-h-12;
}

.BookingInput {
  @apply px-3;
  padding-right: 3rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.BookingSelect {
  @apply px-3;
  padding-right: 2.75rem;
}

.BookingTextarea {
  @apply px-3 py-3;
}

.BookingInput::placeholder,
.BookingTextarea::placeholder {
  @apply text-[0.72rem] font-bold text-[#435046]/55;
}

.BookingInput::placeholder {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.UrgencyChoice,
.ReasonChoice {
  @apply flex items-start gap-3 rounded-lg border border-[#2b7053]/15 bg-white/95 p-3 font-bold text-[#27322a];
  min-width: 0;
}

.UrgencyChoice span,
.ReasonChoice span {
  min-width: 0;
}

.UrgencyNote {
  @apply rounded-lg border border-[#d78a24]/25 bg-[#fff4d6] p-3 text-sm font-bold text-[#7a4b00];
}

.SlotsGrid {
  @apply flex flex-wrap gap-2;
}

.SlotButton {
  @apply rounded-lg border border-[#2b7053]/20 bg-white px-4 py-3 text-sm font-black text-[#2b7053] transition hover:-translate-y-0.5 hover:bg-[#f7fff9];
}

.SelectedSlot {
  @apply border-[#2b7053] bg-[#2b7053] text-white;
}

.ReasonsGroup {
  @apply border-0 p-0;
}

.BookingError {
  @apply rounded-lg border border-[#d93622]/25 bg-[#d93622]/10 p-4 font-bold text-[#7c2418];
}

.ConfirmationBadge {
  @apply grid h-16 w-16 place-items-center rounded-full bg-[#2b7053] text-3xl font-black text-white;
}

.ConfirmationBadge::before {
  content: "✓";
}

@container (min-width: 560px) {
  .BookingGrid {
    @apply grid-cols-2;
  }
}

@media (min-width: 640px) {
  .CalendarPanel,
  .BookingPanel {
    @apply p-5;
  }

  .CalendarWeekdays,
  .CalendarGrid {
    @apply gap-2;
  }

  .CalendarDay {
    @apply min-h-[72px] content-between p-2;
  }

  .DayStatus {
    @apply block text-[0.66rem] tracking-wide;
  }

  .DayNumber {
    @apply text-lg;
  }
}

@media (min-width: 1020px) {
  .RdvLayout {
    @apply grid-cols-[minmax(0,1fr)_440px] items-start;
  }
}
</style>
