<template>
  <svg viewBox="0 0 160 110" width="160" height="110" aria-hidden="true" focusable="false" class="DeviceArt">
    <g fill="none" stroke="currentColor" stroke-width="3" stroke-linejoin="round">
      <template v-if="family === 'laptop'"><rect x="30" y="18" width="100" height="65" rx="6"/><path d="M30 83 14 98h132l-16-15M65 91h30"/><path d="M42 68V31h76v37"/></template>
      <template v-else-if="family === 'desktop'"><rect x="12" y="20" width="84" height="60" rx="5"/><path d="M54 80v17M32 98h44"/><rect x="108" y="12" width="40" height="86" rx="5"/><path d="M116 28h24M116 39h24"/><circle cx="128" cy="80" r="4"/></template>
      <template v-else-if="family === 'console'"><rect x="22" y="20" width="56" height="74" rx="5"/><path d="M33 20v74M40 35h24M40 44h24"/><rect x="88" y="45" width="54" height="40" rx="8"/><path d="M98 65h15M105 58v14"/><circle cx="130" cy="61" r="2"/><circle cx="124" cy="70" r="2"/></template>
      <template v-else-if="family === 'controller'"><path d="M52 30h56c14 0 20 15 25 40 5 25-8 31-24 9H51C35 101 22 95 27 70c5-25 11-40 25-40Z"/><path d="M44 49h20M54 39v20"/><circle cx="73" cy="67" r="8"/><circle cx="97" cy="67" r="8"/><circle cx="117" cy="43" r="2"/><circle cx="126" cy="52" r="2"/><circle cx="108" cy="52" r="2"/><circle cx="117" cy="61" r="2"/></template>
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
