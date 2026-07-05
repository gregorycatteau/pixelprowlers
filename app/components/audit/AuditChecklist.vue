<template>
  <aside class="CheckList" aria-label="Progression du formulaire">
    <p class="CheckListTitle">Progression</p>
    <button
      v-for="item in items"
      :key="item.id"
      class="CheckListItem"
      :class="{ CheckListItemValid: item.valid }"
      type="button"
      @click="$emit('focusItem', item.id)"
    >
      <span class="CheckListIcon" aria-hidden="true">
        <span v-if="item.valid" class="CheckListCheck">✓</span>
        <span v-else class="CheckListPending"></span>
      </span>
      <span class="CheckListLabel">{{ item.label }}</span>
    </button>
  </aside>
</template>

<script setup lang="ts">
defineProps<{
  items: Array<{
    id: string;
    label: string;
    valid: boolean;
  }>;
}>();

defineEmits<{
  focusItem: [id: string];
}>();
</script>

<style scoped>
@reference "../../assets/css/main.css";

.CheckList {
  @apply sticky top-24 grid gap-3 rounded-lg border border-white/40 bg-white/70 p-5 shadow-sm backdrop-blur;
}

.CheckListTitle {
  @apply text-sm font-black uppercase tracking-wide text-[#2b7053];
}

.CheckListItem {
  @apply flex w-full items-center gap-3 rounded-lg border border-transparent bg-transparent p-2 text-left text-sm font-bold text-[#6b746d] transition hover:bg-white/70;
}

.CheckListItemValid {
  @apply text-[#2b7053];
}

.CheckListIcon {
  @apply flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-[#2b7053]/10;
}

.CheckListCheck {
  @apply text-base font-black text-[#2b7053] transition;
}

.CheckListPending {
  @apply h-2.5 w-2.5 animate-pulse rounded-full bg-[#6b746d]/45;
}

.CheckListLabel {
  @apply leading-snug;
}
</style>
