<script setup>
import { computed, useAttrs } from "vue";

const props = defineProps({
  modelValue: { type: [String, Number], default: "" },
  label: { type: String, default: "" },
  error: { type: String, default: "" },
  type: { type: String, default: "text" },
  placeholder: { type: String, default: "" },
});

const emit = defineEmits(["update:modelValue"]);

const inputId = computed(() => `input-${props.label?.replace(/\s/g, "-").toLowerCase()}`);
</script>

<template>
  <div class="input-group" :class="{ 'input-group--error': error }">
    <label v-if="label" :for="inputId" class="input-group__label">
      {{ label }}
    </label>
    <div class="input-group__wrapper">
      <slot name="prefix" />
      <input
        :id="inputId"
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        class="input-group__input"
        v-bind="$attrs"
        @input="emit('update:modelValue', $event.target.value)"
      />
      <slot name="suffix" />
    </div>
    <p v-if="error" class="input-group__error" role="alert">{{ error }}</p>
  </div>
</template>

<style scoped>
.input-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.input-group__label {
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--color-text);
}

.input-group__wrapper {
  display: flex;
  align-items: center;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background-color: var(--color-surface);
  transition: border-color 0.15s ease;
  overflow: hidden;
}

.input-group__wrapper:focus-within {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 2px var(--color-primary-light);
}

.input-group--error .input-group__wrapper {
  border-color: var(--color-danger);
}

.input-group__input {
  flex: 1;
  padding: var(--space-2) var(--space-3);
  border: none;
  outline: none;
  background: transparent;
  color: var(--color-text);
  font-size: var(--text-base);
}

.input-group__input::placeholder {
  color: var(--color-text-muted);
}

.input-group__error {
  font-size: var(--text-xs);
  color: var(--color-danger);
}
</style>
