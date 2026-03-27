<script setup>
import { onMounted, ref } from "vue";
import BaseCard from "@/components/base/BaseCard.vue";
import BaseBadge from "@/components/base/BaseBadge.vue";
import BaseSelect from "@/components/base/BaseSelect.vue";
import SkeletonLoader from "@/components/base/SkeletonLoader.vue";
import EmptyState from "@/components/base/EmptyState.vue";
import { Shield, Users } from "lucide-vue-next";
import { authApi } from "@/api/auth";

const loading = ref(true);
const users = ref([]);

const roleOptions = [
  { value: "developer", label: "Developer" },
  { value: "team_lead", label: "Team Lead" },
  { value: "project_manager", label: "Project Manager" },
  { value: "admin", label: "Admin" },
];

async function loadUsers() {
  loading.value = true;
  try {
    const { data } = await authApi.listUsers();
    users.value = data.results || data;
  } catch {
    // handled
  }
  loading.value = false;
}

async function updateRole(userId, role) {
  await authApi.updateUser(userId, { role });
}

async function toggleActive(userId, isActive) {
  await authApi.updateUser(userId, { is_active: !isActive });
  await loadUsers();
}

onMounted(loadUsers);
</script>

<template>
  <div class="admin-page">
    <div class="admin-page__header">
      <h2 class="admin-page__title">
        <Shield :size="20" /> Admin Panel
      </h2>
    </div>

    <BaseCard :padding="false">
      <template #header>User Management</template>

      <div v-if="loading">
        <SkeletonLoader :count="5" height="50px" />
      </div>

      <table v-else-if="users.length" class="users-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Role</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td class="users-table__name">{{ user.first_name }} {{ user.last_name }}</td>
            <td>{{ user.email }}</td>
            <td>
              <BaseSelect
                :model-value="user.role"
                :options="roleOptions"
                @update:model-value="(v) => updateRole(user.id, v)"
              />
            </td>
            <td>
              <BaseBadge :variant="user.is_active ? 'success' : 'danger'" size="sm">
                {{ user.is_active ? "Active" : "Inactive" }}
              </BaseBadge>
            </td>
            <td>
              <button
                class="toggle-btn"
                @click="toggleActive(user.id, user.is_active)"
              >
                {{ user.is_active ? "Deactivate" : "Activate" }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <EmptyState v-else :icon="Users" title="No users" />
    </BaseCard>
  </div>
</template>

<style scoped>
.admin-page { max-width: 1000px; }
.admin-page__header { display: flex; align-items: center; margin-bottom: var(--space-6); }
.admin-page__title { font-family: var(--font-display); font-size: var(--text-xl); font-weight: 700; display: flex; align-items: center; gap: var(--space-2); }

.users-table { width: 100%; border-collapse: collapse; font-size: var(--text-sm); }
.users-table th { text-align: left; padding: var(--space-3) var(--space-4); font-weight: 600; font-size: var(--text-xs); color: var(--color-text-secondary); text-transform: uppercase; letter-spacing: 0.05em; border-bottom: 1px solid var(--color-border-light); }
.users-table td { padding: var(--space-3) var(--space-4); border-bottom: 1px solid var(--color-border-light); }
.users-table__name { font-weight: 500; }

.toggle-btn { padding: var(--space-1) var(--space-3); border: 1px solid var(--color-border); border-radius: var(--radius-md); background: transparent; font-size: var(--text-xs); color: var(--color-text-secondary); cursor: pointer; transition: all 0.15s ease; }
.toggle-btn:hover { background: var(--color-surface-hover); color: var(--color-text); }
</style>
