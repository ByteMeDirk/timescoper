<script setup>
import { Inbox } from "lucide-vue-next";

defineProps({
  icon: { type: Object, default: () => Inbox },
  title: { type: String, default: "Nothing here yet" },
  description: { type: String, default: "" },
  actionLabel: { type: String, default: "" },
});

defineEmits(["action"]);
</script>

<template>
  <div class="empty-state">
    <component :is="icon" :size="48" class="empty-state__icon" />
    <h3 class="empty-state__title">{{ title }}</h3>
    <p v-if="description" class="empty-state__description">{{ description }}</p>
    <button v-if="actionLabel" class="empty-state__action" @click="$emit('action')">
      {{ actionLabel }}
    </button>
  </div>
</template>

<style scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-12) var(--space-6);
  text-align: center;
}

.empty-state__icon {
  color: var(--color-text-muted);
  margin-bottom: var(--space-4);
}

.empty-state__title {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: var(--space-2);
}

.empty-state__description {
  font-size: var(--text-base);
  color: var(--color-text-secondary);
  max-width: 360px;
  margin-bottom: var(--space-5);
}

.empty-state__action {
  padding: var(--space-2) var(--space-5);
  background: var(--color-primary);
  color: var(--color-primary-text);
  border: none;
  border-radius: var(--radius-md);
  font-weight: 500;
  font-size: var(--text-base);
  transition: background 0.15s ease;
}

.empty-state__action:hover {
  background: var(--color-primary-hover);
}
</style>
