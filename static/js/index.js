const left = document.getElementById("left-side");
let isAnimating = false; // Prevents multiple triggers during animation

const handleOnMove = e => {
  if (isAnimating) return; // Block interaction during animation

  const p = (e.clientX / window.innerWidth) * 100;

  if (p <= 20) {
    // Automatically animate the rest of the swipe to 0%
    isAnimating = true;
    left.style.transition = "width 0.5s ease"; // Smooth animation
    left.style.width = `0%`;

    // Disable swiping after animation
    setTimeout(() => {
      document.onmousemove = null;
      document.ontouchmove = null;
    }, 500); // Match the duration of the CSS transition
  } else {
    // Allow swiping until halfway
    left.style.transition = ""; // Reset transition for smooth user interaction
    left.style.width = `${p}%`;
  }
};

const startMove = () => {
  left.style.width = "100%"; // Start with the left side covering the screen
  document.onmousemove = e => handleOnMove(e);
  document.ontouchmove = e => handleOnMove(e.touches[0]);
};

// Initialize the swiping behavior
startMove();
