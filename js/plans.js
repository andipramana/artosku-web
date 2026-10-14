// The quotas of the plans on the page come from the same place as the app's: the
// app_parameters table of the shared project (read with the public, read-only key,
// like the app does). Nothing here holds a number of its own; if the numbers cannot
// be read the lines stay as they are in the HTML, without numbers.
(function () {
  var URL = 'https://klafrhlcxyyxdbrdenwk.supabase.co/rest/v1/app_parameters';
  var KEY = 'sb_publishable_qWDO6IWishBFPgZnLnDGJw_9CIZs2eR';
  var NAMES = [
    'ai_daily_limit_free', 'ai_daily_limit_free_promo', 'ai_daily_limit_pro', 'ai_daily_limit_max',
    'scan_daily_limit_free', 'scan_daily_limit_pro', 'scan_daily_limit_max'
  ];

  function times(x) {
    var whole = Math.round(x);
    if (Math.abs(x - whole) < 0.05) return whole + 'x';
    return x.toFixed(1).replace('.', ',') + 'x';
  }

  function set(key, text) {
    var el = document.querySelector('[data-plan="' + key + '"]');
    if (el) el.textContent = text;
  }

  fetch(URL + '?select=key,value&key=in.(' + NAMES.join(',') + ')', {
    headers: { apikey: KEY, Authorization: 'Bearer ' + KEY }
  })
    .then(function (r) { return r.ok ? r.json() : Promise.reject(r.status); })
    .then(function (rows) {
      var v = {};
      rows.forEach(function (row) { v[row.key] = parseInt(row.value, 10); });
      var base = v.ai_daily_limit_free;
      var promo = v.ai_daily_limit_free_promo || 0;
      var pro = v.ai_daily_limit_pro;
      var max = v.ai_daily_limit_max;
      if (!(base > 0 && pro > 0 && max > 0)) return;
      set('free-ai', 'Pencatatan AI ' + base + ' per hari' +
        (promo > 0 ? ' (ditambah ' + promo + ' selama masa promo)' : ''));
      // "more than Free" counts from Free's base, not the promo on top of it
      set('pro-ai', 'Pencatatan AI ' + pro + ' per hari, ' + times(pro / base) + ' lebih banyak dari Free');
      set('max-ai', 'Pencatatan AI ' + max + ' per hari, ' + times(max / base) + ' lebih banyak dari Free');
      if (v.scan_daily_limit_free > 0) set('free-scan', 'Scan struk dan mutasi ' + v.scan_daily_limit_free + ' per hari');
      if (v.scan_daily_limit_pro > 0) set('pro-scan', 'Scan struk dan mutasi ' + v.scan_daily_limit_pro + ' per hari');
      if (v.scan_daily_limit_max > 0) set('max-scan', 'Scan struk dan mutasi ' + v.scan_daily_limit_max + ' per hari');
    })
    .catch(function () { /* the lines keep their text without numbers */ });
})();
