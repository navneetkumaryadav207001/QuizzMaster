module.exports = {
  env: {
    browser: true,
    es2021: true,
  },
  extends: [
    "eslint:recommended",
    "plugin:vue/vue3-recommended", // If using Vue
  ],
  parserOptions: {
    ecmaVersion: 2021,
    sourceType: "module", // This line ensures ES module parsing
  },
  rules: {
    "no-unused-vars": "warn",
    semi: ["error", "always"],
    quotes: ["error", "double"],
  },
};
