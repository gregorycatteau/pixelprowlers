<template>
  <div class="HomeSections">
    <section id="atelier" class="Workshop container" aria-labelledby="workshop-title">
      <div class="SectionIntro">
        <p class="eyebrow">Le matériel d’abord</p>
        <h2 id="workshop-title" class="pxp-font-display">Une panne n’est pas<br>une fin de vie.</h2>
        <p>Ordinateurs, téléphones et tablettes : examiner, réparer ce qui peut l’être et prolonger les usages.</p>
      </div>
      <div class="WorkshopGrid">
        <article class="WorkshopCard">
          <EditorialImage name="composant" alt="Illustration d’une soudure de précision sur un composant électronique" caption="réparation au composant" />
          <div class="CardCopy">
            <span class="CardIndex" aria-hidden="true">01 / RÉPARER</span>
            <h3 class="pxp-font-display">Du diagnostic à la micro-soudure.</h3>
            <p>Pannes de carte mère, composants et maintenance : une intervention ciblée quand le diagnostic la justifie.</p>
            <NuxtLink class="EditorialLink" to="/reparation-informatique">Découvrir la réparation <span aria-hidden="true">↗</span></NuxtLink>
          </div>
        </article>
        <article class="WorkshopCard WorkshopCardOffset">
          <EditorialImage name="reemploi" alt="Illustration de la remise en état d’un ordinateur portable" caption="réemploi, hors fiche de vente" />
          <div class="CardCopy">
            <span class="CardIndex" aria-hidden="true">02 / RÉEMPLOYER</span>
            <h3 class="pxp-font-display">Une seconde vie, sans angle mort.</h3>
            <p>Du matériel d’occasion et reconditionné, avec ses caractéristiques, ses tests et ses défauts connus annoncés.</p>
            <NuxtLink class="EditorialLink" to="/materiel-reconditionne">Découvrir le matériel reconditionné <span aria-hidden="true">↗</span></NuxtLink>
          </div>
        </article>
      </div>
    </section>

    <section id="numerique" class="Digital" aria-labelledby="digital-title">
      <div class="container">
        <div class="SectionIntro">
          <p class="eyebrow">Au-delà du matériel</p>
          <h2 id="digital-title" class="pxp-font-display">Garder la main.<br>Sur tous vos outils.</h2>
        </div>
        <div class="DigitalGrid">
          <article v-for="offer in offers" :key="offer.href">
            <span class="CardIndex" aria-hidden="true">{{ offer.number }}</span>
            <h3>{{ offer.title }}</h3>
            <p>{{ offer.description }}</p>
            <NuxtLink class="EditorialLink" :to="offer.href">{{ offer.cta }} <span aria-hidden="true">↗</span></NuxtLink>
          </article>
        </div>
      </div>
    </section>

    <section id="methode" class="Method container" aria-labelledby="method-title">
      <div class="SectionIntro">
        <p class="eyebrow">Pas à pas</p>
        <h2 id="method-title" class="pxp-font-display">Comprendre. Puis agir.</h2>
      </div>
      <ol class="MethodGrid">
        <li><span aria-hidden="true">01</span><h3>Diagnostic</h3><p>Nous examinons votre situation avant de proposer une solution.</p></li>
        <li><span aria-hidden="true">02</span><h3>Proposition</h3><p>Vous validez le périmètre et le prix avant toute intervention.</p></li>
        <li><span aria-hidden="true">03</span><h3>Intervention</h3><p>Nous intervenons dans le cadre convenu et expliquons ce qui a été fait.</p></li>
      </ol>
      <p class="MethodNote">Vos données restent sous votre contrôle ; les accès nécessaires sont définis avec votre accord.</p>
    </section>

    <section id="contact" class="Contact" aria-labelledby="contact-title">
      <div class="container ContactInner">
        <div><p class="eyebrow">Parlons concret</p><h2 id="contact-title" class="pxp-font-display">Qu’est-ce qui vous bloque ?</h2><p>Une panne, un projet ou une question : décrivez simplement votre besoin, sans mot de passe ni code d’accès.</p></div>
        <AppButton href="/contact">Prendre contact</AppButton>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import AppButton from '~/components/ui/AppButton.vue';
import EditorialImage from '~/components/sections/EditorialImage.vue';

const offers = [
  { number: '03', title: 'Conseil & cybersécurité', description: 'Choisir vos outils, résoudre une difficulté et examiner les risques dans un périmètre autorisé.', href: '/services-numeriques#conseil-cybersecurite', cta: 'Faire le point' },
  { number: '04', title: 'Développement', description: 'Des sites, applications et outils métier maintenables, construits à partir de vos usages réels.', href: '/services-numeriques#developpement', cta: 'Parler de mon projet' },
  { number: '05', title: 'Formation & ateliers', description: 'Comprendre, pratiquer et devenir autonome, avec des repères que vous pouvez réutiliser.', href: '/formations', cta: 'Découvrir les formations' },
] as const;
</script>

<style scoped>
@reference "../../assets/css/main.css";
.Workshop, .Method { @apply py-16 md:py-24; }
.SectionIntro { @apply mb-10 grid max-w-2xl gap-4; }
h2 { font-size: clamp(2.8rem, 5vw, 4.8rem); line-height: 1; }
.SectionIntro > p:last-child { @apply max-w-lg leading-relaxed; }
.WorkshopGrid { @apply grid items-start gap-8 md:grid-cols-2 md:gap-12; }
.WorkshopCard { @apply bg-pxp-panel; }
.WorkshopCardOffset { @apply md:mt-20; }
.CardCopy { @apply grid gap-4 p-6 md:p-8; }
.CardIndex { @apply text-xs font-bold tracking-[0.14em] text-pxp-green; }
.CardCopy h3 { @apply text-4xl leading-none md:text-5xl; }
.CardCopy p { @apply max-w-lg leading-relaxed; }
.EditorialLink { @apply inline-flex min-h-11 w-fit items-center gap-4 font-bold text-pxp-green underline decoration-1 underline-offset-4 hover:text-pxp-ink focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-pxp-green; }
.Digital { @apply border-y border-pxp-green/15 bg-[#ebe9df] py-16 md:py-20; }
.DigitalGrid { @apply grid gap-8 md:grid-cols-3; }
.DigitalGrid article { @apply grid content-start gap-4 border-t border-pxp-green/30 pt-6; }
.DigitalGrid h3 { @apply text-xl font-bold; }
.DigitalGrid p { @apply leading-relaxed; }
.MethodGrid { @apply m-0 grid list-none gap-8 p-0 md:grid-cols-3; }
.MethodGrid li { @apply relative grid content-start gap-3 border-t border-pxp-green/35 pt-6; }
.MethodGrid li > span { @apply text-sm font-bold text-pxp-green; }
.MethodGrid li::before { content: ""; @apply absolute -top-1 left-0 size-2 rounded-full bg-pxp-green; }
.MethodGrid h3 { @apply text-xl font-bold; }
.MethodGrid p, .MethodNote { @apply text-sm leading-relaxed; }
.MethodNote { @apply mt-10 max-w-2xl text-pxp-ink/75; }
.Contact { @apply bg-pxp-ink py-14 text-pxp-paper md:py-20; }
.ContactInner { @apply grid items-center gap-8 md:grid-cols-[1fr_auto]; }
.ContactInner > div { @apply grid gap-4; }
.Contact .eyebrow { @apply text-[#a8d5bd]; }
.Contact p:last-child { @apply max-w-xl leading-relaxed; }
.Contact :deep(.ButtonPrimary) { @apply bg-pxp-paper text-pxp-ink shadow-none hover:bg-white focus-visible:ring-white; }
</style>
