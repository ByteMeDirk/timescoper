<script setup>
import { computed } from "vue";
import { Bar } from "vue-chartjs";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip);

const props = defineProps({
  data: { type: Array, required: true },
});

const dayNames = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

const chartData = computed(() => ({
  labels: props.data.map((d, i) => dayNames[i] || d.date),
  datasets: [
    {
      label: "Hours",
      data: props.data.map((d) => d.hours),
      backgroundColor: "rgba(1, 105, 111, 0.7)",
      borderRadius: 6,
      borderSkipped: false,
    },
  ],
}));

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      callbacks: {
        label: (ctx) => `${ctx.parsed.y}h`,
      },
    },
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: { stepSize: 2 },
      grid: { color: "rgba(0,0,0,0.05)" },
    },
    x: {
      grid: { display: false },
    },
  },
};
</script>

<template>
  <div class="weekly-chart">
    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>

<style scoped>
.weekly-chart {
  height: 220px;
}
</style>
