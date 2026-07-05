<template>
  <main class="MainWrapper">
    <!-- Hero Section -->
    <section class="Section HeroSection" aria-labelledby="about-title">
      <div class="Container">
        <NuxtLink to="/" class="BackLink">
          Retour à l'accueil
        </NuxtLink>
        <p class="Eyebrow">À propos</p>
        <h1 id="about-title" class="Title">
          Des années à coder. Et toujours pas capable de me désengager.
        </h1>
        <p class="BodyText">
          Je ne vends pas une solution. Je répare ce qu'on a cassé. Et je transmets pour que ça dure.
        </p>
      </div>
    </section>

      <!-- Parcours : avant/après avec photo -->
      <section class="Section JourneySection" aria-labelledby="journey-title">
        <div class="Container ContainerWide">
          <h2 id="journey-title" class="Subtitle">
            Du TO7-70 aux sommets. Le chemin compte autant que la destination.
          </h2>

          <div class="JourneyGrid">
            <!-- Colonne photo -->
            <div class="JourneyPhotoCol">
              <figure class="JourneyPhotoFrame">
                <img
                  src="/images/about/parcours.jpg"
                  alt="Sur un sentier de montagne, sac à dos chargé, en route vers le sommet"
                  class="JourneyPhoto"
                  loading="lazy"
                  width="896"
                  height="1183"
                >
                <figcaption class="JourneyCaption">
                  Aujourd'hui. Même logique qu'en 1981 : avancer, un pas après l'autre.
                </figcaption>
              </figure>
            </div>

            <!-- Colonne texte -->
            <div class="JourneyTextCol">
              <div class="JourneyBlock">
                <p class="JourneyYear">1981</p>
                <p class="BodyText">
                  Des ronds dessinés au hasard sur un TO7-70. Puis les tableurs sont arrivés,
                  et c'était fun de faire des jeux Tetris sur une calculatrice TI-81 et des
                  dessins ASCII en jouant sur les largeurs de colonnes.
                </p>
              </div>

              <div class="JourneyBlock">
                <p class="JourneyYear">Internet, l'immense terrain de jeu</p>
                <p class="BodyText">
                  Le monde a changé. Internet est arrivé comme une passoire pleine de trous,
                  des terrains de jeu immenses, mais il fallait apprendre à coder. Mon premier
                  jeu interactif en Python générait un nombre, puis un autre deux secondes après,
                  et il fallait donner la réponse. J'étais fier. Python, HTML, CSS pour le fun,
                  puis JavaScript et TypeScript.
                </p>
                <p class="BodyText">
                  Je n'ai pas toujours été très sage. Je suis souvent entré dans des endroits
                  où je n'avais rien à y faire. On était en 2000, et comme je ne faisais rien
                  de mal.
                </p>
              </div>

              <div class="JourneyBlock JourneyPivot">
                <p class="JourneyYear">Le virage</p>
                <p class="BodyText">
                  Puis internet s'est modernisé, durci, capitalisé. Ce virage-là, je ne l'ai
                  pas apprécié du tout. J'ai vite compris, en hacktiviste, que nos données
                  étaient absorbées, revendues, tracées. Alors j'ai viré Windows pour Linux,
                  supprimé le pack Office. Peine et douleur, mais j'ai bossé encore et encore.
                  Surtout, j'ai compris les vraies problématiques de sécurité et exploré en
                  profondeur comment fonctionne réellement internet.
                </p>
                <p class="BodyText">
                  Sans mentir ni trahir, j'aurais pu empocher des millions. Au lieu de ça, je
                  recevais des lettres de menaces de DSI méprisables quand je leur donnais
                  gratuitement une faille à patcher.
                </p>
              </div>

              <div class="JourneyBlock">
                <p class="JourneyYear">1998 → 2002, l'Afrique</p>
                <p class="BodyText">
                  Responsable projet pour des compagnies pétrolières, j'ai enchaîné les
                  déplacements en Afrique. J'y ai vu des gamins surexploités, des hommes
                  mourir dans les décharges de nos déchets électroniques. Ce qu'on jette
                  ici finit dans leurs poumons là-bas. Cette image-là ne m'a plus jamais quitté.
                </p>
              </div>

              <div class="JourneyBlock">
                <p class="JourneyYear">20 ans d'hôpital de nuit</p>
                <p class="BodyText">
                  Alors je suis devenu infirmier, pendant vingt ans. Je codais toujours en
                  douce, des clés pour regarder des films depuis le réseau sans se faire
                  choper, ce genre de chose. Mais le système de santé, pardon, le système
                  d'entretien des maladies, a fini par me lasser.
                </p>
              </div>

              <div class="JourneyBlock JourneyToday">
                <p class="JourneyYear">Le retour, transformé</p>
                <p class="BodyText">
                  Je suis revenu à mes premières amours. J'ai repris la manie de tout coder,
                  et en plus celle de tout vouloir réparer. J'ai suivi une formation pour
                  apprendre à recycler, réparer, redonner une seconde vie. Un i5 gen 6 refusé
                  par Windows 11 ? Confiez-le moi, je le reconfigure avec un vieil Ubuntu et
                  il repart pour au moins 5 ans.
                </p>
                <p class="BodyText">
                  J'ai vu des assos avec des Google Drive où il faut cinq aspirines avant de
                  mettre la main sur le bon fichier. Des associations de plusieurs dizaines
                  de membres faire des commandes à la main sur des fichiers Excel croisés,
                  se plaindre que les résultats n'étaient pas justes. Des producteurs tellement
                  les mains dans la terre par amour qu'ils en oublient de parler d'eux.
                </p>
                <p class="BodyText BodyTextStrong">
                  Alors est né PixelProwlers. Je code, je recycle, je répare, j'optimise,
                  j'accompagne, je forme aux outils de résilience de demain. J'ouvre de
                  nouvelles trajectoires : un site internet contre des légumes de saison ?
                  Deal ! Mais pas avec des Google Drive ni des Microsoft Azure. Et je ne fais
                  rien seul. On fait ensemble.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Nos valeurs -->
      <section class="Section SectionAlt" aria-labelledby="values-title">
        <div class="Container">
          <h2 id="values-title" class="Subtitle">
            Les trois piliers de notre futur travail collaboratif.
          </h2>
          <div class="ValuesGrid">
            <article
              v-for="value in values"
              :key="value.title"
              class="ValueCard"
            >
              <h3 class="ValueCardTitle">{{ value.title }}</h3>
              <p class="ValueCardText">{{ value.text }}</p>
            </article>
          </div>
        </div>
      </section>

      <!-- Quand ça marche bien -->
      <section class="Section" aria-labelledby="fit-title">
        <div class="Container">
          <h2 id="fit-title" class="Subtitle">
            Evaluons nos chances de travailler ensemble. </h2>
          <div class="FitGrid">
            <div class="FitBlock">
              <h3 class="FitBlockTitle">Ça marchera entre nous si</h3>
              <ul class="FitList">
                <li v-for="item in fitFor" :key="item" class="FitListItem">
                  {{ item }}
                </li>
              </ul>
            </div>
            <div class="FitBlock">
              <h3 class="FitBlockTitle">Ça ne marchera pas si</h3>
              <ul class="FitList">
                <li v-for="item in notFitFor" :key="item" class="FitListItem">
                  {{ item }}
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <!-- CTA final -->
      <section class="Section FinalSection" aria-labelledby="final-title">
        <div class="Container">
          <h2 id="final-title" class="Subtitle">
            On en parle ?
          </h2>
          <p class="BodyText">
            Cinq minutes pour savoir si ça vaut le coup d'aller plus loin.
          </p>
          <div class="ActionsGroup">
            <NuxtLink to="/rendez-vous" class="ButtonPrimary">
              Prendre contact
            </NuxtLink>
            <NuxtLink to="/diagnostic-situation" class="ButtonSecondary">
              Faire le diagnostic
            </NuxtLink>
          </div>
        </div>
      </section>
  </main>
</template>

<script setup lang="ts">
const values = [
  {
    title: 'Réparer plutôt que remplacer',
    text: 'On répare ce qui peut l\'être avant de proposer de tout casser pour reconstruire. On ne jette pas pour racheter plus couteux et moins réparable',
  },
  {
    title: 'Transmettre, pas juste livrer',
    text: 'Comme dit le proverbe, si tu veux nourrir un homme, ne lui donnes pas un poisson mais apprends lui à pécher.L\'objectif c\'est que vous puissiez continuer sans nous si besoin.',
  },
  {
    title: 'Dire non quand il faut',
    text: 'Si ce n\'est pas le bon projet ou le bon moment, je vous le dirai franchement. Tout le monde y gagne : vous ne perdez pas de temps, et je ne perds pas mon énergie à faire quelque chose qui ne sert à rien.',
  },
]

const fitFor = [
  'Vous voulez comprendre ce qui a été fait chez vous',
  'Vous cherchez une solution durable, pas un pansement',
  'Vous êtes prêt à être franc sur vos contraintes',
]

const notFitFor = [
  'Seul le prix le plus bas vous intéresse',
  'Vous considérez qu\'un développeur n\'est qu\'un prestataire technique',
  'Vous pensez que je vais tout faire seul, sans vous',
]


useHead({
  title: 'À propos - PixelProwlers',
  meta: [
    {
      name: 'description',
      content: 'Qui est derrière PixelProwlers, comment on travaille, et pour qui c\'est fait.',
    },
  ],
})
</script>

<style scoped>
@reference "../assets/css/main.css";

/* 🎨 Layout & Containers */
.MainWrapper {
  @apply flex flex-col;
}

.Section {
  @apply py-16;
}

.SectionAlt {
  @apply bg-neutral-50;
}

.FinalSection {
  @apply bg-neutral-900 text-white;
}

.Container {
  @apply mx-auto max-w-4xl px-4;
}

.Container {
  @media (min-width: 640px) {
    @apply px-6;
  }
}

.Container {
  @media (min-width: 1024px) {
    @apply px-8;
  }
}

.ContainerWide {
  @apply max-w-6xl;
}

/* 🎨 Hero Section */
.HeroSection {
  @apply pt-24 pb-16 text-center;
}

.BackLink {
  @apply mb-8 inline-flex items-center justify-center rounded-xl border border-primary-600 px-4 py-2 text-sm font-semibold text-primary-600 transition hover:bg-primary-600 hover:text-white;
}

.Eyebrow {
  @apply mb-4 text-sm font-semibold uppercase tracking-wide text-primary-600;
}

.Title {
  @apply text-3xl font-bold leading-tight text-neutral-900;
}

.Title {
  @media (min-width: 768px) {
    @apply text-5xl;
  }
}

.FinalSection .Title,
.FinalSection .Subtitle,
.FinalSection .BodyText {
  @apply text-white;
}

/* 🎨 Typography */
.Subtitle {
  @apply mb-8 text-2xl font-bold text-neutral-900;
}

.Subtitle {
  @media (min-width: 768px) {
    @apply text-3xl;
  }
}

.BodyText {
  @apply mt-4 text-lg leading-relaxed text-neutral-600;
}

.BodyTextStrong {
  @apply font-semibold text-neutral-900;
}

.ContentCopy {
  @apply space-y-4;
}

/* 🎨 Journey Section (parcours + photo) */
.JourneySection {
  @apply bg-neutral-50;
}

.JourneyGrid {
  @apply grid grid-cols-1 gap-12;
}

.JourneyGrid {
  @media (min-width: 1024px) {
    @apply grid-cols-[minmax(0,380px)_1fr] items-start gap-16;
  }
}

.JourneyPhotoCol {
  @apply order-1;
}

.JourneyPhotoCol {
  @media (min-width: 1024px) {
    @apply sticky top-24 order-0;
  }
}

.JourneyPhotoFrame {
  @apply overflow-hidden rounded-2xl border border-neutral-200 bg-white shadow-lg;
}

.JourneyPhoto {
  @apply h-auto w-full object-cover;
  aspect-ratio: 3 / 4;
}

.JourneyCaption {
  @apply border-t border-neutral-200 bg-white px-4 py-3 text-center text-sm italic text-neutral-500;
}

.JourneyTextCol {
  @apply space-y-10;
}

.JourneyBlock {
  @apply border-l-2 border-neutral-200 pl-6;
}

.JourneyPivot {
  @apply border-primary-100;
}

.JourneyToday {
  @apply border-primary-600;
}

.JourneyYear {
  @apply text-sm font-bold uppercase tracking-wide text-primary-600;
}

/* 🎨 Values Grid */
.ValuesGrid {
  @apply grid grid-cols-1 gap-8;
}

.ValuesGrid {
  @media (min-width: 768px) {
    @apply grid-cols-3;
  }
}

.ValueCard {
  @apply rounded-2xl bg-white p-6 shadow-sm;
}

.ValueCardTitle {
  @apply mb-2 text-xl font-semibold text-neutral-900;
}

.ValueCardText {
  @apply text-neutral-600;
}

/* 🎨 Fit Grid */
.FitGrid {
  @apply grid grid-cols-1 gap-8;
}

.FitGrid {
  @media (min-width: 768px) {
    @apply grid-cols-2;
  }
}

.FitBlock {
  @apply rounded-2xl border border-neutral-200 p-6;
}

.FitBlockTitle {
  @apply mb-4 text-xl font-semibold text-neutral-900;
}

.FitList {
  @apply space-y-3;
}

.FitListItem {
  @apply relative pl-6 text-neutral-600;
}

.FitListItem::before {
  @apply absolute left-0 top-0 text-primary-600;
  content: "•";
}

/* 🎨 Actions Group */
.ActionsGroup {
  @apply mt-10 flex flex-col gap-4;
}

.ActionsGroup {
  @media (min-width: 640px) {
    @apply flex-row;
  }
}

/* 🎨 Boutons */
.ButtonPrimary {
  @apply inline-flex items-center justify-center rounded-xl bg-primary-600 px-6 py-3 font-semibold text-white transition hover:bg-primary-700;
}

.ButtonSecondary {
  @apply inline-flex items-center justify-center rounded-xl border border-white px-6 py-3 font-semibold text-white transition hover:bg-white hover:text-neutral-900;
}
</style>
