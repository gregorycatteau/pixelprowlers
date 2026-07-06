<template>
  <footer class="SiteFooter">
    <div class="FooterInner">
      <div class="FooterBrand">
        <img class="FooterLogo" src="/logo-nav-transparent.png" alt="" width="32" height="32">
        <span class="FooterName">PixelProwlers</span>
      </div>

      <nav class="FooterLinks" aria-label="Navigation secondaire">
        <AppButton v-for="link in footerLinks" :key="link.href" variant="nav" :href="link.href">
          {{ link.label }}
        </AppButton>
      </nav>
    </div>
  </footer>
</template>

<script setup lang="ts">
import AppButton from '~/components/ui/AppButton.vue';

const footerLinks = [
  { label: 'Contact', href: '/contact' },
  { label: 'Diagnostic', href: '/diagnostic-situation' },
  { label: 'À propos', href: '/a-propos' },
] as const;
</script>

<style scoped>
@reference "../assets/css/main.css";

.SiteFooter {
  @apply border-t border-[#2b7053]/15 bg-[#17251d] text-white;
}

.FooterInner {
  @apply mx-auto flex w-[min(1120px,calc(100%_-_32px))] flex-col gap-5 py-8;
}

.FooterBrand {
  @apply inline-flex items-center gap-3;
}

.FooterLogo {
  @apply h-8 w-8 rounded-lg object-contain;
}

.FooterName {
  @apply text-base font-black;
}

.FooterLinks {
  @apply flex flex-wrap gap-2;
}

@media (min-width: 768px) {
  .FooterInner {
    @apply flex-row items-center justify-between;
  }
}
</style>
