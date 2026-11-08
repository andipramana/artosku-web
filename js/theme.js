/* Theme toggle. Default is always light; the visitor's choice is kept in localStorage (guarded). */
(function () {
  'use strict';
  var root = document.documentElement;
  var KEY = 'artosku-theme';
  var btn = document.getElementById('themeToggle');
  if (!btn) return;
  var isEn = root.lang === 'en';
  function label() {
    var dark = root.getAttribute('data-theme') === 'dark';
    var text = isEn ? (dark ? 'Switch to light theme' : 'Switch to dark theme') : (dark ? 'Ganti ke tema terang' : 'Ganti ke tema gelap');
    btn.setAttribute('aria-label', text);
    btn.setAttribute('title', text);
    btn.setAttribute('aria-pressed', dark ? 'true' : 'false');
  }
  label();
  btn.addEventListener('click', function () {
    var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    try { localStorage.setItem(KEY, next); } catch (e) { /* storage blocked: choice lasts for this page only */ }
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute('content', next === 'dark' ? '#131B11' : '#F6FAF3');
    label();
  });
})();
