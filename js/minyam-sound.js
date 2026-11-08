/* Minyam chatter, same rule as the app (MaskotSounds.chatter): random clip out of 16, never the same clip twice in a row,
   volume 0.8. Clips load lazily on the first tap, play only after a tap, never autoplay. Mute choice kept in localStorage (guarded). */
(function () {
  'use strict';
  var CLIPS = 16, VOLUME = 0.8, KEY = 'artosku-minyam-mute';
  var body = document.body;
  var base = (body.getAttribute('data-asset') || '') + 'assets/minyam/sfx/';
  var isEn = document.documentElement.lang === 'en';
  var muted = false;
  try { muted = localStorage.getItem(KEY) === '1'; } catch (e) { muted = false; }
  var last = -1, current = null, ext = null;

  function pickExt() {
    if (ext) return ext;
    var a = document.createElement('audio');
    var ok = a.canPlayType && a.canPlayType('audio/mp4; codecs="mp4a.40.2"');
    ext = ok ? 'm4a' : 'mp3';
    return ext;
  }
  function chatter() {
    if (muted) return;
    var n = Math.floor(Math.random() * CLIPS);
    if (n === last) n = (n + 1) % CLIPS;
    last = n;
    try {
      if (current) { current.pause(); }
      var a = new Audio(base + 'chat_' + (n < 9 ? '0' : '') + (n + 1) + '.' + pickExt());
      a.volume = VOLUME;
      current = a;
      var pr = a.play();
      if (pr && pr.catch) pr.catch(function () {
        // m4a refused on this browser: retry once with the mp3 copy
        if (ext === 'm4a') { ext = 'mp3'; var b = new Audio(base + 'chat_' + (n < 9 ? '0' : '') + (n + 1) + '.mp3'); b.volume = VOLUME; current = b; b.play().catch(function () {}); }
      });
    } catch (e) { /* no audio support: stay silent */ }
  }
  window.MinyamSound = { chatter: chatter };

  // every element marked data-minyam-tap makes the sound when tapped (the page script handles the animation)
  document.addEventListener('click', function (ev) {
    var t = ev.target && ev.target.closest ? ev.target.closest('[data-minyam-tap]') : null;
    if (t) chatter();
  });

  // mute buttons (one or more) are marked data-minyam-mute
  function paint(btn) {
    var txt = isEn ? (muted ? 'Turn Minyam sound on' : 'Mute Minyam sound') : (muted ? 'Nyalakan bunyi Minyam' : 'Matikan bunyi Minyam');
    btn.setAttribute('aria-label', txt);
    btn.setAttribute('title', txt);
    btn.setAttribute('aria-pressed', muted ? 'true' : 'false');
  }
  var btns = Array.prototype.slice.call(document.querySelectorAll('[data-minyam-mute]'));
  btns.forEach(function (b) {
    paint(b);
    b.addEventListener('click', function () {
      muted = !muted;
      try { localStorage.setItem(KEY, muted ? '1' : '0'); } catch (e) { /* ignore */ }
      btns.forEach(paint);
    });
  });
})();
