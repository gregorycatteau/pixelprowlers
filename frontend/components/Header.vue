<template>
  <header class="site-header">
    <div class="container-site header-inner">
      <NuxtLink to="/" aria-label="Retour à l'accueil Pixelprowlers" class="brand-link">
        <img src="/logo-nav.png" alt="" width="48" height="48" class="brand-mark" />
        <span class="brand-name">PixelProwlers</span>
      </NuxtLink>

      <nav class="nav-list" aria-label="Navigation principale">
        <NuxtLink
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          class="nav-link"
        >
          {{ item.label }}
        </NuxtLink>
      </nav>
    </div>
  </header>
</template>

<script setup lang="ts">
const navItems = [
  { label: 'Accueil', to: '/' },
  { label: 'Audit site web', to: '/audit-site-web' },
  { label: 'Site maintenable', to: '/developpement' },
  { label: 'Formations', to: '/formations' },
  { label: 'Ressources', to: '/ressources' },
  { label: 'Contact', to: '/contact' },
];
</script>

<style scoped>
.site-header {
  @apply sticky top-0 z-50 border-b border-forest/15 bg-paper/95 backdrop-blur;
}

.header-inner {
  @apply flex flex-wrap items-center justify-between gap-4 py-3 md:min-h-20 md:flex-nowrap;
}

.brand-link {
  @apply inline-flex items-center gap-3 rounded-lg text-ink outline-none transition hover:text-forest focus-visible:ring-2 focus-visible:ring-scan focus-visible:ring-offset-2 focus-visible:ring-offset-paper;
}

.brand-mark {
  @apply h-10 w-10 rounded-lg object-cover md:h-12 md:w-12;
}

.brand-name {
  @apply font-heading text-lg font-extrabold tracking-[0.02em];
}

.nav-list {
  @apply grid min-w-0 basis-full grid-cols-1 gap-2 text-center text-sm font-bold text-ink md:flex md:basis-auto md:items-center md:justify-end md:gap-5;
}

.nav-link {
  @apply rounded-lg border border-forest/15 px-3 py-2 outline-none transition hover:border-scan hover:text-trust focus-visible:ring-2 focus-visible:ring-scan focus-visible:ring-offset-2 focus-visible:ring-offset-paper md:border-0 md:px-0;
}
</style>
