<script setup>
import { onMounted, ref } from "vue";
import { useAuthStore } from "@/stores/auth";
import BaseCard from "@/components/base/BaseCard.vue";
import BaseBadge from "@/components/base/BaseBadge.vue";
import BaseButton from "@/components/base/BaseButton.vue";
import BaseInput from "@/components/base/BaseInput.vue";
import BaseModal from "@/components/base/BaseModal.vue";
import SkeletonLoader from "@/components/base/SkeletonLoader.vue";
import EmptyState from "@/components/base/EmptyState.vue";
import { Users, UserPlus } from "lucide-vue-next";
import client from "@/api/client";

const authStore = useAuthStore();
const loading = ref(true);
const teams = ref([]);
const selectedTeam = ref(null);
const members = ref([]);
const showInviteModal = ref(false);
const inviteEmail = ref("");
const inviteError = ref("");

async function loadTeams() {
  loading.value = true;
  try {
    const { data } = await client.get("/teams/");
    teams.value = data.results || data;
    if (teams.value.length > 0) {
      await selectTeam(teams.value[0]);
    }
  } catch {
    // handled
  }
  loading.value = false;
}

async function selectTeam(team) {
  selectedTeam.value = team;
  try {
    const { data } = await client.get(`/teams/${team.id}/members/`);
    members.value = data.results || data;
  } catch {
    members.value = [];
  }
}

async function inviteMember() {
  inviteError.value = "";
  // In a real app, we'd look up the user by email. Simplified here.
  showInviteModal.value = false;
  inviteEmail.value = "";
}

onMounted(loadTeams);
</script>

<template>
  <div class="team-page">
    <div class="team-page__header">
      <h2 class="team-page__title">Team</h2>
      <BaseButton variant="primary" size="sm" @click="showInviteModal = true">
        <UserPlus :size="16" /> Invite member
      </BaseButton>
    </div>

    <div v-if="loading">
      <SkeletonLoader :count="4" height="60px" />
    </div>

    <div v-else-if="selectedTeam" class="team-content">
      <BaseCard>
        <template #header>
          {{ selectedTeam.name }} — {{ members.length }} members
        </template>

        <div v-if="members.length" class="members-list">
          <div v-for="member in members" :key="member.id" class="member-row">
            <div class="member-info">
              <span class="member-name">{{ member.user_name }}</span>
              <span class="member-email">{{ member.user_email }}</span>
            </div>
            <BaseBadge :variant="member.role === 'lead' ? 'primary' : 'default'" size="sm">
              {{ member.role }}
            </BaseBadge>
          </div>
        </div>
        <EmptyState v-else :icon="Users" title="No members" description="Invite team members to get started." />
      </BaseCard>
    </div>

    <EmptyState v-else :icon="Users" title="No teams yet" description="Create a team to start collaborating." />

    <BaseModal :open="showInviteModal" title="Invite Member" @close="showInviteModal = false">
      <form class="modal-form" @submit.prevent="inviteMember">
        <p v-if="inviteError" class="modal-form__error">{{ inviteError }}</p>
        <BaseInput v-model="inviteEmail" label="Email" type="email" placeholder="member@example.com" required />
        <BaseButton type="submit" variant="primary">Send invite</BaseButton>
      </form>
    </BaseModal>
  </div>
</template>

<style scoped>
.team-page { max-width: 800px; }
.team-page__header { display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--space-6); }
.team-page__title { font-family: var(--font-display); font-size: var(--text-xl); font-weight: 700; }
.members-list { display: flex; flex-direction: column; gap: var(--space-2); }
.member-row { display: flex; justify-content: space-between; align-items: center; padding: var(--space-3); border-radius: var(--radius-md); background: var(--color-bg-sunken); }
.member-info { display: flex; flex-direction: column; }
.member-name { font-weight: 500; font-size: var(--text-sm); }
.member-email { font-size: var(--text-xs); color: var(--color-text-secondary); }
.modal-form { display: flex; flex-direction: column; gap: var(--space-4); }
.modal-form__error { padding: var(--space-2); background: var(--color-danger-light); color: var(--color-danger); border-radius: var(--radius-md); font-size: var(--text-sm); }
</style>
