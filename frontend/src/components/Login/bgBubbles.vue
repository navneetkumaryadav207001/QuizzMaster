<script>
import { inject, watch, onUnmounted, onMounted } from "vue";

export default {
  setup() {
    const theme = inject("theme");

    let starInterval;
    let timeoutIds = [];
    let animationIds = [];

    // Function to create a star
    const createStar = () => {
      const x = Math.random() * window.innerWidth;
      const y = Math.random() * window.innerHeight;
      let size = 5; // Start small
      const maxSize = 15; // Max size to grow

      const star = document.createElement("div");
      star.classList.add("star");
      star.style.position = "fixed";
      star.style.left = `${x}px`;
      star.style.top = `${y}px`;
      star.textContent = "🔘";

      star.style.width = `${size}px`;
      star.style.height = `${size}px`;
      star.style.opacity = "1"; // Fully visible
      document.body.appendChild(star);

      // Grow effect
      const growStar = () => {
        if (size < maxSize) {
          size += 0.2;
          star.style.fontSize = `${size}px`;
          const animId = requestAnimationFrame(growStar);
          animationIds.push(animId);
        }
      };

      growStar(); // Start the growth animation

      // Remove star after 3 seconds
      const removeTimeout = setTimeout(() => {
        star.remove();
      }, 1500);
      timeoutIds.push(removeTimeout);
    };

    // Function to start spawning stars
    const startStarLoop = () => {
      starInterval = setInterval(() => createStar(), 500);
    };

    // Function to stop stars and clear animations
    const stopStars = () => {
      timeoutIds.forEach(clearTimeout);
      animationIds.forEach(cancelAnimationFrame);
      clearInterval(starInterval);
      timeoutIds = [];
      animationIds = [];

      // Remove all stars
      document.querySelectorAll(".star").forEach((star) => star.remove());
    };

    // Start stars on mount if theme is light
    onMounted(() => {
      if (!theme.dark) startStarLoop();
    });

    // Watch for theme changes
    watch(theme, (newTheme) => {
      stopStars();
      if (!newTheme.dark) startStarLoop();
    });

    // Cleanup on unmount
    onUnmounted(() => stopStars());

    return {}; // No need to return anything for rendering
  },
};
</script>

<style scoped></style>
