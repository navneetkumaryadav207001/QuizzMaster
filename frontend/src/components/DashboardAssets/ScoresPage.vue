<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import Cookies from "js-cookie";

const scores = ref([]);
const loading = ref(true);
const errorMessage = ref("");

// Fetch user scores when the component mounts
onMounted(async () => {
  try {
    const response = await axios.get("http://127.0.0.1:5000/scores", {
      headers: {
        Authorization: `JWT ${Cookies.get("access_token")}`, // Pass JWT token
      },
    });

    scores.value = response.data;
  } catch (error) {
    errorMessage.value = "Failed to fetch scores.";
    console.error(error);
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div class="container mt-4">
    <h3 class="text-center">User Scores</h3>

    <div v-if="loading" class="text-center">
      <div class="spinner-border text-primary" />
    </div>

    <div v-else-if="errorMessage" class="alert alert-danger text-center">
      {{ errorMessage }}
    </div>

    <table v-else class="table table-bordered table-striped text-center">
      <thead class="table-dark">
        <tr>
          <th>ID</th>
          <th>Number of Questions</th>
          <th>Date</th>
          <th>Score</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="score in scores" :key="score.id">
          <td>{{ score.id }}</td>
          <td>{{ score.total_questions }}</td>
          <td>{{ new Date(score.attempted_at).toLocaleDateString() }}</td>
          <td>{{ score.score }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.table {
  margin-top: 20px;
}
</style>
