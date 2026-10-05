<template>
  <main class="RepairPage">
    <section class="container RepairHero" aria-labelledby="repair-title">
      <div>
        <p class="eyebrow">Diagnostic · Micro-soudure</p>
        <h1 id="repair-title" class="pxp-font-display">Réparer, jusqu’au composant.</h1>
        <p>Une panne ne signifie pas forcément qu’il faut remplacer votre appareil. Nous examinons ce que vous observez, recherchons la cause et vous expliquons les possibilités avant de proposer une intervention.</p>
        <AppButton href="/contact?besoin=reparation">Décrire ma panne</AppButton>
        <p class="Note">Le diagnostic permet de préciser l’intervention et son coût. Vous décidez avant toute réparation.</p>
      </div>
      <EditorialImage name="microscope" alt="Illustration de micro-soudure sur une carte électronique sous microscope" caption="travail de précision" priority />
    </section>
    <section class="container RepairSection" aria-labelledby="devices-title">
      <h2 id="devices-title">Quels appareils ?</h2>
      <p>Ordinateurs portables ou fixes, téléphones et tablettes : décrivez le type d’appareil, son modèle si vous le connaissez et le symptôme observé. Vous n’avez pas besoin de vocabulaire technique pour faire une demande.</p>
    </section>
    <section class="MicroSection" aria-labelledby="micro-title">
      <div class="container MicroLayout">
        <EditorialImage name="composant" alt="Illustration d’une intervention sur un composant de carte mère" caption="réparation au composant" />
        <div><p class="eyebrow">La précision au service du réemploi</p><h2 id="micro-title" class="pxp-font-display">La micro-soudure, simplement.</h2><p>C’est une intervention sur les composants de la carte mère lorsque le diagnostic la justifie. Le travail de précision sous microscope permet d’intervenir à cette échelle, plutôt que de remplacer systématiquement une carte entière.</p><p>L’examen détermine si cette réparation est adaptée au matériel et à la panne.</p></div>
      </div>
    </section>
    <section class="container RepairSection" aria-labelledby="symptoms-title">
      <h2 id="symptoms-title">Qu’est-ce qui ne fonctionne plus ?</h2>
      <p>Appareil qui ne démarre plus, charge intermittente, connecteur défaillant, écran cassé, autonomie réduite ou ralentissements : ces observations donnent un point de départ au diagnostic. Signalez aussi une chute ou un contact avec un liquide, sans démonter l’appareil pour chercher la cause.</p>
      <p class="Safety"><strong>Batterie gonflée ou chauffe anormale :</strong> ne rechargez plus l’appareil et signalez-le dans votre demande.</p>
    </section>
    <section class="container RepairSection" aria-labelledby="method-title">
      <h2 id="method-title">Trois étapes, avec votre accord</h2>
      <ol class="Steps"><li><h3>1. Examiner</h3><p>Nous partons de votre description, puis examinons le matériel pour préciser la panne.</p></li><li><h3>2. Expliquer</h3><p>Vous recevez une proposition adaptée ; vous validez son périmètre et son coût.</p></li><li><h3>3. Intervenir</h3><p>Nous réalisons l’intervention convenue et expliquons ce qui a été fait et les précautions utiles.</p></li></ol>
    </section>
    <section class="container RepairSection Faq" aria-labelledby="faq-title">
      <h2 id="faq-title">Avant de confier votre appareil</h2>
      <details><summary>Le diagnostic garantit-il une réparation ?</summary><p>Non. Il sert à comprendre la panne et à évaluer ce qui peut raisonnablement être réparé.</p></details>
      <details><summary>Comment protéger mes données ?</summary><p>Ne transmettez aucun mot de passe, code de déverrouillage ou clé de récupération. Une sauvegarde peut être recommandée. Tout accès nécessaire est défini séparément, avec votre accord ; vous déverrouillez vous-même votre appareil.</p></details>
      <details><summary>Puis-je décider après la proposition ?</summary><p>Oui. L’intervention commence après votre accord sur ce qui est proposé.</p></details>
      <details><summary>Et si l’appareil n’est pas réparable ?</summary><p>Nous vous expliquons les limites constatées et les possibilités de réemploi ou d’orientation vers une filière adaptée.</p></details>
    </section>
  </main>
</template>

<script setup lang="ts">
import AppButton from '~/components/ui/AppButton.vue';
import EditorialImage from '~/components/sections/EditorialImage.vue';
useSeoMeta({ title: 'Réparation informatique et micro-soudure | PixelProwlers', description: 'Diagnostic d’ordinateurs, téléphones et tablettes, réparation au composant et micro-soudure lorsque la panne le justifie.', robots: 'index, follow', ogUrl: 'https://pixelprowlers.io/reparation-informatique' });
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
.RepairSection { @apply py-10 md:py-14; }
.MicroSection { @apply bg-pxp-ink py-12 text-pxp-paper; }
.MicroLayout { @apply grid items-center gap-10 md:grid-cols-2; }
.MicroLayout p + p { @apply mt-4; }
.MicroLayout .eyebrow { @apply text-[#a8d5bd]; }
.Steps { @apply grid list-none gap-6 p-0 md:grid-cols-3; }
.Safety { @apply mt-6 rounded-lg border border-pxp-green/30 bg-white p-5; }
.Faq details { @apply border-t border-pxp-green/25 py-4; }
.Faq summary { @apply cursor-pointer font-bold; }
.Faq summary:focus-visible { @apply outline-2 outline-offset-4 outline-pxp-green; }
.Faq details p { @apply mt-4 max-w-3xl; }
.container { @apply mx-auto w-[min(1320px,calc(100%-32px))]; }
:deep(.ButtonPrimary) { @apply bg-pxp-green text-white hover:bg-pxp-ink focus-visible:ring-pxp-green; }
</style>
