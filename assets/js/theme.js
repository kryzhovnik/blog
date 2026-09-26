(function() {
  const storageKey = 'theme';
  const systemTheme = window.matchMedia('(prefers-color-scheme: dark)');
  let preference = readPreference();
  let syncedComments;

  function readPreference() {
    try {
      const saved = localStorage.getItem(storageKey);
      return saved === 'light' || saved === 'dark' ? saved : 'system';
    } catch {
      return 'system';
    }
  }

  function applyTheme() {
    const theme = preference === 'system'
      ? (systemTheme.matches ? 'dark' : 'light')
      : preference;
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

  // Apply the saved theme before the stylesheet loads to avoid a light flash.
  applyTheme();
  systemTheme.addEventListener('change', applyTheme);

  document.addEventListener('DOMContentLoaded', function() {
    const switcher = document.querySelector('.theme-switcher');
    const buttons = switcher.querySelectorAll('[data-theme-choice]');

    function updateButtons() {
      buttons.forEach(function(button) {
        button.setAttribute('aria-pressed', String(button.dataset.themeChoice === preference));
      });
    }

    updateButtons();
    switcher.hidden = false;
    switcher.addEventListener('click', function(event) {
      const button = event.target.closest('[data-theme-choice]');
      if (!button) return;
      preference = button.dataset.themeChoice;
      try {
        if (preference === 'system') {
          localStorage.removeItem(storageKey);
        } else {
          localStorage.setItem(storageKey, preference);
        }
      } catch {
        // The selector still works when browser storage is unavailable.
      }
      applyTheme();
      updateButtons();
    });

    window.addEventListener('storage', function(event) {
      if (event.key === storageKey || event.key === null) {
        preference = readPreference();
        applyTheme();
        updateButtons();
      }
    });

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
