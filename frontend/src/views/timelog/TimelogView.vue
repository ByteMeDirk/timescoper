<script setup>
import { onMounted, ref, computed } from "vue";
import { useTimelogStore } from "@/stores/timelog";
import { useProjectsStore } from "@/stores/projects";
import BaseCard from "@/components/base/BaseCard.vue";
import BaseButton from "@/components/base/BaseButton.vue";
import BaseInput from "@/components/base/BaseInput.vue";
import BaseSelect from "@/components/base/BaseSelect.vue";
import BaseModal from "@/components/base/BaseModal.vue";
import SkeletonLoader from "@/components/base/SkeletonLoader.vue";
import EmptyState from "@/components/base/EmptyState.vue";
import { Plus, Trash2, Clock } from "lucide-vue-next";

const timelogStore = useTimelogStore();
const projectsStore = useProjectsStore();
const loading = ref(true);
const showAddModal = ref(false);
const selectedDate = ref(new Date().toISOString().split("T")[0]);

// Week navigation
const weekDays = computed(() => {
  const date = new Date(selectedDate.value);
  const day = date.getDay();
  const monday = new Date(date);
  monday.setDate(date.getDate() - ((day + 6) % 7));

  return Array.from({ length: 7 }, (_, i) => {
    const d = new Date(monday);
    d.setDate(monday.getDate() + i);
    return d.toISOString().split("T")[0];
  });
});

const entriesByDay = computed(() => {
  const map = {};
  for (const day of weekDays.value) {
    map[day] = timelogStore.entries.filter((e) => e.date === day);
  }
  return map;
});

const dayLabels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

function dayTotal(day) {
  return entriesByDay.value[day]?.reduce((sum, e) => sum + parseFloat(e.hours), 0) || 0;
}

// Add entry form
const newEntry = ref({
  project: "",
  hours: "",
  description: "",
  date: "",
  is_billable: true,
});
const addError = ref("");

function openAddModal(date) {
  newEntry.value = { project: "", hours: "", description: "", date, is_billable: true };
  addError.value = "";
  showAddModal.value = true;
}

async function submitEntry() {
  addError.value = "";
  try {
    await timelogStore.createEntry(newEntry.value);
    showAddModal.value = false;
    await loadEntries();
  } catch (err) {
    addError.value = err.response?.data?.error || "Failed to add entry.";
  }
}

async function removeEntry(id) {
  await timelogStore.deleteEntry(id);
}

async function loadEntries() {
  loading.value = true;
  await Promise.all([
    timelogStore.fetchEntries({
      date__gte: weekDays.value[0],
      date__lte: weekDays.value[6],
    }),
    projectsStore.fetchProjects(),
  ]);
  loading.value = false;
}

const projectOptions = computed(() =>
  projectsStore.projects.map((p) => ({ value: p.id, label: p.name })),
);

onMounted(loadEntries);
</script>

<template>
  <div class="timelog">
    <div class="timelog__header">
      <h2 class="timelog__title">Time Log</h2>
      <p class="timelog__subtitle">
        Week of {{ weekDays[0] }} — {{ weekDays[6] }}
      </p>
    </div>

    <div v-if="loading" class="timelog__skeleton">
      <SkeletonLoader v-for="i in 7" :key="i" height="120px" />
    </div>

    <div v-else class="timelog__week">
      <BaseCard v-for="(day, idx) in weekDays" :key="day" class="timelog__day">
        <template #header>
          <div class="timelog__day-header">
            <span class="timelog__day-name">{{ dayLabels[idx] }}</span>
            <span class="timelog__day-date">{{ day.slice(5) }}</span>
            <span class="timelog__day-total">{{ dayTotal(day) }}h</span>
          </div>
        </template>

        <div v-if="entriesByDay[day]?.length" class="timelog__entries">
          <div v-for="entry in entriesByDay[day]" :key="entry.id" class="timelog__entry">
            <div class="timelog__entry-info">
              <span class="timelog__entry-project">{{ entry.project_name }}</span>
              <span class="timelog__entry-desc">{{ entry.description }}</span>
            </div>
            <div class="timelog__entry-actions">
              <span class="timelog__entry-hours">{{ entry.hours }}h</span>
              <button
                class="timelog__entry-delete"
                aria-label="Delete entry"
                @click="removeEntry(entry.id)"
              >
                <Trash2 :size="14" />
              </button>
            </div>
          </div>
        </div>
        <EmptyState
          v-else
          title="No entries"
          :icon="Clock"
          class="timelog__empty"
        />

        <template #footer>
          <BaseButton variant="ghost" size="sm" @click="openAddModal(day)">
            <Plus :size="14" /> Add entry
          </BaseButton>
        </template>
      </BaseCard>
    </div>

    <!-- Add Entry Modal -->
    <BaseModal :open="showAddModal" title="Add Time Entry" @close="showAddModal = false">
      <form class="modal-form" @submit.prevent="submitEntry">
        <p v-if="addError" class="modal-form__error">{{ addError }}</p>
        <BaseSelect
          v-model="newEntry.project"
          label="Project"
          :options="projectOptions"
          placeholder="Select project..."
        />
        <BaseInput
          v-model="newEntry.hours"
          label="Hours"
          type="number"
          step="0.25"
          min="0.25"
          max="24"
          placeholder="e.g. 2.5"
        />
        <BaseInput
          v-model="newEntry.description"
          label="Description"
          placeholder="What did you work on?"
        />
        <BaseButton type="submit" variant="primary">Save entry</BaseButton>
      </form>
    </BaseModal>
  </div>
</template>

<style scoped>
.timelog {
  max-width: 1200px;
}

.timelog__header {
  margin-bottom: var(--space-6);
}

.timelog__title {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: 700;
}

.timelog__subtitle {
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
  margin-top: var(--space-1);
}

.timelog__skeleton {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: var(--space-4);
}

.timelog__week {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: var(--space-3);
}

.timelog__day-header {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--text-sm);
}

.timelog__day-name {
  font-weight: 600;
}

.timelog__day-date {
  color: var(--color-text-muted);
}

.timelog__day-total {
  margin-left: auto;
  font-weight: 600;
  color: var(--color-primary);
  font-family: var(--font-display);
}

.timelog__entries {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.timelog__entry {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-2);
  background: var(--color-bg-sunken);
  border-radius: var(--radius-sm);
  font-size: var(--text-sm);
}

.timelog__entry-info {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.timelog__entry-project {
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.timelog__entry-desc {
  font-size: var(--text-xs);
  color: var(--color-text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.timelog__entry-actions {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  flex-shrink: 0;
}

.timelog__entry-hours {
  font-weight: 600;
  font-size: var(--text-xs);
}

.timelog__entry-delete {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border: none;
  background: transparent;
  color: var(--color-text-muted);
  border-radius: var(--radius-sm);
  cursor: pointer;
}

.timelog__entry-delete:hover {
  background: var(--color-danger-light);
  color: var(--color-danger);
}

.timelog__empty {
  padding: var(--space-4);
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
  .timelog__week {
    grid-template-columns: 1fr;
  }
}
</style>
