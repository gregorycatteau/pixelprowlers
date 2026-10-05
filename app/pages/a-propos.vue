<template>
  <main class="AboutPage">
    <section class="container AboutHero" aria-labelledby="about-title">
      <div>
        <p class="eyebrow">À propos · Grégory Catteau</p>
        <h1 id="about-title" class="pxp-font-display">Réparer, comprendre, transmettre.</h1>
        <p>J’ai toujours aimé comprendre comment les choses fonctionnent. Le code m’a donné un moyen de construire, de chercher et de résoudre des problèmes. La réparation prolonge aujourd’hui cette démarche : regarder ce qui existe, comprendre ce qui bloque et chercher une solution utile.</p>
        <h2>Un parcours qui relie les métiers</h2>
        <p>Mon parcours m’a conduit du pilotage de projets au métier d’infirmier, tout en continuant à coder. Ces expériences ont gardé une place dans ma façon de travailler : écouter une situation, observer avant d’agir et expliquer ce que l’on propose.</p>
        <p>J’ai suivi une formation pour apprendre à recycler et réparer du matériel. Avec PixelProwlers, je réunis réparation, développement et réemploi. Un ordinateur, un site ou un outil métier mérite d’être examiné avant de décider de tout remplacer.</p>
      </div>
      <figure><img src="/images/about/parcours.jpg" alt="Portrait en randonnée dans un paysage de montagne" width="896" height="1183" loading="lazy" decoding="async"><figcaption>En randonnée.</figcaption></figure>
    </section>
    <section class="container AboutCopy">
      <h2>Transmettre fait partie du travail</h2>
      <p>Je forme et j’accompagne aux outils numériques. Mon objectif est de rendre les explications utilisables : comprendre un choix, retrouver une information, reprendre un geste et savoir quand demander de l’aide. La transmission ne vient pas seulement à la fin ; elle accompagne la résolution du problème.</p>
      <h2>Une méthode simple, avec vous</h2>
      <p>Examiner d’abord, expliquer ensuite, intervenir avec votre accord, puis transmettre ce qui permet de continuer. Je préfère une proposition compréhensible, avec ses limites, à une promesse que le matériel ou la situation ne permettent pas de tenir.</p>
      <p>Réparer et réemployer donnent une place aux ressources déjà disponibles. Développer sert à répondre à un usage réel. Dans les deux cas, je veux que vous gardiez la main sur vos outils et vos décisions.</p>
      <p>Vous avez une panne, une question ou un projet ? Décrivez ce qui vous amène. Nous pourrons préciser ensemble ce qui est utile et ce qui est possible.</p>
      <AppButton href="/contact">Prendre contact</AppButton>
    </section>
  </main>
</template>

<script setup lang="ts">
import AppButton from '~/components/ui/AppButton.vue';
useSeoMeta({ title: 'À propos : réparer, développer et transmettre | PixelProwlers', description: 'Le parcours de Grégory Catteau et la méthode PixelProwlers : examiner, expliquer, intervenir avec accord et transmettre.', robots: 'index, follow', ogUrl: 'https://pixelprowlers.io/a-propos' });
useHead({ link: [{ rel: 'canonical', href: 'https://pixelprowlers.io/a-propos' }] });
</script>

<style scoped>
@reference "../assets/css/main.css";
.AboutPage { @apply bg-pxp-paper text-pxp-ink; }
.AboutHero { @apply grid items-start gap-10 py-14 md:grid-cols-[1.5fr_1fr] md:py-20; }
.AboutHero > div, .AboutCopy { @apply grid gap-6; }
h1 { @apply text-5xl leading-none md:text-6xl; }
h2 { @apply text-2xl font-bold; }
p { @apply leading-relaxed; }
figure { @apply overflow-hidden rounded-lg; }
img { @apply h-auto w-full object-cover; }
figcaption { @apply bg-white p-4 text-sm; }
.AboutCopy { @apply max-w-4xl pb-16; }
.container { @apply mx-auto w-[min(1320px,calc(100%-32px))]; }
:deep(.ButtonPrimary) { @apply bg-pxp-green text-white hover:bg-pxp-ink focus-visible:ring-pxp-green; }
</style>
