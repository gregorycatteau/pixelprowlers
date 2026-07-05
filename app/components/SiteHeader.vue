<template>
  <header class="SiteHeader">
    <nav class="HeaderNav" aria-label="Navigation principale">
      <div class="HeaderInner">
        <a class="BrandLink" href="/" @click="closeMenu">
          <img class="BrandLogo" src="/logo-nav.png" alt="" width="36" height="36">
          <span class="BrandName">PixelProwlers</span>
        </a>

        <div class="DesktopLinks" aria-label="Liens internes">
          <AppButton v-for="link in navLinks" :key="link.href" variant="nav" :href="link.href">
            {{ link.label }}
          </AppButton>
        </div>

        <div class="HeaderActions">
          <AppButton href="/diagnostic-situation">Diagnostic gratuit</AppButton>
          <AppButton href="/rendez-vous">Reprendre la main</AppButton>
        </div>

        <button
          class="MenuToggle"
          type="button"
          :aria-expanded="isMenuOpen"
          aria-controls="mobile-menu"
          aria-label="Ouvrir ou fermer le menu"
          @click="isMenuOpen = !isMenuOpen"
        >
          <span class="MenuLine"></span>
          <span class="MenuLine"></span>
          <span class="MenuLine"></span>
        </button>
      </div>

      <div id="mobile-menu" class="MobileMenu" :class="{ MobileMenuOpen: isMenuOpen }">
        <AppButton v-for="link in navLinks" :key="link.href" variant="nav" :href="link.href" @click="closeMenu">
          {{ link.label }}
        </AppButton>
        <div class="MobileActions">
          <AppButton href="/diagnostic-situation" @click="closeMenu">Diagnostic gratuit</AppButton>
          <AppButton href="/rendez-vous" @click="closeMenu">Reprendre la main</AppButton>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import AppButton from '~/components/ui/AppButton.vue';

const isMenuOpen = ref(false);
const navLinks = [
  { label: 'Audit', href: '/audit-site-web' },
  { label: 'Refonte', href: '/refonte-site' },
  { label: 'Transmission', href: '/transmission-acces' },
  { label: 'Urgence', href: '/urgence' },
  { label: 'À propos', href: '/a-propos' },
] as const;

const closeMenu = () => {
  isMenuOpen.value = false;
};
</script>

<style scoped>
@reference "../assets/css/main.css";

.SiteHeader {
  @apply sticky top-0 z-50 w-full border-b border-neutral-200 bg-white/95 backdrop-blur;
}

.HeaderNav {
  @apply w-full;
}

.HeaderInner {
  @apply mx-auto flex min-h-[70px] w-[min(1280px,calc(100%_-_32px))] items-center justify-between gap-5;
}

.BrandLink,
.DesktopLinks,
.HeaderActions {
  @apply inline-flex items-center;
}

.BrandLink {
  @apply gap-2.5 whitespace-nowrap text-[1.02rem] font-black text-neutral-900 no-underline;
}

.BrandLogo {
  @apply h-9 w-9 rounded-lg object-contain;
}

.BrandName {
  @apply inline-block;
}

.DesktopLinks {
  @apply gap-1 text-[0.94rem] font-semibold text-neutral-700;
}

.HeaderActions {
  @apply gap-2.5;
}

.MenuToggle {
  @apply hidden h-[42px] w-[42px] flex-col items-center justify-center gap-[5px] rounded-lg border border-transparent bg-transparent p-0 text-neutral-800 transition hover:border-[#2b7053]/20 hover:bg-[#2b7053]/10;
}

.MenuLine {
  @apply block h-0.5 w-[18px] rounded-full bg-neutral-800;
}

.MobileMenu {
  @apply mx-auto hidden w-[min(100%_-_32px,1280px)] pb-3.5 text-[0.96rem] font-bold text-neutral-800;
}

.MobileMenuOpen {
  @apply grid gap-2.5;
}

.MobileActions {
  @apply grid gap-2.5 pt-2;
}

@media (max-width: 900px) {
  .DesktopLinks,
  .HeaderActions {
    @apply hidden;
  }

  .MenuToggle {
    @apply inline-flex;
  }

  .HeaderInner {
    @apply w-[min(100%_-_24px,1280px)];
  }
}
</style>
