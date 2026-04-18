// 1. Create and inject the animation styles
const style = document.createElement('style');
style.innerHTML = `
  @keyframes highlightPulse {
    0% { outline: 5px solid red; outline-offset: 0px; }
    50% { outline: 15px solid rgba(255, 0, 0, 0.5); outline-offset: 10px; }
    100% { outline: 5px solid red; outline-offset: 0px; }
  }
  .missing-alt-highlight {
    animation: highlightPulse 1.5s infinite ease-in-out !important;
    position: relative;
    z-index: 9999;
  }
`;
document.head.appendChild(style);

// 2. Select images missing the attribute and apply the class
const images = document.querySelectorAll('img:not([alt])');
images.forEach(img => img.classList.add('missing-alt-highlight'));

console.log(`Found and highlighted ${images.length} images.`);
