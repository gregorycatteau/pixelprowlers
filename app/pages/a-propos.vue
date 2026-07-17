<template>
  <main class="AboutPage">
    <section class="HeroSection" aria-labelledby="about-title">
      <div class="Container">
        <NuxtLink to="/" class="BackLink">
          Retour à l’accueil
        </NuxtLink>

        <p class="Eyebrow">À propos de PixelProwlers</p>

        <h1 id="about-title" class="HeroTitle">
          Un numérique plus sûr, compréhensible et réversible.
        </h1>

        <p class="HeroLead">
          PixelProwlers répare, sécurise et documente vos sites, vos accès
          et vos outils pour que votre activité ne dépende ni d’un prestataire
          opaque ni d’une plateforme qui décide à votre place.
        </p>

        <div class="HeroActions">
          <NuxtLink to="/contact" class="ButtonPrimary">
            Parler de votre situation
          </NuxtLink>

          <NuxtLink to="/diagnostic-situation" class="ButtonSecondary">
            Faire le pré-diagnostic
          </NuxtLink>
        </div>

        <ul class="TrustSummary" aria-label="Principes de PixelProwlers">
          <li>Périmètre défini avant intervention</li>
          <li>Accès limités au strict nécessaire</li>
          <li>Documentation et restitution prévues</li>
        </ul>
      </div>
    </section>

    <section class="Section" aria-labelledby="founder-title">
      <div class="Container ContainerWide">
        <div class="FounderGrid">
          <figure class="FounderPhotoFrame">
            <img
              src="/images/about/parcours.jpg"
              alt="Sur un sentier de montagne, en route vers le sommet"
              class="FounderPhoto"
              loading="lazy"
              width="896"
              height="1183"
            >
            <figcaption class="FounderCaption">
              Avancer avec méthode, rendre le chemin lisible et ne laisser
              personne dépendant derrière soi.
            </figcaption>
          </figure>

          <div class="FounderContent">
            <p class="SectionEyebrow">Qui intervient</p>

            <h2 id="founder-title" class="SectionTitle">
              Un interlocuteur responsable de ce qu’il recommande.
            </h2>

            <div class="Prose">
              <p>
                J’ai commencé à programmer sur un TO7-70, bien avant que le
                numérique devienne indispensable au fonctionnement quotidien
                des entreprises et des associations.
              </p>

              <p>
                Mon parcours a ensuite croisé la gestion de projet, vingt années
                de travail hospitalier de nuit, la réparation informatique et
                la sécurité numérique. Ces expériences ont installé une même
                exigence : comprendre la situation avant d’agir, protéger ce
                qui est sensible et rester fiable lorsque le problème devient
                urgent.
              </p>

              <p>
                PixelProwlers est né de cette convergence. L’objectif n’est pas
                d’ajouter un outil de plus, mais de rendre votre environnement
                plus robuste, plus simple à maintenir et moins dépendant de
                décisions que vous ne maîtrisez pas.
              </p>

              <p>
                Vous échangez directement avec la personne qui analyse,
                intervient et documente. Si une compétence complémentaire est
                nécessaire, elle est identifiée avant l’intervention et son
                rôle vous est expliqué.
              </p>
            </div>

            <div class="FounderStatement">
              <p>
                L’autonomie n’impose pas de tout remplacer. Elle commence par
                savoir où sont vos données, qui possède vos accès et comment
                changer de solution sans perdre votre activité.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="Section SectionAlt" aria-labelledby="positioning-title">
      <div class="Container ContainerWide">
        <p class="SectionEyebrow">Notre positionnement</p>

        <h2 id="positioning-title" class="SectionTitle">
          Reprendre le contrôle, progressivement et sans culpabilisation.
        </h2>

        <p class="SectionIntro">
          Utiliser Microsoft, Google ou une plateforme propriétaire ne fait pas
          de vous un mauvais client. Le rôle de PixelProwlers est de vous montrer
          une trajectoire réaliste pour récupérer vos accès, vos données et votre
          liberté de choix.
        </p>

        <div class="PrinciplesGrid">
          <article
            v-for="principle in principles"
            :key="principle.title"
            class="PrincipleCard"
          >
            <p class="PrincipleIndex">{{ principle.index }}</p>
            <h3 class="PrincipleTitle">{{ principle.title }}</h3>
            <p class="PrincipleText">{{ principle.text }}</p>
          </article>
        </div>
      </div>
    </section>

    <section class="Section TrustSection" aria-labelledby="trust-title">
      <div class="Container ContainerWide">
        <div class="TrustGrid">
          <div>
            <p class="SectionEyebrow SectionEyebrowLight">
              Cadre de confiance
            </p>

            <h2 id="trust-title" class="SectionTitle SectionTitleLight">
              Vos accès ne sont pas une formalité.
            </h2>

            <p class="TrustIntro">
              Une intervention numérique peut exposer des données, des comptes
              et des outils essentiels. Le cadre est donc défini avant toute
              action sensible.
            </p>
          </div>

          <ul class="CommitmentList">
            <li
              v-for="commitment in commitments"
              :key="commitment.title"
              class="CommitmentItem"
            >
              <h3>{{ commitment.title }}</h3>
              <p>{{ commitment.text }}</p>
            </li>
          </ul>
        </div>

        <div class="EthicsNotice">
          <h3>Autorisation et sécurité</h3>
          <p>
            Toute vérification de sécurité est limitée aux systèmes que vous
            possédez ou pour lesquels vous disposez d’une autorisation explicite.
            Aucun test intrusif n’est engagé sans périmètre écrit. Les modalités
            concrètes de conservation, de restitution et de suppression des
            accès sont précisées avant l’intervention.
          </p>
        </div>
      </div>
    </section>

    <section class="Section" aria-labelledby="method-title">
      <div class="Container ContainerWide">
        <p class="SectionEyebrow">Méthode</p>

        <h2 id="method-title" class="SectionTitle">
          Une intervention que vous pouvez suivre et vérifier.
        </h2>

        <ol class="ProcessGrid">
          <li
            v-for="step in processSteps"
            :key="step.number"
            class="ProcessStep"
          >
            <span class="ProcessNumber" aria-hidden="true">
              {{ step.number }}
            </span>
            <h3>{{ step.title }}</h3>
            <p>{{ step.text }}</p>
          </li>
        </ol>
      </div>
    </section>

    <section class="Section SectionAlt" aria-labelledby="promises-title">
      <div class="Container ContainerWide">
        <div class="PromisesGrid">
          <div>
            <p class="SectionEyebrow">Des promesses crédibles</p>

            <h2 id="promises-title" class="SectionTitle">
              Pas de magie, pas de dépendance organisée.
            </h2>

            <p class="SectionIntro">
              La confiance ne repose pas sur des slogans absolus. Elle repose
              sur un périmètre clair, des preuves de travail et des limites
              annoncées honnêtement.
            </p>
          </div>

          <ul class="PromiseList">
            <li v-for="promise in honestPromises" :key="promise">
              {{ promise }}
            </li>
          </ul>
        </div>
      </div>
    </section>

    <section class="Section" aria-labelledby="fit-title">
      <div class="Container ContainerWide">
        <p class="SectionEyebrow">Travailler ensemble</p>

        <h2 id="fit-title" class="SectionTitle">
          Vérifions simplement si l’approche vous convient.
        </h2>

        <div class="FitGrid">
          <article class="FitCard FitCardPositive">
            <h3>PixelProwlers est probablement adapté si</h3>
            <ul>
              <li v-for="item in fitFor" :key="item">
                {{ item }}
              </li>
            </ul>
          </article>

          <article class="FitCard">
            <h3>Une autre approche sera préférable si</h3>
            <ul>
              <li v-for="item in notFitFor" :key="item">
                {{ item }}
              </li>
            </ul>
          </article>
        </div>
      </div>
    </section>

    <section class="FinalSection" aria-labelledby="final-title">
      <div class="Container">
        <p class="SectionEyebrow SectionEyebrowLight">Première étape</p>

        <h2 id="final-title" class="FinalTitle">
          Commençons par comprendre la situation.
        </h2>

        <p class="FinalText">
          Décrivez votre besoin, votre incident ou votre dépendance actuelle.
          Vous saurez ensuite si PixelProwlers peut réellement vous aider et
          quelle serait la prochaine étape.
        </p>

        <div class="HeroActions">
          <NuxtLink to="/contact" class="ButtonPrimary ButtonPrimaryLight">
            Contacter PixelProwlers
          </NuxtLink>

          <NuxtLink to="/diagnostic-situation" class="ButtonSecondaryLight">
            Faire le pré-diagnostic
          </NuxtLink>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
const principles = [
  {
    index: '01',
    title: 'Réparer avant de remplacer',
    text: "Nous conservons ce qui fonctionne et corrigeons ce qui fragilise réellement votre activité.",
  },
  {
    index: '02',
    title: 'Préférer la réversibilité',
    text: "Les formats ouverts, les exports et la maîtrise des accès facilitent un futur changement de solution.",
  },
  {
    index: '03',
    title: 'Sécuriser sans obscurcir',
    text: "Chaque mesure importante doit pouvoir être expliquée, vérifiée et maintenue dans le temps.",
  },
  {
    index: '04',
    title: 'Transmettre au lieu de retenir',
    text: "La documentation et la formation réduisent votre dépendance et facilitent la continuité de votre activité.",
  },
] as const;

const commitments = [
  {
    title: 'Un périmètre convenu',
    text: "Les objectifs, livrables, limites et conditions d’intervention sont clarifiés avant les actions sensibles.",
  },
  {
    title: 'Le minimum d’accès nécessaire',
    text: "Les accès demandés sont proportionnés à la mission et ne doivent pas devenir une dépendance permanente.",
  },
  {
    title: 'Des changements traçables',
    text: "Les décisions et modifications importantes sont documentées pour pouvoir être comprises et contrôlées.",
  },
  {
    title: 'Une restitution organisée',
    text: "Les accès, fichiers et informations utiles sont restitués selon le cadre défini pour la mission.",
  },
] as const;

const processSteps = [
  {
    number: '01',
    title: 'Comprendre',
    text: "Nous clarifions le problème, ses conséquences et les contraintes de votre organisation.",
  },
  {
    number: '02',
    title: 'Prioriser',
    text: "Nous distinguons l’urgent, le risqué et ce qui peut être amélioré progressivement.",
  },
  {
    number: '03',
    title: 'Intervenir',
    text: "Les actions convenues sont réalisées dans un périmètre défini, avec des points de contrôle adaptés.",
  },
  {
    number: '04',
    title: 'Transmettre',
    text: "Vous récupérez les explications, accès et documents nécessaires pour rester maître de la suite.",
  },
] as const;

const honestPromises = [
  "Aucune sécurité n’est présentée comme absolue ou définitive.",
  "Une qualification ou un accusé de réception n’est pas confondu avec une résolution.",
  "Aucune migration complète n’est imposée si une trajectoire progressive est plus réaliste.",
  "Les limites techniques, humaines ou budgétaires sont signalées dès qu’elles sont identifiées.",
] as const;

const fitFor = [
  "Vous souhaitez comprendre ce qui est fait et pourquoi.",
  "Vous recherchez une solution durable plutôt qu’un empilement d’outils.",
  "Vous voulez récupérer la maîtrise de vos données et de vos accès.",
  "Vous acceptez d’avancer par priorités lorsque tout ne peut pas être corrigé en une fois.",
] as const;

const notFitFor = [
  "Vous recherchez une promesse de sécurité totale ou de résultat instantané.",
  "Vous souhaitez masquer une intervention à un propriétaire ou à un responsable légitime.",
  "Vous refusez toute documentation ou participation aux décisions qui concernent votre activité.",
  "Le seul critère possible est le prix le plus bas, indépendamment du risque et de la maintenabilité.",
] as const;

const pageDescription =
  "Découvrez PixelProwlers : une approche indépendante pour réparer, sécuriser et documenter vos sites, vos accès et vos outils.";

useSeoMeta({
  title: "À propos de PixelProwlers — autonomie et sécurité numérique",
  description: pageDescription,
  ogTitle: "À propos de PixelProwlers",
  ogDescription: pageDescription,
  ogType: "website",
  ogUrl: "https://pixelprowlers.io/a-propos",
  twitterCard: "summary",
  twitterTitle: "À propos de PixelProwlers",
  twitterDescription: pageDescription,
});

useHead({
  link: [
    {
      rel: "canonical",
      href: "https://pixelprowlers.io/a-propos",
    },
  ],
});
</script>

<style scoped>
@reference "../assets/css/main.css";

.AboutPage {
  @apply flex flex-col bg-white text-neutral-900;
}

.Container {
  @apply mx-auto w-[min(100%-32px,896px)];
}

.ContainerWide {
  @apply w-[min(100%-32px,1120px)];
}

.Section {
  @apply py-16;
}

.SectionAlt {
  @apply bg-[#f3f7f4];
}

.HeroSection {
  @apply border-b border-pxp-green/15 bg-[#eff8f3] py-16;
}

.BackLink {
  @apply mb-10 inline-flex rounded-lg text-sm font-semibold text-pxp-green underline decoration-pxp-green/30 underline-offset-4 transition hover:decoration-pxp-green focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-pxp-green;
}

.Eyebrow,
.SectionEyebrow {
  @apply mb-4 text-sm font-bold uppercase tracking-[0.14em] text-pxp-green;
}

.HeroTitle {
  @apply max-w-4xl text-4xl font-black leading-tight tracking-tight text-pxp-ink;
}

.HeroLead {
  @apply mt-6 max-w-3xl text-lg leading-relaxed text-neutral-700;
}

.HeroActions {
  @apply mt-8 flex flex-col gap-3;
}

.ButtonPrimary,
.ButtonSecondary,
.ButtonSecondaryLight {
  @apply inline-flex min-h-12 items-center justify-center rounded-xl px-6 py-3 text-center font-bold transition focus-visible:outline-2 focus-visible:outline-offset-4;
}

.ButtonPrimary {
  @apply bg-pxp-green text-white hover:bg-pxp-green/80 focus-visible:outline-pxp-green;
}

.ButtonSecondary {
  @apply border border-pxp-green/40 bg-white text-[#20563f] hover:border-pxp-green hover:bg-[#f7fbf8] focus-visible:outline-pxp-green;
}

.TrustSummary {
  @apply mt-10 grid gap-3 border-t border-pxp-green/15 pt-6 text-sm font-semibold text-neutral-700;
}

.TrustSummary li {
  @apply relative pl-6;
}

.TrustSummary li::before {
  @apply absolute left-0 top-0 font-black text-pxp-green;
  content: "✓";
}

.FounderGrid {
  @apply grid gap-10;
}

.FounderPhotoFrame {
  @apply overflow-hidden rounded-2xl border border-neutral-200 bg-white shadow-sm;
}

.FounderPhoto {
  @apply aspect-4/5 h-full w-full object-cover;
}

.FounderCaption {
  @apply border-t border-neutral-200 px-5 py-4 text-sm leading-relaxed text-neutral-600;
}

.FounderContent {
  @apply self-center;
}

.SectionTitle {
  @apply max-w-3xl text-3xl font-black leading-tight tracking-tight text-pxp-ink;
}

.SectionIntro {
  @apply mt-5 max-w-3xl text-lg leading-relaxed text-neutral-700;
}

.Prose {
  @apply mt-6 space-y-5 text-base leading-7 text-neutral-700;
}

.FounderStatement {
  @apply mt-8 rounded-2xl border-l-4 border-pxp-green bg-[#eff8f3] p-6 font-semibold leading-7 text-pxp-ink;
}

.PrinciplesGrid {
  @apply mt-10 grid gap-5;
}

.PrincipleCard {
  @apply rounded-2xl border border-pxp-green/15 bg-white p-6 shadow-sm;
}

.PrincipleIndex {
  @apply mb-5 text-sm font-black tracking-[0.16em] text-pxp-green;
}

.PrincipleTitle {
  @apply text-xl font-black text-pxp-ink;
}

.PrincipleText {
  @apply mt-3 leading-7 text-neutral-700;
}

.TrustSection {
  @apply bg-pxp-ink text-white;
}

.TrustGrid {
  @apply grid gap-10;
}

.SectionEyebrowLight {
  @apply text-[#9ed7b9];
}

.SectionTitleLight {
  @apply text-white;
}

.TrustIntro {
  @apply mt-5 max-w-2xl text-lg leading-relaxed text-white/75;
}

.CommitmentList {
  @apply grid gap-4;
}

.CommitmentItem {
  @apply rounded-2xl border border-white/15 bg-white/5 p-5;
}

.CommitmentItem h3 {
  @apply text-lg font-black text-white;
}

.CommitmentItem p {
  @apply mt-2 leading-7 text-white/75;
}

.EthicsNotice {
  @apply mt-10 rounded-2xl border border-[#9ed7b9]/30 bg-[#9ed7b9]/10 p-6;
}

.EthicsNotice h3 {
  @apply text-lg font-black text-white;
}

.EthicsNotice p {
  @apply mt-3 max-w-4xl leading-7 text-white/80;
}

.ProcessGrid {
  @apply mt-10 grid gap-5;
}

.ProcessStep {
  @apply rounded-2xl border border-neutral-200 bg-white p-6;
}

.ProcessNumber {
  @apply mb-6 inline-flex h-10 w-10 items-center justify-center rounded-full bg-[#eff8f3] text-sm font-black text-pxp-green;
}

.ProcessStep h3 {
  @apply text-xl font-black text-pxp-ink;
}

.ProcessStep p {
  @apply mt-3 leading-7 text-neutral-700;
}

.PromisesGrid {
  @apply grid gap-10;
}

.PromiseList {
  @apply space-y-4;
}

.PromiseList li {
  @apply relative rounded-xl border border-pxp-green/15 bg-white py-4 pl-12 pr-5 leading-7 text-neutral-700;
}

.PromiseList li::before {
  @apply absolute left-5 top-4 font-black text-pxp-green;
  content: "—";
}

.FitGrid {
  @apply mt-10 grid gap-6;
}

.FitCard {
  @apply rounded-2xl border border-neutral-200 bg-white p-6;
}

.FitCardPositive {
  @apply border-pxp-green/25 bg-[#f7fbf8];
}

.FitCard h3 {
  @apply text-xl font-black text-pxp-ink;
}

.FitCard ul {
  @apply mt-5 space-y-3;
}

.FitCard li {
  @apply relative pl-6 leading-7 text-neutral-700;
}

.FitCard li::before {
  @apply absolute left-0 top-0 font-black text-pxp-green;
  content: "•";
}

.FinalSection {
  @apply bg-[#1f4f3b] py-16 text-white;
}

.FinalTitle {
  @apply max-w-3xl text-3xl font-black leading-tight tracking-tight;
}

.FinalText {
  @apply mt-5 max-w-3xl text-lg leading-relaxed text-white/80;
}

.ButtonPrimaryLight {
  @apply bg-white text-[#1f4f3b] hover:bg-[#eff8f3] focus-visible:outline-white;
}

.ButtonSecondaryLight {
  @apply border border-white/50 text-white hover:border-white hover:bg-white/10 focus-visible:outline-white;
}

@media (min-width: 640px) {
  .HeroActions {
    @apply flex-row flex-wrap;
  }

  .TrustSummary {
    @apply grid-cols-3;
  }
}

@media (min-width: 768px) {
  .Section,
  .FinalSection {
    @apply py-24;
  }

  .HeroSection {
    @apply py-24;
  }

  .HeroTitle {
    @apply text-6xl;
  }

  .SectionTitle,
  .FinalTitle {
    @apply text-4xl;
  }

  .PrinciplesGrid,
  .ProcessGrid,
  .FitGrid {
    @apply grid-cols-2;
  }
}

@media (min-width: 1024px) {
  .FounderGrid {
    @apply grid-cols-[360px_minmax(0,1fr)] gap-16;
  }

  .TrustGrid,
  .PromisesGrid {
    @apply grid-cols-[minmax(0,0.85fr)_minmax(0,1.15fr)] items-start gap-16;
  }

  .ProcessGrid {
    @apply grid-cols-4;
  }
}
</style>