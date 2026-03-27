<script setup>
import { onMounted, ref, computed } from "vue";
import { useTasksStore } from "@/stores/tasks";
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
import { Plus, LayoutGrid, List, CheckSquare } from "lucide-vue-next";

const tasksStore = useTasksStore();
const projectsStore = useProjectsStore();
const authStore = useAuthStore();

const loading = ref(true);
const viewMode = ref("kanban"); // kanban | list
const showCreateModal = ref(false);
const showDetailPanel = ref(false);
const selectedTask = ref(null);

// Filters
const filterProject = ref("");
const filterPriority = ref("");

const filteredTasks = computed(() => {
  let list = tasksStore.tasks;
  if (filterProject.value) list = list.filter((t) => t.project === filterProject.value);
  if (filterPriority.value) list = list.filter((t) => t.priority === filterPriority.value);
  return list;
});

const columns = [
  { key: "backlog", label: "Backlog" },
  { key: "in_progress", label: "In Progress" },
  { key: "in_review", label: "In Review" },
  { key: "done", label: "Done" },
];

function tasksByColumn(status) {
  return filteredTasks.value.filter((t) => t.status === status);
}

// Create task form
const newTask = ref({
  title: "",
  project: "",
  priority: "medium",
  description: "",
});
const createError = ref("");

async function submitTask() {
  createError.value = "";
  try {
    await tasksStore.createTask(newTask.value);
    showCreateModal.value = false;
    newTask.value = { title: "", project: "", priority: "medium", description: "" };
  } catch (err) {
    createError.value = err.response?.data?.error || "Failed to create task.";
  }
}

function openDetail(task) {
  selectedTask.value = task;
  showDetailPanel.value = true;
}

async function updateTaskStatus(taskId, newStatus) {
  await tasksStore.updateTask(taskId, { status: newStatus });
}

const projectOptions = computed(() =>
  projectsStore.projects.map((p) => ({ value: p.id, label: p.name })),
);

const priorityOptions = [
  { value: "low", label: "Low" },
  { value: "medium", label: "Medium" },
  { value: "high", label: "High" },
  { value: "critical", label: "Critical" },
];

async function loadTasks() {
  loading.value = true;
  await Promise.all([
    tasksStore.fetchTasks(),
    projectsStore.fetchProjects(),
  ]);
  loading.value = false;
}

onMounted(loadTasks);
</script>

<template>
  <div class="tasks-page">
    <div class="tasks-page__header">
      <div>
        <h2 class="tasks-page__title">Tasks</h2>
      </div>
      <div class="tasks-page__actions">
        <div class="tasks-page__filters">
          <BaseSelect v-model="filterProject" :options="projectOptions" placeholder="All projects" />
          <BaseSelect v-model="filterPriority" :options="priorityOptions" placeholder="All priorities" />
        </div>
        <div class="tasks-page__view-toggle">
          <button
            :class="['view-btn', { 'view-btn--active': viewMode === 'kanban' }]"
            aria-label="Kanban view"
            @click="viewMode = 'kanban'"
          >
            <LayoutGrid :size="16" />
          </button>
          <button
            :class="['view-btn', { 'view-btn--active': viewMode === 'list' }]"
            aria-label="List view"
            @click="viewMode = 'list'"
          >
            <List :size="16" />
          </button>
        </div>
        <BaseButton variant="primary" size="sm" @click="showCreateModal = true">
          <Plus :size="16" /> New task
        </BaseButton>
      </div>
    </div>

    <!-- Skeleton -->
    <div v-if="loading" class="tasks-page__skeleton">
      <SkeletonLoader v-for="i in 4" :key="i" height="300px" />
    </div>

    <!-- Kanban View -->
    <div v-else-if="viewMode === 'kanban'" class="kanban">
      <div v-for="col in columns" :key="col.key" class="kanban__column">
        <div class="kanban__column-header">
          <span class="kanban__column-title">{{ col.label }}</span>
          <BaseBadge variant="default" size="sm">{{ tasksByColumn(col.key).length }}</BaseBadge>
        </div>
        <div class="kanban__cards">
          <div
            v-for="task in tasksByColumn(col.key)"
            :key="task.id"
            class="kanban__card"
            @click="openDetail(task)"
          >
            <p class="kanban__card-title">{{ task.title }}</p>
            <div class="kanban__card-meta">
              <BaseBadge :variant="task.priority" size="sm">{{ task.priority }}</BaseBadge>
              <span v-if="task.project_name" class="kanban__card-project">{{ task.project_name }}</span>
            </div>
          </div>
          <EmptyState
            v-if="tasksByColumn(col.key).length === 0"
            :icon="CheckSquare"
            title="Empty"
            class="kanban__empty"
          />
        </div>
      </div>
    </div>

    <!-- List View -->
    <div v-else class="task-list">
      <BaseCard :padding="false">
        <table class="task-table">
          <thead>
            <tr>
              <th>Title</th>
              <th>Project</th>
              <th>Status</th>
              <th>Priority</th>
              <th>Assignee</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="task in filteredTasks"
              :key="task.id"
              class="task-table__row"
              @click="openDetail(task)"
            >
              <td class="task-table__title">{{ task.title }}</td>
              <td>{{ task.project_name }}</td>
              <td><BaseBadge :variant="task.status" size="sm">{{ task.status.replace("_", " ") }}</BaseBadge></td>
              <td><BaseBadge :variant="task.priority" size="sm">{{ task.priority }}</BaseBadge></td>
              <td>{{ task.assigned_to_name || "Unassigned" }}</td>
            </tr>
          </tbody>
        </table>
        <EmptyState
          v-if="filteredTasks.length === 0"
          :icon="CheckSquare"
          title="No tasks found"
          description="Create your first task to get started."
          action-label="Create task"
          @action="showCreateModal = true"
        />
      </BaseCard>
    </div>

    <!-- Create Task Modal -->
    <BaseModal :open="showCreateModal" title="Create Task" @close="showCreateModal = false">
      <form class="modal-form" @submit.prevent="submitTask">
        <p v-if="createError" class="modal-form__error">{{ createError }}</p>
        <BaseInput v-model="newTask.title" label="Title" placeholder="Task title" required />
        <BaseSelect v-model="newTask.project" label="Project" :options="projectOptions" placeholder="Select project..." />
        <BaseSelect v-model="newTask.priority" label="Priority" :options="priorityOptions" />
        <BaseInput v-model="newTask.description" label="Description" placeholder="Optional description" />
        <BaseButton type="submit" variant="primary">Create task</BaseButton>
      </form>
    </BaseModal>

    <!-- Task Detail Slide-over -->
    <Teleport to="body">
      <Transition name="slide">
        <div v-if="showDetailPanel && selectedTask" class="detail-overlay" @click.self="showDetailPanel = false">
          <div class="detail-panel">
            <div class="detail-panel__header">
              <h3>{{ selectedTask.title }}</h3>
              <button class="detail-panel__close" @click="showDetailPanel = false">&times;</button>
            </div>
            <div class="detail-panel__body">
              <div class="detail-field">
                <span class="detail-field__label">Status</span>
                <BaseSelect
                  :model-value="selectedTask.status"
                  :options="columns.map((c) => ({ value: c.key, label: c.label }))"
                  @update:model-value="(v) => updateTaskStatus(selectedTask.id, v)"
                />
              </div>
              <div class="detail-field">
                <span class="detail-field__label">Priority</span>
                <BaseBadge :variant="selectedTask.priority" size="md">{{ selectedTask.priority }}</BaseBadge>
              </div>
              <div class="detail-field">
                <span class="detail-field__label">Project</span>
                <span>{{ selectedTask.project_name }}</span>
              </div>
              <div class="detail-field">
                <span class="detail-field__label">Assignee</span>
                <span>{{ selectedTask.assigned_to_name || "Unassigned" }}</span>
              </div>
              <div v-if="selectedTask.description" class="detail-field">
                <span class="detail-field__label">Description</span>
                <p>{{ selectedTask.description }}</p>
              </div>
              <div class="detail-field">
                <span class="detail-field__label">Logged Hours</span>
                <span>{{ selectedTask.total_logged_hours || 0 }}h</span>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<style scoped>
.tasks-page {
  max-width: 1400px;
}

.tasks-page__header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--space-4);
  margin-bottom: var(--space-6);
  flex-wrap: wrap;
}

.tasks-page__title {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: 700;
}

.tasks-page__actions {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  flex-wrap: wrap;
}

.tasks-page__filters {
  display: flex;
  gap: var(--space-2);
}

.tasks-page__view-toggle {
  display: flex;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.view-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border: none;
  background: transparent;
  color: var(--color-text-muted);
  cursor: pointer;
}

.view-btn--active {
  background: var(--color-primary-light);
  color: var(--color-primary);
}

.tasks-page__skeleton {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-4);
}

/* Kanban */
.kanban {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-4);
  min-height: 400px;
}

.kanban__column {
  background: var(--color-bg-sunken);
  border-radius: var(--radius-lg);
  padding: var(--space-3);
}

.kanban__column-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-3);
  padding: 0 var(--space-1);
}

.kanban__column-title {
  font-size: var(--text-sm);
  font-weight: 600;
  color: var(--color-text-secondary);
}

.kanban__cards {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.kanban__card {
  background: var(--color-surface);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-md);
  padding: var(--space-3);
  cursor: pointer;
  transition: box-shadow 0.15s ease;
}

.kanban__card:hover {
  box-shadow: var(--shadow-md);
}

.kanban__card-title {
  font-size: var(--text-sm);
  font-weight: 500;
  margin-bottom: var(--space-2);
}

.kanban__card-meta {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.kanban__card-project {
  font-size: var(--text-xs);
  color: var(--color-text-muted);
}

.kanban__empty {
  padding: var(--space-4);
}

/* List view */
.task-table {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--text-sm);
}

.task-table th {
  text-align: left;
  padding: var(--space-3) var(--space-4);
  font-weight: 600;
  font-size: var(--text-xs);
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-bottom: 1px solid var(--color-border-light);
}

.task-table td {
  padding: var(--space-3) var(--space-4);
  border-bottom: 1px solid var(--color-border-light);
}

.task-table__row {
  cursor: pointer;
  transition: background 0.1s ease;
}

.task-table__row:hover {
  background: var(--color-surface-hover);
}

.task-table__title {
  font-weight: 500;
}

/* Detail slide-over */
.detail-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.3);
  z-index: 100;
  display: flex;
  justify-content: flex-end;
}

.detail-panel {
  width: 420px;
  max-width: 100%;
  background: var(--color-surface);
  height: 100%;
  box-shadow: var(--shadow-lg);
  display: flex;
  flex-direction: column;
}

.detail-panel__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-5);
  border-bottom: 1px solid var(--color-border-light);
}

.detail-panel__header h3 {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: 700;
}

.detail-panel__close {
  font-size: 1.5rem;
  border: none;
  background: transparent;
  color: var(--color-text-muted);
  cursor: pointer;
  line-height: 1;
}

.detail-panel__body {
  flex: 1;
  padding: var(--space-5);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.detail-field {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
}

.detail-field__label {
  font-size: var(--text-xs);
  font-weight: 600;
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
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

/* Slide transition */
.slide-enter-active,
.slide-leave-active {
  transition: opacity 0.2s ease;
}
.slide-enter-active .detail-panel,
.slide-leave-active .detail-panel {
  transition: transform 0.25s ease;
}
.slide-enter-from,
.slide-leave-to {
  opacity: 0;
}
.slide-enter-from .detail-panel {
  transform: translateX(100%);
}
.slide-leave-to .detail-panel {
  transform: translateX(100%);
}

@media (max-width: 1023px) {
  .kanban {
    grid-template-columns: repeat(2, 1fr);
  }
  .tasks-page__skeleton {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 767px) {
  .kanban {
    grid-template-columns: 1fr;
  }
  .tasks-page__skeleton {
    grid-template-columns: 1fr;
  }
  .detail-panel {
    width: 100%;
  }
}
</style>
