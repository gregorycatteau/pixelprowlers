<template>
  <main class="ticket-page">
    <section class="about-hero" aria-labelledby="ticket-title">
      <div class="article-container">
        <p class="eyebrow">Suivi ticket</p>
        <h1 id="ticket-title">{{ ticket?.ticketId || 'Votre ticket' }}</h1>
        <p>Consultez le statut et ajoutez un message si besoin.</p>
      </div>
    </section>

    <section class="manifest-section" aria-labelledby="ticket-detail-title">
      <div class="article-container">
        <div v-if="isLoading" class="contact-panel">
          <h2 id="ticket-detail-title">Chargement du ticket.</h2>
        </div>
        <div v-else-if="error" class="contact-panel">
          <h2 id="ticket-detail-title">Ticket introuvable.</h2>
          <p>{{ error }}</p>
          <AppButton href="/contact">Ouvrir un ticket</AppButton>
        </div>
        <article v-else-if="ticket" class="ticket-panel">
          <header class="ticket-header">
            <div>
              <h2 id="ticket-detail-title">{{ ticket.ticketId }}</h2>
              <p>{{ ticket.demandLabel }} · créé le {{ formatDate(ticket.createdAt) }}</p>
            </div>
            <span class="status-pill">{{ statusLabel(ticket.status) }}</span>
          </header>

          <section class="ticket-messages" aria-labelledby="ticket-messages-title">
            <h3 id="ticket-messages-title">Conversation</h3>
            <article v-for="message in ticket.messages" :key="message.id" class="ticket-message">
              <div class="ticket-message-header">
                <strong>{{ message.authorName || message.author }}</strong>
                <span>{{ formatDate(message.createdAt) }}</span>
              </div>
              <p>{{ message.message }}</p>
            </article>
          </section>

          <form class="ticket-reply" @submit.prevent="addMessage">
            <label class="text-field">
              <span>Ajouter un message</span>
              <textarea v-model="reply" required maxlength="1200" rows="5" placeholder="Votre réponse..."></textarea>
            </label>
            <AppButton variant="validate" type="submit" :disabled="!reply.trim() || isAddingReply" :loading="isAddingReply">
              {{ isAddingReply ? 'Envoi...' : 'Envoyer' }}
            </AppButton>
            <p v-if="replyError" class="form-error">{{ replyError }}</p>
          </form>
        </article>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import AppButton from '~/components/ui/AppButton.vue';
import { statusLabel, useContactTicket } from '~/composables/useContact';
import { formatDate } from '~/utils/formatDate';

const route = useRoute();
const { ticket, error, isLoading, reply, replyError, isAddingReply, load, addMessage } = useContactTicket();

onMounted(() => {
  load(String(route.params.token || ''));
});
</script>

<style scoped>
.ticket-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 18px;
  border-bottom: 1px solid rgba(43, 112, 83, 0.14);
  padding-bottom: 20px;
}

.status-pill {
  flex: 0 0 auto;
  border-radius: 999px;
  padding: 8px 12px;
  background: rgba(37, 99, 235, 0.1);
  color: #1d4ed8;
  font-size: 0.88rem;
  font-weight: 900;
}

.ticket-messages,
.ticket-reply {
  margin-top: 30px;
}

.ticket-message {
  margin-top: 14px;
  border: 1px solid rgba(43, 112, 83, 0.12);
  border-radius: 8px;
  background: white;
  padding: 16px;
}

.ticket-message-header {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 8px;
  color: #596158;
  font-size: 0.92rem;
}
</style>
