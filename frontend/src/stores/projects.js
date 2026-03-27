import { defineStore } from "pinia";
import { ref } from "vue";
import { projectsApi } from "@/api/projects";

export const useProjectsStore = defineStore("projects", () => {
  const projects = ref([]);
  const currentProject = ref(null);
  const loading = ref(false);
  const error = ref(null);

  async function fetchProjects(params = {}) {
    loading.value = true;
    error.value = null;
    try {
      const { data } = await projectsApi.list(params);
      projects.value = data.results || data;
    } catch (err) {
      error.value = err.response?.data?.error || "Failed to load projects";
    } finally {
      loading.value = false;
    }
  }

  async function fetchProject(id) {
    loading.value = true;
    error.value = null;
    try {
      const { data } = await projectsApi.get(id);
      currentProject.value = data;
      return data;
    } catch (err) {
      error.value = err.response?.data?.error || "Failed to load project";
    } finally {
      loading.value = false;
    }
  }

  async function createProject(payload) {
    const { data } = await projectsApi.create(payload);
    projects.value.unshift(data);
    return data;
  }

  async function updateProject(id, payload) {
    const { data } = await projectsApi.update(id, payload);
    const idx = projects.value.findIndex((p) => p.id === id);
    if (idx !== -1) projects.value[idx] = data;
    if (currentProject.value?.id === id) currentProject.value = data;
    return data;
  }

  async function deleteProject(id) {
    await projectsApi.delete(id);
    projects.value = projects.value.filter((p) => p.id !== id);
  }

  return {
    projects,
    currentProject,
    loading,
    error,
    fetchProjects,
    fetchProject,
    createProject,
    updateProject,
    deleteProject,
  };
});
