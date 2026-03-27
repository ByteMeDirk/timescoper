<script setup>
import { onMounted, ref, computed } from "vue";
import { useProjectsStore } from "@/stores/projects";
import { useAuthStore } from "@/stores/auth";
import BaseCard from "@/components/base/BaseCard.vue";
import BaseButton from "@/components/base/BaseButton.vue";
import BaseInput from "@/components/base/BaseInput.vue";
import BaseSelect from "@/components/base/BaseSelect.vue";
import BaseBadge from "@/components/base/BaseBadge.vue";
import BaseModal from "@/components/base/BaseModal.vue";
import SkeletonLoader from "@/components/base/SkeletonLoader.vue";
import EmptyState from "@/components/base/EmptyState.vue";
import { Plus, FolderKanban } from "lucide-vue-next";

const projectsStore = useProjectsStore();
const authStore = useAuthStore();
const loading = ref(true);
const showCreateModal = ref(false);

const newProject = ref({ name: "", description: "", team: "", budget_hours: "", status: "active" });
const createError = ref("");

const canManage = computed(() =>
  ["team_lead", "project_manager", "admin"].includes(authStore.userRole),
);

function burnPct(project) {
  if (!project.budget_hours || project.budget_hours === 0) return 0;
  return Math.min(100, Math.round((project.total_logged_hours / project.budget_hours) * 100));
}

function burnColor(pct) {
  if (pct >= 90) return "var(--color-danger)";
  if (pct >= 70) return "var(--color-warning)";
  return "var(--color-primary)";
}

const statusOptions = [
  { value: "active", label: "Active" },
  { value: "on_hold", label: "On Hold" },
  { value: "completed", label: "Completed" },
  { value: "archived", label: "Archived" },
];

async function submitProject() {
  createError.value = "";
  try {
    await projectsStore.createProject(newProject.value);
    showCreateModal.value = false;
    newProject.value = { name: "", description: "", team: "", budget_hours: "", status: "active" };
  } catch (err) {
    createError.value = err.response?.data?.error || "Failed to create project.";
  }
}

onMounted(async () => {
  await projectsStore.fetchProjects();
  loading.value = false;
});
</script>

<template>
  <div class="projects-page">
    <div class="projects-page__header">
      <h2 class="projects-page__title">Projects</h2>
      <BaseButton v-if="canManage" variant="primary" size="sm" @click="showCreateModal = true">
        <Plus :size="16" /> New project
      </BaseButton>
    </div>

    <div v-if="loading" class="projects-grid">
      <SkeletonLoader v-for="i in 6" :key="i" height="180px" />
    </div>

    <div v-else-if="projectsStore.projects.length" class="projects-grid">
      <BaseCard v-for="project in projectsStore.projects" :key="project.id" class="project-card">
        <div class="project-card__top">
          <div class="project-card__name-row">
            <h3 class="project-card__name">{{ project.name }}</h3>
            <BaseBadge :variant="project.status === 'active' ? 'success' : 'default'" size="sm">
              {{ project.status.replace("_", " ") }}
            </BaseBadge>
          </div>
          <p v-if="project.description" class="project-card__desc">{{ project.description }}</p>
        </div>

        <div class="project-card__stats">
          <div class="project-card__stat">
            <span class="project-card__stat-value">{{ project.task_count || 0 }}</span>
            <span class="project-card__stat-label">Tasks</span>
          </div>
          <div class="project-card__stat">
            <span class="project-card__stat-value">{{ project.total_logged_hours || 0 }}h</span>
            <span class="project-card__stat-label">Logged</span>
          </div>
          <div v-if="project.budget_hours" class="project-card__stat">
            <span class="project-card__stat-value">{{ project.budget_hours }}h</span>
            <span class="project-card__stat-label">Budget</span>
          </div>
        </div>

        <div v-if="project.budget_hours" class="project-card__burn">
          <div class="burn-bar">
            <div
              class="burn-bar__fill"
              :style="{ width: burnPct(project) + '%', backgroundColor: burnColor(burnPct(project)) }"
            />
          </div>
          <span class="burn-bar__label">{{ burnPct(project) }}% used</span>
        </div>
      </BaseCard>
    </div>

    <EmptyState
      v-else
      :icon="FolderKanban"
      title="No projects yet"
      description="Create your first project to start tracking work."
      :action-label="canManage ? 'Create project' : ''"
      @action="showCreateModal = true"
    />

    <BaseModal :open="showCreateModal" title="Create Project" @close="showCreateModal = false">
      <form class="modal-form" @submit.prevent="submitProject">
        <p v-if="createError" class="modal-form__error">{{ createError }}</p>
        <BaseInput v-model="newProject.name" label="Name" placeholder="Project name" required />
        <BaseInput v-model="newProject.description" label="Description" placeholder="Brief description" />
        <BaseInput v-model="newProject.budget_hours" label="Budget (hours)" type="number" min="0" placeholder="e.g. 200" />
        <BaseSelect v-model="newProject.status" label="Status" :options="statusOptions" />
        <BaseButton type="submit" variant="primary">Create project</BaseButton>
      </form>
    </BaseModal>
  </div>
</template>

<style scoped>
.projects-page {
  max-width: 1200px;
}

.projects-page__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-6);
}

.projects-page__title {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: 700;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: var(--space-4);
}

.project-card__top {
  margin-bottom: var(--space-4);
}

.project-card__name-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-1);
}

.project-card__name {
  font-family: var(--font-display);
  font-size: var(--text-md);
  font-weight: 700;
}

.project-card__desc {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.project-card__stats {
  display: flex;
  gap: var(--space-6);
  margin-bottom: var(--space-4);
}

.project-card__stat {
  display: flex;
  flex-direction: column;
}

.project-card__stat-value {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: var(--text-md);
}

.project-card__stat-label {
  font-size: var(--text-xs);
  color: var(--color-text-muted);
}

.project-card__burn {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.burn-bar {
  flex: 1;
  height: 6px;
  background: var(--color-bg-sunken);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.burn-bar__fill {
  height: 100%;
  border-radius: var(--radius-full);
  transition: width 0.3s ease;
}

.burn-bar__label {
  font-size: var(--text-xs);
  color: var(--color-text-muted);
  white-space: nowrap;
}

.modal-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.modal-form__error {
  padding: var(--space-2);
  background: var(--color-danger-light);
  color: var(--color-danger);
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
}

@media (max-width: 767px) {
  .projects-grid {
    grid-template-columns: 1fr;
  }
}
</style>
