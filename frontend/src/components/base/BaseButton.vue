<script setup>
import { computed } from "vue";
import { Loader2 } from "lucide-vue-next";

const props = defineProps({
  variant: {
    type: String,
    default: "primary",
    validator: (v) => ["primary", "secondary", "ghost", "danger"].includes(v),
  },
  size: {
    type: String,
    default: "md",
    validator: (v) => ["sm", "md", "lg"].includes(v),
  },
  loading: { type: Boolean, default: false },
  disabled: { type: Boolean, default: false },
  type: { type: String, default: "button" },
});

defineEmits(["click"]);

const classes = computed(() => [
  "btn",
  `btn--${props.variant}`,
  `btn--${props.size}`,
  { "btn--loading": props.loading },
]);
</script>

<template>
  <button
    :class="classes"
    :type="type"
    :disabled="disabled || loading"
    @click="$emit('click', $event)"
  >
    <Loader2 v-if="loading" class="btn__spinner" :size="16" />
    <slot v-else />
  </button>
</template>

<style scoped>
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  border: 1px solid transparent;
  border-radius: var(--radius-md);
  font-family: var(--font-body);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s ease;
  white-space: nowrap;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Sizes */
.btn--sm {
  padding: var(--space-1) var(--space-3);
  font-size: var(--text-sm);
  height: 32px;
}
.btn--md {
  padding: var(--space-2) var(--space-4);
  font-size: var(--text-base);
  height: 38px;
}
.btn--lg {
  padding: var(--space-3) var(--space-6);
  font-size: var(--text-md);
  height: 44px;
}

/* Variants */
.btn--primary {
  background-color: var(--color-primary);
  color: var(--color-primary-text);
}
.btn--primary:hover:not(:disabled) {
  background-color: var(--color-primary-hover);
}

.btn--secondary {
  background-color: transparent;
  color: var(--color-text);
  border-color: var(--color-border);
}
.btn--secondary:hover:not(:disabled) {
  background-color: var(--color-surface-hover);
}

.btn--ghost {
  background-color: transparent;
  color: var(--color-text-secondary);
}
.btn--ghost:hover:not(:disabled) {
  background-color: var(--color-surface-hover);
  color: var(--color-text);
}

.btn--danger {
  background-color: var(--color-danger);
  color: #fff;
}
.btn--danger:hover:not(:disabled) {
  background-color: var(--color-danger-hover);
}

/* Loading spinner */
.btn__spinner {
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>
