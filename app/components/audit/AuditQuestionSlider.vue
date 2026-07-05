<template>
  <article class="QuestionCard">
    <div class="QuestionHeader">
      <h3 class="QuestionTitle">{{ question.label }}</h3>
      <span class="QuestionValue">{{ modelValue }}/10</span>
    </div>
    <input
      class="QuestionSlider"
      type="range"
      min="0"
      max="10"
      step="1"
      :value="modelValue"
      :aria-label="question.label"
      @input="$emit('update:modelValue', Number(($event.target as HTMLInputElement).value))"
    >
    <div class="QuestionScale" aria-hidden="true">
      <span>0</span>
      <span>5</span>
      <span>10</span>
    </div>
  </article>
</template>

<script setup lang="ts">
import type { AuditQuestion } from '~/composables/useAudit';

defineProps<{
  question: AuditQuestion;
  modelValue: number;
}>();

defineEmits<{
  'update:modelValue': [value: number];
}>();
</script>

<style scoped>
@reference "../../assets/css/main.css";

.QuestionCard {
  @apply grid gap-4 rounded-lg border border-[#2b7053]/15 bg-white p-5;
}

.QuestionHeader {
  @apply flex flex-wrap items-start justify-between gap-3;
}

.QuestionTitle {
  @apply max-w-[680px] text-lg font-black leading-snug text-[#17251d];
}

.QuestionValue {
  @apply rounded-lg bg-[#2b7053] px-3 py-1 text-sm font-black text-white;
}

.QuestionSlider {
  @apply h-2 w-full cursor-pointer appearance-none rounded-full bg-[#2b7053]/20 accent-[#2b7053];
}

.QuestionScale {
  @apply flex justify-between text-sm font-bold text-[#596158];
}
</style>
