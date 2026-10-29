(() => {
  "use strict";
  // ---- tombol tema: awal mengikuti sistem (skrip di <head>), pilihan user disimpan ----
  const tt = document.getElementById("themeToggle");
  if (tt) tt.addEventListener("click", () => {
    const next = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    try { localStorage.setItem("tut-theme", next); } catch (e) {}
  });
})();
(() => {
  "use strict";
  // Pencarian Buku Panduan (rancangan: menyaring kartu di halaman; versi final memakai data JSON dari generator).
  const input = document.getElementById("tutQ");
  const status = document.getElementById("tutStatus");
  const empty = document.getElementById("tutEmpty");
  const start = document.getElementById("mulai"), toc = document.getElementById("tutToc");
  if (!input) return;
  const cards = [...document.querySelectorAll(".tut-card")];
  const groups = [...document.querySelectorAll(".tut-group")];
  const isEn = document.documentElement.lang === "en";

  const norm = (s) => s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
  // toleran salah ketik ringan: jarak edit <= 1 untuk kata >= 5 huruf
  const near = (a, b) => {
    if (Math.abs(a.length - b.length) > 1 || a.length < 5) return false;
    let i = 0, j = 0, miss = 0;
    while (i < a.length && j < b.length) {
      if (a[i] === b[j]) { i++; j++; continue; }
      if (++miss > 1) return false;
      if (a.length > b.length) i++; else if (a.length < b.length) j++; else { i++; j++; }
    }
    return miss + (a.length - i) + (b.length - j) <= 1;
  };
  const words = (s) => norm(s).split(/[^a-z0-9]+/).filter(Boolean);

  const score = (card, terms) => {
    const title = norm(card.dataset.title), kw = norm(card.dataset.keywords), body = norm(card.textContent);
    const kwWords = words(card.dataset.keywords + " " + card.dataset.title);
    let total = 0;
    for (const t of terms) {
      let s = 0;
      if (title.includes(t)) s = 6;
      else if (kw.includes(t)) s = 4;
      else if (body.includes(t)) s = 2;
      else if (kwWords.some((w) => near(t, w))) s = 1;
      if (!s) return 0;
      total += s;
    }
    return total;
  };

  const run = () => {
    const q = input.value.trim();
    const terms = words(q);
    if (!terms.length) {
      cards.forEach((c) => { c.hidden = false; c.style.order = ""; });
      groups.forEach((g) => (g.hidden = false));
      if (start) start.hidden = false; if (toc) toc.hidden = false;
      empty.classList.remove("is-on");
      status.textContent = "";
      return;
    }
    let shown = 0;
    cards.forEach((c) => {
      const s = score(c, terms);
      c.hidden = s === 0;
      c.style.order = String(-s);
      if (s) shown++;
    });
    groups.forEach((g) => (g.hidden = ![...g.querySelectorAll(".tut-card")].some((c) => !c.hidden)));
    if (start) start.hidden = true; if (toc) toc.hidden = true;
    empty.classList.toggle("is-on", shown === 0);
    status.textContent = shown
      ? (isEn ? shown + " guide(s) found" : shown + " panduan ditemukan")
      : "";
  };

  const params = new URLSearchParams(location.search);
  if (params.get("q")) input.value = params.get("q");
  input.addEventListener("input", run);
  run();
})();
