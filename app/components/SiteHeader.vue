<template>
  <header class="SiteHeader">
    <nav class="HeaderNav" aria-label="Navigation principale">
      <div class="HeaderInner container">
        <NuxtLink class="BrandLink" to="/" aria-label="PixelProwlers, retour à l'accueil" @click="closeMenu()">
          <img class="BrandLogo" src="/logo-nav-transparent.png" alt="PixelProwlers" width="240" height="90">
        </NuxtLink>

        <div class="DesktopLinks" aria-label="Liens internes">
          <NuxtLink
            v-for="link in navLinks"
            :key="link.href"
            class="NavLink"
            active-class="is-active"
            exact-active-class="is-active"
            :to="link.href"
          >
            {{ link.label }}
          </NuxtLink>
        </div>

        <div class="HeaderRight">
          <div class="HeaderActions">
            <NuxtLink class="ActionButton ActionButtonGreen" to="/diagnostic-situation">
              Demander un diagnostic
            </NuxtLink>
          </div>

          <button
            class="MenuToggle"
            type="button"
            :aria-expanded="isMenuOpen"
            aria-controls="mobile-menu"
            :aria-label="isMenuOpen ? 'Fermer le menu' : 'Ouvrir le menu'"
            @click="toggleMenu"
            ref="menuButtonRef"
          >
            <svg v-if="!isMenuOpen" class="MenuIcon" viewBox="0 0 24 24" aria-hidden="true">
              <path d="M4 7h16M4 12h16M4 17h16" fill="none" stroke="currentColor" stroke-linecap="round" stroke-width="2.2" />
            </svg>
            <svg v-else class="MenuIcon" viewBox="0 0 24 24" aria-hidden="true">
              <path d="M6 6l12 12M18 6L6 18" fill="none" stroke="currentColor" stroke-linecap="round" stroke-width="2.2" />
            </svg>
          </button>
        </div>
      </div>

      <div class="MobileMenuShell">
        <div
          id="mobile-menu"
          ref="mobileMenuRef"
          class="MobileMenu"
          :class="{ MobileMenuOpen: isMenuOpen }"
          :aria-hidden="!isMenuOpen"
        >
          <NuxtLink
            v-for="link in navLinks"
            :key="link.href"
            class="MobileLink"
            active-class="is-active"
            exact-active-class="is-active"
            :to="link.href"
            @click="closeMenu()"
          >
            {{ link.label }}
          </NuxtLink>
          <div class="MobileActions">
            <NuxtLink class="ActionButton ActionButtonGreen" to="/diagnostic-situation" @click="closeMenu()">
              Demander un diagnostic
            </NuxtLink>
          </div>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup lang="ts">
import { nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue';

const route = useRoute();
const isMenuOpen = ref(false);
const menuButtonRef = ref<HTMLButtonElement | null>(null);
const mobileMenuRef = ref<HTMLElement | null>(null);
let previousBodyOverflow = '';

const navLinks = [
  { label: 'Accueil', href: '/' },
  { label: 'Audit sécurité', href: '/audit-site-web' },
  { label: 'Développement web', href: '/refonte-site' },
  { label: 'Réparation & Linux', href: '/reparation-informatique' },
  { label: 'Accès sécurisés', href: '/transmission-acces' },
  { label: 'Urgence', href: '/urgence' },
  { label: 'À propos', href: '/a-propos' },
  { label: 'Contact', href: '/contact' },
] as const;

const closeMenu = (options: { restoreFocus?: boolean } = {}) => {
  isMenuOpen.value = false;

  if (options.restoreFocus) {
    menuButtonRef.value?.focus();
  }
};

const toggleMenu = () => {
  isMenuOpen.value ? closeMenu() : (isMenuOpen.value = true);
};

const handleKeydown = (event: KeyboardEvent) => {
  if (event.key === 'Escape' && isMenuOpen.value) {
    closeMenu({ restoreFocus: true });
  }
};

watch(isMenuOpen, async (isOpen) => {
  if (!import.meta.client) {
    return;
  }

  if (isOpen) {
    previousBodyOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    await nextTick();
    mobileMenuRef.value?.querySelector<HTMLElement>('a')?.focus();
    return;
  }

  document.body.style.overflow = previousBodyOverflow;
});

watch(() => route.path, () => closeMenu());

onMounted(() => {
  window.addEventListener('keydown', handleKeydown);
});

onBeforeUnmount(() => {
  window.removeEventListener('keydown', handleKeydown);

  if (import.meta.client) {
    document.body.style.overflow = previousBodyOverflow;
  }
});
</script>

<style scoped>
@reference "../assets/css/main.css";

/* --- LAYOUT PRINCIPAL --- */
.SiteHeader {
  @apply sticky top-0 z-50 w-full;
}

.HeaderNav {
  @apply w-full border-b;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.035), transparent 68%),
    #102033;
  border-color: rgba(255, 255, 255, 0.16);
  box-shadow: 0 10px 24px rgba(16, 32, 51, 0.18);
}

.HeaderInner {
  @apply mx-auto flex min-h-18 items-center justify-between gap-4 py-2.5;
}

.BrandLink {
  @apply inline-flex shrink-0 items-center rounded-md text-white no-underline transition;
}

.BrandLink:focus-visible {
  @apply outline-2 outline-offset-4 outline-white;
}

.BrandLogo {
  @apply h-auto w-[clamp(132px,15vw,164px)];
}

.DesktopLinks {
  @apply hidden items-center gap-1 xl:inline-flex;
}

.NavLink {
  @apply relative inline-flex min-h-11 items-center rounded-md px-3 py-2 text-[0.92rem] font-bold text-white no-underline transition-[background-color,color] duration-(--motion-feedback) ease-(--motion-ease-standard);
  background: transparent;
  text-underline-offset: 6px;
}

.NavLink:hover,
.NavLink:focus-visible {
  background: rgba(255, 255, 255, 0.12);
  color: #ffffff;
}

.NavLink.is-active {
  @apply underline decoration-2;
  background: rgba(94, 234, 212, 0.14);
  font-weight: 850;
  text-decoration-color: #5eead4;
}

.NavLink.is-active::before {
  @apply absolute inset-x-3 -bottom-[3px] block h-[3px] rounded-full;
  content: "";
  background: #5eead4;
}

.NavLink:focus-visible {
  @apply outline-2 outline-offset-2 outline-white;
}

.HeaderRight {
  @apply inline-flex items-center gap-3;
}

.HeaderActions {
  @apply hidden items-center xl:inline-flex;
}

.ActionButton {
  @apply inline-flex min-h-11 items-center justify-center rounded-md px-4 py-2.5 text-[0.94rem] font-extrabold text-white no-underline transition;
}

.ActionButton:hover,
.ActionButton:focus-visible {
  @apply outline-2 outline-offset-2 outline-white;
  background: #0d9488;
  color: #ffffff;
}

.ActionButtonGreen {
  background: #0f766e;
}

.MenuToggle {
  @apply inline-flex h-11 w-11 items-center justify-center rounded-md border text-white transition xl:hidden;
  border-color: rgba(255, 255, 255, 0.28);
  background: rgba(255, 255, 255, 0.08);
}

.MenuToggle:hover,
.MenuToggle:focus-visible {
  background: #ffffff;
  color: #102033;
}

.MenuToggle:focus-visible {
  @apply outline-2 outline-offset-2 outline-white;
}

.MenuIcon {
  @apply h-5 w-5;
}

.MobileMenuShell {
  @apply mx-auto w-[min(100%-32px,1120px)];
}

.MobileMenu {
  @apply pointer-events-none grid max-h-0 translate-y-[-6px] overflow-hidden pb-0 opacity-0 transition-all duration-(--motion-standard) ease-(--motion-ease-standard);
}

.MobileMenuOpen {
  @apply pointer-events-auto max-h-[calc(100vh-88px)] translate-y-0 gap-3 overflow-y-auto pb-4 opacity-100;
}

.MobileLink {
  @apply rounded-md border px-4 py-3.5 text-[1rem] font-bold text-white no-underline opacity-0 transition-[background-color,color,opacity,transform] duration-(--motion-standard) ease-(--motion-ease-enter);
  border-color: rgba(255, 255, 255, 0.22);
  background: #172a42;
  text-underline-offset: 6px;
  transform: translateY(6px);
}

/*
 * Légère cascade à l’ouverture : chaque lien apparaît avec un décalage
 * croissant, pour donner une sensation d’espace plutôt qu’un bloc figé.
 * N’a d’effet que si le panneau est ouvert (les liens fermés restent à
 * opacity 0, déjà neutralisés par pointer-events-none sur le parent).
 */
.MobileMenuOpen .MobileLink {
  opacity: 1;
  transform: none;
}

.MobileMenuOpen .MobileLink:nth-child(1) { transition-delay: 20ms; }
.MobileMenuOpen .MobileLink:nth-child(2) { transition-delay: 45ms; }
.MobileMenuOpen .MobileLink:nth-child(3) { transition-delay: 70ms; }
.MobileMenuOpen .MobileLink:nth-child(4) { transition-delay: 95ms; }
.MobileMenuOpen .MobileLink:nth-child(5) { transition-delay: 120ms; }
.MobileMenuOpen .MobileLink:nth-child(6) { transition-delay: 145ms; }
.MobileMenuOpen .MobileLink:nth-child(7) { transition-delay: 170ms; }
.MobileMenuOpen .MobileLink:nth-child(8) { transition-delay: 195ms; }

.MobileLink:hover,
.MobileLink:focus-visible {
  background: rgba(255, 255, 255, 0.12);
  color: #ffffff;
}

.MobileLink.is-active {
  @apply underline decoration-2;
  background: rgba(94, 234, 212, 0.14);
  border-color: rgba(94, 234, 212, 0.4);
  font-weight: 850;
  text-decoration-color: #5eead4;
}

.MobileLink:focus-visible {
  @apply outline-2 outline-offset-2 outline-white;
}

.MobileActions {
  @apply grid gap-3;
}

@media (max-width: 1279px) {
  .DesktopLinks { @apply hidden; }
}

@media (max-width: 767px) {
  .HeaderNav {
    background: #102033;
  }
  .HeaderInner {
    @apply min-w-0 gap-2;
  }
  .BrandLogo {
    @apply w-[clamp(132px,42vw,160px)];
  }
}

@media (min-width: 821px) and (max-width: 1279px) {
  .ActionButton { @apply min-w-42.5; }
}
</style>
