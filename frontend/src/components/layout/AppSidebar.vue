<script setup>
import { computed, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import {
  LayoutDashboard,
  Clock,
  CheckSquare,
  FolderKanban,
  BarChart3,
  Users,
  Shield,
  ChevronLeft,
  ChevronRight,
  Timer,
} from "lucide-vue-next";

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const collapsed = ref(false);

const navItems = computed(() => {
  const items = [
    { name: "Dashboard", icon: LayoutDashboard, path: "/dashboard" },
    { name: "Time Log", icon: Clock, path: "/timelog" },
    { name: "Tasks", icon: CheckSquare, path: "/tasks" },
    { name: "Projects", icon: FolderKanban, path: "/projects" },
  ];

  if (["project_manager", "admin"].includes(authStore.userRole)) {
    items.push({ name: "Reports", icon: BarChart3, path: "/reports" });
  }

  if (["team_lead", "admin"].includes(authStore.userRole)) {
    items.push({ name: "Team", icon: Users, path: "/team" });
  }

  if (authStore.isAdmin) {
    items.push({ name: "Admin", icon: Shield, path: "/admin" });
  }

  return items;
});

function isActive(path) {
  return route.path === path;
}
</script>

<template>
  <aside class="sidebar" :class="{ 'sidebar--collapsed': collapsed }">
    <div class="sidebar__brand">
      <Timer :size="24" class="sidebar__logo" />
      <span v-if="!collapsed" class="sidebar__title">TimeScoper</span>
    </div>

    <nav class="sidebar__nav">
      <router-link
        v-for="item in navItems"
        :key="item.path"
        :to="item.path"
        class="sidebar__link"
        :class="{ 'sidebar__link--active': isActive(item.path) }"
        :aria-label="item.name"
      >
        <component :is="item.icon" :size="20" />
        <span v-if="!collapsed" class="sidebar__link-text">{{ item.name }}</span>
      </router-link>
    </nav>

    <button
      class="sidebar__toggle"
      :aria-label="collapsed ? 'Expand sidebar' : 'Collapse sidebar'"
      @click="collapsed = !collapsed"
    >
      <ChevronLeft v-if="!collapsed" :size="18" />
      <ChevronRight v-else :size="18" />
    </button>
  </aside>
</template>

<style scoped>
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  width: var(--sidebar-width);
  background: var(--color-surface);
  border-right: 1px solid var(--color-border-light);
  display: flex;
  flex-direction: column;
  z-index: 50;
  transition: width 0.2s ease;
}

.sidebar--collapsed {
  width: var(--sidebar-collapsed);
}

.sidebar__brand {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-4) var(--space-4);
  border-bottom: 1px solid var(--color-border-light);
  min-height: var(--navbar-height);
}

.sidebar__logo {
  color: var(--color-primary);
  flex-shrink: 0;
}

.sidebar__title {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: 700;
  color: var(--color-text);
  white-space: nowrap;
}

.sidebar__nav {
  flex: 1;
  padding: var(--space-3);
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  overflow-y: auto;
}

.sidebar__link {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  font-size: var(--text-base);
  font-weight: 500;
  text-decoration: none;
  transition: all 0.15s ease;
  white-space: nowrap;
}

.sidebar__link:hover {
  background: var(--color-surface-hover);
  color: var(--color-text);
  text-decoration: none;
}

.sidebar__link--active {
  background: var(--color-primary-light);
  color: var(--color-primary);
}

.sidebar__link-text {
  overflow: hidden;
  text-overflow: ellipsis;
}

.sidebar__toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-3);
  border: none;
  border-top: 1px solid var(--color-border-light);
  background: transparent;
  color: var(--color-text-muted);
  transition: all 0.15s ease;
}

.sidebar__toggle:hover {
  background: var(--color-surface-hover);
  color: var(--color-text);
}

@media (max-width: 1023px) and (min-width: 768px) {
  .sidebar {
    width: var(--sidebar-collapsed);
  }
  .sidebar__title,
  .sidebar__link-text {
    display: none;
  }
}

@media (max-width: 767px) {
  .sidebar {
    display: none;
  }
}
</style>
