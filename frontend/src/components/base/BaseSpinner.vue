<script setup>
import { Loader2 } from "lucide-vue-next";

defineProps({
  size: { type: Number, default: 24 },
  label: { type: String, default: "Loading" },
});
</script>

<template>
  <div class="spinner" role="status" :aria-label="label">
    <Loader2 :size="size" class="spinner__icon" />
    <span class="sr-only">{{ label }}</span>
  </div>
</template>

<style scoped>
.spinner {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.spinner__icon {
  animation: spin 0.8s linear infinite;
  color: var(--color-primary);
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  border: 0;
}
</style>
