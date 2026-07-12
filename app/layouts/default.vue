<template>
  <div class="LayoutWrapper">
    <a class="SkipLink" href="#main-content">Aller au contenu principal</a>
    <SiteHeader />
    <div id="main-content" class="LayoutContent" tabindex="-1">
      <slot />
    </div>
    <SiteFooter />
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
@reference "../assets/css/main.css";

.LayoutWrapper {
  @apply flex min-h-screen flex-col;
}

.LayoutContent {
  @apply flex-1 outline-none;
}

.SkipLink {
  @apply fixed left-4 top-4 z-[100] -translate-y-24 rounded-md bg-white px-4 py-3 text-sm font-extrabold text-pxp-blue no-underline shadow-lg transition;
}

.SkipLink:focus {
  @apply translate-y-0 outline-2 outline-offset-2 outline-pxp-blue;
}
</style>
