<template>
  <div class="login-page">
    <bg-stars />
    <paper-plane />
    <paper-plane />
    <paper-plane />
    <paper-plane />
    <paper-plane />

    <div v-if="!login" class="login-card">
      <h1>Login</h1>
      {{ response }}
      <form class="max-width-400" @submit.prevent="validateForm">
        <!-- Email Section -->
        <div class="mb-3">
          <label class="form-label"><b>Email address</b></label>
          <input
            id="loginEmail"
            v-model="email"
            type="email"
            class="form-control"
            aria-describedby="emailHelp"
            autocomplete="off"
          />
          <div v-if="email.length > 0" class="errors">
            <p v-if="!email.includes('@')">* Missing '@'</p>
            <p v-else-if="email.length < 5">* Email is too short</p>
            <p v-else-if="!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)">
              * Invalid email format
            </p>
          </div>
          <small>We'll never share your email with anyone else.</small>
        </div>

        <!-- Password Section -->
        <div class="mb-3">
          <label class="form-label"><b>Password</b></label>
          <input
            id="loginPassword"
            v-model="password"
            type="password"
            class="form-control"
            autocomplete="off"
          />
          <div v-if="password.length > 0" class="errors">
            <p v-if="password.length < 6">
              * Password must be at least 6 characters
            </p>
            <p v-else-if="!/[A-Z]/.test(password)">
              * Password must contain at least one uppercase letter
            </p>
            <p v-else-if="!/[0-9]/.test(password)">
              * Password must contain at least one number
            </p>
          </div>
        </div>

        <!-- Submit Button -->
        <div id="submit-button">
          <button
            type="submit"
            :class="theme.dark ? 'btn btn-light' : 'btn btn-dark'"
          >
            Submit
          </button>
        </div>
        <p>OR</p>
        <div class="s-button">
          <button
            v-if="!login"
            :class="theme.dark ? 'btn btn-light' : 'btn btn-dark'"
            @click="login = !login"
          >
            Register user
          </button>
        </div>
      </form>
    </div>
    <div v-else class="register-card">
      <!-- Register Heading -->
      <h1>Register</h1>

      <!-- Response -->
      <div class="register-response">
        {{ registerData.response }}
      </div>
      <form class="max-width-400" @submit.prevent="validateRegisterForm">
        <!-- Register Email -->
        <div class="mb-3">
          <label class="form-label"><b>Email address</b></label>
          <input
            id="registarEmail"
            v-model="registerData.email"
            type="email"
            class="form-control"
            aria-describedby="emailHelp"
            autocomplete="off"
          />
          <small>We'll never share your email with anyone else.</small>
        </div>

        <!-- Password Section -->
        <div class="mb-3">
          <label class="form-label"><b>Password</b></label>
          <input
            id="registerPassword"
            v-model="registerData.password"
            type="password"
            class="form-control"
            autocomplete="off"
          />
        </div>

        <!-- Full Name -->
        <div class="mb-3">
          <label class="form-label"><b>Full Name</b></label>
          <input
            id="registerFullname"
            v-model="registerData.fullname"
            class="form-control"
            autocomplete="off"
          />
        </div>

        <!-- Qualification -->
        <div class="mb-3">
          <label class="form-label"><b>Qualification</b></label>
          <input
            id="registerQualification"
            v-model="registerData.qualification"
            class="form-control"
            autocomplete="off"
          />
        </div>

        <!-- DOB -->
        <div class="mb-3">
          <label class="form-label"><b>Date OF B</b></label>
          <input
            id="registerDOB"
            v-model="registerData.DOB"
            type="date"
            class="form-control"
            autocomplete="off"
          />
        </div>
        <!-- Submit Button -->
        <div id="submit-button">
          <button
            type="submit"
            :class="theme.dark ? 'btn btn-light' : 'btn btn-dark'"
          >
            Submit
          </button>
        </div>
        <p>OR</p>
        <div class="s-button">
          <button
            v-if="login"
            :class="theme.dark ? 'btn btn-light' : 'btn btn-dark'"
            @click="login = !login"
          >
            Login
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { inject } from "vue";
import bgStars from "./Login/bgStars.vue";
import PaperPlane from "./Login/PaperPlane.vue";
import axios from "axios";
import Cookies from "js-cookie";

export default {
  components: {
    bgStars,
    PaperPlane,
  },
  emits: ["loggedIn"],
  setup() {
    const theme = inject("theme");

    return { theme };
  },
  data() {
    return {
      email: "",
      password: "",
      login: 0,
      response: "",
      registerData: {},
    };
  },
  methods: {
    async validateRegisterForm() {
      let passwordError = "";
      let emailError = "";
      let fullnameError = "";
      let qualificationError = "";
      let dobError = "";

      if (!this.registerData.fullname) {
        fullnameError = "fullname cannot be empty.";
      }
      if (!this.registerData.qualification) {
        qualificationError = "qualification cannot be empty.";
      }
      if (!this.registerData.DOB) {
        dobError = "DOB cannot be empty.";
      }

      if (!this.registerData.password) {
        passwordError = "Password cannot be empty.";
      } else if (this.password.length < 6) {
        passwordError = "Password must be at least 6 characters.";
      } else if (
        !/[A-Z]/.test(this.registerData.password) ||
        !/[0-9]/.test(this.registerData.password)
      ) {
        passwordError =
          "Password must contain at least one uppercase letter and one number.";
      }

      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!this.registerData.email) {
        emailError = "Email cannot be empty.";
      } else if (this.registerData.email.length < 5) {
        emailError = "Email is too short.";
      } else if (!emailRegex.test(this.registerData.email)) {
        emailError = "Invalid email format.";
      }
      if (emailError) {
        this.registerData.response = emailError;
        return;
      }
      if (passwordError) {
        this.registerData.response = passwordError;
        return;
      }
      if (fullnameError) {
        this.registerData.response = fullnameError;
        return;
      }
      if (qualificationError) {
        this.registerData.response = qualificationError;
        return;
      }
      if (dobError) {
        this.registerData.response = dobError;
        return;
      }

      if (!passwordError && !emailError && !fullnameError) {
        const response = await axios.post("http://127.0.0.1:5000/register", {
          email: this.registerData.email,
          password: this.registerData.password,
          qualification: this.registerData.qualification,
          fullname: this.registerData.fullname,
          dob: this.registerData.DOB,
        });
        this.registerData.response = response.data.message;
      }
    },
    async validateForm() {
      this.emailError = "";
      this.passwordError = "";

      // Email Validation
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!this.email) {
        this.emailError = "Email cannot be empty.";
      } else if (this.email.length < 5) {
        this.emailError = "Email is too short.";
      } else if (!emailRegex.test(this.email)) {
        this.emailError = "Invalid email format.";
      }

      // Password Validation
      if (!this.password) {
        this.passwordError = "Password cannot be empty.";
      } else if (this.password.length < 6) {
        this.passwordError = "Password must be at least 6 characters.";
      } else if (!/[A-Z]/.test(this.password) || !/[0-9]/.test(this.password)) {
        this.passwordError =
          "Password must contain at least one uppercase letter and one number.";
      }

      // Final check
      if (!this.emailError && !this.passwordError) {
        const response = await axios.post("http://127.0.0.1:5000/login", {
          email: this.email,
          password: this.password,
        });
        Cookies.set("access_token", response.data.access_token, {
          expires: 1, // 1 day expiry
          secure: true, // Only send over HTTPS
          sameSite: "Strict",
        });

        Cookies.set("is_admin", response.data.is_admin, {
          expires: 1,
          secure: true,
          sameSite: "Strict",
        });
        if (response.data.access_token) {
          this.$emit("LoggedIn");
        }

        this.response = response.data.error;
      }
    },
  },
};
</script>

<style scoped>
form {
  width: 50%;
}
.max-width-400 {
  max-width: 400px;
}
#submit-button {
  display: flex;
  align-items: center;
  justify-content: center;
}

.errors p {
  color: red;
  font-size: 0.9em;
  margin-top: 5px;
}

.login-card {
  border: 1px solid var(--text-color);
  border-radius: 2%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 1%;
  background-color: var(--bg-color);
  z-index: 2;
}

.register-card {
  border: 1px solid var(--text-color);
  border-radius: 2%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 1%;
  background-color: var(--bg-color);
  z-index: 2;
}
.login-page {
  height: 100vh;
  width: 100vw;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.or {
  width: 100%;
  display: flex;
  justify-content: center;
  margin: 10px 0;
  font-weight: bold;
}

p {
  display: flex;
  justify-content: center;
  font-weight: bold;
}
.s-button {
  display: flex;
  justify-content: center;
}

input {
  height: 20px;
}
</style>
