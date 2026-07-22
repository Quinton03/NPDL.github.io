(function () {
  function setOpen(fold, panel, btn, open) {
    fold.classList.toggle('is-open', open);
    if (panel) {
      panel.classList.toggle('is-open', open);
      panel.hidden = !open;
    }
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    var label = fold.querySelector('.spine-title');
    var name = label ? label.textContent.trim() : 'section';
    btn.setAttribute('aria-label', (open ? 'Collapse ' : 'Expand ') + name);
  }

  document.querySelectorAll('.fold-toggle').forEach(function (btn) {
    var fold = btn.closest('.fold');
    var panelId = btn.getAttribute('aria-controls');
    var panel = panelId ? document.getElementById(panelId) : null;
    var startOpen = fold && fold.classList.contains('is-open');
    if (panel) setOpen(fold, panel, btn, !!startOpen);

    btn.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      if (!fold) return;
      var open = !fold.classList.contains('is-open');
      setOpen(fold, panel, btn, open);
    });
  });
})();
