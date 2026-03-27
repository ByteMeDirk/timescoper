<script setup>
defineProps({
  width: { type: String, default: "100%" },
  height: { type: String, default: "1rem" },
  borderRadius: { type: String, default: "var(--radius-md)" },
  count: { type: Number, default: 1 },
});
</script>

<template>
  <div class="skeleton-group">
    <div
      v-for="i in count"
      :key="i"
      class="skeleton"
      :style="{ width, height, borderRadius }"
      aria-hidden="true"
    />
  </div>
</template>

<style scoped>
.skeleton-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.skeleton {
  background: linear-gradient(
    90deg,
    var(--color-bg-sunken) 25%,
    var(--color-border-light) 50%,
    var(--color-bg-sunken) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s ease-in-out infinite;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
</style>
