<script setup>
import { onMounted, onUnmounted, ref, watch } from "vue";
import { X } from "lucide-vue-next";

const props = defineProps({
  open: { type: Boolean, default: false },
  title: { type: String, default: "" },
});

const emit = defineEmits(["close"]);
const modalRef = ref(null);

function onKeydown(e) {
  if (e.key === "Escape") emit("close");
}

function onBackdropClick(e) {
  if (e.target === e.currentTarget) emit("close");
}

onMounted(() => document.addEventListener("keydown", onKeydown));
onUnmounted(() => document.removeEventListener("keydown", onKeydown));

// Trap focus
watch(
  () => props.open,
  (isOpen) => {
    if (isOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }
  },
);
</script>

<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="open" class="modal-backdrop" @click="onBackdropClick">
        <div ref="modalRef" class="modal" role="dialog" aria-modal="true" :aria-label="title">
          <div class="modal__header">
            <h3 class="modal__title">{{ title }}</h3>
            <button class="modal__close" aria-label="Close modal" @click="emit('close')">
              <X :size="18" />
            </button>
          </div>
          <div class="modal__body">
            <slot />
          </div>
          <div v-if="$slots.footer" class="modal__footer">
            <slot name="footer" />
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: var(--space-4);
}

.modal {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  width: 100%;
  max-width: 520px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.modal__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-4) var(--space-5);
  border-bottom: 1px solid var(--color-border-light);
}

.modal__title {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: 700;
}

.modal__close {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  color: var(--color-text-secondary);
  border-radius: var(--radius-sm);
  transition: all 0.15s ease;
}

.modal__close:hover {
  background: var(--color-surface-hover);
  color: var(--color-text);
}

.modal__body {
  padding: var(--space-5);
  overflow-y: auto;
  flex: 1;
}

.modal__footer {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-3);
  padding: var(--space-4) var(--space-5);
  border-top: 1px solid var(--color-border-light);
}

/* Transitions */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s ease;
}
.modal-enter-active .modal,
.modal-leave-active .modal {
  transition: transform 0.2s ease;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
.modal-enter-from .modal {
  transform: scale(0.95) translateY(10px);
}
.modal-leave-to .modal {
  transform: scale(0.95) translateY(10px);
}
</style>
