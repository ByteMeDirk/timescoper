import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const routes = [
  {
    path: "/login",
    name: "login",
    component: () => import("@/views/auth/LoginView.vue"),
    meta: { layout: "auth", guest: true },
  },
  {
    path: "/register",
    name: "register",
    component: () => import("@/views/auth/RegisterView.vue"),
    meta: { layout: "auth", guest: true },
  },
  {
    path: "/",
    redirect: "/dashboard",
  },
  {
    path: "/dashboard",
    name: "dashboard",
    component: () => import("@/views/dashboard/DashboardView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/timelog",
    name: "timelog",
    component: () => import("@/views/timelog/TimelogView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/tasks",
    name: "tasks",
    component: () => import("@/views/tasks/TasksView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/projects",
    name: "projects",
    component: () => import("@/views/projects/ProjectsView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/reports",
    name: "reports",
    component: () => import("@/views/reporting/ReportsView.vue"),
    meta: { requiresAuth: true, roles: ["project_manager", "admin"] },
  },
  {
    path: "/team",
    name: "team",
    component: () => import("@/views/team/TeamView.vue"),
    meta: { requiresAuth: true, roles: ["team_lead", "admin"] },
  },
  {
    path: "/admin",
    name: "admin",
    component: () => import("@/views/admin/AdminView.vue"),
    meta: { requiresAuth: true, roles: ["admin"] },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();

  // Initialise auth state if needed
  if (authStore.isAuthenticated && !authStore.user) {
    await authStore.init();
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next({ name: "login", query: { redirect: to.fullPath } });
  }

  if (to.meta.guest && authStore.isAuthenticated) {
    return next({ name: "dashboard" });
  }

  if (to.meta.roles && authStore.user) {
    if (!to.meta.roles.includes(authStore.user.role)) {
      return next({ name: "dashboard" });
    }
  }

  next();
});

export default router;
