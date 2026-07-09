<template>
  <header class="SiteHeader" :class="{ 'is-home': isHome }">
    <!-- Mascotte Sauveteur (position fixe en haut à droite) -->
    <div class="RescueProwler" aria-hidden="true">
      <svg
        class="RescueLadder"
        viewBox="0 0 120 180"
        xmlns="http://www.w3.org/2000/svg"
      >
        <!-- Échelle -->
        <rect x="50" y="0" width="8" height="180" fill="#d4a574" stroke="#8b6914" stroke-width="1" />
        <rect x="46" y="0" width="16" height="8" fill="#d4a574" stroke="#8b6914" stroke-width="1" />
        <rect x="46" y="30" width="16" height="8" fill="#d4a574" stroke="#8b6914" stroke-width="1" />
        <rect x="46" y="60" width="16" height="8" fill="#d4a574" stroke="#8b6914" stroke-width="1" />
        <rect x="46" y="90" width="16" height="8" fill="#d4a574" stroke="#8b6914" stroke-width="1" />
        <rect x="46" y="120" width="16" height="8" fill="#d4a574" stroke="#8b6914" stroke-width="1" />
        <rect x="46" y="150" width="16" height="8" fill="#d4a574" stroke="#8b6914" stroke-width="1" />

        <!-- Sauveteur (PixelProwlers) -->
        <g transform="translate(30, 20)">
          <!-- Corps -->
          <rect x="50" y="40" width="40" height="60" fill="#1a2b3c" rx="5" />
          <!-- Tête -->
          <circle cx="70" cy="30" r="12" fill="#1a2b3c" />
          <!-- Casque -->
          <path d="M60 20 L80 20 L75 10 L65 10 Z" fill="#00bcd4" />
          <!-- Visage -->
          <circle cx="68" cy="28" r="1" fill="#ffffff" />
          <circle cx="72" cy="28" r="1" fill="#ffffff" />
          <path d="M68 32 Q70 34 72 32" stroke="#ffffff" stroke-width="1" fill="none" />
          <!-- Bras -->
          <rect x="40" y="45" width="10" height="20" fill="#1a2b3c" rx="2" />
          <rect x="90" y="45" width="10" height="20" fill="#1a2b3c" rx="2" />
          <!-- Jambes -->
          <rect x="55" y="100" width="10" height="25" fill="#1a2b3c" rx="2" />
          <rect x="65" y="100" width="10" height="25" fill="#1a2b3c" rx="2" />
          <!-- Échelle tenue -->
          <rect x="35" y="60" width="8" height="20" fill="#d4a574" rx="1" />
        </g>
      </svg>
    </div>

    <nav class="HeaderNav" aria-label="Navigation principale">
      <div class="HeaderInner container">
        <!-- Logo -->
        <NuxtLink class="BrandLink" to="/" aria-label="PixelProwlers, retour à l'accueil" @click="closeMenu">
          <img class="BrandLogo" src="/logo-nav-transparent.png" alt="PixelProwlers" width="240" height="90">
        </NuxtLink>

        <!-- Menu Desktop -->
        <div class="DesktopLinks" aria-label="Liens internes">
          <NuxtLink
            v-for="link in navLinks"
            :key="link.href"
            class="NavLink"
            :to="link.href"
          >
            {{ link.label }}
          </NuxtLink>
        </div>

        <!-- Icônes utilitaires et actions -->
        <div class="HeaderRight">
          <div class="UtilityIcons" aria-label="Raccourcis">
            <NuxtLink
              v-for="shortcut in shortcuts"
              :key="shortcut.href"
              class="IconLink"
              :to="shortcut.href"
              :aria-label="shortcut.label"
              :title="shortcut.label"
            >
              <svg v-if="shortcut.kind === 'user'" class="IconSvg" viewBox="0 0 24 24" aria-hidden="true">
                <path d="M20 21a8 8 0 0 0-16 0" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" />
                <circle cx="12" cy="8" r="4" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" />
              </svg>
              <svg v-else-if="shortcut.kind === 'lock'" class="IconSvg" viewBox="0 0 24 24" aria-hidden="true">
                <rect x="5" y="11" width="14" height="10" rx="2" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" />
                <path d="M8 11V8a4 4 0 0 1 8 0v3" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" />
              </svg>
              <svg v-else-if="shortcut.kind === 'bell'" class="IconSvg" viewBox="0 0 24 24" aria-hidden="true">
                <path d="M6 17h12l-1.2-2.4V11a4.8 4.8 0 0 0-9.6 0v3.6L6 17Z" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" />
                <path d="M10 19a2 2 0 0 0 4 0" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" />
              </svg>
            </NuxtLink>
          </div>

          <!-- Bouton d'action principal -->
          <div v-if="!isHome" class="HeaderActions">
            <NuxtLink class="ActionButton ActionButtonGreen" to="/diagnostic-situation">
              Faire le diagnostic gratuit
            </NuxtLink>
          </div>

          <!-- Bouton menu mobile -->
          <button
            class="MenuToggle"
            type="button"
            :aria-expanded="isMenuOpen"
            aria-controls="mobile-menu"
            aria-label="Ouvrir ou fermer le menu"
            @click="isMenuOpen = !isMenuOpen"
          >
            <svg class="MenuIcon" viewBox="0 0 24 24" aria-hidden="true">
              <path d="M4 7h16M4 12h16M4 17h16" fill="none" stroke="currentColor" stroke-linecap="round" stroke-width="2.2" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Menu Mobile -->
      <div class="MobileMenuShell">
        <div id="mobile-menu" class="MobileMenu" :class="{ MobileMenuOpen: isMenuOpen }">
          <NuxtLink v-for="link in navLinks" :key="link.href" class="MobileLink" :to="link.href" @click="closeMenu">
            {{ link.label }}
          </NuxtLink>
          <div class="MobileShortcuts">
            <NuxtLink v-for="shortcut in shortcuts" :key="shortcut.href" class="MobileShortcut" :to="shortcut.href" @click="closeMenu">
              {{ shortcut.label }}
            </NuxtLink>
          </div>
          <div v-if="!isHome" class="MobileActions">
            <NuxtLink class="ActionButton ActionButtonGreen" to="/diagnostic-situation" @click="closeMenu">
              Faire le diagnostic gratuit
            </NuxtLink>
          </div>
        </div>
      </div>
    </nav>

    <!-- Vagues avec plage de sable -->
    <div class="NavWave" aria-hidden="true"></div>
  </header>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';

const route = useRoute();
const isMenuOpen = ref(false);
const isHome = computed(() => route.path === '/');

const navLinks = [
  { label: 'Audit', href: '/audit-site-web' },
  { label: 'Refonte', href: '/refonte-site' },
  { label: 'Transmission', href: '/transmission-acces' },
  { label: 'Urgence', href: '/urgence' },
  { label: 'À propos', href: '/a-propos' },
] as const;

const shortcuts = [
  { label: 'Accès contact', href: '/contact', kind: 'user' },
  { label: 'Sécurité', href: '/transmission-acces', kind: 'lock' },
  { label: 'Alertes', href: '/urgence', kind: 'bell' },
] as const;

const closeMenu = () => {
  isMenuOpen.value = false;
};
</script>

<style scoped>
@reference "../assets/css/main.css";

/* --- LAYOUT PRINCIPAL --- */
.SiteHeader {
  @apply relative z-50 w-full;
}

/* --- NAVBAR PRINCIPALE --- */
.HeaderNav {
  @apply sticky top-0 z-50 w-full overflow-hidden border-b backdrop-blur-xl;
  background: linear-gradient(135deg, #0c4a6e, #0891b2, #10b981);
  border-color: rgba(6, 182, 212, 0.6);
  box-shadow:
    0 4px 18px rgba(0, 0, 0, 0.3),
    inset 0 -1px 0 rgba(224, 242, 254, 0.22);
}

/* --- EFFETS D'EAU (VAGUES + ECUME) --- */
.HeaderNav::before,
.HeaderNav::after {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  will-change: transform, opacity;
}

.HeaderNav::before {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 100' preserveAspectRatio='xMidYMid slice'%3E%3Cpath d='M0,50 Q50,30 100,50 T200,50 L200,100 L0,100 Z' fill='rgba(255,255,255,0.12)' opacity='0.8'/%3E%3Cpath d='M0,60 Q50,40 100,60 T200,60 L200,100 L0,100 Z' fill='rgba(255,255,255,0.18)' opacity='0.9'/%3E%3Cpath d='M0,70 Q50,50 100,70 T200,70 L200,100 L0,100 Z' fill='rgba(255,255,255,0.24)'/%3E%3Ccircle cx='30' cy='95' r='2' fill='white' opacity='0.7'/%3E%3Ccircle cx='80' cy='90' r='1.5' fill='white' opacity='0.7'/%3E%3Ccircle cx='130' cy='95' r='2' fill='white' opacity='0.7'/%3E%3Ccircle cx='180' cy='90' r='1.5' fill='white' opacity='0.7'/%3E%3C/svg%3E");
  background-repeat: repeat-x;
  background-size: 220px 110px;
  opacity: 0.9;
  animation: waveReverse 10s ease-in-out infinite;
}

.HeaderNav::after {
  background:
    radial-gradient(circle at 6% 100%, rgba(224, 242, 254, 0.35) 0 1px, transparent 2px),
    radial-gradient(circle at 36% 95%, rgba(224, 242, 254, 0.28) 0 1px, transparent 2px),
    radial-gradient(circle at 72% 100%, rgba(224, 242, 254, 0.32) 0 1px, transparent 2px);
  background-size: 180px 80px;
  opacity: 0.55;
  animation: bubbleRise 4s ease-in-out infinite;
}

/* --- CONTENU INTERNE --- */
.HeaderInner {
  @apply relative z-10 mx-auto flex min-h-20.5 items-center justify-between gap-5 py-3;
}

/* --- LOGO --- */
.BrandLink {
  @apply inline-flex min-w-0 items-center text-white no-underline;
}

.BrandLogo {
  @apply h-auto w-[clamp(140px,20vw,190px)];
  filter: drop-shadow(0 8px 18px rgba(2, 6, 23, 0.35));
}

/* --- MENU DESKTOP --- */
.DesktopLinks {
  @apply hidden items-center gap-8 lg:inline-flex;
}

.NavLink {
  @apply relative rounded-full px-4 py-2 text-[1.05rem] font-semibold text-white no-underline transition;
  /* --- CONTRASTE RENFORCÉ POUR MALVOYANTS --- */
  text-shadow:
    0 1px 2px rgba(0, 0, 0, 0.5),
    0 2px 4px rgba(0, 0, 0, 0.3),
    0 0 0 1px rgba(255, 255, 255, 0.4);
  letter-spacing: 0.02em;
  /* ---------------------------------------- */
  animation: shipFloat 7s ease-in-out infinite;
  will-change: transform;
}

.NavLink::before {
  content: "";
  position: absolute;
  right: 12px;
  bottom: 0;
  left: 12px;
  height: 3px;
  border-radius: 999px;
  background: linear-gradient(90deg, transparent, rgba(224, 242, 254, 0.3), #06b6d4, rgba(224, 242, 254, 0.3), transparent);
  opacity: 0.7;
  transform: translateY(8px);
}

.NavLink:nth-child(2) { animation-delay: -1s; }
.NavLink:nth-child(3) { animation-delay: -2s; }
.NavLink:nth-child(4) { animation-delay: -3s; }
.NavLink:nth-child(5) { animation-delay: -4s; }

.NavLink:hover,
.NavLink:focus-visible {
  @apply text-white;
  box-shadow:
    0 10px 22px rgba(2, 6, 23, 0.18),
    inset 0 0 0 1px rgba(224, 242, 254, 0.3);
}

/* --- ICÔNES UTILITAIRES --- */
.HeaderRight {
  @apply inline-flex items-center gap-3;
}

.UtilityIcons {
  @apply inline-flex items-center gap-3;
}

.IconLink {
  @apply inline-flex h-8 w-8 items-center justify-center rounded-full text-white transition;
  animation: iconWave 5s ease-in-out infinite;
  filter: drop-shadow(0 6px 10px rgba(2, 6, 23, 0.28));
  will-change: transform;
}

.IconLink:nth-child(2) { animation-delay: -1.6s; }
.IconLink:nth-child(3) { animation-delay: -3.2s; }

.IconLink:hover,
.IconLink:focus-visible {
  @apply text-white;
  transform: rotate(15deg);
}

.IconSvg {
  @apply h-8 w-8;
}

/* --- BOUTONS D'ACTION --- */
.HeaderActions {
  @apply hidden items-center gap-3 xl:inline-flex;
}

.ActionButton {
  @apply inline-flex h-12.5 min-w-50 items-center justify-center rounded-full px-6 text-[1rem] font-bold text-white no-underline transition;
  box-shadow: 0 12px 30px rgba(2, 6, 23, 0.22);
}

.ActionButton:hover,
.ActionButton:focus-visible {
  @apply -translate-y-0.5;
}

.ActionButtonGreen {
  background: linear-gradient(180deg, #10b981 0%, #047857 100%);
}

/* --- BOUTON MENU MOBILE --- */
.MenuToggle {
  @apply inline-flex h-8 w-8 items-center justify-center rounded-full border bg-white/10 text-white transition lg:hidden;
  border-color: rgba(224, 242, 254, 0.42);
}

.MenuToggle:hover,
.MenuToggle:focus-visible {
  @apply text-white;
  transform: rotate(15deg);
}

.MenuIcon {
  @apply h-5 w-5;
}

/* --- MASCOTTE SAUVETEUR --- */
.RescueProwler {
  @apply absolute top-4 right-6 z-20 hidden lg:block;
  animation: rescueFloat 8s ease-in-out infinite;
}

.RescueLadder {
  @apply h-45 w-auto;
  filter: drop-shadow(0 12px 24px rgba(0, 0, 0, 0.3));
}

/* --- MENU MOBILE --- */
.MobileMenuShell {
  @apply relative z-10 mx-auto w-[min(100%-24px,1280px)];
}

.MobileMenu {
  @apply grid max-h-0 overflow-hidden pb-0 opacity-0 transition-all duration-300 ease-out;
}

.MobileMenuOpen {
  @apply max-h-120 gap-3 pb-4 opacity-100;
}

.MobileLink,
.MobileShortcut {
  @apply rounded-lg border px-4 py-3 text-[1rem] font-semibold text-white no-underline transition;
  border-color: rgba(224, 242, 254, 0.24);
  background: rgba(26, 43, 60, 0.58);
  animation: shipFloat 7s ease-in-out infinite;
  will-change: transform;
}

.MobileLink:hover,
.MobileShortcut:hover,
.MobileLink:focus-visible,
.MobileShortcut:focus-visible {
  @apply text-white;
}

.MobileShortcuts,
.MobileActions {
  @apply grid gap-3;
}

/* --- PLAGE DE SABLE FIN --- */
.NavWave {
  @apply h-5.5 w-full;
  background:
    linear-gradient(180deg,
      rgba(245, 230, 205, 0.8) 0%,
      rgba(238, 221, 190, 0.9) 50%,
      rgba(222, 203, 170, 1) 100%
    ),
    linear-gradient(90deg, #0c4a6e, #0891b2, #10b981);
  clip-path: polygon(
    0 0, 100% 0, 100% 60%, 92% 78%, 82% 55%, 70% 82%, 55% 50%,
    40% 80%, 25% 55%, 15% 82%, 5% 60%, 0 85%
  );
  animation: waveBreathe 10s ease-in-out infinite;
  will-change: clip-path;
  position: relative;
}

.NavWave::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 100%;
  background:
    repeating-linear-gradient(
      90deg,
      transparent,
      transparent 2px,
      rgba(255, 255, 255, 0.15) 2px,
      rgba(255, 255, 255, 0.15) 4px
    );
  opacity: 0.3;
  pointer-events: none;
}

/* --- ANIMATIONS --- */
@keyframes waveReverse {
  0%, 100% { transform: translateY(-6px) translateX(0); }
  25% { transform: translateY(5px) translateX(12px); }
  50% { transform: translateY(12px) translateX(24px); }
  75% { transform: translateY(4px) translateX(12px); }
}

@keyframes bubbleRise {
  0%, 100% { transform: translateY(0) translateX(0); opacity: 0.44; }
  50% { transform: translateY(8px) translateX(18px); opacity: 0.68; }
}

@keyframes shipFloat {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  25% { transform: translateY(-3px) rotate(0.5deg); }
  50% { transform: translateY(0) rotate(0deg); }
  75% { transform: translateY(2px) rotate(-0.5deg); }
}

@keyframes iconWave {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

@keyframes waveBreathe {
  0%, 100% {
    clip-path: polygon(
      0 0, 100% 0, 100% 60%, 92% 78%, 82% 55%, 70% 82%, 55% 50%,
      40% 80%, 25% 55%, 15% 82%, 5% 60%, 0 85%
    );
  }
  50% {
    clip-path: polygon(
      0 0, 100% 0, 100% 70%, 92% 55%, 82% 80%, 70% 55%, 55% 85%,
      40% 60%, 25% 85%, 15% 60%, 5% 85%, 0 65%
    );
  }
}

@keyframes rescueFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}

/* --- RESPONSIVE --- */
@media (max-width: 1024px) {
  .DesktopLinks { @apply hidden; }
}

@media (max-width: 767px) {
  .HeaderNav {
    background: linear-gradient(135deg, #0a3a5a, #067a8a, #0d9488);
  }
  .HeaderNav::before, .HeaderNav::after { display: none; }
  .NavWave { height: 16px; animation: none; }
  .RescueProwler { display: none !important; }
  .HeaderInner {
    @apply min-w-0 gap-2;
  }
  .BrandLogo {
    @apply w-[clamp(132px,42vw,160px)];
  }
  .UtilityIcons {
    @apply gap-2;
  }
  .IconLink {
    @apply h-7 w-7;
  }
  .IconSvg {
    @apply h-6 w-6;
  }
}

@media (max-width: 820px) {
  .HeaderActions { @apply hidden; }
}

@media (min-width: 821px) and (max-width: 1279px) {
  .ActionButton { @apply min-w-42.5; }
}
</style>
