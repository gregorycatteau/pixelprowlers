<template>
  <a
    v-if="href"
    :class="buttonClasses"
    :href="href"
    :aria-disabled="isUnavailable ? 'true' : undefined"
    @click="handleClick"
  >
    <slot />
  </a>
  <button
    v-else
    :class="buttonClasses"
    :type="type"
    :disabled="isUnavailable"
    @click="handleClick"
  >
    <span v-if="loading" class="ButtonIcon" aria-hidden="true">
      <svg viewBox="0 0 24 24" class="loading-icon">
        <circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="3" opacity="0.25" />
        <path d="M21 12a9 9 0 0 0-9-9" fill="none" stroke="currentColor" stroke-linecap="round" stroke-width="3" />
      </svg>
    </span>
    <slot />
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue';

type ButtonVariant = 'primary' | 'secondary' | 'validate' | 'ghost' | 'nav' | 'danger';
type ButtonSize = 'sm' | 'md' | 'lg';

const props = withDefaults(defineProps<{
  href?: string;
  variant?: ButtonVariant;
  size?: ButtonSize;
  type?: 'button' | 'submit';
  disabled?: boolean;
  loading?: boolean;
}>(), {
  variant: 'primary',
  size: 'md',
  type: 'button',
  disabled: false,
  loading: false,
});

const emit = defineEmits<{
  click: [event: MouseEvent];
}>();

const variantClasses: Record<ButtonVariant, string> = {
  primary: 'ButtonPrimary',
  secondary: 'ButtonSecondary',
  validate: 'ButtonValidate',
  ghost: 'ButtonGhost',
  nav: 'ButtonNav',
  danger: 'ButtonDanger',
};

const sizeClasses: Record<ButtonSize, string> = {
  sm: 'ButtonSmall',
  md: '',
  lg: 'ButtonLarge',
};

const isUnavailable = computed(() => props.disabled || props.loading);

const buttonClasses = computed(() => [
  'ButtonBase',
  variantClasses[props.variant],
  sizeClasses[props.size],
  { 'is-loading': props.loading },
]);

// Empêche un lien désactivé ou en chargement de déclencher une navigation.
const handleClick = (event: MouseEvent) => {
  if (isUnavailable.value) {
    event.preventDefault();
    return;
  }

  emit('click', event);
};
</script>

<style scoped>
.loading-icon {
  width: 1rem;
  height: 1rem;
  animation: button-spin 1s linear infinite;
}

@keyframes button-spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
