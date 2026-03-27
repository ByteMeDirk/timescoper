import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { authApi } from "@/api/auth";

export const useAuthStore = defineStore("auth", () => {
  const user = ref(null);
  const accessToken = ref(sessionStorage.getItem("ts_access_token") || null);
  const refreshToken = ref(sessionStorage.getItem("ts_refresh_token") || null);
  const loading = ref(false);
  const error = ref(null);

  const isAuthenticated = computed(() => !!accessToken.value);
  const userRole = computed(() => user.value?.role || null);
  const isAdmin = computed(() => userRole.value === "admin");
  const isTeamLead = computed(
    () => ["team_lead", "admin"].includes(userRole.value),
  );
  const isProjectManager = computed(
    () => ["project_manager", "admin"].includes(userRole.value),
  );

  function setTokens(access, refresh) {
    accessToken.value = access;
    refreshToken.value = refresh;
    sessionStorage.setItem("ts_access_token", access);
    sessionStorage.setItem("ts_refresh_token", refresh);
  }

  function clearAuth() {
    user.value = null;
    accessToken.value = null;
    refreshToken.value = null;
    sessionStorage.removeItem("ts_access_token");
    sessionStorage.removeItem("ts_refresh_token");
  }

  async function login(email, password) {
    loading.value = true;
    error.value = null;
    try {
      const { data } = await authApi.login(email, password);
      setTokens(data.access, data.refresh);
      await fetchMe();
    } catch (err) {
      error.value =
        err.response?.data?.error || err.response?.data?.detail || "Login failed";
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function register(payload) {
    loading.value = true;
    error.value = null;
    try {
      await authApi.register(payload);
    } catch (err) {
      error.value =
        err.response?.data?.error || "Registration failed";
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function fetchMe() {
    try {
      const { data } = await authApi.getMe();
      user.value = data;
    } catch {
      clearAuth();
    }
  }

  function logout() {
    clearAuth();
  }

  // Restore session on page load
  async function init() {
    if (accessToken.value) {
      await fetchMe();
    }
  }

  return {
    user,
    accessToken,
    refreshToken,
    loading,
    error,
    isAuthenticated,
    userRole,
    isAdmin,
    isTeamLead,
    isProjectManager,
    login,
    register,
    fetchMe,
    logout,
    init,
  };
});
