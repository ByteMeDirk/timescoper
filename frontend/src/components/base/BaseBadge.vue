<script setup>
import { computed } from "vue";

const props = defineProps({
  variant: {
    type: String,
    default: "default",
    validator: (v) =>
      [
        "default",
        "primary",
        "success",
        "warning",
        "danger",
        "backlog",
        "in_progress",
        "in_review",
        "done",
        "cancelled",
        "low",
        "medium",
        "high",
        "critical",
      ].includes(v),
  },
  size: {
    type: String,
    default: "sm",
    validator: (v) => ["sm", "md"].includes(v),
  },
});

const colorMap = {
  default: { bg: "var(--color-bg-sunken)", text: "var(--color-text-secondary)" },
  primary: { bg: "var(--color-primary-light)", text: "var(--color-primary)" },
  success: { bg: "var(--color-success-light)", text: "var(--color-success)" },
  warning: { bg: "var(--color-warning-light)", text: "var(--color-warning)" },
  danger: { bg: "var(--color-danger-light)", text: "var(--color-danger)" },
  // Task statuses
  backlog: { bg: "var(--color-bg-sunken)", text: "var(--color-text-secondary)" },
  in_progress: { bg: "#e0f0ff", text: "#0066cc" },
  in_review: { bg: "var(--color-warning-light)", text: "var(--color-warning)" },
  done: { bg: "var(--color-success-light)", text: "var(--color-success)" },
  cancelled: { bg: "var(--color-danger-light)", text: "var(--color-danger)" },
  // Priorities
  low: { bg: "var(--color-bg-sunken)", text: "var(--color-text-secondary)" },
  medium: { bg: "#e0f0ff", text: "#0066cc" },
  high: { bg: "var(--color-warning-light)", text: "var(--color-warning)" },
  critical: { bg: "var(--color-danger-light)", text: "var(--color-danger)" },
};

const style = computed(() => {
  const c = colorMap[props.variant] || colorMap.default;
  return { backgroundColor: c.bg, color: c.text };
});
</script>

<template>
  <span class="badge" :class="`badge--${size}`" :style="style">
    <slot />
  </span>
</template>

<style scoped>
.badge {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  font-weight: 500;
  border-radius: var(--radius-full);
  white-space: nowrap;
}

.badge--sm {
  padding: 2px var(--space-2);
  font-size: var(--text-xs);
}

.badge--md {
  padding: var(--space-1) var(--space-3);
  font-size: var(--text-sm);
}
</style>
