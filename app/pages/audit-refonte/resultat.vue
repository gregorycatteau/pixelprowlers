<template>
  <main class="RefonteResultPage" aria-labelledby="refonte-result-title">
    <section class="RefonteResultPanel" aria-live="polite">
      <p class="eyebrow">Refonte · prise en charge manuelle</p>
      <h1 id="refonte-result-title">{{ result ? 'Votre demande est enregistrée.' : 'Retrouver votre demande.' }}</h1>
      <p v-if="isLoading">Récupération du dossier…</p>
      <template v-else-if="result">
        <p>Référence : {{ result.reference }}</p>
        <p class="SiteAddress">Site concerné : {{ result.site_url }}</p>
        <p>L’analyse automatique est désactivée. L’atelier dispose de votre questionnaire pour étudier votre projet et vous répondre.</p>
        <AppButton v-if="safeFollowupPath(result.followup_path)" :href="result.followup_path">Suivre ma demande et échanger</AppButton>
        <p>Conservez votre lien de suivi personnel. Il permet de lire la réponse de l’atelier et d’ajouter un message, sans compte client.</p>
      </template>
      <template v-else>
        <p role="alert">{{ error || 'La référence est manquante.' }}</p>
        <p>Cette confirmation nécessite le navigateur qui a enregistré la demande. Si vous avez conservé votre lien personnel de ticket, utilisez-le pour poursuivre l’échange.</p>
        <AppButton href="/contact">Contacter l’atelier</AppButton>
      </template>
    </section>
  </main>
</template>
<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import AppButton from '~/components/ui/AppButton.vue';
import { REFONTE_AUDIT_QUERY, graphqlErrorMessage, graphqlRequest } from '~/utils/graphql';
import { safeFollowupPath } from '~/utils/followup';
const route = useRoute();
const reference = computed(() => typeof route.query.reference === 'string' ? route.query.reference : '');
type ManualResult = { reference: string; site_url: string; followup_path: string };
const result = ref<ManualResult | null>(null);
const isLoading = ref(false);
const error = ref('');
useHead({ title: 'Votre demande de refonte | Pixelprowlers', meta: [{ name: 'robots', content: 'noindex, nofollow' }, { name: 'referrer', content: 'no-referrer' }] });
onMounted(async () => {
  if (!reference.value) return;
  isLoading.value = true;
  try {
    const response = await graphqlRequest<{ refonteAudit: ManualResult }>(REFONTE_AUDIT_QUERY, { reference: reference.value });
    result.value = response.refonteAudit;
  } catch (failure) {
    error.value = graphqlErrorMessage(failure, 'Ce dossier n’est pas accessible dans cette session.');
  } finally {
    isLoading.value = false;
  }
});
</script>
<style scoped>
@reference "../../assets/css/main.css";
.RefonteResultPage { @apply mx-auto w-full max-w-4xl px-5 py-12 sm:py-20; }
.RefonteResultPanel { @apply grid gap-6 rounded-lg border border-pxp-green/20 bg-pxp-panel p-6 sm:p-10; }
h1 { @apply text-4xl leading-tight sm:text-5xl; }
p { @apply leading-relaxed; }
.SiteAddress { @apply break-all; }
</style>
