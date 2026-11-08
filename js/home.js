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
      stories: [{"label": "Gaji, transfer, makan, parkir", "text": "gaji masuk 5jt ke rekening BCA, transfer 1jt dari BCA ke pocket dana darurat, makan siang 25rb pakai GoPay, parkir 2rb cash", "items": [{"kind": "income", "amount": 5000000, "cat": "Gaji", "wallet": "BCA"}, {"kind": "transfer", "amount": 1000000, "from": "BCA", "to": "Pocket Dana Darurat"}, {"kind": "expense", "amount": 25000, "cat": "Makan", "wallet": "GoPay"}, {"kind": "expense", "amount": 2000, "cat": "Parkir", "wallet": "Tunai"}]}, {"label": "Belanja, bensin, arisan", "text": "belanja sayur 45rb dan bensin 30rb pakai OVO, terima transferan arisan 200rb", "items": [{"kind": "expense", "amount": 45000, "cat": "Belanja", "wallet": "OVO"}, {"kind": "expense", "amount": 30000, "cat": "Transport", "wallet": "OVO"}, {"kind": "income", "amount": 200000, "cat": "Arisan", "wallet": "Tunai"}]}, {"label": "Listrik dan kopi", "text": "bayar listrik 350rb dari BCA, kopi 18rb cash", "items": [{"kind": "expense", "amount": 350000, "cat": "Tagihan", "wallet": "BCA"}, {"kind": "expense", "amount": 18000, "cat": "Makan", "wallet": "Tunai"}]}],
      income: 'Pemasukan', expense: 'Pengeluaran', today: 'Hari ini', cash: 'Tunai', other: 'Lainnya', saved: 'Sudah dicatat hari ini',
      noAmount: 'Belum ada nominalnya. Tulis jumlahnya, misalnya 25 ribu.', count: '{n} fitur'
    },
    en: {
      bubbles: ['Hi, I am Minyam. Tap me.', 'I help you log your money.', 'Try the "Try it yourself" box below.', 'Log a little every day.', 'I like matcha. Do you?'],
      stories: [{"label": "Salary, transfer, lunch, parking", "text": "salary 5m into BCA, moved 1m from BCA to emergency fund pocket, lunch 25k with GoPay, parking 2k cash", "items": [{"kind": "income", "amount": 5000000, "cat": "Salary", "wallet": "BCA"}, {"kind": "transfer", "amount": 1000000, "from": "BCA", "to": "Emergency Fund Pocket"}, {"kind": "expense", "amount": 25000, "cat": "Food", "wallet": "GoPay"}, {"kind": "expense", "amount": 2000, "cat": "Parking", "wallet": "Cash"}]}, {"label": "Groceries, fuel, savings club", "text": "groceries 45k and fuel 30k with OVO, received 200k savings club transfer", "items": [{"kind": "expense", "amount": 45000, "cat": "Shopping", "wallet": "OVO"}, {"kind": "expense", "amount": 30000, "cat": "Transport", "wallet": "OVO"}, {"kind": "income", "amount": 200000, "cat": "Savings club", "wallet": "Cash"}]}, {"label": "Electricity and coffee", "text": "electricity 350k from BCA, coffee 18k cash", "items": [{"kind": "expense", "amount": 350000, "cat": "Bills", "wallet": "BCA"}, {"kind": "expense", "amount": 18000, "cat": "Food", "wallet": "Cash"}]}],
      income: 'Income', expense: 'Expense', today: 'Today', cash: 'Cash', other: 'Other', saved: 'Logged today',
      noAmount: 'No amount yet. Write one, for example 25k.', count: '{n} features'
    }
  }[LANG];

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

  /* ---------- one sentence, many entries: a scripted demo (fixed results, no parsing of visitor text) ---------- */
  var input = $('#tryInput'), chipBox = $('#tryChips'), tryImg = $('#tryMascotImg'), mic = $('#tryMic');
  var empty = $('#tryEmpty'), reading = $('#tryReading'), list = $('#txList'), sum = $('#txSum'), replayBtn = $('#tryReplay');
  blinker(tryImg);
  var money = function (n) { return 'Rp' + Math.round(n).toLocaleString(LANG === 'id' ? 'id-ID' : 'en-US'); };
  var STR = LANG === 'id'
    ? { income: 'PEMASUKAN', expense: 'PENGELUARAN', transfer: 'TRANSFER', sum: '{n} transaksi dari 1 kalimat', inn: 'Masuk', out: 'Keluar' }
    : { income: 'INCOME', expense: 'EXPENSE', transfer: 'TRANSFER', sum: '{n} transactions from 1 sentence', inn: 'In', out: 'Out' };
  function esc(s) { return String(s).replace(/[&<>]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]; }); }
  function card(it) {
    var cls = it.kind === 'income' ? 'in' : it.kind === 'transfer' ? 'xfer' : 'out';
    var icon = it.kind === 'income' ? 'ph-arrow-down-left' : it.kind === 'transfer' ? 'ph-arrows-left-right' : 'ph-arrow-up-right';
    var label = it.kind === 'income' ? STR.income : it.kind === 'transfer' ? STR.transfer : STR.expense;
    var sub = it.kind === 'transfer' ? esc(it.from) + ' &rarr; ' + esc(it.to) : esc(it.cat) + ' &middot; ' + esc(it.wallet);
    var sign = it.kind === 'income' ? '+' : it.kind === 'expense' ? '-' : '';
    return '<li class="txc txc--' + cls + '"><i class="ph ' + icon + '" aria-hidden="true"></i><strong>' + label + '</strong><b>' + sign + money(it.amount) + '</b><span>' + sub + '</span></li>';
  }
  var runId = 0, lastIdx = 0;
  function wait(ms, id) { return new Promise(function (res) { setTimeout(function () { res(id === runId); }, ms); }); }
  async function play(idx, typed) {
    var id = ++runId, story = T.stories[idx];
    lastIdx = idx;
    $$('.chip', chipBox).forEach(function (c, k) { c.setAttribute('aria-pressed', k === idx ? 'true' : 'false'); });
    list.innerHTML = ''; sum.hidden = true; reading.hidden = true; empty.hidden = true;
    var text = story.text;
    if (typed && !REDUCED) {
      input.value = ''; mic.classList.add('on');
      var per = Math.max(1, Math.ceil(text.length / 120)), n = 0;   // about 2.2 s for the long sample
      while (n < text.length) {
        n = Math.min(text.length, n + per); input.value = text.slice(0, n);
        if (!(await wait(18, id))) return;
      }
      mic.classList.remove('on');
    } else { input.value = text; }
    if (!REDUCED) {
      reading.hidden = false;
      if (!(await wait(400, id))) return;
      reading.hidden = true;
    }
    for (var i = 0; i < story.items.length; i++) {
      list.insertAdjacentHTML('beforeend', card(story.items[i]));
      if (!REDUCED && !(await wait(120, id))) return;
    }
    var inn = 0, outc = 0;
    story.items.forEach(function (it) { if (it.kind === 'income') inn += it.amount; else if (it.kind === 'expense') outc += it.amount; });
    sum.innerHTML = STR.sum.replace('{n}', story.items.length) + ' <span>' + STR.inn + ' ' + money(inn) + '</span><span>' + STR.out + ' ' + money(outc) + '</span>';
    sum.hidden = false;
    react(tryImg, 'joy', 1300);
  }
  T.stories.forEach(function (st, k) {
    var b = document.createElement('button');
    b.type = 'button'; b.className = 'chip'; b.textContent = st.label; b.setAttribute('aria-pressed', k === 0 ? 'true' : 'false');
    b.addEventListener('click', function () { play(k, true); });
    chipBox.appendChild(b);
  });
  if (replayBtn) replayBtn.addEventListener('click', function () { play(lastIdx, true); });
  input.value = T.stories[0].text;
  var coba = $('#coba');
  if ('IntersectionObserver' in window && coba) {
    var seen = false, io = new IntersectionObserver(function (ents) {
      if (!seen && ents[0].isIntersecting) { seen = true; io.disconnect(); play(0, true); }
    }, { threshold: 0.3 });
    io.observe(coba);
  } else { play(0, false); }

  /* ---------- tabs (ways to log, business features) ---------- */
  $$('.how').forEach(function (box) {
    var tabs = $$('[role="tab"]', box);
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


  /* ---------- Mode Bisnis: mini cashier ---------- */
  var B = null;
  try { B = JSON.parse(body.getAttribute('data-biz')); } catch (e) { B = null; }
  var posItems = $('#posItems');
  if (B && posItems) {
    var qty = B.biz_products.map(function () { return 0; }), payIdx = 0;
    var posImg = $('#posMascot'), rcpt = $('#posReceipt'), totEl = $('#posTotal'), makeBtn = $('#posMake'), payBox = $('#posPay');
    var rp = function (n) { return 'Rp' + n.toLocaleString(LANG === 'id' ? 'id-ID' : 'en-US'); };
    blinker(posImg);
    var outs = [], quiet = false;
    B.biz_products.forEach(function (p, i) {
      var li = document.createElement('li');
      var name = document.createElement('button');
      name.type = 'button'; name.className = 'name';
      name.innerHTML = '<span></span><small></small>';
      name.firstChild.textContent = p[0]; name.lastChild.textContent = rp(p[1]);
      var step = document.createElement('span'); step.className = 'step';
      var minus = document.createElement('button'), plus = document.createElement('button'), out = document.createElement('output');
      minus.type = plus.type = 'button'; minus.textContent = '-'; plus.textContent = '+'; out.textContent = '0';
      minus.setAttribute('aria-label', '- ' + p[0]); plus.setAttribute('aria-label', '+ ' + p[0]);
      function set(n) { qty[i] = Math.max(0, n); out.textContent = String(qty[i]); total(); }
      name.addEventListener('click', function () { set(qty[i] + 1); });
      plus.addEventListener('click', function () { set(qty[i] + 1); });
      minus.addEventListener('click', function () { set(qty[i] - 1); });
      step.appendChild(minus); step.appendChild(out); step.appendChild(plus);
      li.appendChild(name); li.appendChild(step); posItems.appendChild(li);
      outs.push(set);
    });
    B.biz_pays.forEach(function (name, i) {
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'chip'; b.textContent = name; b.setAttribute('aria-pressed', i === 0 ? 'true' : 'false');
      b.addEventListener('click', function () {
        payIdx = i; $$('.chip', payBox).forEach(function (c, k) { c.setAttribute('aria-pressed', k === i ? 'true' : 'false'); });
      });
      payBox.appendChild(b);
    });
    function total() {
      var t = 0; B.biz_products.forEach(function (p, i) { t += p[1] * qty[i]; });
      totEl.textContent = rp(t); return t;
    }
    function esc(s) { return String(s).replace(/[&<>]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]; }); }
    makeBtn.addEventListener('click', function () {
      var t = total();
      if (!t) { rcpt.innerHTML = '<p class="receipt__empty">' + esc(B.biz_cart_empty) + '</p>'; if (!quiet) react(posImg, 'wait', 1400); return; }
      var lines = '';
      B.biz_products.forEach(function (p, i) { if (qty[i]) lines += '<div class="ln"><span>' + qty[i] + ' x ' + esc(p[0]) + '</span><span>' + rp(p[1] * qty[i]) + '</span></div>'; });
      rcpt.innerHTML = '<h4>' + esc(B.biz_shop) + '</h4><div>' + esc(B.biz_date_label) + '</div><hr>' + lines + '<hr><div class="ln tot"><span>' + esc(B.biz_total) + '</span><span>' + rp(t) + '</span></div><div class="ln"><span>' + esc(B.biz_paid) + '</span><span>' + esc(B.biz_pays[payIdx]) + '</span></div><div class="ty">' + esc(B.biz_thanks) + '</div>';
      rcpt.classList.remove('fresh'); void rcpt.offsetWidth; rcpt.classList.add('fresh');
      if (!quiet) react(posImg, payIdx === 0 ? 'coin' : 'joy', 1500);
    });
    outs[0](1); outs[1](1);
    quiet = true; makeBtn.click(); quiet = false;
  }
  var bizAll = $('#bizAll');
  if (bizAll) bizAll.addEventListener('click', function () {
    var chip = $('#allChips .chip[data-g="bisnis"]');
    if (chip) chip.click();
    var tgt = $('#semua'); if (tgt) tgt.scrollIntoView({ behavior: REDUCED ? 'auto' : 'smooth' });
  });

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
