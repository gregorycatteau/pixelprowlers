<template>
  <main class="ReusePage">
    <section class="container ReuseIntro">
      <div>
        <p class="eyebrow">Réemploi · Matériel reconditionné</p>
        <h1 class="pxp-font-display">Une seconde vie pour votre prochain ordinateur.</h1>
        <p>Nous remettons en état du matériel informatique pour prolonger son usage. Décrivez vos besoins et votre budget : nous vous indiquons les possibilités et les disponibilités.</p>
        <p>Indiquez l’usage prévu et une fourchette de budget dans le formulaire. Les caractéristiques, l’état, les défauts connus, les tests et le prix d’un exemplaire vous sont communiqués avant toute décision. Cette page est une présentation du réemploi, pas un catalogue de machines disponibles.</p>
        <AppButton href="/contact?besoin=reemploi">Demander les disponibilités</AppButton>
      </div>
      <EditorialImage name="reemploi" alt="Illustration d’un ordinateur portable en cours de réparation" caption="réemploi, hors fiche de vente" priority />
    </section>
  </main>
</template>

<script setup lang="ts">
import AppButton from '~/components/ui/AppButton.vue';
import EditorialImage from '~/components/sections/EditorialImage.vue';
useSeoMeta({ title: 'Matériel reconditionné et réemploi | PixelProwlers', description: 'Décrivez vos besoins en matériel informatique reconditionné et demandez les disponibilités à PixelProwlers.' });
useHead({ link: [{ rel: 'canonical', href: 'https://pixelprowlers.io/materiel-reconditionne' }] });
</script>

<style scoped>
@reference "../assets/css/main.css";
.ReusePage { @apply bg-pxp-paper text-pxp-ink; }
.ReuseIntro { @apply grid items-center gap-10 py-16 md:grid-cols-2 md:py-24; }
.ReuseIntro > div { @apply grid gap-6; }
h1 { @apply text-5xl leading-none md:text-6xl; }
p { @apply leading-relaxed; }
</style>
