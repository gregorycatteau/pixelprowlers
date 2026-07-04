<template>
  <SiteShell>
    <main class="MainWrapper">
      <!-- Hero Section -->
      <section class="Section HeroSection" aria-labelledby="about-title">
        <div class="Container">
          <p class="Eyebrow">À propos</p>
          <h1 id="about-title" class="Title">
            Des années à coder. Et toujours pas capable de me désengager.
          </h1>
          <p class="BodyText">
            Je ne vends pas une solution. Je répare ce qu'on a cassé. Et je transmets pour que ça dure.
          </p>
        </div>
      </section>

      <!-- Notre histoire -->
      <section class="Section" aria-labelledby="story-title">
        <div class="Container">
          <h2 id="story-title" class="Subtitle">
            Comment on passe de 40 ans d'optimisme à "attendez, il y a un problème".
          </h2>
          <div class="ContentCopy">
            <p class="BodyText">
              J'ai commencé à coder en 1981. Autodidacte, pas d'école, pas de diplôme, juste l'envie de faire tourner les trucs.
            </p>
            <p class="BodyText">
              PixelProwlers, c'est faire du code qui dure, utiliser des machines qui ont une deuxième vie, et transmettre pour que les équipes gagnent en autonomie.
            </p>
          </div>
        </div>
      </section>

      <!-- Nos valeurs -->
      <section class="Section SectionAlt" aria-labelledby="values-title">
        <div class="Container">
          <h2 id="values-title" class="Subtitle">
            Les trois piliers de comment on travaille.
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
            Pour qui c'est fait, pour qui ça ne l'est pas.
          </h2>
          <div class="FitGrid">
            <div class="FitBlock">
              <h3 class="FitBlockTitle">Ça marche avec vous si</h3>
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
            <NuxtLink to="/contact" class="ButtonPrimary">
              Prendre contact
            </NuxtLink>
            <NuxtLink to="/diagnostic" class="ButtonSecondary">
              Faire le diagnostic
            </NuxtLink>
          </div>
        </div>
      </section>
    </main>
  </SiteShell>
</template>

<script setup lang="ts">
const values = [
  {
    title: 'Réparer plutôt que remplacer',
    text: 'On répare ce qui peut l\'être avant de proposer de tout casser pour reconstruire.',
  },
  {
    title: 'Transmettre, pas juste livrer',
    text: 'L\'objectif c\'est que vous puissiez continuer sans nous si besoin.',
  },
  {
    title: 'Dire non quand il faut',
    text: 'Si ce n\'est pas le bon projet ou le bon moment, on vous le dit franchement.',
  },
]

const fitFor = [
  'Vous voulez comprendre ce qui a été fait chez vous',
  'Vous cherchez une solution durable, pas un pansement',
  'Vous êtes prêt à être franc sur vos contraintes',
]

const notFitFor = [
  'Vous cherchez le prestataire le moins cher',
  'Vous voulez une solution miracle en 24h',
  'Vous n\'êtes pas prêt à donner accès à l\'existant',
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

/* 🎨 Hero Section */
.HeroSection {
  @apply pt-24 pb-16 text-center;
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

.ContentCopy {
  @apply space-y-4;
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
