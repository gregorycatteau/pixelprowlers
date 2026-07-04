<template>
  <div class="site-shell">
    <NavTop />
    <slot />
  </div>
</template>

<script setup lang="ts">
import NavTop from '~/components/layout/NavTop.vue';
</script>
