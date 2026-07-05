<template>
  <div class="LayoutWrapper">
    <SiteHeader />
    <slot />
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
</style>
