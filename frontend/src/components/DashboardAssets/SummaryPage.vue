<template>
  <div
    v-if="is_admin"
    style="
      display: flex;
      width: 90vw;
      height: 90vh;
      justify-content: space-around;
    "
  >
    <div>
      <h2>Quiz Questions Distribution</h2>
      <apexchart
        type="bar"
        :options="barChartOptions"
        :series="barChartSeries"
        class="chart1"
      />
    </div>

    <div>
      <h2>Subjects and Their Chapters</h2>
      <apexchart
        type="pie"
        :options="pieChartOptions"
        :series="pieChartSeries"
        class="chart2"
      />
    </div>
  </div>

  <div
    v-else
    style="
      display: flex;
      width: 90vw;
      height: 90vh;
      justify-content: space-around;
    "
  >
    <div>
      <h2>Your Quiz Scores</h2>
      <apexchart
        type="bar"
        :options="scoreBarChartOptions"
        :series="scoreBarChartSeries"
        class="chart3"
      />
    </div>

    <div>
      <h2>Score Distribution</h2>
      <apexchart
        type="pie"
        :options="scorePieChartOptions"
        :series="scorePieChartSeries"
        class="chart4"
      />
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, onMounted } from "vue";
import axios from "axios";
import Cookies from "js-cookie";
import VueApexCharts from "vue3-apexcharts";

export default defineComponent({
  components: { apexchart: VueApexCharts },
  setup() {
    const is_admin = ref(Cookies.get("is_admin") === "true");
    const authHeader = {
      headers: { Authorization: `JWT ${Cookies.get("access_token")}` },
    };

    // Admin Charts
    const quizzes = ref([]);
    const subjects = ref([]);
    const barChartOptions = ref({
      chart: { type: "bar" },
      xaxis: { categories: [] },
      title: { text: "Quiz Questions Count" },
    });
    const barChartSeries = ref([{ name: "Questions Count", data: [] }]);
    const pieChartOptions = ref({
      labels: [],
      title: { text: "Subjects and Chapters" },
    });
    const pieChartSeries = ref([]);

    // User Charts
    const scores = ref([]);
    const scoreBarChartOptions = ref({
      chart: { type: "bar" },
      xaxis: { categories: [] },
      title: { text: "Your Quiz Scores" },
    });
    const scoreBarChartSeries = ref([{ name: "Score", data: [] }]);
    const scorePieChartOptions = ref({
      labels: [],
      title: { text: "Score Distribution" },
    });
    const scorePieChartSeries = ref([]);

    const fetchAdminData = async () => {
      try {
        const [quizRes, subjectRes] = await Promise.all([
          axios.get("http://127.0.0.1:5000/Quizzs", authHeader),
          axios.get("http://127.0.0.1:5000/subjects", authHeader),
        ]);

        quizzes.value = quizRes.data.map((quiz) => ({
          title: quiz.name,
          questions_count: quiz.questions.length,
        }));

        subjects.value = subjectRes.data.map((subject) => ({
          name: subject.name,
          chapter_count: subject.chapters.length,
        }));

        // ✅ Fix: Replace the entire options object
        barChartOptions.value = {
          ...barChartOptions.value,
          xaxis: { categories: quizzes.value.map((q) => q.title) },
        };
        barChartSeries.value = [
          {
            name: "Questions Count",
            data: quizzes.value.map((q) => q.questions_count),
          },
        ];

        pieChartOptions.value = {
          ...pieChartOptions.value,
          labels: subjects.value.map((s) => s.name),
        };
        pieChartSeries.value = subjects.value.map((s) => s.chapter_count);
      } catch (error) {
        console.error("Error fetching admin data:", error);
      }
    };

    const fetchUserData = async () => {
      try {
        const scoresRes = await axios.get(
          "http://127.0.0.1:5000/scores",
          authHeader
        );
        scores.value = scoresRes.data.map((score) => ({
          quiz: score.quiz_id,
          points: score.score,
        }));

        console.log(scores);

        // ✅ Fix: Replace the entire options object
        scoreBarChartOptions.value = {
          ...scoreBarChartOptions.value,
          xaxis: { categories: scores.value.map((s) => s.quiz) },
        };
        scoreBarChartSeries.value = [
          { name: "Score", data: scores.value.map((s) => s.points) },
        ];

        scorePieChartOptions.value = {
          ...scorePieChartOptions.value,
          labels: scores.value.map((s) => s.quiz),
        };
        scorePieChartSeries.value = scores.value.map((s) => s.points);
      } catch (error) {
        console.error("Error fetching user scores:", error);
      }
    };

    onMounted(() => {
      if (is_admin.value) {
        fetchAdminData();
      } else {
        fetchUserData();
      }
    });

    return {
      is_admin,
      barChartOptions,
      barChartSeries,
      pieChartOptions,
      pieChartSeries,
      scoreBarChartOptions,
      scoreBarChartSeries,
      scorePieChartOptions,
      scorePieChartSeries,
    };
  },
});
</script>

<style scoped>
h2 {
  text-align: center;
  margin-bottom: 20px;
}
</style>
