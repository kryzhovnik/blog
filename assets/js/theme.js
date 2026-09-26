(function() {
  const systemTheme = window.matchMedia('(prefers-color-scheme: dark)');
  let syncedComments;

  function applyTheme() {
    const theme = systemTheme.matches ? 'dark' : 'light';
    document.documentElement.dataset.theme = theme;

    const comments = document.querySelector('.giscus-frame');
    if (comments) {
      comments.contentWindow.postMessage({ giscus: { setConfig: { theme } } }, 'https://giscus.app');
    }

    const script = document.querySelector('script[data-giscus]');
    if (script) {
      script.dataset.theme = theme;
    }
  }

  // Apply the system theme before the stylesheet loads to avoid a light flash.
  applyTheme();
  systemTheme.addEventListener('change', applyTheme);

  document.addEventListener('DOMContentLoaded', function() {
    applyTheme();
    const script = document.querySelector('script[data-giscus]');
    if (script) {
      script.src = script.dataset.src;
    }
  });

  // Giscus can finish loading after the user changes the theme.
  window.addEventListener('message', function(event) {
    const comments = document.querySelector('.giscus-frame');
    if (event.origin === 'https://giscus.app' &&
        event.source === comments?.contentWindow && event.data?.giscus &&
        comments !== syncedComments) {
      syncedComments = comments;
      applyTheme();
    }
  });
})();
