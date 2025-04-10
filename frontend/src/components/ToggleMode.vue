<template>
  <button class="btn rounded-circle" @click="toggleTheme">
    <i :class="darkMode ? 'bi bi-sun-fill text-white' : 'bi bi-moon-fill'" />
  </button>
</template>

<script>
export default {
  emits: ["themeUpdated"], // Correct event definition
  data() {
    return {
      theme: "light",
      darkMode: false,
    };
  },
  mounted() {
    this.setTheme(this.theme);
  },
  methods: {
    toggleTheme() {
      // Toggle theme data
      this.theme = this.theme === "light" ? "dark" : "light";
      this.setTheme(this.theme);

      // Toggle darkMode state correctly
      this.darkMode = !this.darkMode;

      // Emit the updated theme state
      this.$emit("themeUpdated", this.darkMode);
    },
    setTheme(theme) {
      document.documentElement.setAttribute("data-theme", theme);
    },
  },
};
</script>

<style scoped>
button {
  width: 50px;
  height: 50px;
}
</style>
