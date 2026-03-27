import { ref, onMounted } from "vue";

export function useTheme() {
  const isDark = ref(false);

  function toggle() {
    isDark.value = !isDark.value;
    document.documentElement.setAttribute(
      "data-theme",
      isDark.value ? "dark" : "light",
    );
  }

  onMounted(() => {
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    isDark.value = prefersDark;
    document.documentElement.setAttribute(
      "data-theme",
      prefersDark ? "dark" : "light",
    );
  });

  return { isDark, toggle };
}
