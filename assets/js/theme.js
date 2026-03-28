// Theme toggle — persists preference in localStorage
(function() {
  var STORAGE_KEY = 'cookbook-theme';
  var saved = localStorage.getItem(STORAGE_KEY);

  // Apply saved preference immediately (before paint) to prevent flash
  if (saved === 'dark') {
    document.documentElement.setAttribute('data-theme', 'dark');
  }

  document.addEventListener('DOMContentLoaded', function() {
    // Create toggle button
    var btn = document.createElement('button');
    btn.className = 'theme-toggle';
    btn.setAttribute('aria-label', 'Toggle dark mode');
    btn.setAttribute('title', 'Toggle dark mode');
    btn.innerHTML = '<span class="icon-moon">🌙</span><span class="icon-sun">☀️</span>';
    document.body.appendChild(btn);

    btn.addEventListener('click', function() {
      var isDark = document.documentElement.getAttribute('data-theme') === 'dark';
      if (isDark) {
        document.documentElement.removeAttribute('data-theme');
        localStorage.setItem(STORAGE_KEY, 'light');
      } else {
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem(STORAGE_KEY, 'dark');
      }
    });
  });
})();
