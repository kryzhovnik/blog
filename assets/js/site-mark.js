// Morph the header mark from the shape this tab showed last:
// the home page asterisk turns into the arrow on other pages, and back.
(function() {
  const root = document.documentElement;
  const shape = root.dataset.siteMark;
  const key = 'siteMark';

  function remember() {
    try {
      sessionStorage.setItem(key, shape);
    } catch (e) {}
  }

  let previous = null;
  try {
    previous = sessionStorage.getItem(key);
  } catch (e) {}
  remember();

  // A page restored from the back/forward cache still shows its own shape.
  window.addEventListener('pageshow', function(event) {
    if (event.persisted) remember();
  });

  if (!previous || previous === shape) return;

  // Paint the previous shape first, then switch so the CSS transition runs.
  root.dataset.siteMark = previous;
  document.addEventListener('DOMContentLoaded', function() {
    requestAnimationFrame(function() {
      requestAnimationFrame(function() {
        root.dataset.siteMark = shape;
      });
    });
  });
})();
