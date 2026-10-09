<template>
  <main class="ReusePage">
    <section class="container ReuseIntro">
      <div>
        <p class="eyebrow">Réemploi · Matériel reconditionné</p>
        <h1 class="pxp-font-display">Un ordinateur adapté à vos usages. Une seconde vie pour le matériel.</h1>
        <p>Dans le Médoc, pour le quotidien, les études ou le travail : dites-nous ce que vous voulez faire et votre budget. Nous cherchons avec vous les possibilités de réemploi et les disponibilités.</p>
        <p>Pour chaque exemplaire proposé, vous disposez des caractéristiques, des tests réalisés, de l’état et des défauts connus, avec son prix et ses photos réelles. Contactez-nous pour connaître les disponibilités.</p>
        <AppButton href="/contact?besoin=reemploi">Trouver mon ordinateur</AppButton>
      </div>
      <EditorialImage name="reemploi" alt="Illustration d’un ordinateur portable en cours de réparation" caption="réemploi, hors fiche de vente" priority />
    </section>
  </main>
</template>

<script setup lang="ts">
import AppButton from '~/components/ui/AppButton.vue';
import EditorialImage from '~/components/sections/EditorialImage.vue';
useSeoMeta({ title: 'Matériel reconditionné dans le Médoc | PixelProwlers', description: 'Un ordinateur reconditionné pour vos usages dans le Médoc : indiquez votre budget et demandez les disponibilités à PixelProwlers.' });
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
