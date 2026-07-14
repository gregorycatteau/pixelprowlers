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
        <div v-else-if="confirmation" class="contact-panel">
          <h2 id="confirmation-ticket-title">Numéro de dossier : {{ confirmation.numeroDossier }}</h2>
          <p>{{ confirmation.message }}</p>
          <p>Vous savez maintenant par où commencer : votre site, vos accès et vos priorités vont être clarifiés.</p>
          <p>Réponse sous 24h. Sans engagement. Pas d’accès demandé sans validation.</p>
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

type ContactConfirmation = { numeroDossier: string; message: string };

const confirmation = ref<ContactConfirmation | null>(null);
const error = ref('');

onMounted(() => {
  try {
    const stored = sessionStorage.getItem('pixelprowlers-contact-confirmation');
    const parsed = stored ? JSON.parse(stored) as ContactConfirmation : null;
    if (!parsed?.numeroDossier || !/^\d{11}$/.test(parsed.numeroDossier) || !parsed.message) {
      throw new Error('invalid confirmation');
    }
    confirmation.value = parsed;
  } catch {
    error.value = "Le numéro de dossier n'est plus disponible dans cette session.";
  }
});
</script>
