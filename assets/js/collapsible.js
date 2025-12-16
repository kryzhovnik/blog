document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.collapsible-header').forEach(function(header) {
    header.addEventListener('click', function() {
      this.parentElement.classList.add('expanded');
    });
  });
});
