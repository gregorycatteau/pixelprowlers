<template>
  <SiteShell>
    <main class="contact-page">
      <section class="about-hero" aria-labelledby="confirmation-title">
        <div class="article-container">
          <p class="eyebrow">Ticket ouvert</p>
          <h1 id="confirmation-title">Merci. On a reçu votre demande.</h1>
          <p>Voici votre numéro de ticket. On vous recontacte rapidement.</p>
        </div>
      </section>

      <section class="manifest-section" aria-labelledby="confirmation-ticket-title">
        <div class="article-container">
          <div v-if="isLoading" class="contact-panel">
            <h2 id="confirmation-ticket-title">Chargement du ticket.</h2>
          </div>
          <div v-else-if="error" class="contact-panel">
            <h2 id="confirmation-ticket-title">Ticket introuvable.</h2>
            <p>{{ error }}</p>
            <AppButton href="/contact">Réessayer</AppButton>
          </div>
          <div v-else-if="ticket" class="contact-panel">
            <h2 id="confirmation-ticket-title">Ticket ID : {{ ticket.ticketId }}</h2>
            <p>{{ contactEmailLabel(ticket) }} : {{ maskEmail(ticket.email) }}</p>
            <div class="result-actions">
              <AppButton :href="`/ticket/${ticket.secretToken}`">Consulter votre ticket</AppButton>
              <AppButton variant="secondary" href="/">Retour à l'accueil</AppButton>
              <AppButton variant="secondary" href="/diagnostic-situation">Faire le diagnostic</AppButton>
            </div>
          </div>
        </div>
      </section>
    </main>
  </SiteShell>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import SiteShell from '~/components/layout/SiteShell.vue';
import AppButton from '~/components/ui/AppButton.vue';
import { contactEmailLabel, useContactTicket } from '~/composables/useContact';
import { maskEmail } from '~/utils/formatDate';

const route = useRoute();
const { ticket, error, isLoading, load } = useContactTicket();

onMounted(() => {
  load(typeof route.query.token === 'string' ? route.query.token : '');
});
</script>
