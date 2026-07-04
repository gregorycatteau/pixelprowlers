<template>
  <nav class="top-nav" aria-label="Navigation principale">
    <div class="nav-inner">
      <a class="brand" href="/" @click="closeMenu">
        <img class="brand-logo" src="/logo-nav.png" alt="" width="36" height="36">
        <span>PixelProwlers</span>
      </a>

      <div class="desktop-links" aria-label="Liens internes">
        <AppButton v-for="link in navLinks" :key="link.href" variant="nav" :href="link.href">
          {{ link.label }}
        </AppButton>
      </div>

      <div class="nav-actions">
        <AppButton href="/diagnostic-situation">Diagnostic gratuit</AppButton>
        <AppButton href="/#contact">Reprendre la main</AppButton>
      </div>

      <button
        class="ButtonBase ButtonGhost menu-toggle"
        type="button"
        :aria-expanded="isMenuOpen"
        aria-controls="mobile-menu"
        aria-label="Ouvrir ou fermer le menu"
        @click="isMenuOpen = !isMenuOpen"
      >
        <span></span>
        <span></span>
        <span></span>
      </button>
    </div>

    <div id="mobile-menu" class="mobile-menu" :class="{ open: isMenuOpen }">
      <AppButton v-for="link in navLinks" :key="link.href" variant="nav" :href="link.href" @click="closeMenu">
        {{ link.label }}
      </AppButton>
      <div class="mobile-actions">
        <AppButton href="/diagnostic-situation" @click="closeMenu">Diagnostic gratuit</AppButton>
        <AppButton href="/#contact" @click="closeMenu">Reprendre la main</AppButton>
      </div>
    </div>
  </nav>
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
.top-nav {
  position: sticky;
  top: 0;
  z-index: 50;
  width: 100%;
  border-bottom: 1px solid #e5e7eb;
  background: rgba(255, 255, 255, 0.94);
  backdrop-filter: blur(16px);
}

.nav-inner {
  display: flex;
  width: min(1280px, calc(100% - 32px));
  min-height: 70px;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  margin: 0 auto;
}

.brand,
.desktop-links,
.nav-actions {
  display: inline-flex;
  align-items: center;
}

.brand {
  gap: 10px;
  color: #111827;
  font-size: 1.02rem;
  font-weight: 900;
  text-decoration: none;
  white-space: nowrap;
}

.brand-logo {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  object-fit: contain;
}

.desktop-links {
  gap: 4px;
  color: #374151;
  font-size: 0.94rem;
  font-weight: 650;
}

.nav-actions {
  gap: 10px;
}

.menu-toggle {
  display: none;
  width: 42px;
  height: 42px;
  flex-direction: column;
  gap: 5px;
  padding: 0;
}

.menu-toggle span {
  display: block;
  width: 18px;
  height: 2px;
  border-radius: 999px;
  background: #1f2937;
}

.mobile-menu {
  display: none;
  width: min(100% - 32px, 1280px);
  margin: 0 auto;
  padding: 0 0 14px;
  color: #1f2937;
  font-size: 0.96rem;
  font-weight: 750;
}

.mobile-menu.open {
  display: grid;
  gap: 10px;
}

.mobile-actions {
  display: grid;
  gap: 10px;
  padding-top: 8px;
}

@media (max-width: 900px) {
  .desktop-links,
  .nav-actions {
    display: none;
  }

  .menu-toggle {
    display: inline-flex;
  }

  .nav-inner {
    width: min(100% - 24px, 1280px);
  }
}
</style>
