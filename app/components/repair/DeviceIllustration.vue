<template>
  <svg viewBox="0 0 160 110" width="160" height="110" aria-hidden="true" focusable="false" class="DeviceArt">
    <g fill="none" stroke="currentColor" stroke-width="3" stroke-linejoin="round">
      <template v-if="family === 'laptop'"><rect x="30" y="18" width="100" height="65" rx="6"/><path d="M30 83 14 98h132l-16-15M65 91h30"/><path d="M42 68V31h76v37"/></template>
      <template v-else-if="family === 'desktop'"><rect x="12" y="20" width="84" height="60" rx="5"/><path d="M54 80v17M32 98h44"/><rect x="108" y="12" width="40" height="86" rx="5"/><path d="M116 28h24M116 39h24"/><circle cx="128" cy="80" r="4"/></template>
      <template v-else><rect :x="family === 'phone' ? 51 : 33" y="10" :width="family === 'phone' ? 58 : 94" height="90" rx="9"/><path d="M70 18h20M73 92h14"/><path :d="family === 'phone' ? 'M60 30h40v50H60z' : 'M43 30h74v50H43z'"/></template>
      <path d="M8 10h16v12M152 102h-16V90" opacity=".3"/>
    </g>
  </svg>
</template>
<script setup lang="ts">
import type { DeviceFamily } from '~/utils/repairGrid';
defineProps<{ family: DeviceFamily }>();
</script>
<style scoped>
@reference "../../assets/css/main.css";
.DeviceArt { @apply mx-auto h-24 w-full max-w-40 text-pxp-green; }
</style>
