<template>
  <article class="group h-full rounded-lg border border-forest/15 bg-paper p-6 shadow-sm transition hover:-translate-y-1 hover:border-trust/45 hover:shadow-soft">
    <div class="mb-5 flex h-12 w-12 items-center justify-center rounded-lg bg-trust/10 text-trust">
      <svg class="h-7 w-7" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
        <path v-if="icon === 'code'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 9l-4 3 4 3m8-6l4 3-4 3M14 5l-4 14" />
        <path v-else-if="icon === 'hardware'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3h6m-8 4h10a2 2 0 012 2v8a2 2 0 01-2 2H7a2 2 0 01-2-2V9a2 2 0 012-2zm3 4h4m-4 4h2" />
        <path v-else-if="icon === 'shield'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3l7 4v5c0 5-3.5 8-7 9-3.5-1-7-4-7-9V7l7-4zm-3 9l2 2 4-5" />
        <path v-else-if="icon === 'training'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6l8 4-8 4-8-4 8-4zm-5 7v3c0 1.5 2.2 3 5 3s5-1.5 5-3v-3" />
        <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
      </svg>
    </div>

    <h3 class="text-2xl text-ink">{{ title }}</h3>
    <p class="mt-4 leading-7 text-muted">{{ description }}</p>

    <NuxtLink v-if="href" :to="href" class="mt-6 inline-flex rounded-md font-bold text-forest outline-none transition hover:text-trust focus-visible:ring-2 focus-visible:ring-scan focus-visible:ring-offset-2 focus-visible:ring-offset-paper">
      {{ linkLabel }}
    </NuxtLink>
  </article>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  title: string;
  description: string;
  icon?: 'code' | 'hardware' | 'shield' | 'training' | 'bolt';
  href?: string;
  linkLabel?: string;
}>(), {
  icon: 'bolt',
  href: '',
  linkLabel: 'Découvrir',
});
</script>
