import { defineStore } from "pinia";
import { ref } from "vue";
import { reportingApi } from "@/api/reporting";

export const useReportingStore = defineStore("reporting", () => {
  const dailySummary = ref(null);
  const weeklySummary = ref(null);
  const projectUtilisation = ref(null);
  const teamActivity = ref(null);
  const loading = ref(false);
  const error = ref(null);

  async function fetchDailySummary(params = {}) {
    loading.value = true;
    error.value = null;
    try {
      const { data } = await reportingApi.dailySummary(params);
      dailySummary.value = data;
    } catch (err) {
      error.value = err.response?.data?.error || "Failed to load daily summary";
    } finally {
      loading.value = false;
    }
  }

  async function fetchWeeklySummary(params = {}) {
    loading.value = true;
    error.value = null;
    try {
      const { data } = await reportingApi.weeklySummary(params);
      weeklySummary.value = data;
    } catch (err) {
      error.value = err.response?.data?.error || "Failed to load weekly summary";
    } finally {
      loading.value = false;
    }
  }

  async function fetchProjectUtilisation(projectId) {
    loading.value = true;
    error.value = null;
    try {
      const { data } = await reportingApi.projectUtilisation(projectId);
      projectUtilisation.value = data;
    } catch (err) {
      error.value = err.response?.data?.error || "Failed to load utilisation";
    } finally {
      loading.value = false;
    }
  }

  async function fetchTeamActivity(params = {}) {
    loading.value = true;
    error.value = null;
    try {
      const { data } = await reportingApi.teamActivity(params);
      teamActivity.value = data;
    } catch (err) {
      error.value = err.response?.data?.error || "Failed to load team activity";
    } finally {
      loading.value = false;
    }
  }

  return {
    dailySummary,
    weeklySummary,
    projectUtilisation,
    teamActivity,
    loading,
    error,
    fetchDailySummary,
    fetchWeeklySummary,
    fetchProjectUtilisation,
    fetchTeamActivity,
  };
});
