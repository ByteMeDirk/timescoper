<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";
import AppSidebar from "@/components/layout/AppSidebar.vue";
import AppNavbar from "@/components/layout/AppNavbar.vue";
import MobileNav from "@/components/layout/MobileNav.vue";
import { useAuthStore } from "@/stores/auth";

const route = useRoute();
const authStore = useAuthStore();

const isAuthPage = computed(() => {
  return route.meta?.layout === "auth";
});
</script>

<template>
  <div v-if="isAuthPage" class="auth-layout">
    <router-view />
  </div>
  <div v-else class="app-layout">
    <AppSidebar v-if="authStore.isAuthenticated" />
    <div class="app-main">
      <AppNavbar v-if="authStore.isAuthenticated" />
      <main class="app-content">
        <router-view />
      </main>
    </div>
    <MobileNav v-if="authStore.isAuthenticated" />
  </div>
</template>

<style scoped>
.auth-layout {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--color-bg);
}

.app-layout {
  display: flex;
  min-height: 100vh;
  background-color: var(--color-bg);
}

.app-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.app-content {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-6);
}

@media (min-width: 1024px) {
  .app-main {
    margin-left: var(--sidebar-width);
  }
}

@media (max-width: 1023px) and (min-width: 768px) {
  .app-main {
    margin-left: var(--sidebar-collapsed);
  }
}

@media (max-width: 767px) {
  .app-content {
    padding: var(--space-4);
    padding-bottom: calc(var(--mobile-nav-height) + var(--space-4));
  }
}
</style>
