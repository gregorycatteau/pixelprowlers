<template>
  <main class="result-page">
    <section class="diagnostic-hero" aria-labelledby="result-title">
      <div class="form-container">
        <p class="eyebrow">Diagnostic personnalisé</p>
        <h1 id="result-title">Votre demande est prise en charge.</h1>
        <p>Vous savez maintenant par où commencer. Un expert va analyser votre situation.</p>
        <p v-if="ticket" class="ticket-pill">Ticket de suivi : {{ ticket.id }}</p>
      </div>
    </section>

    <section class="result-section" aria-labelledby="result-analysis-title">
      <div class="form-container">
        <div v-if="isLoading" class="result-panel">
          <p class="result-kicker">Chargement</p>
          <h2 id="result-analysis-title">On récupère votre diagnostic.</h2>
        </div>

        <div v-else-if="error" class="result-panel">
          <p class="result-kicker">Ticket introuvable</p>
          <h2 id="result-analysis-title">On ne trouve pas cette réponse.</h2>
          <p>{{ error }}</p>
          <AppButton href="/diagnostic-situation">Relancer le diagnostic</AppButton>
        </div>

        <article v-else-if="content && ticket" class="result-panel">
          <p class="result-kicker">{{ content.kicker }}</p>
          <h2 id="result-analysis-title">{{ content.title }}</h2>
          <p class="context-copy">{{ content.context }}</p>

          <div class="advice-block">
            <h3>Notre conseil</h3>
            <p><strong>{{ content.advice }}</strong></p>
            <ul class="plain-list good-list">
              <li v-for="reason in content.reasons" :key="reason">{{ reason }}</li>
            </ul>
          </div>

          <div class="option-grid">
            <section class="option-box">
              <h3>Option A : {{ content.pixelTitle }}</h3>
              <ul>
                <li v-for="item in content.pixelItems" :key="item">{{ item }}</li>
              </ul>
              <p class="decision-copy">Chaque semaine sans correction augmente le risque de blocage ou de perte.</p>
              <p class="decision-copy">Vous savez exactement quoi faire, dans le bon ordre.</p>
              <AppButton :href="content.ctaHref">{{ content.cta }}</AppButton>
              <p class="cta-note">Réponse sous 24h. Sans engagement. Pas d’accès demandé sans validation.</p>
            </section>

            <section class="option-box muted">
              <h3>Option B : Vous pouvez aussi</h3>
              <ul>
                <li v-for="item in content.alternativeItems" :key="item">{{ item }}</li>
              </ul>
              <p><strong>Notre conseil honnête :</strong> {{ content.honestAdvice }}</p>
            </section>
          </div>

          <footer class="result-footer">
            <h2>Vous voulez avancer ?</h2>
            <div class="result-actions">
              <AppButton :href="content.ctaHref">{{ content.cta }}</AppButton>
              <AppButton variant="secondary" href="/contact">Être accompagné sur mon problème</AppButton>
            </div>
            <p class="cta-note">Vous retrouvez le contrôle de votre site. Vous ne partagez jamais vos accès sans cadre clair. Aucune modification sans votre accord.</p>
            <p>
              Ticket de suivi : <strong>{{ ticket.id }}</strong><br>
              {{ emailConfirmationLabel(ticket) }} : {{ maskedEmail }}<br>
              Vous pouvez revenir à cette page quand vous voulez.
            </p>
          </footer>
        </article>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import AppButton from '~/components/ui/AppButton.vue';
import { emailConfirmationLabel, useDiagnosticResult } from '~/composables/useDiagnostic';

const route = useRoute();
const { ticket, isLoading, error, content, maskedEmail, load } = useDiagnosticResult();

onMounted(() => {
  load(String(route.params.ticketId || ''));
});
</script>

<style scoped>
.result-section {
  padding: 48px 0 84px;
  background: #f7f4ea;
}

.result-kicker {
  color: #2b7053;
  font-size: 0.82rem;
  font-weight: 950;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.result-panel h2 {
  margin-top: 12px;
  font-size: clamp(2rem, 5vw, 3.55rem);
  line-height: 1.03;
}

.context-copy,
.result-panel > p:not(.result-kicker) {
  margin-top: 20px;
  color: #27322a;
  font-size: 1.08rem;
  line-height: 1.72;
}

.advice-block {
  margin-top: 32px;
  border-left: 5px solid #2b7053;
  padding-left: 18px;
}

.option-grid {
  display: grid;
  gap: 18px;
  margin-top: 34px;
}

.option-box {
  border: 1px solid rgba(43, 112, 83, 0.15);
  border-radius: 8px;
  background: white;
  padding: 22px;
}

.result-footer {
  margin-top: 34px;
  border-top: 1px solid rgba(43, 112, 83, 0.14);
  padding-top: 28px;
}

.ticket-pill {
  display: inline-flex;
  width: fit-content;
  border: 1px solid rgba(43, 112, 83, 0.18);
  border-radius: 8px;
  background: white;
  padding: 9px 12px;
  color: #2b4b39 !important;
  font-size: 0.95rem !important;
  font-weight: 900 !important;
}

.cta-note {
  margin-top: 12px;
  color: #596158;
  font-size: 0.94rem;
  font-weight: 800;
  line-height: 1.55;
}

.decision-copy {
  margin-top: 12px;
  color: #27322a;
  font-weight: 850;
  line-height: 1.55;
}
</style>
