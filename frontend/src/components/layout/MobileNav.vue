<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import {
  LayoutDashboard,
  Clock,
  CheckSquare,
  FolderKanban,
  BarChart3,
} from "lucide-vue-next";

const route = useRoute();
const authStore = useAuthStore();

const navItems = computed(() => {
  const items = [
    { name: "Dashboard", icon: LayoutDashboard, path: "/dashboard" },
    { name: "Time", icon: Clock, path: "/timelog" },
    { name: "Tasks", icon: CheckSquare, path: "/tasks" },
    { name: "Projects", icon: FolderKanban, path: "/projects" },
  ];

  if (["project_manager", "admin"].includes(authStore.userRole)) {
    items.push({ name: "Reports", icon: BarChart3, path: "/reports" });
  }

  return items.slice(0, 5);
});

function isActive(path) {
  return route.path === path;
}
</script>

<template>
  <nav class="mobile-nav" aria-label="Mobile navigation">
    <router-link
      v-for="item in navItems"
      :key="item.path"
      :to="item.path"
      class="mobile-nav__item"
      :class="{ 'mobile-nav__item--active': isActive(item.path) }"
      :aria-label="item.name"
    >
      <component :is="item.icon" :size="20" />
      <span class="mobile-nav__label">{{ item.name }}</span>
    </router-link>
  </nav>
</template>

<style scoped>
.mobile-nav {
  display: none;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: var(--mobile-nav-height);
  background: var(--color-surface);
  border-top: 1px solid var(--color-border-light);
  z-index: 50;
  justify-content: space-around;
  align-items: center;
  padding: 0 var(--space-2);
}

@media (max-width: 767px) {
  .mobile-nav {
    display: flex;
  }
}

.mobile-nav__item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  padding: var(--space-1);
  color: var(--color-text-muted);
  font-size: var(--text-xs);
  text-decoration: none;
  transition: color 0.15s ease;
  min-width: 56px;
}

.mobile-nav__item:hover,
.mobile-nav__item--active {
  color: var(--color-primary);
  text-decoration: none;
}

.mobile-nav__label {
  font-weight: 500;
}
</style>
