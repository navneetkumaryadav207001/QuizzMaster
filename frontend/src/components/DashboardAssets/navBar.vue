<template>
  <div class="navbarMine">
    <nav
      :class="
        theme.dark
          ? 'navbar navbar-dark bg-dark justify-content-between'
          : 'navbar navbar-light bg-light justify-content-between'
      "
    >
      <nav
        :class="
          theme.dark
            ? 'navbar navbar-expand-lg navbar-dark bg-dark'
            : 'navbar navbar-expand-lg navbar-light bg-light'
        "
      >
        <button
          class="navbar-toggler"
          type="button"
          data-toggle="collapse"
          data-target="#navbarNavAltMarkup"
          aria-controls="navbarNavAltMarkup"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon" />
        </button>
        <div id="navbarNavAltMarkup" class="collapse navbar-collapse">
          <div class="navbar-nav">
            <button
              class="nav-item nav-link active"
              @click="currentPage.currentPage = 'home'"
            >
              Home
            </button>
            <button
              v-if="admin"
              class="nav-item nav-link"
              @click="currentPage.currentPage = 'quizz'"
            >
              Quizz
            </button>
            <button
              v-else
              class="nav-item nav-link"
              @click="currentPage.currentPage = 'scores'"
            >
              Scores
            </button>
            <button
              class="nav-item nav-link"
              @click="currentPage.currentPage = 'summary'"
            >
              Summary
            </button>
            <a class="nav-item nav-link disabled" href="#"
              ><p v-if="admin">Admin</p>
              <p v-else>User</p></a
            >
          </div>
        </div>
      </nav>
      <div class="left justify-content-between">
        <form class="form-inline searchbar">
          <input
            class="form-control mr-sm-2"
            type="search"
            placeholder="Search"
            aria-label="Search"
          />
          <button class="btn btn-outline-success my-2 my-sm-0" type="submit">
            Search
          </button>
        </form>
        <button
          class="btn btn-outline-danger my-2 my-sm-0"
          type="submit"
          @click="$emit('loggedOut')"
        >
          Log out
        </button>
      </div>
    </nav>
  </div>
</template>

<script>
import { inject, ref, onMounted } from "vue";
import Cookies from "js-cookie"; // Ensure you have installed js-cookie: npm install js-cookie

export default {
  emits: ["loggedOut"],
  setup() {
    const theme = inject("theme");
    const currentPage = inject("currentPage");

    return { theme, currentPage };
  },

  data() {
    return {
      admin: Cookies.get("is_admin") == "true",
    };
  },
};
</script>

<style scoped>
p {
  display: inline;
}

.searchbar {
  display: flex;
}
.left {
  display: flex;
}
</style>
