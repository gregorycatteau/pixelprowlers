<template>
  <section class="Handoff" :class="{ HandoffCompact: compact }" aria-labelledby="handoff-title">
    <h2 id="handoff-title">Comment nous confier votre appareil ?</h2>
    <p v-if="compact">Pour une réparation, convenons des modalités de prise en charge après un premier échange. Attendez leur confirmation avant tout dépôt ou envoi.</p>
    <template v-else>
      <ol>
        <li><h3>Décrire la panne</h3><p>Indiquez l’appareil, le modèle si connu et le symptôme.</p></li>
        <li><h3>Convenir des modalités</h3><p>Lieu et mode de prise en charge se définissent après contact.</p></li>
        <li><h3>Attendre la confirmation</h3><p>Ne déposez ni n’expédiez l’appareil avant notre accord sur les modalités.</p></li>
      </ol>
      <NuxtLink class="HandoffLink" to="/contact?besoin=reparation">Décrire ma panne <span aria-hidden="true">→</span></NuxtLink>
    </template>
  </section>
</template>

<script setup lang="ts">
/** Présente les étapes du premier contact, sans supposer de modalité d’accueil. */
withDefaults(defineProps<{ compact?: boolean }>(), { compact: false });
</script>

<style scoped>
@reference "../../assets/css/main.css";
.Handoff { @apply rounded-lg border border-pxp-green/25 bg-white p-6 text-pxp-ink md:p-8; }
h2 { @apply mb-6 text-2xl font-bold md:text-3xl; }
ol { @apply m-0 grid list-none gap-6 p-0 md:grid-cols-3; }
h3 { @apply mb-2 text-lg font-bold; }
p { @apply leading-relaxed; }
.HandoffLink { @apply mt-6 inline-flex min-h-11 items-center gap-3 rounded text-pxp-green font-semibold underline underline-offset-4; }
.HandoffLink:focus-visible { @apply outline-2 outline-offset-4 outline-pxp-green; }
.HandoffCompact { @apply p-5 md:p-6; }
.HandoffCompact h2 { @apply mb-3 text-xl; }
</style>
