<script setup>
defineProps({
  padding: { type: Boolean, default: true },
});
</script>

<template>
  <div class="card" :class="{ 'card--padded': padding }">
    <div v-if="$slots.header" class="card__header">
      <slot name="header" />
    </div>
    <div class="card__body">
      <slot />
    </div>
    <div v-if="$slots.footer" class="card__footer">
      <slot name="footer" />
    </div>
  </div>
</template>

<style scoped>
.card {
  background: var(--color-surface);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
}

.card--padded .card__body {
  padding: var(--space-5);
}

.card__header {
  padding: var(--space-4) var(--space-5);
  border-bottom: 1px solid var(--color-border-light);
  font-family: var(--font-display);
  font-weight: 600;
}

.card__footer {
  padding: var(--space-3) var(--space-5);
  border-top: 1px solid var(--color-border-light);
  background: var(--color-bg-sunken);
}
</style>
