<template>
  <div class="container mt-4">
    <div v-if="!isAdmin" class="alert alert-danger">
      Access Denied: Administrator privileges required
    </div>

    <div v-else>
      <h2 class="mb-4">Quizz Management</h2>
      <div class="row">
        <div v-for="Quizz in Quizzs" :key="Quizz.id" class="col-md-4 mb-4">
          <div class="card">
            <div class="card-header bg-primary text-white">
              {{ Quizz.name }}
              <button
                class="btn btn-sm btn-outline-primary me-1"
                @click="
                  showEditQuizzModal = true;
                  selectedQuizz = Quizz;
                "
              >
                <i class="bi bi-pencil" />
              </button>
              <button
                class="btn btn-sm btn-outline-danger"
                @click="deleteQuizz(Quizz.id)"
              >
                <i class="bi bi-trash" />
              </button>
            </div>
            <div class="card-body p-0">
              <table class="table table-striped mb-0">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Question</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="question in Quizz.questions" :key="question.id">
                    <td>{{ question.id }}</td>
                    <td>{{ question.text }}</td>
                    <td>
                      <button class="btn btn-sm btn-outline-primary me-1">
                        <i class="bi bi-pencil" />
                      </button>
                      <button
                        class="btn btn-sm btn-outline-danger"
                        @click="deletequestion(Quizz.id, question.id)"
                      >
                        <i class="bi bi-trash" />
                      </button>
                    </td>
                  </tr>
                  <tr>
                    <button
                      class="btn btn-success btn-lg"
                      @click="
                        showAddQuestionModal(Quizz.id, Quizz.chapter_id);
                        currentQuizz = Quizz.id;
                      "
                    >
                      <i class="bi bi-plus-circle me-2" />Add question
                    </button>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- Add Quizz Button -->
      <div class="text-center mt-4">
        <button
          class="btn btn-success btn-lg"
          @click="showAddQuizzModal = true"
        >
          <i class="bi bi-plus-circle me-2" />Add Quizz
        </button>
      </div>

      <!-- Add Quizz Modal -->
      <div
        class="modal"
        tabindex="-1"
        :class="{ 'show d-block': showAddQuizzModal }"
      >
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Add New Quizz</h5>
              <button
                type="button"
                class="btn-close"
                @click="closeAddQuizzModal"
              />
            </div>
            <div class="modal-body">
              <form @submit.prevent="saveQuizz">
                <div class="mb-3">
                  <label class="form-label">Quizz Name</label>
                  <input
                    v-model="newQuizz.name"
                    type="text"
                    class="form-control"
                    required
                  />
                </div>
                <div class="mb-3">
                  <label class="form-label">Description</label>
                  <textarea
                    v-model="newQuizz.description"
                    class="form-control"
                    rows="3"
                  />
                </div>
                <div class="mb-3">
                  <label class="form-label">Chapter</label>
                  <select
                    v-model="newQuizz.chapter_id"
                    class="form-control"
                    required
                  >
                    <option
                      v-for="chapter in chapters"
                      :key="chapter.id"
                      :value="chapter.id"
                    >
                      {{ chapter.name }}
                    </option>
                  </select>
                </div>
                <div class="mb-3">
                  <label class="form-label">Date</label>
                  <input
                    v-model="newQuizz.date"
                    type="date"
                    class="form-control"
                    required
                  />
                </div>
                <div class="mb-3">
                  <label class="form-label">Duration (minutes)</label>
                  <input
                    v-model="newQuizz.duration"
                    type="number"
                    class="form-control"
                    required
                  />
                </div>

                <!-- Response Messages -->
                <div
                  v-if="submitResponse.message"
                  :class="[
                    'alert',
                    submitResponse.success ? 'alert-success' : 'alert-danger',
                  ]"
                >
                  {{ submitResponse.message }}
                </div>

                <div class="modal-footer">
                  <button
                    type="button"
                    class="btn btn-secondary"
                    @click="closeAddQuizzModal"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    class="btn btn-primary"
                    :disabled="isSubmitting"
                  >
                    <span
                      v-if="isSubmitting"
                      class="spinner-border spinner-border-sm me-1"
                    />
                    Save Quizz
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>

      <!-- Modal Backdrop -->
      <div v-if="showAddQuizzModal" class="modal-backdrop fade show" />
    </div>

    <!-- Add Question Modal -->
    <div
      class="modal"
      tabindex="-1"
      :class="{ 'show d-block': showQuestionModal }"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add New Question</h5>
            <button
              type="button"
              class="btn-close"
              @click="closeAddQuestionModal"
            />
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveQuestion">
              <div class="mb-3">
                <label class="form-label">Chapter ID</label>
                <input
                  v-model="currentQuizz"
                  type="text"
                  class="form-control"
                  disabled
                />
              </div>
              <div class="mb-3">
                <label class="form-label">Question Title</label>
                <input
                  v-model="newQuestion.question_title"
                  type="text"
                  class="form-control"
                  required
                />
              </div>
              <div class="mb-3">
                <label class="form-label">Question Text</label>
                <input
                  v-model="newQuestion.text"
                  type="text"
                  class="form-control"
                  required
                />
              </div>
              <div class="mb-3">
                <label class="form-label">Option A</label>
                <input
                  v-model="newQuestion.option_a"
                  type="text"
                  class="form-control"
                  required
                />
              </div>
              <div class="mb-3">
                <label class="form-label">Option B</label>
                <input
                  v-model="newQuestion.option_b"
                  type="text"
                  class="form-control"
                  required
                />
              </div>
              <div class="mb-3">
                <label class="form-label">Option C</label>
                <input
                  v-model="newQuestion.option_c"
                  type="text"
                  class="form-control"
                  required
                />
              </div>
              <div class="mb-3">
                <label class="form-label">Option D</label>
                <input
                  v-model="newQuestion.option_d"
                  type="text"
                  class="form-control"
                  required
                />
              </div>
              <div class="mb-3">
                <label class="form-label">Correct Option</label>
                <select
                  v-model="newQuestion.correct_option"
                  class="form-control"
                  required
                >
                  <option value="A">A</option>
                  <option value="B">B</option>
                  <option value="C">C</option>
                  <option value="D">D</option>
                </select>
              </div>
              <div class="modal-footer">
                <button
                  type="button"
                  class="btn btn-secondary"
                  @click="closeAddQuestionModal"
                >
                  Cancel
                </button>
                <button type="submit" class="btn btn-primary">
                  Save Question
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    <div v-if="showQuestionModal" class="modal-backdrop fade show" />

    <!--Edit Quizz Modal-->
    <div
      class="modal"
      tabindex="-1"
      :class="{ 'show d-block': showAddQuizzModal }"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add New Quizz</h5>
            <button
              type="button"
              class="btn-close"
              @click="closeAddQuizzModal"
            />
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveQuizz">
              <div class="mb-3">
                <label class="form-label">Quizz Name</label>
                <input
                  v-model="newQuizz.name"
                  type="text"
                  class="form-control"
                  required
                />
              </div>
              <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea
                  v-model="newQuizz.description"
                  class="form-control"
                  rows="3"
                />
              </div>
              <div class="mb-3">
                <label class="form-label">Chapter</label>
                <select
                  v-model="newQuizz.chapter_id"
                  class="form-control"
                  required
                >
                  <option
                    v-for="chapter in chapters"
                    :key="chapter.id"
                    :value="chapter.id"
                  >
                    {{ chapter.name }}
                  </option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label">Date</label>
                <input
                  v-model="newQuizz.date"
                  type="date"
                  class="form-control"
                  required
                />
              </div>
              <div class="mb-3">
                <label class="form-label">Duration (minutes)</label>
                <input
                  v-model="newQuizz.duration"
                  type="number"
                  class="form-control"
                  required
                />
              </div>

              <!-- Response Messages -->
              <div
                v-if="submitResponse.message"
                :class="[
                  'alert',
                  submitResponse.success ? 'alert-success' : 'alert-danger',
                ]"
              >
                {{ submitResponse.message }}
              </div>

              <div class="modal-footer">
                <button
                  type="button"
                  class="btn btn-secondary"
                  @click="closeAddQuizzModal"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  class="btn btn-primary"
                  :disabled="isSubmitting"
                >
                  <span
                    v-if="isSubmitting"
                    class="spinner-border spinner-border-sm me-1"
                  />
                  Save Quizz
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Backdrop -->
    <div v-if="showAddQuizzModal" class="modal-backdrop fade show" />

    <!--Edit Question Modal-->
    <div
      class="modal"
      tabindex="-1"
      :class="{ 'show d-block': showQuestionModal }"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add New Question</h5>
            <button
              type="button"
              class="btn-close"
              @click="closeAddQuestionModal"
            />
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveQuestion">
              <div class="mb-3">
                <label class="form-label">Chapter ID</label>
                <input
                  v-model="currentQuizz"
                  type="text"
                  class="form-control"
                  disabled
                />
              </div>
              <div class="mb-3">
                <label class="form-label">Question Title</label>
                <input
                  v-model="newQuestion.question_title"
                  type="text"
                  class="form-control"
                  required
                />
              </div>
              <div class="mb-3">
                <label class="form-label">Question Text</label>
                <input
                  v-model="newQuestion.text"
                  type="text"
                  class="form-control"
                  required
                />
              </div>
              <div class="mb-3">
                <label class="form-label">Option A</label>
                <input
                  v-model="newQuestion.option_a"
                  type="text"
                  class="form-control"
                  required
                />
              </div>
              <div class="mb-3">
                <label class="form-label">Option B</label>
                <input
                  v-model="newQuestion.option_b"
                  type="text"
                  class="form-control"
                  required
                />
              </div>
              <div class="mb-3">
                <label class="form-label">Option C</label>
                <input
                  v-model="newQuestion.option_c"
                  type="text"
                  class="form-control"
                  required
                />
              </div>
              <div class="mb-3">
                <label class="form-label">Option D</label>
                <input
                  v-model="newQuestion.option_d"
                  type="text"
                  class="form-control"
                  required
                />
              </div>
              <div class="mb-3">
                <label class="form-label">Correct Option</label>
                <select
                  v-model="newQuestion.correct_option"
                  class="form-control"
                  required
                >
                  <option value="A">A</option>
                  <option value="B">B</option>
                  <option value="C">C</option>
                  <option value="D">D</option>
                </select>
              </div>
              <div class="modal-footer">
                <button
                  type="button"
                  class="btn btn-secondary"
                  @click="closeAddQuestionModal"
                >
                  Cancel
                </button>
                <button type="submit" class="btn btn-primary">
                  Save Question
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    <div v-if="showQuestionModal" class="modal-backdrop fade show" />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import Cookies from "js-cookie";
import axios from "axios";

const isAdmin = ref(false);
const Quizzs = ref([]);
const chapters = ref([]);
const showAddQuizzModal = ref(false);
const showQuestionModal = ref(false);
const isSubmitting = ref(false);
const currentQuizz = ref(-1);

const newQuizz = ref({
  name: "",
  description: "",
  chapter_id: "",
  date: "",
  duration: "",
});
const newQuestion = ref({
  chapter_id: "",
  question_title: " ",
  text: "",
  option_a: "",
  option_b: "",
  option_c: "",
  option_d: "",
  correct_option: "",
});

const submitResponse = ref({ message: "", success: false });

onMounted(async () => {
  const adminStatus = Cookies.get("is_admin");
  isAdmin.value = adminStatus === "true";
  if (isAdmin.value) {
    try {
      const response = await axios.get("http://127.0.0.1:5000/Quizzs", {
        headers: { Authorization: `JWT ${Cookies.get("access_token")}` },
      });
      Quizzs.value = response.data;
      const chaptersResponse = await axios.get(
        "http://127.0.0.1:5000/chapters",
        {
          headers: { Authorization: `JWT ${Cookies.get("access_token")}` },
        }
      );
      chapters.value = chaptersResponse.data;
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  }
});

const saveQuizz = async () => {
  submitResponse.value = { message: "", success: false };
  isSubmitting.value = true;
  try {
    const response = await axios.post(
      "http://127.0.0.1:5000/Quizzs",
      newQuizz.value,
      {
        headers: { Authorization: `JWT ${Cookies.get("access_token")}` },
      }
    );
    Quizzs.value.push(response.data);
    submitResponse.value = {
      message: "Quizz added successfully!",
      success: true,
    };
    setTimeout(() => {
      closeAddQuizzModal();
      newQuizz.value = {};
    }, 500);
  } catch (error) {
    submitResponse.value = {
      message: error.response?.data?.message || "Failed to add Quizz",
      success: false,
    };
  } finally {
    isSubmitting.value = false;
  }
};

const closeAddQuizzModal = () => {
  showAddQuizzModal.value = false;
  submitResponse.value = { message: "", success: false };
  newQuizz.value = {};
};

const showAddQuestionModal = (quizId, chapterId) => {
  newQuestion.value = {
    chapter_id: chapterId,
    quiz_id: quizId,
    text: "",
    option_a: "",
    option_b: "",
    option_c: "",
    option_d: "",
    correct_option: "",
  };
  showQuestionModal.value = true;
};

const closeAddQuestionModal = () => {
  showQuestionModal.value = false;
};

const saveQuestion = async () => {
  try {
    await axios.post("http://127.0.0.1:5000/questions", newQuestion.value, {
      headers: { Authorization: `JWT ${Cookies.get("access_token")}` },
    });
    closeAddQuestionModal();
    location.reload();
  } catch (error) {
    console.error("Error saving question:", error);
  }
};

const deletequestion = async (quizzId, questionId) => {
  try {
    const response = await fetch("http://localhost:5000/questions", {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        Authorization: `JWT ${Cookies.get("access_token")}`, // Send JWT in Authorization header
      },
      body: JSON.stringify({ id: questionId }),
    });

    const data = await response.json();
    if (response.ok) {
      console.log("Chapter deleted successfully:", data);
      location.reload();
    } else {
      console.error("Error deleting chapter:", data.error);
    }
  } catch (error) {
    console.error("Request failed:", error);
  }
};

const deleteQuizz = async (QuizzId) => {
  try {
    const response = await fetch("http://localhost:5000/Quizzs", {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        Authorization: `JWT ${Cookies.get("access_token")}`, // Using "JWT" instead of "Bearer"
      },
      body: JSON.stringify({ id: QuizzId }),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Failed to delete Quizz");
    }

    console.log("Quizz deleted successfully:", data.message);
    location.reload();
    return data;
  } catch (error) {
    console.error("Error deleting Quizz:", error.message);
  }
};
</script>
