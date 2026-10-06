<template>
  <section class="HeroSection" aria-labelledby="hero-title">
    <div class="HeroInner">
      <div class="HeroContent">
        <p class="HeroEyebrow">{{ eyebrow }}</p>
        <h1 id="hero-title" class="pxp-font-display">{{ title }}</h1>
        <p class="HeroSubtitle">{{ subtitle }}</p>
        <div class="HeroActions">
          <AppButton :href="ctaLink">{{ ctaText }}</AppButton>
          <AppButton variant="secondary" :href="secondaryCtaLink">{{ secondaryCtaText }}</AppButton>
        </div>
        <p v-if="ctaNote" class="HeroNote">{{ ctaNote }}</p>
        <div class="HeroSignature" aria-hidden="true"><span></span> Réparer. Réemployer. Transmettre.</div>
      </div>
      <EditorialImage name="microscope" alt="Illustration d’une intervention sur une carte électronique sous microscope" caption="micro-soudure" priority sizes="(min-width: 1024px) 58vw, 100vw" />
    </div>
  </section>
</template>

<script setup lang="ts">
import AppButton from '~/components/ui/AppButton.vue';
import EditorialImage from '~/components/sections/EditorialImage.vue';

defineProps<{
  eyebrow: string;
  title: string;
  subtitle: string;
  ctaText: string;
  ctaLink: string;
  secondaryCtaText: string;
  secondaryCtaLink: string;
  ctaNote?: string;
}>();
</script>

<style scoped>
@reference "../../assets/css/main.css";
.HeroSection { @apply bg-pxp-ink text-pxp-paper; }
.HeroInner { @apply mx-auto grid max-w-[1600px] lg:grid-cols-[0.9fr_1.2fr]; }
.HeroContent { @apply relative grid content-center gap-6 px-6 py-12 md:px-12 md:py-16 lg:px-14; }
.HeroEyebrow { @apply text-xs font-bold uppercase tracking-[0.18em] text-[#a8d5bd]; }
h1 { @apply max-w-xl font-bold; font-size: clamp(3.3rem, 5.1vw, 6rem); line-height: 0.96; overflow-wrap: normal; }
.HeroSubtitle { @apply max-w-lg text-base leading-relaxed text-pxp-paper/90 md:text-lg; }
.HeroActions { @apply flex flex-wrap gap-3; }
.HeroActions :deep(.ButtonPrimary) { @apply bg-pxp-paper text-pxp-ink shadow-none hover:bg-white focus-visible:ring-white; }
.HeroActions :deep(.ButtonSecondary) { @apply border-pxp-paper/60 bg-transparent text-pxp-paper hover:bg-white/10 focus-visible:ring-white; }
.HeroNote { @apply max-w-md text-xs leading-relaxed text-pxp-paper/80; }
.HeroSignature { @apply mt-3 flex items-center gap-3 text-xs font-semibold tracking-wide text-[#a8d5bd]; }
.HeroSignature span { @apply relative block h-px w-12 bg-[#a8d5bd]; }
.HeroSignature span::after { content: ""; @apply absolute right-0 -top-1 size-2 rounded-full border border-[#a8d5bd] bg-pxp-ink; }
.HeroInner :deep(figure) { @apply min-h-72 lg:min-h-[610px]; }
.HeroInner :deep(img) { @apply h-full; }
@media (max-width: 1023px) {
  .HeroInner :deep(figure) { @apply order-first; max-height: 350px; }
  .HeroInner :deep(img) { aspect-ratio: 16 / 9; }
}
@media (max-width: 639px) {
  .HeroContent { @apply gap-4 py-8; }
  .HeroInner :deep(figure) { @apply h-48 min-h-0; }
  h1 { font-size: 2.75rem; }
  .HeroSubtitle { @apply text-[0.9375rem]; }
}
</style>
