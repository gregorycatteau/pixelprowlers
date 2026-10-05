<template>
  <figure class="EditorialImage">
    <img
      :src="`/images/editorial/${name}-960.webp`"
      :srcset="`/images/editorial/${name}-480.webp 480w, /images/editorial/${name}-960.webp 960w${name === 'microscope' ? ', /images/editorial/microscope-1536.webp 1536w' : ''}`"
      :sizes="sizes"
      :alt="alt"
      width="960"
      height="640"
      :loading="priority ? 'eager' : 'lazy'"
      :fetchpriority="priority ? 'high' : 'auto'"
      decoding="async"
    >
    <figcaption>Illustration générée · {{ caption }}</figcaption>
  </figure>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  name: 'microscope' | 'composant' | 'reemploi';
  alt: string;
  caption: string;
  sizes?: string;
  priority?: boolean;
}>(), {
  sizes: '(min-width: 1024px) 50vw, 100vw',
  priority: false,
});
</script>

<style scoped>
@reference "../../assets/css/main.css";
.EditorialImage { @apply relative m-0 overflow-hidden bg-pxp-ink; }
img { @apply block h-full w-full object-cover; aspect-ratio: 3 / 2; object-position: center 62%; }
figcaption { @apply absolute bottom-3 left-3 right-3 w-fit rounded bg-pxp-ink px-2 py-1 text-[0.65rem] font-semibold text-white; }
</style>
