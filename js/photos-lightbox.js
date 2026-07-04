(function () {
  var figures = document.querySelectorAll('.gallery figure');
  if (!figures.length) return;

  var items = Array.prototype.map.call(figures, function (fig) {
    var img = fig.querySelector('img');
    var cap = fig.querySelector('figcaption');
    return {
      src: img.getAttribute('src'),
      alt: img.getAttribute('alt') || '',
      caption: cap ? cap.textContent : ''
    };
  });

  var current = 0;
  var lastFocus = null;

  var dialog = document.createElement('dialog');
  dialog.className = 'lightbox';
  dialog.setAttribute('aria-label', 'Expanded photo');

  var frame = document.createElement('div');
  frame.className = 'lightbox__frame';

  var closeBtn = document.createElement('button');
  closeBtn.type = 'button';
  closeBtn.className = 'lightbox__close';
  closeBtn.setAttribute('aria-label', 'Close');
  closeBtn.textContent = '\u00d7';

  var prevBtn = document.createElement('button');
  prevBtn.type = 'button';
  prevBtn.className = 'lightbox__nav lightbox__prev';
  prevBtn.setAttribute('aria-label', 'Previous photo');
  prevBtn.textContent = '\u2039';

  var nextBtn = document.createElement('button');
  nextBtn.type = 'button';
  nextBtn.className = 'lightbox__nav lightbox__next';
  nextBtn.setAttribute('aria-label', 'Next photo');
  nextBtn.textContent = '\u203a';

  var figure = document.createElement('figure');
  figure.className = 'lightbox__figure';

  var imgEl = document.createElement('img');
  imgEl.className = 'lightbox__img';

  var capEl = document.createElement('figcaption');
  capEl.className = 'lightbox__cap';

  figure.appendChild(imgEl);
  figure.appendChild(capEl);
  frame.appendChild(closeBtn);
  frame.appendChild(prevBtn);
  frame.appendChild(figure);
  frame.appendChild(nextBtn);
  dialog.appendChild(frame);
  document.body.appendChild(dialog);

  function show(index) {
    current = (index + items.length) % items.length;
    var item = items[current];
    imgEl.src = item.src;
    imgEl.alt = item.alt;
    capEl.textContent = item.caption;
    prevBtn.disabled = items.length < 2;
    nextBtn.disabled = items.length < 2;
  }

  function open(index) {
    lastFocus = document.activeElement;
    show(index);
    dialog.showModal();
    closeBtn.focus();
  }

  function close() {
    dialog.close();
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  function step(delta) {
    show(current + delta);
  }

  Array.prototype.forEach.call(figures, function (fig, index) {
    var img = fig.querySelector('img');
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'gallery-open';
    btn.setAttribute('aria-label', 'View larger: ' + (img.getAttribute('alt') || 'photo'));
    img.parentNode.insertBefore(btn, img);
    btn.appendChild(img);
    btn.addEventListener('click', function () { open(index); });
  });

  closeBtn.addEventListener('click', close);
  prevBtn.addEventListener('click', function () { step(-1); });
  nextBtn.addEventListener('click', function () { step(1); });

  dialog.addEventListener('click', function (e) {
    if (e.target === dialog) close();
  });

  dialog.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft') { e.preventDefault(); step(-1); }
    if (e.key === 'ArrowRight') { e.preventDefault(); step(1); }
  });
})();
