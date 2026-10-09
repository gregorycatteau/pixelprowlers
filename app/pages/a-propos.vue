<template>
  <main class="AboutPage">
    <section class="container AboutHero" aria-labelledby="about-title"><div><p class="eyebrow">PixelProwlers · Grégory Catteau</p><h1 id="about-title" class="pxp-font-display">Grégory, votre interlocuteur.</h1><p>Avec PixelProwlers, je propose la réparation informatique et le réemploi dans le Médoc, ainsi que le développement et la transmission. Mon point de départ : vous écouter, comprendre ce qui bloque et expliquer les possibilités.</p><AppButton href="/contact">Parlons de votre besoin</AppButton></div><figure><img src="/images/about/greg-labo-960.webp" srcset="/images/about/greg-labo-480.webp 480w, /images/about/greg-labo-960.webp 960w, /images/about/greg-labo-1086.webp 1086w" sizes="(min-width: 768px) 40vw, calc(100vw - 32px)" alt="Grégory Catteau observant une carte électronique au microscope" width="1086" height="1448" decoding="async"><figcaption>Grégory, au microscope.</figcaption></figure></section>
    <section class="container AboutCopy"><h2>Observer avant d’agir.</h2><p>Du pilotage de projets au métier d’infirmier, j’ai continué à coder. Ces expériences nourrissent ma façon de travailler : écouter une situation, examiner les faits et rendre les explications utiles.</p><p>Une formation au recyclage et à la réparation du matériel a prolongé cette démarche. Un ordinateur, un site ou un outil mérite d’être examiné avant de décider de tout remplacer.</p><h2>Expliquer pour transmettre.</h2><p>Je forme et j’accompagne aux outils numériques : comprendre un choix, reprendre un geste, retrouver une information. Avec PixelProwlers, le diagnostic débouche sur une proposition compréhensible ; l’intervention se fait avec votre accord.</p><AppButton href="/contact?besoin=reparation">Décrire ma panne</AppButton></section>
  </main>
</template>
<script setup lang="ts">
import AppButton from '~/components/ui/AppButton.vue';
useSeoMeta({ title: 'À propos : réparer, développer et transmettre | PixelProwlers', description: 'Grégory Catteau, votre interlocuteur PixelProwlers : réparation et réemploi dans le Médoc, développement et transmission. Examiner, expliquer, agir avec accord.', robots: 'index, follow', ogUrl: 'https://pixelprowlers.io/a-propos' });
useHead({ link: [{ rel: 'canonical', href: 'https://pixelprowlers.io/a-propos' }] });
</script>

<style scoped>
@reference "../assets/css/main.css";
.AboutPage { @apply bg-pxp-paper text-pxp-ink; }
.AboutHero { @apply grid items-center gap-8 py-10 md:grid-cols-[1.5fr_1fr] md:py-16; }
.AboutHero > div, .AboutCopy { @apply grid gap-5; }
h1 { @apply text-5xl leading-none md:text-6xl; }
h2 { @apply text-3xl font-bold; }
p { @apply leading-relaxed; }
figure { @apply overflow-hidden; }
img { @apply aspect-[3/4] w-full object-cover; }
figcaption { @apply bg-white px-4 py-2 text-sm; }
.AboutCopy { @apply max-w-4xl pb-16; }
</style>
