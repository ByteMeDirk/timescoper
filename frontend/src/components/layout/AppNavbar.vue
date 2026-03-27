<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { Sun, Moon, LogOut, User } from "lucide-vue-next";

const authStore = useAuthStore();
const router = useRouter();

const isDark = ref(document.documentElement.getAttribute("data-theme") === "dark");

function toggleTheme() {
  isDark.value = !isDark.value;
  document.documentElement.setAttribute(
    "data-theme",
    isDark.value ? "dark" : "light",
  );
}

function logout() {
  authStore.logout();
  router.push("/login");
}
</script>

<template>
  <header class="navbar">
    <div class="navbar__left">
      <h1 class="navbar__page-title">
        {{ $route.name?.charAt(0).toUpperCase() + $route.name?.slice(1) }}
      </h1>
    </div>
    <div class="navbar__right">
      <button
        class="navbar__icon-btn"
        :aria-label="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
        @click="toggleTheme"
      >
        <Moon v-if="!isDark" :size="18" />
        <Sun v-else :size="18" />
      </button>
      <div class="navbar__user">
        <User :size="16" />
        <span class="navbar__user-name">{{ authStore.user?.first_name }}</span>
      </div>
      <button class="navbar__icon-btn" aria-label="Log out" @click="logout">
        <LogOut :size="18" />
      </button>
    </div>
  </header>
</template>

<style scoped>
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: var(--navbar-height);
  padding: 0 var(--space-6);
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border-light);
  flex-shrink: 0;
}

.navbar__page-title {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: 700;
}

.navbar__right {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.navbar__icon-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border: none;
  border-radius: var(--radius-md);
  background: transparent;
  color: var(--color-text-secondary);
  transition: all 0.15s ease;
}

.navbar__icon-btn:hover {
  background: var(--color-surface-hover);
  color: var(--color-text);
}

.navbar__user {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

.navbar__user-name {
  font-weight: 500;
}

@media (max-width: 767px) {
  .navbar {
    padding: 0 var(--space-4);
  }
  .navbar__user-name {
    display: none;
  }
}
</style>
