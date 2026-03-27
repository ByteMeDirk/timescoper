<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import BaseInput from "@/components/base/BaseInput.vue";
import BaseButton from "@/components/base/BaseButton.vue";
import BaseCard from "@/components/base/BaseCard.vue";
import { Timer } from "lucide-vue-next";

const router = useRouter();
const authStore = useAuthStore();

const form = ref({
  email: "",
  first_name: "",
  last_name: "",
  password: "",
  password_confirm: "",
});
const fieldErrors = ref({});

async function handleRegister() {
  fieldErrors.value = {};
  try {
    await authStore.register(form.value);
    router.push({ name: "login", query: { registered: "true" } });
  } catch (err) {
    if (err.response?.data?.fields) {
      fieldErrors.value = err.response.data.fields;
    }
  }
}
</script>

<template>
  <div class="register-page">
    <BaseCard class="register-card">
      <div class="register-header">
        <Timer :size="36" class="register-logo" />
        <h1 class="register-title">Create Account</h1>
        <p class="register-subtitle">Join TimeScoper to start tracking</p>
      </div>

      <form class="register-form" @submit.prevent="handleRegister">
        <p v-if="authStore.error" class="register-error" role="alert">
          {{ authStore.error }}
        </p>

        <div class="register-row">
          <BaseInput
            v-model="form.first_name"
            label="First name"
            placeholder="Jane"
            :error="fieldErrors.first_name?.[0]"
            required
          />
          <BaseInput
            v-model="form.last_name"
            label="Last name"
            placeholder="Doe"
            :error="fieldErrors.last_name?.[0]"
            required
          />
        </div>

        <BaseInput
          v-model="form.email"
          label="Email"
          type="email"
          placeholder="you@example.com"
          :error="fieldErrors.email?.[0]"
          autocomplete="email"
          required
        />

        <BaseInput
          v-model="form.password"
          label="Password"
          type="password"
          placeholder="At least 8 characters"
          :error="fieldErrors.password?.[0]"
          autocomplete="new-password"
          required
        />

        <BaseInput
          v-model="form.password_confirm"
          label="Confirm password"
          type="password"
          placeholder="Repeat your password"
          :error="fieldErrors.password_confirm?.[0]"
          autocomplete="new-password"
          required
        />

        <BaseButton
          type="submit"
          variant="primary"
          size="lg"
          :loading="authStore.loading"
          class="register-submit"
        >
          Create account
        </BaseButton>
      </form>

      <p class="register-footer">
        Already have an account?
        <router-link to="/login">Sign in</router-link>
      </p>
    </BaseCard>
  </div>
</template>

<style scoped>
.register-page {
  width: 100%;
  max-width: 440px;
}

.register-header {
  text-align: center;
  padding: var(--space-8) var(--space-6) var(--space-4);
}

.register-logo {
  color: var(--color-primary);
  margin-bottom: var(--space-3);
}

.register-title {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: 700;
  margin-bottom: var(--space-1);
}

.register-subtitle {
  color: var(--color-text-secondary);
  font-size: var(--text-base);
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  padding: var(--space-4) var(--space-6);
}

.register-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-4);
}

.register-error {
  padding: var(--space-3);
  background: var(--color-danger-light);
  color: var(--color-danger);
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  text-align: center;
}

.register-submit {
  width: 100%;
  margin-top: var(--space-2);
}

.register-footer {
  text-align: center;
  padding: var(--space-4) var(--space-6) var(--space-6);
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}
</style>
