import { defineStore } from "pinia";
import { ref } from "vue";
import { timelogApi } from "@/api/timelog";

export const useTimelogStore = defineStore("timelog", () => {
  const entries = ref([]);
  const myDailyLog = ref([]);
  const loading = ref(false);
  const error = ref(null);

  async function fetchEntries(params = {}) {
    loading.value = true;
    error.value = null;
    try {
      const { data } = await timelogApi.list(params);
      entries.value = data.results || data;
    } catch (err) {
      error.value = err.response?.data?.error || "Failed to load time entries";
    } finally {
      loading.value = false;
    }
  }

  async function fetchMyLog(date) {
    loading.value = true;
    error.value = null;
    try {
      const { data } = await timelogApi.myLog(date);
      myDailyLog.value = data.results || data;
    } catch (err) {
      error.value = err.response?.data?.error || "Failed to load daily log";
    } finally {
      loading.value = false;
    }
  }

  async function createEntry(payload) {
    const { data } = await timelogApi.create(payload);
    entries.value.unshift(data);
    return data;
  }

  async function updateEntry(id, payload) {
    const { data } = await timelogApi.update(id, payload);
    const idx = entries.value.findIndex((e) => e.id === id);
    if (idx !== -1) entries.value[idx] = data;
    return data;
  }

  async function deleteEntry(id) {
    await timelogApi.delete(id);
    entries.value = entries.value.filter((e) => e.id !== id);
  }

  return {
    entries,
    myDailyLog,
    loading,
    error,
    fetchEntries,
    fetchMyLog,
    createEntry,
    updateEntry,
    deleteEntry,
  };
});
