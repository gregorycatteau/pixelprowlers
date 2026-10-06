<template>
  <div class="HomeSections">
    <section id="atelier" class="Workshop container" aria-labelledby="workshop-title">
      <h2 id="workshop-title" class="pxp-font-display">Ça vous arrive ?</h2>
      <div class="Symptoms"><article><h3>Il ne démarre plus.</h3><p>Écran noir, arrêt soudain : recherchons la cause.</p></article><article><h3>Il ne charge plus.</h3><p>Un connecteur ou un composant peut être en cause.</p></article><article><h3>Il fonctionne mal.</h3><p>Ralentissements, autonomie réduite : faisons le point.</p></article></div>
      <div class="WorkshopGrid">
        <article class="WorkshopCard"><EditorialImage name="composant" alt="Illustration d’une soudure de précision sur un composant électronique" caption="réparation au composant" /><div class="CardCopy"><p class="eyebrow">Réparation · Micro-soudure</p><h3 class="pxp-font-display">Réparer plus finement.</h3><p>La panne d’une carte mère ne condamne pas forcément l’appareil. Le diagnostic détermine si une intervention ciblée, sous microscope, peut prolonger sa vie.</p><NuxtLink class="EditorialLink" to="/reparation-informatique">Comprendre la micro-soudure ↗</NuxtLink></div></article>
        <article class="WorkshopCard WorkshopCardOffset"><EditorialImage name="reemploi" alt="Illustration de la remise en état d’un ordinateur portable" caption="réemploi, hors fiche de vente" /><div class="CardCopy"><p class="eyebrow">Matériel reconditionné</p><h3 class="pxp-font-display">Votre prochain ordinateur a déjà une histoire.</h3><p>Quotidien, études ou travail : cherchons du matériel adapté à vos usages. Caractéristiques, tests et défauts connus vous sont présentés avant votre choix.</p><NuxtLink class="EditorialLink" to="/contact?besoin=reemploi">Trouver mon ordinateur ↗</NuxtLink></div></article>
      </div>
    </section>
    <section class="Person container" aria-labelledby="person-title"><img src="/images/about/parcours.jpg" alt="Grégory Catteau en randonnée" width="896" height="1183" loading="lazy" decoding="async"><div><p class="eyebrow">Votre interlocuteur</p><h2 id="person-title" class="pxp-font-display">Grégory, avec vous.</h2><p>Écouter, examiner, expliquer : je relie réparation, développement et transmission pour rendre vos outils utiles plus longtemps.</p><NuxtLink class="EditorialLink" to="/a-propos">Faire connaissance ↗</NuxtLink></div></section>
    <section id="numerique" class="Digital" aria-labelledby="digital-title"><div class="container"><h2 id="digital-title" class="pxp-font-display">Et pour vos autres outils ?</h2><div class="DigitalGrid"><article v-for="offer in offers" :key="offer.href"><h3>{{ offer.title }}</h3><p>{{ offer.description }}</p><NuxtLink class="EditorialLink" :to="offer.href">{{ offer.cta }} ↗</NuxtLink></article></div></div></section>
    <section id="contact" class="Contact" aria-labelledby="contact-title"><div class="container ContactInner"><div><h2 id="contact-title" class="pxp-font-display">Commençons par votre panne.</h2><p>Décrivez ce que vous observez. Nous convenons ensemble de la prise en charge.</p></div><AppButton href="/contact?besoin=reparation">Décrire ma panne</AppButton></div></section>
  </div>
</template>
<script setup lang="ts">
import AppButton from '~/components/ui/AppButton.vue';
import EditorialImage from '~/components/sections/EditorialImage.vue';
const offers = [
  { title: 'Conseil & cybersécurité', description: 'Résoudre une difficulté et sécuriser vos usages.', href: '/services-numeriques#conseil-cybersecurite', cta: 'Faire le point' },
  { title: 'Développement', description: 'Un site ou un outil conçu pour votre activité.', href: '/services-numeriques#developpement', cta: 'Parler de mon projet' },
  { title: 'Formation', description: 'Pratiquer pour être plus autonome au quotidien.', href: '/formations', cta: 'Découvrir les ateliers' },
] as const;
</script>
<style scoped>
@reference "../../assets/css/main.css";
.Workshop { @apply py-12 md:py-16; }
h2 { @apply mb-8; font-size: clamp(2.5rem, 4vw, 4rem); line-height: 1.05; }
.Symptoms { @apply mb-10 grid gap-6 md:grid-cols-3; }
.Symptoms article { @apply border-t border-pxp-green/30 pt-4; }
h3 { @apply mb-3 text-xl font-bold; }
p { @apply leading-relaxed; }
.WorkshopGrid { @apply grid items-start gap-8 md:grid-cols-2 md:gap-12; }
.WorkshopCard { @apply bg-pxp-panel; }
.WorkshopCardOffset { @apply md:mt-16; }
.CardCopy { @apply grid gap-4 p-6 md:p-8; }
.CardCopy h3 { @apply m-0 text-4xl leading-none md:text-5xl; }
.EditorialLink { @apply inline-flex min-h-11 w-fit items-center gap-3 font-semibold text-pxp-green underline underline-offset-4 hover:text-pxp-ink focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-pxp-green; }
.Person { @apply grid items-center gap-8 pb-14 md:grid-cols-[240px_1fr] md:gap-12; }
.Person img { @apply aspect-[4/3] w-full max-w-xs object-cover object-[50%_35%] md:aspect-square; }
.Person p { @apply max-w-2xl; }
.Person h2 { @apply my-4; }
.Digital { @apply border-y border-pxp-green/15 bg-[#ebe9df] py-12 md:py-16; }
.DigitalGrid { @apply grid gap-8 md:grid-cols-3; }
.DigitalGrid article { @apply grid content-start gap-3 border-t border-pxp-green/30 pt-5; }
.Contact { @apply bg-pxp-ink py-12 text-pxp-paper; }
.ContactInner { @apply grid items-center gap-8 md:grid-cols-[1fr_auto]; }
.ContactInner h2 { @apply mb-4; }
.Contact :deep(.ButtonPrimary) { @apply bg-pxp-paper text-pxp-ink hover:bg-white focus-visible:ring-white; }
</style>
