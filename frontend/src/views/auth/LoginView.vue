<script setup>
import { ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import BaseInput from "@/components/base/BaseInput.vue";
import BaseButton from "@/components/base/BaseButton.vue";
import BaseCard from "@/components/base/BaseCard.vue";
import { Timer } from "lucide-vue-next";

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

const email = ref("");
const password = ref("");
const fieldErrors = ref({});

async function handleLogin() {
  fieldErrors.value = {};
  try {
    await authStore.login(email.value, password.value);
    const redirect = route.query.redirect || "/dashboard";
    router.push(redirect);
  } catch (err) {
    if (err.response?.data?.fields) {
      fieldErrors.value = err.response.data.fields;
    }
  }
}
</script>

<template>
  <div class="login-page">
    <BaseCard class="login-card">
      <div class="login-header">
        <Timer :size="36" class="login-logo" />
        <h1 class="login-title">TimeScoper</h1>
        <p class="login-subtitle">Sign in to your account</p>
      </div>

      <form class="login-form" @submit.prevent="handleLogin">
        <p v-if="authStore.error" class="login-error" role="alert">
          {{ authStore.error }}
        </p>

        <BaseInput
          v-model="email"
          label="Email"
          type="email"
          placeholder="you@example.com"
          :error="fieldErrors.email?.[0]"
          autocomplete="email"
          required
        />

        <BaseInput
          v-model="password"
          label="Password"
          type="password"
          placeholder="Enter your password"
          :error="fieldErrors.password?.[0]"
          autocomplete="current-password"
          required
        />

        <BaseButton
          type="submit"
          variant="primary"
          size="lg"
          :loading="authStore.loading"
          class="login-submit"
        >
          Sign in
        </BaseButton>
      </form>

      <p class="login-footer">
        Don't have an account?
        <router-link to="/register">Create one</router-link>
      </p>
    </BaseCard>
  </div>
</template>

<style scoped>
.login-page {
  width: 100%;
  max-width: 400px;
}

.login-card {
  padding: 0;
}

.login-header {
  text-align: center;
  padding: var(--space-8) var(--space-6) var(--space-4);
}

.login-logo {
  color: var(--color-primary);
  margin-bottom: var(--space-3);
}

.login-title {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: 700;
  margin-bottom: var(--space-1);
}

.login-subtitle {
  color: var(--color-text-secondary);
  font-size: var(--text-base);
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  padding: var(--space-4) var(--space-6);
}

.login-error {
  padding: var(--space-3);
  background: var(--color-danger-light);
  color: var(--color-danger);
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  text-align: center;
}

.login-submit {
  width: 100%;
  margin-top: var(--space-2);
}

.login-footer {
  text-align: center;
  padding: var(--space-4) var(--space-6) var(--space-6);
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}
</style>
