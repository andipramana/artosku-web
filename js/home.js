/* Landing page behaviour. No libraries, no network calls. The demo parses text in the browser only. */
(function () {
  'use strict';
  var body = document.body;
  var LANG = body.getAttribute('data-lang') === 'en' ? 'en' : 'id';
  var ASSET = body.getAttribute('data-asset') || '';
  var REDUCED = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var src = function (name) { return ASSET + 'assets/minyam/' + name + '.webp'; };

  var T = {
    id: {
      bubbles: ['Hai, aku Minyam. Ketuk aku.', 'Aku ikut mencatat uangmu.', 'Coba kolom "Coba sendiri" di bawah.', 'Catat tiap hari, ya.', 'Aku suka matcha. Kamu?'],
      samples: ['makan siang 25 ribu pakai gopay', 'gaji masuk 6,5 jt ke bca', 'bensin 50rb tunai', 'kopi 18k ovo'],
      income: 'Pemasukan', expense: 'Pengeluaran', today: 'Hari ini', cash: 'Tunai', other: 'Lainnya', saved: 'Sudah dicatat hari ini',
      noAmount: 'Belum ada nominalnya. Tulis jumlahnya, misalnya 25 ribu.', count: '{n} fitur'
    },
    en: {
      bubbles: ['Hi, I am Minyam. Tap me.', 'I help you log your money.', 'Try the "Try it yourself" box below.', 'Log a little every day.', 'I like matcha. Do you?'],
      samples: ['lunch 25k with gopay', 'salary 6.5m into bca', 'fuel 50k cash', 'coffee 18k ovo'],
      income: 'Income', expense: 'Expense', today: 'Today', cash: 'Cash', other: 'Other', saved: 'Logged today',
      noAmount: 'No amount yet. Write one, for example 25k.', count: '{n} features'
    }
  }[LANG];

  var CATS = {
    id: [['Gaji', /gaji|bonus|thr/], ['Makan', /makan|kopi|jajan|sarapan|minum|resto|nasi|bakso|warung|snack/], ['Transport', /bensin|ojek|grab|gojek|parkir|tol|bus|kereta|angkot|taksi/],
      ['Belanja', /belanja|beli|baju|minimarket|sepatu|skincare/], ['Tagihan', /listrik|pulsa|internet|wifi|tagihan|cicilan|kos|sewa|air pdam/],
      ['Hiburan', /nonton|film|game|bioskop|netflix|spotify|konser/], ['Kesehatan', /obat|dokter|apotek|klinik|vitamin/]],
    en: [['Salary', /salary|bonus|payday/], ['Food', /lunch|dinner|breakfast|coffee|food|snack|eat|meal|restaurant|drink/], ['Transport', /fuel|gas|taxi|grab|gojek|parking|toll|bus|train|ride/],
      ['Shopping', /shop|buy|groceries|clothes|shoes|skincare/], ['Bills', /electric|bill|internet|wifi|rent|installment|phone credit/],
      ['Entertainment', /movie|film|game|cinema|netflix|spotify|concert/], ['Health', /medicine|doctor|pharmacy|clinic|vitamin/]]
  }[LANG];
  var INCOME = /gaji|bonus|terima|dapat|masuk|thr|refund|salary|received|got paid|income|payday/;
  var WALLETS = [['GoPay', /gopay/], ['OVO', /\bovo\b/], ['DANA', /\bdana\b/], ['ShopeePay', /shopee ?pay/], ['BCA', /\bbca\b/], ['BNI', /\bbni\b/], ['BRI', /\bbri\b/],
    ['Mandiri', /mandiri/], ['Jago', /\bjago\b/], [T.cash, /tunai|cash/]];

  /* ---------- mascot (blink by swapping real renders) ---------- */
  ['blink', 'joy', 'wait', 'squash'].forEach(function (n) { var i = new Image(); i.src = src(n); });
  function blinker(img) {
    if (REDUCED || !img) return;
    (function loop() {
      setTimeout(function () {
        if (img.dataset.lock !== '1' && img.dataset.worn !== '1') {
          img.src = src('blink');
          setTimeout(function () { if (img.dataset.lock !== '1' && img.dataset.worn !== '1') img.src = src('idle'); }, 140);
        }
        loop();
      }, 2600 + Math.random() * 2600);
    })();
  }
  function react(img, pose, ms) {
    if (!img) return;
    img.dataset.lock = '1';
    img.src = src(pose);
    clearTimeout(img._t);
    img._t = setTimeout(function () { img.dataset.lock = '0'; img.src = src('idle'); }, ms || 1100);
  }

  /* hero */
  var heroBtn = $('#heroMascot'), heroImg = $('#heroMascotImg'), bubble = $('#heroBubble'), bi = 0;
  blinker(heroImg);
  if (heroBtn) heroBtn.addEventListener('click', function () {
    bi = (bi + 1) % T.bubbles.length;
    bubble.textContent = T.bubbles[bi];
    heroBtn.classList.remove('jump'); void heroBtn.offsetWidth; heroBtn.classList.add('jump');
    react(heroImg, bi % 2 ? 'joy' : 'squash', 900);
  });

  /* ---------- try it ---------- */
  var form = $('#tryForm'), input = $('#tryInput'), chipBox = $('#tryChips'), tryImg = $('#tryMascotImg');
  var box = $('#tryResult'), empty = $('#tryEmpty'), tbody = $('#tryBody');
  blinker(tryImg);
  var money = function (n) { return 'Rp' + Math.round(n).toLocaleString(LANG === 'id' ? 'id-ID' : 'en-US'); };

  function parseAmount(s) {
    var re = /(\d+(?:[.,]\d+)*)\s*(juta|jt|million|mil|m|ribu|rb|thousand|k)?(?![a-z])/gi, m, first = null, withUnit = null;
    while ((m = re.exec(s))) {
      var raw = m[1], v;
      if (/^\d{1,3}([.,]\d{3})+$/.test(raw)) v = parseFloat(raw.replace(/[.,]/g, ''));
      else v = parseFloat(raw.replace(',', '.'));
      if (isNaN(v)) continue;
      var u = (m[2] || '').toLowerCase(), mult = 1;
      if (/^(juta|jt|million|mil|m)$/.test(u)) mult = 1e6; else if (u) mult = 1e3;
      var hit = { value: v * mult, text: m[0] };
      if (!first) first = hit;
      if (u && !withUnit) withUnit = hit;
    }
    return withUnit || first;
  }
  function analyse(text) {
    var low = text.toLowerCase(), amt = parseAmount(low);
    if (!amt) return null;
    var wallet = T.cash, wtext = '';
    for (var i = 0; i < WALLETS.length; i++) { var wm = low.match(WALLETS[i][1]); if (wm) { wallet = WALLETS[i][0]; wtext = wm[0]; break; } }
    var cat = T.other;
    for (var j = 0; j < CATS.length; j++) if (CATS[j][1].test(low)) { cat = CATS[j][0]; break; }
    var income = INCOME.test(low);
    if (income && cat === T.other) cat = LANG === 'id' ? 'Gaji' : 'Salary';
    var name = low.replace(amt.text, ' ');
    if (wtext) name = name.replace(new RegExp('\\b(pakai|via|dengan|with|using|into|from|ke|dari)?\\s*' + wtext.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')), ' ');
    name = name.replace(/\b(masuk|received|rp|idr)\b/g, ' ').replace(/\s+/g, ' ').trim();
    if (!name) name = cat;
    name = name.charAt(0).toUpperCase() + name.slice(1);
    return { name: name, amount: amt.value, cat: cat, wallet: wallet, income: income };
  }
  function show(text) {
    var r = analyse(text);
    if (!r) {
      box.classList.remove('run'); tbody.hidden = true; empty.hidden = false; empty.textContent = T.noAmount;
      react(tryImg, 'wait', 1600); return;
    }
    empty.hidden = true; tbody.hidden = false;
    $('#trName').textContent = r.name;
    $('#trAmount').textContent = (r.income ? '+' : '-') + money(r.amount);
    $('#trAmount').className = r.income ? 'in' : '';
    $('#trType').textContent = r.income ? T.income : T.expense;
    $('#trCat').textContent = r.cat;
    $('#trWallet').textContent = r.wallet;
    $('#trDate').textContent = T.today;
    box.classList.remove('run'); void box.offsetWidth; box.classList.add('run');
    react(tryImg, 'joy', 1100);
  }
  T.samples.forEach(function (s) {
    var b = document.createElement('button');
    b.type = 'button'; b.className = 'chip'; b.textContent = s;
    b.addEventListener('click', function () { input.value = s; show(s); });
    chipBox.appendChild(b);
  });
  if (input && T.samples.length) { input.value = T.samples[0]; show(T.samples[0]); }
  if (form) form.addEventListener('submit', function (e) { e.preventDefault(); if (input.value.trim()) show(input.value.trim()); });

  /* ---------- ways to log (tabs) ---------- */
  var tabs = $$('.tabs [role="tab"]');
  function pick(tab, focus) {
    tabs.forEach(function (t) {
      var on = t === tab;
      t.setAttribute('aria-selected', on ? 'true' : 'false');
      t.tabIndex = on ? 0 : -1;
      $('#' + t.getAttribute('aria-controls')).hidden = !on;
    });
    if (focus) tab.focus();
  }
  tabs.forEach(function (t, i) {
    t.addEventListener('click', function () { pick(t); });
    t.addEventListener('keydown', function (e) {
      var k = e.key, n = null;
      if (k === 'ArrowRight') n = tabs[(i + 1) % tabs.length];
      else if (k === 'ArrowLeft') n = tabs[(i - 1 + tabs.length) % tabs.length];
      else if (k === 'Home') n = tabs[0]; else if (k === 'End') n = tabs[tabs.length - 1];
      if (n) { e.preventDefault(); pick(n, true); }
    });
  });

  /* ---------- Minyam: items and streak ---------- */
  var ITEMS = {
    id: [['topi_koboi', 'Topi koboi'], ['kacamata_bulat', 'Kacamata'], ['mahkota_emas', 'Mahkota'], ['topi_koki', 'Topi koki'], ['topi_baret', 'Baret'], ['syal_kain', 'Syal'], ['dasi_kupu', 'Dasi kupu'], ['jubah_merah', 'Jubah']],
    en: [['topi_koboi', 'Cowboy hat'], ['kacamata_bulat', 'Glasses'], ['mahkota_emas', 'Crown'], ['topi_koki', 'Chef hat'], ['topi_baret', 'Beret'], ['syal_kain', 'Scarf'], ['dasi_kupu', 'Bow tie'], ['jubah_merah', 'Cape']]
  }[LANG];
  var NONE = LANG === 'id' ? 'Lepas' : 'Take off';
  var wear = $('#wearImg'), stage = wear && wear.parentNode, itemBox = $('#items');
  function dress(file, btn) {
    wear.dataset.worn = file === 'idle' ? '0' : '1';
    wear.src = src(file);
    stage.classList.remove('swap'); void stage.offsetWidth; stage.classList.add('swap');
    $$('.chip', itemBox).forEach(function (c) { c.setAttribute('aria-pressed', c === btn ? 'true' : 'false'); });
  }
  if (itemBox) {
    var none = document.createElement('button');
    none.type = 'button'; none.className = 'chip'; none.textContent = NONE; none.setAttribute('aria-pressed', 'true');
    none.addEventListener('click', function () { dress('idle', none); });
    itemBox.appendChild(none);
    ITEMS.forEach(function (it) {
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'chip'; b.textContent = it[1]; b.setAttribute('aria-pressed', 'false');
      var im = new Image(); im.src = src('item_' + it[0]);
      b.addEventListener('click', function () { dress('item_' + it[0], b); });
      itemBox.appendChild(b);
    });
  }
  var sb = $('#streakBtn'), sn = $('#streakNum');
  if (sb) sb.addEventListener('click', function () {
    sn.textContent = String(parseInt(sn.textContent, 10) + 1);
    sb.disabled = true; sb.textContent = T.saved;
    if (wear.dataset.worn !== '1') { wear.dataset.lock = '1'; wear.src = src('joy'); setTimeout(function () { wear.dataset.lock = '0'; wear.src = src('idle'); }, 1100); }
    stage.classList.remove('swap'); void stage.offsetWidth; stage.classList.add('swap');
  });
  blinker(wear);

  /* ---------- all features: search + category chips ---------- */
  var q = $('#allSearch'), gchips = $$('#allChips .chip'), groups = $$('#allList .grp'), none2 = $('#allNone'), cnt = $('#allCount');
  var cur = 'all', expanded = false, more = $('#allMore');
  function filter() {
    var term = (q.value || '').toLowerCase().trim(), total = 0;
    var collapsed = !expanded && !term && cur === 'all';
    groups.forEach(function (g) {
      var inGroup = cur === 'all' || g.getAttribute('data-g') === cur, any = false;
      $$('li', g).forEach(function (li) {
        var ok = inGroup && (!term || li.getAttribute('data-s').indexOf(term) !== -1);
        if (ok) total++;
        var vis = ok && (!collapsed || li.hasAttribute('data-top'));
        li.hidden = !vis; if (vis) any = true;
      });
      g.hidden = !any;
    });
    cnt.textContent = T.count.replace('{n}', total);
    none2.hidden = total !== 0;
    more.hidden = !collapsed;
  }
  if (more) more.addEventListener('click', function () { expanded = true; filter(); });
  if (q) {
    q.addEventListener('input', filter);
    filter();
    gchips.forEach(function (c) {
      c.addEventListener('click', function () {
        cur = c.getAttribute('data-g');
        gchips.forEach(function (x) { x.setAttribute('aria-pressed', x === c ? 'true' : 'false'); });
        filter();
      });
    });
  }
})();
