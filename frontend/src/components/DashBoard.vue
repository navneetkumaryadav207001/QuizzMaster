<template>
  <div class="dashboard">
    <nav-bar @loggedOut="$emit('loggedOut')" />
    <home-page v-if="currentPage.currentPage == 'home'" />
    <scores-page v-else-if="currentPage.currentPage == 'scores'" />
    <quizz-page v-else-if="currentPage.currentPage == 'quizz'" />
    <summary-page v-else-if="currentPage.currentPage == 'summary'" />
  </div>
</template>

<script scoped>
import HomePage from "./DashboardAssets/HomePage.vue";
import navBar from "./DashboardAssets/navBar.vue";
import QuizzPage from "./DashboardAssets/QuizzPage.vue";
import SummaryPage from "./DashboardAssets/SummaryPage.vue";
import ScoresPage from "./DashboardAssets/ScoresPage.vue";
import { provide, reactive } from "vue";

export default {
  components: {
    navBar,
    HomePage,
    QuizzPage,
    SummaryPage,
    ScoresPage,
  },
  emits: ["loggedOut"],

  setup() {
    const currentPage = reactive({ currentPage: "home" });
    provide("currentPage", currentPage);
    return { currentPage };
  },
};
</script>

<style scoped>
.dashboard {
  width: 100vw;
  height: 100vh;
}
</style>
