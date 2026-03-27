import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { tasksApi } from "@/api/tasks";

export const useTasksStore = defineStore("tasks", () => {
  const tasks = ref([]);
  const currentTask = ref(null);
  const loading = ref(false);
  const error = ref(null);

  const tasksByStatus = computed(() => {
    const groups = {
      backlog: [],
      in_progress: [],
      in_review: [],
      done: [],
    };
    for (const task of tasks.value) {
      if (groups[task.status]) {
        groups[task.status].push(task);
      }
    }
    return groups;
  });

  async function fetchTasks(params = {}) {
    loading.value = true;
    error.value = null;
    try {
      const { data } = await tasksApi.list(params);
      tasks.value = data.results || data;
    } catch (err) {
      error.value = err.response?.data?.error || "Failed to load tasks";
    } finally {
      loading.value = false;
    }
  }

  async function fetchTask(id) {
    loading.value = true;
    error.value = null;
    try {
      const { data } = await tasksApi.get(id);
      currentTask.value = data;
      return data;
    } catch (err) {
      error.value = err.response?.data?.error || "Failed to load task";
    } finally {
      loading.value = false;
    }
  }

  async function createTask(payload) {
    const { data } = await tasksApi.create(payload);
    tasks.value.unshift(data);
    return data;
  }

  async function updateTask(id, payload) {
    const { data } = await tasksApi.update(id, payload);
    const idx = tasks.value.findIndex((t) => t.id === id);
    if (idx !== -1) tasks.value[idx] = data;
    if (currentTask.value?.id === id) currentTask.value = data;
    return data;
  }

  async function deleteTask(id) {
    await tasksApi.delete(id);
    tasks.value = tasks.value.filter((t) => t.id !== id);
  }

  return {
    tasks,
    currentTask,
    loading,
    error,
    tasksByStatus,
    fetchTasks,
    fetchTask,
    createTask,
    updateTask,
    deleteTask,
  };
});
