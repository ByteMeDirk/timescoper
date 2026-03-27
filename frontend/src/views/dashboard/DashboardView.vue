<script setup>
import { onMounted, ref, computed } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useTimelogStore } from "@/stores/timelog";
import { useTasksStore } from "@/stores/tasks";
import { useReportingStore } from "@/stores/reporting";
import BaseCard from "@/components/base/BaseCard.vue";
import BaseButton from "@/components/base/BaseButton.vue";
import BaseInput from "@/components/base/BaseInput.vue";
import BaseSelect from "@/components/base/BaseSelect.vue";
import BaseBadge from "@/components/base/BaseBadge.vue";
import SkeletonLoader from "@/components/base/SkeletonLoader.vue";
import EmptyState from "@/components/base/EmptyState.vue";
import WeeklyChart from "@/components/reporting/WeeklyChart.vue";
import { Clock, CheckSquare, AlertTriangle, TrendingUp, Plus } from "lucide-vue-next";
import { useProjectsStore } from "@/stores/projects";

const authStore = useAuthStore();
const timelogStore = useTimelogStore();
const tasksStore = useTasksStore();
const reportingStore = useReportingStore();
const projectsStore = useProjectsStore();

const loading = ref(true);
const today = new Date().toISOString().split("T")[0];

// Quick add form
const quickAdd = ref({
  project: "",
  hours: "",
  description: "",
});
const quickAddError = ref("");

const todayHours = computed(() => reportingStore.dailySummary?.total_hours || 0);
const weeklyHours = computed(() => reportingStore.weeklySummary?.total_hours || 0);
const openTasks = computed(
  () => tasksStore.tasks.filter((t) => t.status === "in_progress").length,
);
const overdueTasks = computed(
  () =>
    tasksStore.tasks.filter(
      (t) => t.due_date && t.due_date < today && t.status !== "done" && t.status !== "cancelled",
    ).length,
);
const myInProgressTasks = computed(() =>
  tasksStore.tasks
    .filter(
      (t) =>
        t.status === "in_progress" &&
        t.assigned_to === authStore.user?.id,
    )
    .slice(0, 5),
);

async function loadDashboard() {
  loading.value = true;
  await Promise.all([
    reportingStore.fetchDailySummary({ date: today }),
    reportingStore.fetchWeeklySummary(),
    tasksStore.fetchTasks({ assigned_to: authStore.user?.id }),
    timelogStore.fetchMyLog(today),
    projectsStore.fetchProjects(),
  ]);
  loading.value = false;
}

async function submitQuickAdd() {
  quickAddError.value = "";
  if (!quickAdd.value.project || !quickAdd.value.hours) {
    quickAddError.value = "Project and hours are required.";
    return;
  }
  try {
    await timelogStore.createEntry({
      project: quickAdd.value.project,
      hours: quickAdd.value.hours,
      description: quickAdd.value.description,
      date: today,
      is_billable: true,
    });
    quickAdd.value = { project: "", hours: "", description: "" };
    await reportingStore.fetchDailySummary({ date: today });
    await timelogStore.fetchMyLog(today);
  } catch (err) {
    quickAddError.value = err.response?.data?.error || "Failed to add entry.";
  }
}

const projectOptions = computed(() =>
  projectsStore.projects.map((p) => ({ value: p.id, label: p.name })),
);

onMounted(loadDashboard);
</script>

<template>
  <div class="dashboard">
    <h2 class="dashboard__greeting">
      Good {{ new Date().getHours() < 12 ? "morning" : new Date().getHours() < 18 ? "afternoon" : "evening" }}, {{ authStore.user?.first_name }}
    </h2>

    <!-- KPI Cards -->
    <div class="dashboard__kpi-row" v-if="!loading">
      <BaseCard class="kpi-card">
        <div class="kpi-card__content">
          <Clock :size="20" class="kpi-card__icon kpi-card__icon--primary" />
          <div>
            <p class="kpi-card__value">{{ todayHours }}h</p>
            <p class="kpi-card__label">Today</p>
          </div>
        </div>
      </BaseCard>
      <BaseCard class="kpi-card">
        <div class="kpi-card__content">
          <TrendingUp :size="20" class="kpi-card__icon kpi-card__icon--success" />
          <div>
            <p class="kpi-card__value">{{ weeklyHours }}h</p>
            <p class="kpi-card__label">This week</p>
          </div>
        </div>
      </BaseCard>
      <BaseCard class="kpi-card">
        <div class="kpi-card__content">
          <CheckSquare :size="20" class="kpi-card__icon kpi-card__icon--primary" />
          <div>
            <p class="kpi-card__value">{{ openTasks }}</p>
            <p class="kpi-card__label">Open tasks</p>
          </div>
        </div>
      </BaseCard>
      <BaseCard class="kpi-card">
        <div class="kpi-card__content">
          <AlertTriangle :size="20" class="kpi-card__icon kpi-card__icon--danger" />
          <div>
            <p class="kpi-card__value">{{ overdueTasks }}</p>
            <p class="kpi-card__label">Overdue</p>
          </div>
        </div>
      </BaseCard>
    </div>
    <div v-else class="dashboard__kpi-row">
      <SkeletonLoader v-for="i in 4" :key="i" height="80px" />
    </div>

    <div class="dashboard__grid">
      <!-- Quick Add Time Entry -->
      <BaseCard>
        <template #header>
          <div class="section-header">
            <Plus :size="18" />
            <span>Quick Add Time</span>
          </div>
        </template>
        <form class="quick-add-form" @submit.prevent="submitQuickAdd">
          <p v-if="quickAddError" class="quick-add-form__error">{{ quickAddError }}</p>
          <BaseSelect
            v-model="quickAdd.project"
            label="Project"
            :options="projectOptions"
            placeholder="Select project..."
          />
          <BaseInput
            v-model="quickAdd.hours"
            label="Hours"
            type="number"
            step="0.25"
            min="0.25"
            max="24"
            placeholder="e.g. 2.5"
          />
          <BaseInput
            v-model="quickAdd.description"
            label="Description"
            placeholder="What did you work on?"
          />
          <BaseButton type="submit" variant="primary" size="md">
            Log time
          </BaseButton>
        </form>
      </BaseCard>

      <!-- Weekly Chart -->
      <BaseCard>
        <template #header>Weekly Hours</template>
        <div v-if="loading">
          <SkeletonLoader height="200px" />
        </div>
        <WeeklyChart
          v-else-if="reportingStore.weeklySummary?.daily"
          :data="reportingStore.weeklySummary.daily"
        />
        <EmptyState v-else title="No data yet" description="Start logging time to see your weekly chart." />
      </BaseCard>

      <!-- Today's Log -->
      <BaseCard>
        <template #header>Today's Log</template>
        <div v-if="loading">
          <SkeletonLoader :count="3" height="40px" />
        </div>
        <div v-else-if="timelogStore.myDailyLog.length > 0" class="today-log">
          <div v-for="entry in timelogStore.myDailyLog" :key="entry.id" class="today-log__item">
            <div class="today-log__info">
              <span class="today-log__project">{{ entry.project_name }}</span>
              <span class="today-log__desc">{{ entry.description }}</span>
            </div>
            <span class="today-log__hours">{{ entry.hours }}h</span>
          </div>
        </div>
        <EmptyState v-else title="No entries today" description="Use the quick add form to log your first entry." />
      </BaseCard>

      <!-- My Tasks -->
      <BaseCard>
        <template #header>My Tasks</template>
        <div v-if="loading">
          <SkeletonLoader :count="3" height="40px" />
        </div>
        <div v-else-if="myInProgressTasks.length > 0" class="my-tasks">
          <div v-for="task in myInProgressTasks" :key="task.id" class="my-tasks__item">
            <div class="my-tasks__info">
              <span class="my-tasks__title">{{ task.title }}</span>
              <span class="my-tasks__project">{{ task.project_name }}</span>
            </div>
            <BaseBadge :variant="task.priority">{{ task.priority }}</BaseBadge>
          </div>
        </div>
        <EmptyState v-else title="No active tasks" description="Tasks assigned to you will appear here." />
      </BaseCard>
    </div>
  </div>
</template>

<style scoped>
.dashboard {
  max-width: 1200px;
}

.dashboard__greeting {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: 700;
  margin-bottom: var(--space-6);
}

.dashboard__kpi-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: var(--space-4);
  margin-bottom: var(--space-6);
}

.kpi-card__content {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.kpi-card__icon {
  flex-shrink: 0;
}

.kpi-card__icon--primary { color: var(--color-primary); }
.kpi-card__icon--success { color: var(--color-success); }
.kpi-card__icon--danger { color: var(--color-danger); }

.kpi-card__value {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: 700;
}

.kpi-card__label {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}

.dashboard__grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
  gap: var(--space-4);
}

.section-header {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-weight: 600;
}

.quick-add-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.quick-add-form__error {
  padding: var(--space-2);
  background: var(--color-danger-light);
  color: var(--color-danger);
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
}

.today-log {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.today-log__item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-md);
  background: var(--color-bg-sunken);
}

.today-log__info {
  display: flex;
  flex-direction: column;
}

.today-log__project {
  font-size: var(--text-sm);
  font-weight: 500;
}

.today-log__desc {
  font-size: var(--text-xs);
  color: var(--color-text-secondary);
}

.today-log__hours {
  font-weight: 600;
  font-family: var(--font-display);
  color: var(--color-primary);
}

.my-tasks {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.my-tasks__item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-md);
  background: var(--color-bg-sunken);
}

.my-tasks__info {
  display: flex;
  flex-direction: column;
}

.my-tasks__title {
  font-size: var(--text-sm);
  font-weight: 500;
}

.my-tasks__project {
  font-size: var(--text-xs);
  color: var(--color-text-secondary);
}

@media (max-width: 767px) {
  .dashboard__grid {
    grid-template-columns: 1fr;
  }
  .dashboard__kpi-row {
    grid-template-columns: 1fr 1fr;
  }
}
</style>
