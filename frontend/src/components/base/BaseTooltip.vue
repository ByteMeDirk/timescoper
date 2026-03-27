<script setup>
import { ref } from "vue";

defineProps({
  text: { type: String, required: true },
  position: {
    type: String,
    default: "top",
    validator: (v) => ["top", "bottom", "left", "right"].includes(v),
  },
});

const visible = ref(false);
</script>

<template>
  <div
    class="tooltip-wrapper"
    @mouseenter="visible = true"
    @mouseleave="visible = false"
    @focus="visible = true"
    @blur="visible = false"
  >
    <slot />
    <Transition name="tooltip">
      <span v-if="visible" class="tooltip" :class="`tooltip--${position}`" role="tooltip">
        {{ text }}
      </span>
    </Transition>
  </div>
</template>

<style scoped>
.tooltip-wrapper {
  position: relative;
  display: inline-flex;
}

.tooltip {
  position: absolute;
  padding: var(--space-1) var(--space-2);
  font-size: var(--text-xs);
  font-weight: 500;
  color: #fff;
  background: var(--color-text);
  border-radius: var(--radius-sm);
  white-space: nowrap;
  pointer-events: none;
  z-index: 100;
}

.tooltip--top {
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  margin-bottom: 6px;
}

.tooltip--bottom {
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  margin-top: 6px;
}

.tooltip-enter-active,
.tooltip-leave-active {
  transition: opacity 0.15s ease;
}
.tooltip-enter-from,
.tooltip-leave-to {
  opacity: 0;
}
</style>
