(function () {
  var mosaic = document.getElementById('photo-mosaic');
  if (!mosaic) return;

  var cells = Array.prototype.slice.call(mosaic.querySelectorAll('.mosaic__cell'));
  if (!cells.length) return;

  var GAP = 32;
  var raf = null;

  function columnsFor(width) {
    if (width < 640) return [1];
    if (width < 960) return [0.44, 0.56];
    // Uneven columns → same aspect ratios get different heights → no visual rows
    return [0.30, 0.40, 0.30];
  }

  function layout() {
    var totalW = mosaic.clientWidth;
    if (!totalW) return;

    var fracs = columnsFor(totalW);
    var n = fracs.length;
    var usable = totalW - GAP * (n - 1);
    var colW = [];
    var colX = [];
    var colH = [];
    var x = 0;
    var i;

    for (i = 0; i < n; i++) {
      colW[i] = Math.floor(usable * fracs[i]);
      colX[i] = x;
      colH[i] = 0;
      x += colW[i] + GAP;
    }
    // Absorb rounding remainder into the last column
    colW[n - 1] += totalW - (x - GAP);

    for (i = 0; i < cells.length; i++) {
      var cell = cells[i];
      var img = cell.querySelector('img');
      if (!img || !img.naturalWidth) continue;

      // Prefer the shortest column; portraits bias toward the narrower ones
      var portrait = img.naturalHeight > img.naturalWidth * 1.05;
      var col = 0;
      for (var c = 1; c < n; c++) {
        if (colH[c] < colH[col]) col = c;
      }
      if (portrait && n > 1) {
        // Pick the shortest among the narrower columns
        var best = col;
        for (c = 0; c < n; c++) {
          if (colW[c] <= colW[best] && colH[c] <= colH[best] + 80) best = c;
        }
        col = best;
      }

      var w = colW[col];
      var h = Math.round(w * (img.naturalHeight / img.naturalWidth));

      cell.style.position = 'absolute';
      cell.style.width = w + 'px';
      cell.style.left = colX[col] + 'px';
      cell.style.top = colH[col] + 'px';
      cell.style.margin = '0';

      colH[col] += h + GAP;
    }

    var maxH = 0;
    for (i = 0; i < n; i++) {
      if (colH[i] > maxH) maxH = colH[i];
    }
    mosaic.style.height = Math.max(0, maxH - GAP) + 'px';
    mosaic.classList.add('is-packed');
  }

  function schedule() {
    if (raf != null) cancelAnimationFrame(raf);
    raf = requestAnimationFrame(function () {
      raf = null;
      layout();
    });
  }

  function whenReady() {
    var pending = cells.length;
    function done() {
      pending -= 1;
      if (pending <= 0) schedule();
    }
    cells.forEach(function (cell) {
      var img = cell.querySelector('img');
      if (!img) { done(); return; }
      if (img.complete && img.naturalWidth) done();
      else {
        img.addEventListener('load', done, { once: true });
        img.addEventListener('error', done, { once: true });
      }
    });
  }

  whenReady();
  window.addEventListener('resize', schedule);
})();
