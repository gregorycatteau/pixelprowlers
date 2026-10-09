<template>
  <main class="RepairPage">
    <div class="container"><RepairJourney /></div>
    <div id="prise-en-charge" class="container HandoffSection"><p class="LocalNote">Une demande depuis le Médoc ? Décrivez votre panne : nous préciserons ensemble les modalités de prise en charge.</p><RepairHandoff /></div>
    <section id="micro-soudure" class="MicroSection" aria-labelledby="micro-title">
      <div class="container MicroLayout">
        <EditorialImage name="composant" alt="Illustration d’une intervention sur un composant de carte mère" caption="réparation au composant" />
        <div><p class="eyebrow">La précision au service du réemploi</p><h2 id="micro-title" class="pxp-font-display">Une carte mère en panne peut aussi se réparer.</h2><p>La micro-soudure permet d’intervenir sur certains connecteurs et composants de la carte électronique. Le diagnostic détermine si cette intervention peut prolonger la vie de votre appareil.</p><p>Un travail de précision sous microscope, guidé par la panne identifiée.</p></div>
      </div>
    </section>
    <section class="container RepairSection" aria-labelledby="symptoms-title">
      <h2 id="symptoms-title">Une précaution utile</h2>
      <p class="Safety"><strong>Batterie gonflée ou chauffe anormale :</strong> ne rechargez plus l’appareil et signalez-le dans votre demande.</p>
    </section>
    <section class="container RepairSection" aria-labelledby="method-title">
      <h2 id="method-title">Trois étapes, avec votre accord</h2>
      <ol class="Steps"><li><h3>1. Examiner</h3><p>Nous partons de votre description, puis examinons le matériel pour préciser la panne.</p></li><li><h3>2. Expliquer</h3><p>Vous recevez une proposition adaptée ; vous validez son périmètre et son coût.</p></li><li><h3>3. Intervenir</h3><p>Nous réalisons l’intervention convenue et expliquons ce qui a été fait et les précautions utiles.</p></li></ol>
    </section>
    <section class="container RepairSection Faq" aria-labelledby="faq-title">
      <h2 id="faq-title">Avant de confier votre appareil</h2>
      <details><summary>Le diagnostic garantit-il une réparation ?</summary><p>Non. Il sert à comprendre la panne et à évaluer ce qui peut raisonnablement être réparé.</p></details>
      <details><summary>Comment protéger mes données ?</summary><p>Une sauvegarde peut être recommandée. Tout accès nécessaire est défini avec votre accord. <NuxtLink to="/confidentialite">Consulter la confidentialité</NuxtLink>.</p></details>
      <details><summary>Puis-je décider après la proposition ?</summary><p>Oui. L’intervention commence après votre accord sur ce qui est proposé.</p></details>
      <details><summary>Et si l’appareil n’est pas réparable ?</summary><p>Nous vous expliquons les limites constatées et les possibilités de réemploi ou d’orientation vers une filière adaptée.</p></details>
    </section>
  </main>
</template>

<script setup lang="ts">
import RepairJourney from '~/components/repair/RepairJourney.vue';
import EditorialImage from '~/components/sections/EditorialImage.vue';
import RepairHandoff from '~/components/sections/RepairHandoff.vue';
useSeoMeta({ title: 'Réparation informatique et micro-soudure en Médoc | PixelProwlers', description: 'Réparation informatique dans le Médoc : estimez votre budget pour un ordinateur, téléphone, tablette ou console. Diagnostic et micro-soudure selon la panne.', robots: 'index, follow', ogUrl: 'https://pixelprowlers.io/reparation-informatique' });
useHead({ link: [{ rel: 'canonical', href: 'https://pixelprowlers.io/reparation-informatique' }] });
</script>

<style scoped>
@reference "../assets/css/main.css";
.RepairPage { @apply bg-pxp-paper text-pxp-ink; }
.RepairHero { @apply grid items-center gap-10 py-14 md:grid-cols-2 md:py-20; }
.RepairHero > div { @apply grid gap-6; }
h1 { @apply text-5xl leading-none md:text-6xl; }
h2 { @apply mb-5 text-3xl font-bold; }
h3 { @apply mb-3 text-xl font-bold; }
p { @apply leading-relaxed; }
.Note { @apply text-sm; }
.LocalNote { @apply mb-6 max-w-3xl text-lg leading-relaxed; }
.HandoffSection { @apply pb-4 scroll-mt-32; }
.RepairSection { @apply py-10 md:py-14; }
.MicroSection { @apply scroll-mt-32 bg-pxp-ink py-12 text-pxp-paper; }
.MicroLayout { @apply grid items-center gap-10 md:grid-cols-2; }
.MicroLayout p + p { @apply mt-4; }
.MicroLayout .eyebrow { @apply text-[#a8d5bd]; }
.Symptoms { @apply grid gap-6 md:grid-cols-3; }
.Symptoms article { @apply border-t border-pxp-green/25 pt-4; }
.Steps { @apply grid list-none gap-6 p-0 md:grid-cols-3; }
.Safety { @apply mt-6 rounded-lg border border-pxp-green/30 bg-white p-5; }
.Faq details { @apply border-t border-pxp-green/25 py-4; }
.Faq summary { @apply cursor-pointer font-bold; }
.Faq summary:focus-visible { @apply outline-2 outline-offset-4 outline-pxp-green; }
.Faq details p { @apply mt-4 max-w-3xl; }
.container { @apply mx-auto w-[min(1320px,calc(100%-32px))]; }
:deep(.ButtonPrimary) { @apply bg-pxp-green text-white hover:bg-pxp-ink focus-visible:ring-pxp-green; }
</style>
