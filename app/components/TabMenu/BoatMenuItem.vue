<template>
  <li class="BoatMenuItem" :class="{ 'is-active': isActive }">
    <NuxtLink v-if="href" :to="href" class="BoatMenuItemLink">
      <span class="BoatMenuIcon" :class="icon" aria-hidden="true"></span>
      <span>{{ label }}</span>
    </NuxtLink>
    <span v-else class="BoatMenuItemLink">
      <span class="BoatMenuIcon" :class="icon" aria-hidden="true"></span>
      <span>{{ label }}</span>
    </span>
    <span class="BoatWake" aria-hidden="true"></span>
  </li>
</template>

<script setup lang="ts">
interface Props {
  icon: string;
  label: string;
  href?: string;
  isActive?: boolean;
}

defineProps<Props>();
</script>

<style scoped>
.BoatMenuItem {
  position: relative;
  color: #1f2937;
  font-size: 1rem;
  font-weight: 700;
  animation: boat-float 7.5s ease-in-out infinite;
  transition:
    color 0.3s ease,
    transform 0.3s ease;
  will-change: transform;
}

.BoatMenuItem:hover,
.BoatMenuItem:focus-within {
  color: #ea580c;
  transform: rotate(15deg) translateY(-5px);
}

.BoatMenuItem.is-active {
  color: #ea580c;
}

.BoatMenuItemLink {
  display: flex;
  min-width: 92px;
  min-height: 64px;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.35rem;
  border-radius: 0 0 18px 18px;
  background: rgba(255, 255, 255, 0.9);
  padding: 0.6rem 1rem;
  color: inherit;
  text-decoration: none;
  box-shadow: 0 14px 28px rgba(2, 6, 23, 0.18);
}

.BoatMenuIcon {
  width: 1.7rem;
  height: 1.7rem;
  color: currentColor;
}

.BoatMenuIcon::before {
  display: block;
  font-size: 1.45rem;
  line-height: 1;
}

.fa-search::before {
  content: "🔍";
}

.fa-hammer::before {
  content: "🔨";
}

.fa-exchange-alt::before {
  content: "🔁";
}

.fa-exclamation-triangle::before {
  content: "⚠️";
}

.fa-info-circle::before {
  content: "ℹ️";
}

.BoatWake {
  position: absolute;
  right: 10%;
  bottom: -0.45rem;
  left: 10%;
  height: 0.3rem;
  border-radius: 999px;
  background: linear-gradient(90deg, transparent, #f97316, #2563eb, transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.BoatMenuItem:hover .BoatWake,
.BoatMenuItem:focus-within .BoatWake {
  opacity: 1;
}

@keyframes boat-float {
  0%,
  100% {
    transform: translateY(0) rotate(0deg);
  }

  50% {
    transform: translateY(-4px) rotate(0.75deg);
  }
}
</style>
