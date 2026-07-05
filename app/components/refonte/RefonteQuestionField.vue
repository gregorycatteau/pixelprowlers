<template>
  <article class="RefonteQuestionCard">
    <h3 class="RefonteQuestionTitle">{{ question.label }}</h3>

    <textarea
      v-if="question.type === 'text'"
      class="RefonteTextarea"
      rows="4"
      :value="modelValue as string"
      :placeholder="question.placeholder"
      @input="$emit('update:modelValue', ($event.target as HTMLTextAreaElement).value)"
    ></textarea>

    <select
      v-else-if="question.type === 'select'"
      class="RefonteSelect"
      :value="modelValue as string"
      @change="$emit('update:modelValue', ($event.target as HTMLSelectElement).value)"
    >
      <option value="">Choisir une réponse</option>
      <option v-for="option in question.options" :key="option" :value="option">{{ option }}</option>
    </select>

    <div v-else-if="question.type === 'radio'" class="RefonteChoiceGrid">
      <label v-for="option in question.options" :key="option" class="RefonteChoice">
        <input
          type="radio"
          :name="question.id"
          :value="option"
          :checked="modelValue === option"
          @change="$emit('update:modelValue', option)"
        >
        <span>{{ option }}</span>
      </label>
    </div>

    <div v-else-if="question.type === 'checkbox'" class="RefonteChoiceGrid">
      <label v-for="option in question.options" :key="option" class="RefonteChoice">
        <input
          type="checkbox"
          :value="option"
          :checked="Array.isArray(modelValue) && modelValue.includes(option)"
          @change="toggleOption(option)"
        >
        <span>{{ option }}</span>
      </label>
    </div>

    <div v-else class="RefonteChoiceGrid">
      <label class="RefonteChoice">
        <input type="radio" :name="question.id" :checked="modelValue === true" @change="$emit('update:modelValue', true)">
        <span>Oui</span>
      </label>
      <label class="RefonteChoice">
        <input type="radio" :name="question.id" :checked="modelValue === false" @change="$emit('update:modelValue', false)">
        <span>Non</span>
      </label>
    </div>
  </article>
</template>

<script setup lang="ts">
import type { RefonteQuestion } from '~/composables/useRefonteAudit';

const props = defineProps<{
  question: RefonteQuestion;
  modelValue: string | string[] | boolean;
}>();

const emit = defineEmits<{
  'update:modelValue': [value: string | string[] | boolean];
}>();

const toggleOption = (option: string) => {
  const current = Array.isArray(props.modelValue) ? props.modelValue : [];
  emit('update:modelValue', current.includes(option)
    ? current.filter((item) => item !== option)
    : [...current, option]);
};
</script>

<style scoped>
@reference "../../assets/css/main.css";

.RefonteQuestionCard {
  @apply grid gap-4 rounded-lg border border-[#2b7053]/15 bg-white p-5;
}

.RefonteQuestionTitle {
  @apply text-lg font-black leading-snug text-[#17251d];
}

.RefonteTextarea,
.RefonteSelect {
  @apply w-full min-w-0 rounded-lg border border-[#2b7053]/18 bg-[#fbfaf5] px-4 py-3 font-bold text-[#17251d] outline-none transition focus:border-[#2b7053] focus:ring-2 focus:ring-[#2b7053]/20;
}

.RefonteTextarea::placeholder {
  @apply text-xs font-bold text-[#435046]/55;
}

.RefonteChoiceGrid {
  @apply grid gap-3;
}

.RefonteChoice {
  @apply flex items-start gap-3 rounded-lg border border-[#2b7053]/15 bg-[#fbfaf5] p-4 font-bold text-[#27322a] transition hover:border-[#2b7053]/45;
}

.RefonteChoice input {
  @apply mt-1 shrink-0;
}

@media (min-width: 680px) {
  .RefonteChoiceGrid {
    @apply grid-cols-2;
  }
}
</style>
