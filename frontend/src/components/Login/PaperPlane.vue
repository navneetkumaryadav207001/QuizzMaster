<template>
  <div ref="plane" @click="destroyPlane">➤</div>
</template>

<script>
import { inject, ref, onMounted, onUnmounted } from "vue";

export default {
  setup() {
    const theme = inject("theme");
    const plane = ref(null);
    const animationFrameId = ref(null); // Store animation frame ID

    return { theme, plane, animationFrameId };
  },
  mounted() {
    this.spawn();
  },
  beforeUnmount() {
    // Stop animation loop before component unmounts
    if (this.animationFrameId) {
      cancelAnimationFrame(this.animationFrameId);
    }

    // Remove plane trails
    document
      .querySelectorAll(".plane-trail")
      .forEach((trail) => trail.remove());
  },
  methods: {
    spawn() {
      const plane = this.plane;
      if (!plane) return;

      plane.style.pointerEvents = "auto";
      let x = window.innerWidth / 2;
      let y = 0;
      let currentAngle = Math.random() * 180;
      let targetAngle = currentAngle;
      const speed = 2;
      const turnSpeed = 1;

      setInterval(() => {
        targetAngle = Math.random() * 360;
      }, 2000);

      let lastTime = performance.now();
      let trailCounter = 0;

      this.planeMoving = true;

      const movePlane = () => {
        if (!this.planeMoving) return;

        const now = performance.now();
        const deltaTime = (now - lastTime) / 16.67;
        lastTime = now;

        const rect = plane.getBoundingClientRect();

        trailCounter += deltaTime;
        if (trailCounter >= 5) {
          const trail = document.createElement("div");
          trail.classList.add("plane-trail");
          trail.style.position = "fixed";
          trail.style.left = `${rect.left + rect.width / 2 - 4}px`;
          trail.style.top = `${rect.top + rect.height / 2 - 4}px`;
          trail.style.width = "8px";
          trail.style.height = "8px";
          trail.style.borderRadius = "50%";
          trail.style.backgroundColor = this.theme?.dark ? "white" : "black";
          trail.style.opacity = "1";
          trail.style.transition = "opacity 0.8s ease-out";
          document.body.appendChild(trail);

          setTimeout(() => (trail.style.opacity = "0"), 0);
          setTimeout(() => trail.remove(), 800);

          trailCounter = 0;
        }

        x += Math.cos((currentAngle * Math.PI) / 180) * speed * deltaTime;
        y += Math.sin((currentAngle * Math.PI) / 180) * speed * deltaTime;

        if (currentAngle < targetAngle) {
          currentAngle += turnSpeed * deltaTime;
          if (currentAngle > targetAngle) currentAngle = targetAngle;
        } else if (currentAngle > targetAngle) {
          currentAngle -= turnSpeed * deltaTime;
          if (currentAngle < targetAngle) currentAngle = targetAngle;
        }

        if (x < 0) x = window.innerWidth;
        if (x > window.innerWidth) x = 0;
        if (y < 0) y = window.innerHeight;
        if (y > window.innerHeight) y = 0;

        plane.style.transform = `translate(${x}px, ${y}px) rotate(${currentAngle}deg)`;

        this.animationFrameId = requestAnimationFrame(movePlane);
      };
      this.animationFrameId = requestAnimationFrame(movePlane);
    },

    destroyPlane() {
      this.planeMoving = false;

      const plane = this.plane;
      const rect = plane.getBoundingClientRect();
      const numBlocks = 20;

      for (let i = 0; i < numBlocks; i++) {
        const block = document.createElement("div");
        block.style.position = "fixed";
        block.style.left = `${rect.left + rect.width / 2}px`;
        block.style.top = `${rect.top + rect.height / 2}px`;
        block.style.width = "10px";
        block.style.height = "10px";
        block.style.backgroundColor = this.theme?.dark ? "white" : "black";
        block.style.opacity = "1";
        block.style.transition = "transform 0.5s ease-out, opacity 0.5s";
        document.body.appendChild(block);

        const angle = Math.random() * 360;
        const distance = Math.random() * 100 + 20;
        const dx = Math.cos((angle * Math.PI) / 180) * distance;
        const dy = Math.sin((angle * Math.PI) / 180) * distance;

        plane.style.pointerEvents = "none";

        setTimeout(() => {
          block.style.transform = `translate(${dx}px, ${dy}px) rotate(${
            Math.random() * 360
          }deg)`;
          block.style.opacity = "0";
        }, 0);

        setTimeout(() => block.remove(), 500);
      }

      plane.style.opacity = 0;

      document
        .querySelectorAll(".plane-trail")
        .forEach((trail) => trail.remove());

      setTimeout(() => {
        plane.style.transition = "none";
        plane.style.opacity = 1;
        plane.style.transform = "translate(0, 0) rotate(0deg)";

        this.spawn();
      }, 500);
    },
  },
};
</script>

<style scoped>
img {
  height: 50px;
  transform: rotate(90deg);
}
div {
  position: fixed;
  left: 0;
  top: 0;
  font-size: 30px;
  transform-origin: center center;
  width: fit-content;
  height: fit-content;
  z-index: 1;
  cursor: pointer;
}
</style>
