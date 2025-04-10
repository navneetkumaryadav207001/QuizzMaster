<script>
import { inject, watch, onUnmounted } from "vue";

export default {
  setup() {
    const theme = inject("theme");

    let starInterval;
    let timeoutIds = [];
    let animationIds = [];

    const createStar = () => {
      const x = Math.random() * window.innerWidth;
      const y = Math.random() * window.innerHeight;
      const size = 10;

      const star = document.createElement("div");
      star.classList.add("star");
      star.style.position = "fixed";
      star.style.left = `${x}px`;
      star.style.top = `${y}px`;
      star.textContent = "*";
      star.style.width = `${size}px`;
      star.style.height = `${size}px`;
      star.style.color = "white";
      star.style.borderRadius = "50%";
      star.style.opacity = "0";

      document.body.appendChild(star);

      // Twinkle animation setup
      let opacity = 0;
      let growing = true;
      let isTwinkling = true;

      const twinkle = () => {
        if (!isTwinkling) return;

        if (growing) {
          opacity += 0.02;
          if (opacity >= 1) growing = false;
        } else {
          opacity -= 0.01;
          if (opacity <= 0.2) growing = true;
        }

        star.style.opacity = opacity;
        const animId = requestAnimationFrame(twinkle);
        animationIds.push(animId);
      };

      twinkle();

      // Remove star after 3 seconds
      const removeTimeout = setTimeout(() => {
        isTwinkling = false;
        star.remove();
      }, 3000);

      timeoutIds.push(removeTimeout);
    };

    const startStarLoop = () => {
      starInterval = setInterval(() => createStar(), 100);
    };

    const stopStars = () => {
      // Clear any pending stars and running animations
      timeoutIds.forEach(clearTimeout);
      animationIds.forEach(cancelAnimationFrame);
      clearInterval(starInterval);
      timeoutIds = [];
      animationIds = [];

      // Remove all visible stars
      document.querySelectorAll(".star").forEach((star) => star.remove());
    };

    // Watch theme change to restart the stars
    watch(theme, (newTheme) => {
      stopStars();
      if (newTheme.dark) startStarLoop();
    });

    // Cleanup when component unmounts
    onUnmounted(() => stopStars());

    // If the theme starts dark, spawn stars immediately
    if (theme.dark) startStarLoop();

    return { theme };
  },
};
</script>
