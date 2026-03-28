// Category filter for the homepage recipe grid
(function() {
  document.addEventListener('DOMContentLoaded', function() {
    var filterBar = document.getElementById('filter-bar');
    var grid = document.getElementById('recipe-grid');
    var countEl = document.getElementById('recipe-count');

    if (!filterBar || !grid) return;

    var buttons = filterBar.querySelectorAll('.filter-btn');
    var cards = grid.querySelectorAll('.recipe-card');
    var totalCount = cards.length;

    // Update the count display
    function updateCount(shown, category) {
      if (category === 'all') {
        countEl.innerHTML = 'Showing all <strong>' + totalCount + '</strong> recipes';
      } else {
        var label = filterBar.querySelector('[data-filter="' + category + '"]');
        var catName = label ? label.textContent.trim() : category;
        countEl.innerHTML = 'Showing <strong>' + shown + '</strong> ' + catName + ' recipe' + (shown !== 1 ? 's' : '');
      }
    }

    // Filter cards
    function filterCards(category) {
      var visibleCount = 0;
      var delay = 0;

      cards.forEach(function(card) {
        if (category === 'all' || card.getAttribute('data-category') === category) {
          card.style.display = '';
          // Re-trigger entrance animation
          card.style.animation = 'none';
          card.offsetHeight; // trigger reflow
          card.style.animation = 'cardFadeIn 0.5s var(--ease-out) ' + delay + 's both';
          delay += 0.025;
          visibleCount++;
        } else {
          card.style.display = 'none';
        }
      });

      updateCount(visibleCount, category);
    }

    // Button click handlers
    buttons.forEach(function(btn) {
      btn.addEventListener('click', function() {
        // Update active state
        buttons.forEach(function(b) { b.classList.remove('active'); });
        btn.classList.add('active');

        // Filter
        filterCards(btn.getAttribute('data-filter'));
      });
    });

    // Initialize with the count
    updateCount(totalCount, 'all');
  });
})();
