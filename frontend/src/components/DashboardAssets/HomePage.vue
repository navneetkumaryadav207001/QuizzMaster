<template>
  <div class="container mt-4">
    <div v-if="!isAdmin" class="alert alert-danger">
      <h2 class="text-center mb-4">Upcoming Quizzes</h2>
      <table class="table table-striped">
        <thead class="table-dark">
          <tr>
            <th>ID</th>
            <th>Number of Questions</th>
            <th>Date</th>
            <th>Duration (mins)</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="quiz in upcomingQuizzes" :key="quiz.id">
            <td>{{ quiz.id }}</td>
            <td>{{ quiz.questions.length }}</td>
            <td>{{ formatDate(quiz.date) }}</td>
            <td>{{ quiz.duration }}</td>
            <td>
              <button class="btn btn-info btn-sm me-2" @click="viewQuiz(quiz)">
                View
              </button>
              <button class="btn btn-success btn-sm" @click="startQuiz(quiz)">
                Start
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <!--Modal For View-->
      <div
        v-if="showModal"
        class="modal fade show d-block"
        tabindex="-1"
        style="background: rgba(0, 0, 0, 0.5)"
      >
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Quiz Details</h5>
              <button type="button" class="btn-close" @click="closeModal" />
            </div>
            <div class="modal-body">
              <p><strong>ID:</strong> {{ selectedQuiz.id }}</p>
              <p><strong>Name:</strong> {{ selectedQuiz.name }}</p>
              <p><strong>Date:</strong> {{ formatDate(selectedQuiz.date) }}</p>
              <p><strong>Duration:</strong> {{ selectedQuiz.duration }} mins</p>
              <p>
                <strong>Number of Questions:</strong>
                {{ selectedQuiz.questions.length }}
              </p>
              <hr />
              <h6>Questions:</h6>
              <ul>
                <li v-for="q in selectedQuiz.questions" :key="q.id">
                  {{ q.text }}
                </li>
              </ul>
            </div>
            <div class="modal-footer">
              <button
                type="button"
                class="btn btn-secondary"
                @click="closeModal"
              >
                Close
              </button>
            </div>
          </div>
        </div>
        <!--Modal for Start-->
      </div>
      <div
        v-if="isQuizActive"
        class="modal fade show d-block"
        tabindex="-1"
        style="background: rgba(0, 0, 0, 0.5)"
      >
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Quiz: {{ currentQuiz.name }}</h5>
              <button type="button" class="btn-close" @click="closeQuiz" />
            </div>
            <div class="modal-body">
              <!-- Timer -->
              <p><strong>Time Left:</strong> {{ formatTimeLeft }}</p>

              <!-- Question -->
              <h6>
                Question {{ currentQuestionIndex + 1 }} of
                {{ currentQuiz.questions.length }}
              </h6>
              <p>{{ currentQuiz.questions[currentQuestionIndex].text }}</p>

              <!-- Options -->
              <div v-for="(option, index) in options" :key="index">
                <input
                  :id="'option' + index"
                  v-model="userAnswers[currentQuestionIndex]"
                  type="radio"
                  :value="option"
                />
                <label :for="'option' + index">{{ option }}</label>
              </div>
            </div>
            <div class="modal-footer">
              <button
                v-if="!isLastQuestion"
                class="btn btn-primary"
                @click="nextQuestion"
              >
                Save & Next
              </button>
              <button class="btn btn-success" @click="submitQuiz">
                Submit
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else>
      <h2 class="mb-4">Subject Management</h2>
      <div class="row">
        <div
          v-for="subject in subjects"
          :key="subject.id"
          class="col-md-4 mb-4"
        >
          <div class="card">
            <div class="card-header bg-white text-dark">
              {{ subject.name }}
              <button
                class="btn btn-sm btn-outline-primary me-1"
                @click="
                  showEditSubjectModal = true;
                  selectedSubject = subject;
                "
              >
                <i class="bi bi-pencil" />
              </button>
              <button
                class="btn btn-sm btn-outline-danger"
                @click="deleteSubject(subject.id)"
              >
                <i class="bi bi-trash" />
              </button>
            </div>
            <div class="card-body p-0">
              <table class="table table-striped mb-0">
                <thead>
                  <tr>
                    <th>Chapter</th>
                    <th>Quizzes</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="chapter in subject.chapters" :key="chapter.id">
                    <td>{{ chapter.name }}</td>
                    <td>{{ chapter.quizz_count }}</td>
                    <td>
                      <button
                        class="btn btn-sm btn-outline-primary me-1"
                        @click="
                          showEditChapterModal = true;
                          selectedChapter = chapter;
                          selectedSubject = subject;
                        "
                      >
                        <i class="bi bi-pencil" />
                      </button>
                      <button
                        class="btn btn-sm btn-outline-danger"
                        @click="deleteChapter(subject.id, chapter.id)"
                      >
                        <i class="bi bi-trash" />
                      </button>
                    </td>
                  </tr>
                  <tr>
                    <button
                      class="btn btn-success btn-lg"
                      @click="
                        showAddChapterModal = true;
                        currentSubject = subject.id;
                      "
                    >
                      <i class="bi bi-plus-circle me-2" />Add Chapter
                    </button>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- Add Subject Button -->
      <div class="text-center mt-4">
        <button
          class="btn btn-success btn-lg"
          @click="showAddSubjectModal = true"
        >
          <i class="bi bi-plus-circle me-2" />Add Subject
        </button>
      </div>

      <!-- Add Subject Modal -->
      <div
        class="modal"
        tabindex="-1"
        :class="{ 'show d-block': showAddSubjectModal }"
      >
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Add New Subject</h5>
              <button
                type="button"
                class="btn-close"
                @click="closeAddSubjectModal"
              />
            </div>
            <div class="modal-body">
              <form @submit.prevent="saveSubject">
                <div class="mb-3">
                  <label class="form-label">Subject Name</label>
                  <input
                    v-model="newSubject.name"
                    type="text"
                    class="form-control"
                    required
                  />
                </div>
                <div class="mb-3">
                  <label class="form-label">Description</label>
                  <textarea
                    v-model="newSubject.description"
                    class="form-control"
                    rows="3"
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
                    @click="closeAddSubjectModal"
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
                    Save Subject
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>

      <!-- Modal Backdrop -->
      <div
        v-if="
          showAddSubjectModal ||
          showAddChapterModal ||
          showEditChapterModal ||
          showEditSubjectModal
        "
        class="modal-backdrop fade show"
      />

      <!-- Edit Chapter Modal -->
      <div
        class="modal"
        tabindex="-1"
        :class="{ 'show d-block': showEditChapterModal }"
      >
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Edit Chapter</h5>
              <button
                type="button"
                class="btn-close"
                @click="closeEditChapterModal"
              />
            </div>
            <div class="modal-body">
              <form
                @submit.prevent="
                  editChapterf(selectedSubject.id, selectedChapter.id)
                "
              >
                <div class="mb-3">
                  <label class="form-label">Chapter Name</label>
                  <input
                    v-model="editChapter.name"
                    type="text"
                    class="form-control"
                    required
                  />
                </div>
                <div class="mb-3">
                  <label class="form-label">Description</label>
                  <textarea
                    v-model="editChapter.description"
                    class="form-control"
                    rows="3"
                  />
                </div>

                <div class="modal-footer">
                  <button
                    type="button"
                    class="btn btn-secondary"
                    @click="closeEditChapterModal"
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
                    Edit Chapter
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
      <!-- Edit Subject Modal -->
      <div
        class="modal"
        tabindex="-1"
        :class="{ 'show d-block': showEditSubjectModal }"
      >
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Edit Subject</h5>
              <button
                type="button"
                class="btn-close"
                @click="closeEditSubjectModal"
              />
            </div>
            <div class="modal-body">
              <form @submit.prevent="editSubjectf(selectedSubject.id)">
                <div class="mb-3">
                  <label class="form-label">Subject Name</label>
                  <input
                    v-model="editSubject.name"
                    type="text"
                    class="form-control"
                    required
                  />
                </div>
                <div class="mb-3">
                  <label class="form-label">Description</label>
                  <textarea
                    v-model="editSubject.description"
                    class="form-control"
                    rows="3"
                  />
                </div>

                <div class="modal-footer">
                  <button
                    type="button"
                    class="btn btn-secondary"
                    @click="closeEditSubjectModal"
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
                    Edit Subject
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>

      <!-- Add Chapter Modal -->
      <div
        class="modal"
        tabindex="-1"
        :class="{ 'show d-block': showAddChapterModal }"
      >
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Add New Chapter</h5>
              <button
                type="button"
                class="btn-close"
                @click="closeAddChapterModal"
              />
            </div>
            <div class="modal-body">
              <form @submit.prevent="saveChapter(currentSubject)">
                <div class="mb-3">
                  <label class="form-label">Chapter Name</label>
                  <input
                    v-model="newChapter.name"
                    type="text"
                    class="form-control"
                    required
                  />
                </div>
                <div class="mb-3">
                  <label class="form-label">Description</label>
                  <textarea
                    v-model="newChapter.description"
                    class="form-control"
                    rows="3"
                  />
                </div>

                <!-- Response Messages -->
                <div
                  v-if="submitResponseChapter.message"
                  :class="[
                    'alert',
                    submitResponse.success ? 'alert-success' : 'alert-danger',
                  ]"
                >
                  {{ submitResponseChapter.message }}
                </div>

                <div class="modal-footer">
                  <button
                    type="button"
                    class="btn btn-secondary"
                    @click="closeAddChapterModal"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    class="btn btn-primary"
                    :disabled="isSubmittingChapter"
                  >
                    <span
                      v-if="isSubmittingChapter"
                      class="spinner-border spinner-border-sm me-1"
                    />
                    Add Chapter
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import Cookies from "js-cookie";
import axios from "axios";

const isAdmin = ref(false);
const subjects = ref([]);
const showAddSubjectModal = ref(false);
const showAddChapterModal = ref(false);
const isSubmitting = ref(false);
const isSubmittingChapter = ref(false);
const currentSubject = ref(-1);
const showModal = ref(false);
const selectedQuiz = ref(null);
const isQuizActive = ref(false);
const currentQuiz = ref({});
const currentQuestionIndex = ref(0);
const userAnswers = ref([]);
const timeLeft = ref(0);
const selectedChapter = ref(null);
const showEditChapterModal = ref(false);
const showEditSubjectModal = ref(false);
const selectedSubject = ref(null);
let timer = null;
const quizzes = ref([]);
const authHeader = {
  headers: { Authorization: `JWT ${Cookies.get("access_token")}` },
};

const fetchQuizzes = async () => {
  try {
    const response = await axios.get(
      "http://127.0.0.1:5000/Quizzs",
      authHeader
    );
    quizzes.value = response.data;
  } catch (error) {
    console.error("Error fetching quizzes:", error);
  }
};

const formatDate = (dateString) => {
  const options = { year: "numeric", month: "short", day: "numeric" };
  return new Date(dateString).toLocaleDateString(undefined, options);
};

const viewQuiz = (quiz) => {
  selectedQuiz.value = quiz;
  showModal.value = true;
};

// Start quiz function
const startQuiz = (quiz) => {
  isQuizActive.value = true;
  currentQuiz.value = quiz;
  currentQuestionIndex.value = 0;
  userAnswers.value = new Array(quiz.questions.length).fill(null);
  timeLeft.value = quiz.duration * 60; // Convert minutes to seconds

  // Start countdown timer
  if (timer) clearInterval(timer);
  timer = setInterval(() => {
    if (timeLeft.value > 0) {
      timeLeft.value--;
    } else {
      clearInterval(timer);
      submitQuiz(); // Auto-submit when time runs out
    }
  }, 1000);
};

const formatTimeLeft = computed(() => {
  const minutes = Math.floor(timeLeft.value / 60);
  const seconds = timeLeft.value % 60;
  return `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
});

// Submit quiz function
const submitQuiz = async () => {
  clearInterval(timer);
  isQuizActive.value = false;

  try {
    const response = await axios.post(
      "http://127.0.0.1:5000/scores",
      {
        quiz_id: currentQuiz.value.id,
        date: currentQuiz.value.date,
        total_questions: currentQuiz.value.questions.length,
        answers: userAnswers.value,
      },
      {
        headers: { Authorization: `JWT ${Cookies.get("access_token")}` },
      }
    );
    alert("Quiz submitted successfully! Score: " + response.data.score);
  } catch (error) {
    console.error("Error submitting quiz:", error);
  }
};

// Close quiz modal
const closeQuiz = () => {
  isQuizActive.value = false;
  clearInterval(timer);
};

// Reactive state variables

// New subject form data
const newSubject = ref({
  name: "",
  description: "",
});

const newChapter = ref({
  name: "",
  description: "",
});
const editChapter = ref({
  name: "",
  description: "",
});
const editSubject = ref({
  name: "",
  description: "",
});

// Submit response tracking
const submitResponse = ref({
  message: "",
  success: false,
});
const submitResponseChapter = ref({
  message: "",
  success: false,
});

// Check admin status on component mount
onMounted(async () => {
  // Check is_admin cookie

  fetchQuizzes();
  const adminStatus = Cookies.get("is_admin");

  // Convert string to boolean
  isAdmin.value = adminStatus === "true";

  // If admin, fetch subjects
  if (isAdmin.value) {
    try {
      const response = await axios.get("http://127.0.0.1:5000/subjects", {
        headers: {
          Authorization: `JWT ${Cookies.get("access_token")}`, // Send JWT in Authorization header
        },
      });
      subjects.value = response.data;
    } catch (error) {
      console.error("Error fetching subjects:", error);
    }
  }
});

// Method to save new subject
const saveSubject = async () => {
  // Reset previous responses
  submitResponse.value = { message: "", success: false };
  isSubmitting.value = true;

  try {
    // Call backend to add subject
    const response = await axios.post(
      "http://127.0.0.1:5000/subjects",
      newSubject.value,
      {
        headers: {
          Authorization: `JWT ${Cookies.get("access_token")}`, // Send JWT in Authorization header
        },
      }
    );

    // Update UI
    subjects.value.push(response.data);

    // Show success message
    submitResponse.value = {
      message: "Subject added successfully!",
      success: true,
    };

    // Reset form and close modal after 2 seconds
    setTimeout(() => {
      closeAddSubjectModal();
      newSubject.value = { name: "", description: "" };
    }, 500);
  } catch (error) {
    // Handle error
    submitResponse.value = {
      message: error.response?.data?.message || "Failed to add subject",
      success: false,
    };
  } finally {
    isSubmitting.value = false;
  }
};

const saveChapter = async (id) => {
  // Reset previous responses
  submitResponseChapter.value = { message: "", success: false };
  isSubmittingChapter.value = true;

  try {
    // Call backend to add subject
    const response = await axios.post(
      `http://127.0.0.1:5000/subjects/${currentSubject.value}/chapters`,
      newChapter.value,
      {
        headers: {
          Authorization: `JWT ${Cookies.get("access_token")}`, // Send JWT in Authorization header
        },
      }
    );

    // Show success message
    submitResponseChapter.value = {
      message: "Chapter added successfully!",
      success: true,
    };

    // Reset form and close modal after 2 seconds
    setTimeout(() => {
      closeAddChapterModal();
      newChapter.value = { name: "", description: "" };
      location.reload();
    }, 500);
  } catch (error) {
    // Handle error
    submitResponseChapter.value = {
      message: error.response?.data?.message || "Failed to add Chapter",
      success: false,
    };
  } finally {
    isSubmittingChapter.value = false;
  }
};
const editChapterf = async (subjectId, chapterId) => {
  try {
    const response = await fetch(
      `http://localhost:5000/subjects/${subjectId}/chapters`,
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `JWT ${Cookies.get("access_token")}`, // Send JWT in Authorization header
        },
        body: JSON.stringify({
          id: chapterId,
          name: editChapter.value.name,
          description: editChapter.value.description,
        }),
      }
    );

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
const editSubjectf = async (subjectId) => {
  try {
    const response = await fetch("http://localhost:5000/subjects", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `JWT ${Cookies.get("access_token")}`, // Using "JWT" instead of "Bearer"
      },
      body: JSON.stringify({
        id: subjectId,
        name: editSubject.value.name,
        description: editSubject.value.description,
      }),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Failed to edit subject");
    }

    console.log("Subject edit successfully:", data.message);
    location.reload();
    return data;
  } catch (error) {
    console.error("Error edit subject:", error.message);
  }
};
const deleteChapter = async (subjectId, chapterId) => {
  try {
    const response = await fetch(
      `http://localhost:5000/subjects/${subjectId}/chapters`,
      {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Authorization: `JWT ${Cookies.get("access_token")}`, // Send JWT in Authorization header
        },
        body: JSON.stringify({ id: chapterId }),
      }
    );

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

const deleteSubject = async (subjectId) => {
  try {
    const response = await fetch("http://localhost:5000/subjects", {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        Authorization: `JWT ${Cookies.get("access_token")}`, // Using "JWT" instead of "Bearer"
      },
      body: JSON.stringify({ id: subjectId }),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Failed to delete subject");
    }

    console.log("Subject deleted successfully:", data.message);
    location.reload();
    return data;
  } catch (error) {
    console.error("Error deleting subject:", error.message);
  }
};

// Modal control methods
const closeAddSubjectModal = () => {
  showAddSubjectModal.value = false;
  submitResponse.value = { message: "", success: false };
  newSubject.value = { name: "", description: "" };
};

const closeAddChapterModal = () => {
  showAddChapterModal.value = false;
  submitResponseChapter.value = { message: "", success: false };
  newChapter.value = { name: "", description: "" };
};

const closeModal = () => {
  showModal.value = false;
  selectedQuiz.value = null;
};
const closeEditChapterModal = () => {
  showEditChapterModal.value = false;
  selectedChapter.value = null;
};
const closeEditSubjectModal = () => {
  showEditSubjectModal.value = false;
  selectedSubject.value = null;
};
const nextQuestion = () => {
  if (currentQuestionIndex.value < currentQuiz.value.questions.length - 1) {
    currentQuestionIndex.value++;
  }
};

const upcomingQuizzes = computed(() => {
  return quizzes.value.filter((quiz) => new Date(quiz.date) >= new Date());
});

// Get options (mocked for now)
const options = computed(() => {
  // ✅ Ensure `currentQuiz` and `questions` exist
  if (
    !currentQuiz.value ||
    !currentQuiz.value.questions ||
    currentQuiz.value.questions.length === 0
  ) {
    console.warn("No valid quiz or questions found.");
    return [];
  }

  // ✅ Ensure `currentQuestionIndex` is within valid range
  if (
    currentQuestionIndex.value < 0 ||
    currentQuestionIndex.value >= currentQuiz.value.questions.length
  ) {
    console.warn("Invalid question index:", currentQuestionIndex.value);
    return [];
  }

  // ✅ Fetch the correct question safely
  const question = currentQuiz.value.questions[currentQuestionIndex.value];
  return [
    question.option_a,
    question.option_b,
    question.option_c,
    question.option_d,
  ];
});
</script>

<style scoped>
.card {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.card:hover {
  transform: scale(1.02);
}

.modal-backdrop {
  opacity: 0.5;
}
</style>
