<template>
  <div class="app">
    <toggle-mode class="toggle-mode" @themeUpdated="updateTheme" />
    <login-page v-if="!loggedIn" @loggedIn="loggedIn = true" />
    <dash-board v-else @loggedOut="logout" />
  </div>
</template>

<script>
import ToggleMode from "./components/ToggleMode.vue";
import LoginPage from "./components/LoginPage.vue";

import { provide, reactive, ref } from "vue";
import DashBoard from "./components/DashBoard.vue";

import Cookies from "js-cookie";

export default {
  components: {
    ToggleMode,
    LoginPage,
    DashBoard,
  },

  setup() {
    // Make theme reactive for reactivity in children
    const themeState = reactive({ dark: false });
    provide("theme", themeState); // Return themeState so methods can use it
    return { themeState };
  },

  data() {
    return {
      loggedIn: !!Cookies.get("access_token"),
    };
  },

  methods: {
    updateTheme() {
      // Toggle the themeState's dark value
      this.themeState.dark = !this.themeState.dark;

      // Update the global document theme attribute
      const newTheme = this.themeState.dark ? "dark" : "light";
      document.documentElement.setAttribute("data-theme", newTheme);
    },
    logout() {
      this.loggedIn = false;
      Cookies.remove("access_token");
      Cookies.remove("is_admin");
    },
  },
};
</script>

<style>
/* Define light theme */
:root[data-theme="light"] {
  --bg-color: #ffffff;
  --text-color: #333333;
}

/* Define dark theme */
:root[data-theme="dark"] {
  --bg-color: #121212;
  --text-color: #ffffff;
}

.toggle-mode {
  position: fixed;
  bottom: 0px;
  right: 0px;
}

/* Apply variables */
.app {
  background-color: var(--bg-color);
  color: var(--text-color);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>
