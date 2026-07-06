<template>
  <nav
    class="TabMenu"
    aria-label="Navigation principale"
    :style="{
      '--wave-image': `url('${waveSvg}')`,
      '--splash-image': `url('${splashSvg}')`,
    }"
  >
    <div class="TabMenuWaves" aria-hidden="true"></div>
    <div class="TabMenuSplash" aria-hidden="true"></div>

    <div class="TabMenuInner">
      <NuxtLink class="TabMenuBrand" to="/" aria-label="PixelProwlers, retour à l'accueil">
        PixelProwlers
      </NuxtLink>

      <ul class="TabMenuList">
        <BoatMenuItem
          v-for="item in items"
          :key="item.label"
          :icon="item.icon"
          :label="item.label"
          :href="item.href"
          :is-active="currentPath === item.href"
        />
      </ul>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import waveSvg from '~/assets/images/waves.svg?url';
import splashSvg from '~/assets/images/splash.svg?url';
import BoatMenuItem from './BoatMenuItem.vue';

interface MenuItem {
  icon: string;
  label: string;
  href?: string;
}

interface Props {
  items: MenuItem[];
}

defineProps<Props>();

const route = useRoute();
const currentPath = computed(() => route.path);
</script>

<style scoped>
.TabMenu {
  position: sticky;
  top: 0;
  z-index: 100;
  height: 5rem;
  overflow: hidden;
  background: linear-gradient(135deg, #0f172a, #1e3a8a, #0891b2);
  box-shadow: 0 18px 36px rgba(2, 6, 23, 0.22);
}

.TabMenuWaves,
.TabMenuSplash {
  position: absolute;
  right: 0;
  bottom: 0;
  left: 0;
  pointer-events: none;
  will-change: background-position, transform, opacity;
}

.TabMenuWaves {
  height: 6rem;
  background-image: var(--wave-image);
  background-repeat: repeat-x;
  background-size: 2000px 96px;
  animation: tab-wave 10s linear infinite;
}

.TabMenuSplash {
  height: 1.25rem;
  background-image: var(--splash-image);
  background-repeat: repeat-x;
  background-size: 100px 20px;
  animation: tab-splash 7s ease-in-out infinite;
}

.TabMenuInner {
  position: relative;
  z-index: 2;
  display: flex;
  height: 100%;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
  margin: 0 1rem;
  border-radius: 0 0 28px 28px;
  background: rgba(255, 255, 255, 0.92);
  padding: 0 1rem;
  backdrop-filter: blur(10px);
}

.TabMenuBrand {
  flex: 0 0 auto;
  color: #1e3a8a;
  font-size: 1.1rem;
  font-weight: 900;
  text-decoration: none;
}

.TabMenuList {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: clamp(0.65rem, 2.4vw, 2rem);
  list-style: none;
}

@keyframes tab-wave {
  0% {
    background-position-x: 0;
  }

  100% {
    background-position-x: -2000px;
  }
}

@keyframes tab-splash {
  0%,
  100% {
    opacity: 0.66;
    transform: translateY(0);
  }

  50% {
    opacity: 1;
    transform: translateY(-3px);
  }
}

@media (max-width: 900px) {
  .TabMenu {
    height: auto;
    min-height: 5rem;
  }

  .TabMenuInner {
    align-items: flex-start;
    overflow-x: auto;
    padding: 0.5rem 0.75rem 0.8rem;
  }

  .TabMenuList {
    min-width: max-content;
  }
}
</style>
