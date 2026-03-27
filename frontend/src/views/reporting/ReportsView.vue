<script setup>
import { onMounted, ref } from "vue";
import { useReportingStore } from "@/stores/reporting";
import BaseCard from "@/components/base/BaseCard.vue";
import BaseInput from "@/components/base/BaseInput.vue";
import SkeletonLoader from "@/components/base/SkeletonLoader.vue";
import EmptyState from "@/components/base/EmptyState.vue";
import WeeklyChart from "@/components/reporting/WeeklyChart.vue";
import { BarChart3 } from "lucide-vue-next";

const reportingStore = useReportingStore();
const loading = ref(true);
const activeTab = ref("individual");

const tabs = [
  { key: "individual", label: "Individual" },
  { key: "team", label: "Team" },
  { key: "project", label: "Project" },
];

onMounted(async () => {
  await reportingStore.fetchWeeklySummary();
  loading.value = false;
});
</script>

<template>
  <div class="reports-page">
    <h2 class="reports-page__title">Reports</h2>

    <div class="reports-page__tabs">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        :class="['tab-btn', { 'tab-btn--active': activeTab === tab.key }]"
        @click="activeTab = tab.key"
      >
        {{ tab.label }}
      </button>
    </div>

    <div v-if="loading" class="reports-page__skeleton">
      <SkeletonLoader height="300px" />
      <SkeletonLoader height="200px" />
    </div>

    <div v-else>
      <!-- Individual tab -->
      <div v-if="activeTab === 'individual'" class="reports-content">
        <BaseCard>
          <template #header>Weekly Hours</template>
          <WeeklyChart
            v-if="reportingStore.weeklySummary?.daily"
            :data="reportingStore.weeklySummary.daily"
          />
          <EmptyState v-else title="No data" :icon="BarChart3" description="Log time to see your report." />
        </BaseCard>

        <BaseCard v-if="reportingStore.weeklySummary">
          <template #header>Summary</template>
          <div class="summary-grid">
            <div class="summary-item">
              <span class="summary-item__value">{{ reportingStore.weeklySummary.total_hours }}h</span>
              <span class="summary-item__label">Total hours</span>
            </div>
            <div class="summary-item">
              <span class="summary-item__value">{{ reportingStore.weeklySummary.billable_hours }}h</span>
              <span class="summary-item__label">Billable hours</span>
            </div>
            <div class="summary-item">
              <span class="summary-item__value">{{ reportingStore.weeklySummary.entry_count }}</span>
              <span class="summary-item__label">Entries</span>
            </div>
          </div>
        </BaseCard>
      </div>

      <!-- Team / Project tabs — placeholder -->
      <div v-else class="reports-content">
        <EmptyState
          :icon="BarChart3"
          title="Coming soon"
          description="Team and project reports are being built."
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.reports-page {
  max-width: 1000px;
}

.reports-page__title {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: 700;
  margin-bottom: var(--space-5);
}

.reports-page__tabs {
  display: flex;
  gap: var(--space-1);
  margin-bottom: var(--space-6);
  border-bottom: 1px solid var(--color-border-light);
}

.tab-btn {
  padding: var(--space-2) var(--space-4);
  border: none;
  background: transparent;
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--color-text-secondary);
  cursor: pointer;
  border-bottom: 2px solid transparent;
  margin-bottom: -1px;
  transition: all 0.15s ease;
}

.tab-btn--active {
  color: var(--color-primary);
  border-bottom-color: var(--color-primary);
}

.reports-page__skeleton {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.reports-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-4);
}

.summary-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.summary-item__value {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: 700;
}

.summary-item__label {
  font-size: var(--text-xs);
  color: var(--color-text-muted);
}
</style>
