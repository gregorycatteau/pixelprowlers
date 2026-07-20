<template>
  <main class="contact-page">
    <section class="about-hero" aria-labelledby="confirmation-title">
      <div class="article-container">
        <p class="eyebrow">Ticket ouvert</p>
        <h1 id="confirmation-title">Votre demande est prise en charge.</h1>
        <p>Première étape vers la reprise de contrôle. Un expert va analyser votre situation.</p>
      </div>
    </section>

    <section class="manifest-section" aria-labelledby="confirmation-ticket-title">
      <div class="article-container">
        <div v-if="error" class="contact-panel">
          <h2 id="confirmation-ticket-title">Confirmation indisponible.</h2>
          <p>{{ error }}</p>
          <AppButton href="/contact">Réessayer</AppButton>
        </div>
        <div v-else-if="confirmation" v-reveal class="contact-panel confirmation-panel">
          <h2 id="confirmation-ticket-title" class="dossier-pill">
            Numéro de dossier : {{ confirmation.numeroDossier }}
          </h2>
          <p>{{ confirmation.message }}</p>
          <p>Vous savez maintenant par où commencer : votre site, vos accès et vos priorités vont être clarifiés.</p>
          <p>Votre demande est enregistrée. Conservez votre référence de dossier. Aucun accès ne sera demandé sans validation.</p>
          <div class="result-actions">
            <AppButton variant="secondary" href="/">Retour à l'accueil</AppButton>
            <AppButton variant="secondary" href="/diagnostic-situation">Faire le diagnostic</AppButton>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import AppButton from '~/components/ui/AppButton.vue';
import {
  CONTACT_CONFIRMATION_STORAGE_KEY,
  parseStoredContactConfirmation,
  type ContactConfirmation,
} from '~/composables/useContact';

const confirmation = ref<ContactConfirmation | null>(null);
const error = ref('');

onMounted(() => {
  const stored = sessionStorage.getItem(CONTACT_CONFIRMATION_STORAGE_KEY);
  const parsed = parseStoredContactConfirmation(stored);

  if (!parsed) {
    error.value = "Le numéro de dossier n'est plus disponible dans cette session.";
    return;
  }

  confirmation.value = parsed;
});
</script>

<style scoped>
@reference "../../assets/css/main.css";

/* Accent de succès sobre : une bordure haute, pas une bannière. */
.confirmation-panel {
  border-top: 3px solid var(--color-pxp-green);
}

.dossier-pill {
  display: inline-flex;
  width: fit-content;
  border: 1px solid rgba(43, 112, 83, 0.18);
  border-radius: 8px;
  background: white;
  padding: 9px 14px;
  color: #2b4b39 !important;
  font-size: 1.05rem !important;
  font-weight: 900 !important;
}
</style>
