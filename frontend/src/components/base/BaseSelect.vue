<script setup>
import { computed } from "vue";
import { ChevronDown } from "lucide-vue-next";

const props = defineProps({
  modelValue: { type: [String, Number], default: "" },
  label: { type: String, default: "" },
  options: { type: Array, default: () => [] },
  placeholder: { type: String, default: "Select..." },
  error: { type: String, default: "" },
});

const emit = defineEmits(["update:modelValue"]);

const selectId = computed(() => `select-${props.label?.replace(/\s/g, "-").toLowerCase()}`);
</script>

<template>
  <div class="select-group" :class="{ 'select-group--error': error }">
    <label v-if="label" :for="selectId" class="select-group__label">
      {{ label }}
    </label>
    <div class="select-group__wrapper">
      <select
        :id="selectId"
        :value="modelValue"
        class="select-group__select"
        @change="emit('update:modelValue', $event.target.value)"
      >
        <option value="" disabled>{{ placeholder }}</option>
        <option v-for="opt in options" :key="opt.value" :value="opt.value">
          {{ opt.label }}
        </option>
      </select>
      <ChevronDown :size="16" class="select-group__icon" />
    </div>
    <p v-if="error" class="select-group__error" role="alert">{{ error }}</p>
  </div>
</template>

<style scoped>
.select-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.select-group__label {
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--color-text);
}

.select-group__wrapper {
  position: relative;
}

.select-group__select {
  width: 100%;
  padding: var(--space-2) var(--space-8) var(--space-2) var(--space-3);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  color: var(--color-text);
  font-size: var(--text-base);
  appearance: none;
  cursor: pointer;
  transition: border-color 0.15s ease;
}

.select-group__select:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 2px var(--color-primary-light);
  outline: none;
}

.select-group--error .select-group__select {
  border-color: var(--color-danger);
}

.select-group__icon {
  position: absolute;
  right: var(--space-3);
  top: 50%;
  transform: translateY(-50%);
  color: var(--color-text-muted);
  pointer-events: none;
}

.select-group__error {
  font-size: var(--text-xs);
  color: var(--color-danger);
}
</style>
