"""Builds index.html (ID) and en/index.html (EN) of the landing page from one template.

  python tools/build_home.py

Texts live in the T dictionaries below; markup in TEMPLATE. css/home.css and js/home.js are shared.
No em-dash anywhere on the page (house rule for the landing page).
"""
import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ID = dict(
    lang='id', prefix='', other_href='en/', other_label='English', other_lang='en', home='./',
    title='Artosku | Catat keuangan, datanya di HP-mu',
    desc='Catat pengeluaran dengan mengetik, bicara, atau foto struk. Catatan tersimpan di HP-mu. Ada Minyam yang menemani. Gratis di Google Play.',
    og_title='Artosku: catat keuangan semudah bercerita',
    og_desc='Catatan keuangan tersimpan di HP-mu. Catat dengan AI semudah bercerita, ditemani Minyam.',
    skip='Langsung ke konten',
    nav_try='Coba sendiri', nav_how='Cara mencatat', nav_data='Datamu', nav_features='Fitur', nav_minyam='Minyam', nav_plans='Paket', nav_faq='FAQ',
    nav_dl='Unduh',
    h1='Catatanmu di <span class="nw">HP-mu</span>. Mencatat semudah bercerita.',
    hero_sub='Ketik, bicara, atau foto struk. AI menyiapkan catatannya, kamu yang memutuskan.',
    cta_how='Lihat cara kerjanya',
    play_alt='Dapatkan di Google Play',
    hero_stage_label='Minyam, maskot Artosku. Ketuk untuk menyapa.',
    bubble_start='Hai, aku Minyam. Ketuk aku.',
    try_h='Coba sendiri',
    try_sub='Tulis satu transaksi seperti kamu bercerita.',
    try_label='Ceritakan transaksinya',
    try_ph='makan siang 25 ribu pakai gopay',
    try_btn='Catat',
    try_note='Contoh di browser. Di aplikasi, AI yang membaca ceritamu.',
    try_r_title='Hasilnya', try_r_amount='Nominal', try_r_cat='Kategori', try_r_wallet='Wallet', try_r_type='Jenis', try_r_date='Tanggal',
    try_empty='Tulis atau pilih contoh di atas, hasilnya muncul di sini.',
    how_h='Cara mencatat',
    how_sub='Pilih yang paling cepat untukmu hari ini.',
    tab_type='Ketik', tab_voice='Suara', tab_photo='Foto struk', tab_bank='Mutasi bank', tab_notif='Notifikasi',
    how_type_t='Tulis seperti chat.',
    how_type_p='Satu kalimat, bisa beberapa transaksi sekaligus. AI mengisi nominal, kategori, dan wallet. Kamu cek, lalu simpan.',
    how_voice_t='Ucapkan, jangan ketik.',
    how_voice_p='Tekan mikrofon dan sebut transaksinya. Cocok saat tangan penuh atau sedang di jalan.',
    how_photo_t='Foto struknya.',
    how_photo_p='Nama toko dan total dibaca dari foto. Fotonya tetap tersimpan di HP-mu sebagai lampiran.',
    how_bank_t='Tangkapan layar mutasi.',
    how_bank_p='Unggah mutasi dari aplikasi bank. Kamu pilih baris mana yang mau dicatat.',
    how_notif_t='Dari notifikasi.',
    how_notif_p='Notifikasi bank dan e-wallet menjadi draf transaksi. Draf menunggu persetujuanmu, tidak disimpan sendiri.',
    ui_voice_hint='Mendengarkan...', ui_voice_said='"bensin lima puluh ribu"',
    ui_receipt_shop='Toko Sejahtera', ui_receipt_total='Total', ui_receipt_items='3 barang',
    ui_bank_pick='Pilih yang dicatat',
    ui_notif_app='GoPay', ui_notif_text='Pembayaran Rp32.000 ke Kedai Kopi berhasil', ui_notif_draft='Draf siap dicek', ui_notif_save='Simpan',
    ui_save='Simpan',
    data_h='Datamu ada di mana?',
    data_sub='Jawaban jujur, tanpa tanda bintang.',
    data_phone_h='Di HP-mu',
    data_phone_1='Catatan dan foto struk tersimpan di HP-mu.',
    data_phone_2='Catat manual dan notifikasi jalan tanpa internet.',
    data_phone_3='Backup ke Google Drive milikmu sendiri, saat kamu mau.',
    data_out_h='Keluar dari HP, hanya kalau kamu pakai',
    data_out_1='AI dan scan mutasi mengirim teks ke penyedia AI, setelah kamu setuju.',
    data_out_2='Wallet bersama disimpan di server supaya bisa dibuka bersama.',
    data_out_3='Kurs mata uang butuh internet.',
    data_bottom='Tanpa iklan. Datamu tidak dijual.',
    data_privacy='Baca Kebijakan Privasi',
    feat_h='Yang ada di dalamnya',
    f_wallet_t='Wallet dan wallet bersama', f_wallet_p='Pisahkan uang tunai, bank, dan e-wallet. Undang pasangan atau keluarga ke wallet bersama.',
    f_budget_t='Anggaran', f_budget_p='Batasi tiap kategori dan lihat sisanya sebelum bulan habis.',
    f_bill_t='Tagihan dan pengingat', f_bill_p='Cicilan dan tagihan rutin diingatkan sebelum jatuh tempo.',
    f_report_t='Laporan', f_report_p='Ke mana uangmu pergi, per kategori dan per periode yang kamu pilih.',
    f_asset_t='Aset dan target', f_asset_p='Catat aset, lalu sisihkan uang untuk target tabunganmu.',
    f_biz_t='Mode Bisnis', f_biz_p='Kasir, stok, nota, dan pre-order untuk usahamu, terpisah dari catatan pribadi.',
    f_biz_badge='Paket Max',
    ui_budget_food='Makan', ui_budget_left='sisa Rp420.000',
    min_h='Minyam ikut mencatat',
    min_p='Catat tiap hari, streak-mu naik, dan Minyam bisa dapat item baru. Coba pakaikan sesuatu.',
    min_stage='Minyam yang sedang dipakaikan item',
    min_pick='Pilih item', min_none='Lepas',
    streak_label='Streak', streak_day='hari', streak_btn='Catat hari ini', streak_done='Sudah dicatat hari ini',
    items=[('topi_koboi', 'Topi koboi'), ('kacamata_bulat', 'Kacamata'), ('mahkota_emas', 'Mahkota'), ('topi_koki', 'Topi koki'),
           ('topi_baret', 'Baret'), ('syal_kain', 'Syal'), ('dasi_kupu', 'Dasi kupu'), ('jubah_merah', 'Jubah')],
    plans_h='Paket',
    plans_sub='Mulai gratis. Naik paket kalau butuh jatah AI lebih besar.',
    p_free='Free', p_free_p='Catat manual, notifikasi, laporan, anggaran, wallet, dan backup ke Drive. AI dengan jatah harian.',
    p_pro='Pro', p_pro_p='Jatah AI lebih besar untuk yang rutin mencatat dengan AI.',
    p_max='Max', p_max_p='Jatah AI paling besar, ditambah Mode Bisnis: kasir, stok, nota, dan pre-order.',
    plans_note='Harga tampil di aplikasi lewat Google Play.',
    faq_h='Pertanyaan umum',
    faqs=[
        ('Apakah Artosku gratis?', 'Bisa dipakai gratis. Ada paket Pro dan Max untuk jatah AI yang lebih besar, dan Mode Bisnis ada di paket Max.'),
        ('Apakah bisa tanpa internet?', 'Catat manual, notifikasi, dan melihat laporan jalan tanpa internet. AI, scan mutasi, wallet bersama, dan kurs mata uang butuh internet.'),
        ('Data apa yang dikirim ke luar HP?', 'Catatan dan foto struk tetap di HP. Teks yang kamu minta dibaca AI dikirim ke penyedia AI setelah kamu setuju. Wallet bersama disimpan di server. Backup ke Google Drive masuk ke akun Drive-mu sendiri.'),
        ('Apakah ada iklan?', 'Tidak ada iklan, dan datamu tidak dijual.'),
        ('Bagaimana cara memasangnya?', 'Cari Artosku di Google Play, atau pakai tombol unduh di halaman ini.'),
        ('Bisa dipakai di iPhone?', 'Untuk saat ini baru Android.'),
    ],
    dl_h='Mulai dari catatan pertama.',
    dl_p='Pertanyaan atau masukan? Kirim ke',
    all_h='Semua fitur', all_sub='Semua yang ada di aplikasi, per kategori. Ketuk satu untuk membaca caranya.',
    all_btn='Lihat semua fitur ({n})', show_all='Tampilkan semua ({n})', all_count='{n} fitur', search_label='Cari fitur', search_ph='mis. anggaran, struk, backup',
    chip_all='Semua', no_result='Tidak ada fitur yang cocok.', badge_pro='Pro', badge_max='Max',
    foot_guide='Panduan', foot_privacy='Kebijakan Privasi', foot_terms='Syarat dan Ketentuan',
    foot_made='Dibuat oleh Andi Pramana.',
    path_tutorial='tutorial/', path_privacy='privacy.html', path_terms='terms.html', asset='',
)

EN = dict(
    lang='en', prefix='../', other_href='../', other_label='Bahasa Indonesia', other_lang='id', home='./',
    title='Artosku | Track your money, data stays on your phone',
    desc='Log spending by typing, talking, or snapping a receipt. Your records stay on your phone. Minyam keeps you company. Free on Google Play.',
    og_title='Artosku: money tracking as easy as telling a story',
    og_desc='Your finance records stay on your phone. Log with AI as easily as telling a story, with Minyam beside you.',
    skip='Skip to content',
    nav_try='Try it', nav_how='How to log', nav_data='Your data', nav_features='Features', nav_minyam='Minyam', nav_plans='Plans', nav_faq='FAQ',
    nav_dl='Get it',
    h1='Your records on your phone. Logging as easy as telling a story.',
    hero_sub='Type, talk, or snap a receipt. AI prepares the entry, you decide.',
    cta_how='See how it works',
    play_alt='Get it on Google Play',
    hero_stage_label='Minyam, the Artosku mascot. Tap to say hi.',
    bubble_start='Hi, I am Minyam. Tap me.',
    try_h='Try it yourself',
    try_sub='Write one transaction the way you would tell it.',
    try_label='Tell the transaction',
    try_ph='lunch 25k with gopay',
    try_btn='Log it',
    try_note='A sample in your browser. In the app, AI reads your story.',
    try_r_title='Result', try_r_amount='Amount', try_r_cat='Category', try_r_wallet='Wallet', try_r_type='Type', try_r_date='Date',
    try_empty='Write something or pick a sample above, the result shows up here.',
    how_h='Ways to log',
    how_sub='Pick whichever is fastest for you today.',
    tab_type='Type', tab_voice='Voice', tab_photo='Receipt photo', tab_bank='Bank statement', tab_notif='Notifications',
    how_type_t='Write it like a chat.',
    how_type_p='One sentence, or several transactions at once. AI fills in the amount, category, and wallet. You check, then save.',
    how_voice_t='Say it, do not type it.',
    how_voice_p='Tap the microphone and say the transaction. Handy when your hands are full or you are on the go.',
    how_photo_t='Snap the receipt.',
    how_photo_p='The shop and total are read from the photo. The photo stays on your phone as an attachment.',
    how_bank_t='A screenshot of the statement.',
    how_bank_p='Upload a statement from your bank app. You choose which rows to log.',
    how_notif_t='From notifications.',
    how_notif_p='Bank and e-wallet notifications become draft transactions. Drafts wait for your approval, nothing saves by itself.',
    ui_voice_hint='Listening...', ui_voice_said='"fuel fifty thousand"',
    ui_receipt_shop='Toko Sejahtera', ui_receipt_total='Total', ui_receipt_items='3 items',
    ui_bank_pick='Choose what to log',
    ui_notif_app='GoPay', ui_notif_text='Payment of Rp32,000 to Kedai Kopi succeeded', ui_notif_draft='Draft ready to check', ui_notif_save='Save',
    ui_save='Save',
    data_h='Where is your data?',
    data_sub='An honest answer, no asterisks.',
    data_phone_h='On your phone',
    data_phone_1='Records and receipt photos are stored on your phone.',
    data_phone_2='Manual logging and notifications work without internet.',
    data_phone_3='Backup to your own Google Drive, whenever you want.',
    data_out_h='Leaves the phone, only if you use it',
    data_out_1='AI and statement scan send text to an AI provider, after you agree.',
    data_out_2='Shared wallets live on a server so you can open them together.',
    data_out_3='Currency rates need internet.',
    data_bottom='No ads. Your data is not sold.',
    data_privacy='Read the Privacy Policy',
    feat_h='What is inside',
    f_wallet_t='Wallets and shared wallets', f_wallet_p='Keep cash, bank, and e-wallets apart. Invite a partner or family to a shared wallet.',
    f_budget_t='Budgets', f_budget_p='Cap each category and see what is left before the month ends.',
    f_bill_t='Bills and reminders', f_bill_p='Installments and recurring bills are reminded before they are due.',
    f_report_t='Reports', f_report_p='Where your money goes, by category and by the period you choose.',
    f_asset_t='Assets and goals', f_asset_p='Record assets, then set money aside for your savings goals.',
    f_biz_t='Business Mode', f_biz_p='Cashier, stock, receipts, and pre-orders for your business, kept apart from personal records.',
    f_biz_badge='Max plan',
    ui_budget_food='Food', ui_budget_left='Rp420,000 left',
    min_h='Minyam logs along',
    min_p='Log every day, your streak grows, and Minyam can get new items. Try dressing it up.',
    min_stage='Minyam wearing an item',
    min_pick='Pick an item', min_none='Take off',
    streak_label='Streak', streak_day='days', streak_btn='Log today', streak_done='Logged today',
    items=[('topi_koboi', 'Cowboy hat'), ('kacamata_bulat', 'Glasses'), ('mahkota_emas', 'Crown'), ('topi_koki', 'Chef hat'),
           ('topi_baret', 'Beret'), ('syal_kain', 'Scarf'), ('dasi_kupu', 'Bow tie'), ('jubah_merah', 'Cape')],
    plans_h='Plans',
    plans_sub='Start free. Move up when you need a bigger AI allowance.',
    p_free='Free', p_free_p='Manual logging, notifications, reports, budgets, wallets, and Drive backup. AI with a daily allowance.',
    p_pro='Pro', p_pro_p='A bigger AI allowance for those who log with AI regularly.',
    p_max='Max', p_max_p='The biggest AI allowance, plus Business Mode: cashier, stock, receipts, and pre-orders.',
    plans_note='Prices show in the app through Google Play.',
    faq_h='Common questions',
    faqs=[
        ('Is Artosku free?', 'You can use it for free. Pro and Max plans give a bigger AI allowance, and Business Mode is in Max.'),
        ('Does it work without internet?', 'Manual logging, notifications, and reports work offline. AI, statement scan, shared wallets, and currency rates need internet.'),
        ('What leaves my phone?', 'Records and receipt photos stay on the phone. Text you ask AI to read goes to an AI provider after you agree. Shared wallets are stored on a server. A Google Drive backup goes into your own Drive account.'),
        ('Are there ads?', 'No ads, and your data is not sold.'),
        ('How do I install it?', 'Search for Artosku on Google Play, or use the download button on this page.'),
        ('Is there an iPhone version?', 'Android only for now.'),
    ],
    dl_h='Start with your first entry.',
    dl_p='Questions or feedback? Write to',
    all_h='All features', all_sub='Everything in the app, by category. Tap one to read how it works.',
    all_btn='See all features ({n})', show_all='Show all ({n})', all_count='{n} features', search_label='Search features', search_ph='e.g. budget, receipt, backup',
    chip_all='All', no_result='No feature matches.', badge_pro='Pro', badge_max='Max',
    foot_guide='Guide', foot_privacy='Privacy Policy', foot_terms='Terms of Service',
    foot_made='Made by Andi Pramana.',
    path_tutorial='tutorial/', path_privacy='privacy.html', path_terms='terms.html', asset='../',
)

TEMPLATE = r'''<!doctype html>
<html lang="{{lang}}">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<title>{{title}}</title>
<meta name="description" content="{{desc}}" />
<meta name="theme-color" content="#F6FAF3" />
<meta property="og:type" content="website" />
<meta property="og:title" content="{{og_title}}" />
<meta property="og:description" content="{{og_desc}}" />
<meta property="og:image" content="https://artosku.my.id/assets/og-cover.png" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{{og_title}}" />
<meta name="twitter:description" content="{{og_desc}}" />
<meta name="twitter:image" content="https://artosku.my.id/assets/og-cover.png" />
<link rel="icon" href="{{asset}}assets/artosku-app-icon.svg" type="image/svg+xml" />
<link rel="apple-touch-icon" href="{{asset}}assets/artosku-app-icon.png" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="https://unpkg.com/@phosphor-icons/web@2.1.1/src/regular/style.css" />
<link rel="stylesheet" href="{{asset}}css/home.css" />
<link rel="preload" as="image" href="{{asset}}assets/minyam/idle.webp" type="image/webp" />
<script type="application/ld+json">{"@context":"https://schema.org","@type":"MobileApplication","name":"Artosku","operatingSystem":"ANDROID","applicationCategory":"FinanceApplication","offers":{"@type":"Offer","price":"0","priceCurrency":"IDR"}}</script>
<link rel="alternate" hreflang="id" href="https://artosku.my.id/" />
<link rel="alternate" hreflang="en" href="https://artosku.my.id/en/" />
<link rel="alternate" hreflang="x-default" href="https://artosku.my.id/" />
</head>
<body data-lang="{{lang}}" data-asset="{{asset}}">
<a class="skip" href="#main">{{skip}}</a>

<header class="nav">
  <div class="wrap nav__in">
    <a class="nav__brand" href="#top" aria-label="Artosku"><img src="{{asset}}assets/logo-mark.png" alt="" width="34" height="34" /><span>Artosku</span></a>
    <nav class="nav__links" aria-label="Menu">
      <a href="#coba">{{nav_try}}</a><a href="#cara">{{nav_how}}</a><a href="#data">{{nav_data}}</a><a href="#fitur">{{nav_features}}</a><a href="#minyam">{{nav_minyam}}</a><a href="#paket">{{nav_plans}}</a><a href="#faq">{{nav_faq}}</a>
    </nav>
    <div class="nav__end">
      <a class="nav__lang" href="{{other_href}}" hreflang="{{other_lang}}" lang="{{other_lang}}">{{other_label}}</a>
      <a class="btn btn--small" href="#unduh">{{nav_dl}}</a>
    </div>
  </div>
</header>

<main id="main">

<section class="hero" id="top">
  <div class="wrap hero__in">
    <div class="hero__copy">
      <h1>{{h1}}</h1>
      <p class="hero__sub">{{hero_sub}}</p>
      <div class="hero__cta">
        <a class="play" href="https://play.google.com/store/apps/details?id=com.artosku" target="_blank" rel="noopener"><img src="{{asset}}assets/google-play-badge.svg" alt="{{play_alt}}" width="160" height="48" /></a>
        <a class="btn btn--ghost" href="#coba">{{cta_how}}</a>
      </div>
    </div>
    <div class="hero__stage">
      <div class="bubble" id="heroBubble" aria-live="polite">{{bubble_start}}</div>
      <button class="mascot mascot--hero" id="heroMascot" type="button" aria-label="{{hero_stage_label}}">
        <img id="heroMascotImg" src="{{asset}}assets/minyam/idle.webp" alt="" width="400" height="400" fetchpriority="high" />
      </button>
    </div>
  </div>
</section>

<section class="sec sec--tint" id="coba">
  <div class="wrap">
    <h2>{{try_h}}</h2>
    <p class="lead">{{try_sub}}</p>
    <div class="try">
      <div class="try__in">
        <form id="tryForm" autocomplete="off">
          <label for="tryInput">{{try_label}}</label>
          <div class="try__row">
            <input id="tryInput" type="text" inputmode="text" placeholder="{{try_ph}}" maxlength="120" />
            <button class="btn" type="submit">{{try_btn}}</button>
          </div>
        </form>
        <div class="chips" id="tryChips" role="group" aria-label="{{try_h}}"></div>
        <p class="note"><i class="ph ph-info" aria-hidden="true"></i> {{try_note}}</p>
      </div>
      <div class="try__out">
        <div class="try__mascot"><img id="tryMascotImg" src="{{asset}}assets/minyam/idle.webp" alt="" width="400" height="400" loading="lazy" /></div>
        <div class="card tx" id="tryResult" aria-live="polite">
          <p class="tx__empty" id="tryEmpty">{{try_empty}}</p>
          <div class="tx__body" id="tryBody" hidden>
            <p class="tx__title" id="trName"></p>
            <dl>
              <div><dt>{{try_r_amount}}</dt><dd id="trAmount"></dd></div>
              <div><dt>{{try_r_type}}</dt><dd id="trType"></dd></div>
              <div><dt>{{try_r_cat}}</dt><dd id="trCat"></dd></div>
              <div><dt>{{try_r_wallet}}</dt><dd id="trWallet"></dd></div>
              <div><dt>{{try_r_date}}</dt><dd id="trDate"></dd></div>
            </dl>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="sec" id="cara">
  <div class="wrap">
    <h2>{{how_h}}</h2>
    <p class="lead">{{how_sub}}</p>
    <div class="how">
      <div class="tabs" role="tablist" aria-label="{{how_h}}">
        <button role="tab" id="tab-type" aria-controls="pan-type" aria-selected="true"><i class="ph ph-keyboard" aria-hidden="true"></i>{{tab_type}}</button>
        <button role="tab" id="tab-voice" aria-controls="pan-voice" aria-selected="false" tabindex="-1"><i class="ph ph-microphone" aria-hidden="true"></i>{{tab_voice}}</button>
        <button role="tab" id="tab-photo" aria-controls="pan-photo" aria-selected="false" tabindex="-1"><i class="ph ph-receipt" aria-hidden="true"></i>{{tab_photo}}</button>
        <button role="tab" id="tab-bank" aria-controls="pan-bank" aria-selected="false" tabindex="-1"><i class="ph ph-bank" aria-hidden="true"></i>{{tab_bank}}</button>
        <button role="tab" id="tab-notif" aria-controls="pan-notif" aria-selected="false" tabindex="-1"><i class="ph ph-bell-ringing" aria-hidden="true"></i>{{tab_notif}}</button>
      </div>
      <div class="how__panels">
        <div role="tabpanel" id="pan-type" aria-labelledby="tab-type" class="pan">
          <div class="pan__copy"><h3>{{how_type_t}}</h3><p>{{how_type_p}}</p></div>
          <div class="phone">
            <div class="ui-input"><span>{{try_ph}}</span><i class="ph ph-paper-plane-tilt" aria-hidden="true"></i></div>
            <div class="ui-tx"><b>Rp25.000</b><span>{{trcat_food}} &middot; GoPay</span><button class="btn btn--small" type="button" tabindex="-1">{{ui_save}}</button></div>
          </div>
        </div>
        <div role="tabpanel" id="pan-voice" aria-labelledby="tab-voice" class="pan" hidden>
          <div class="pan__copy"><h3>{{how_voice_t}}</h3><p>{{how_voice_p}}</p></div>
          <div class="phone">
            <div class="ui-mic"><i class="ph ph-microphone" aria-hidden="true"></i></div>
            <p class="ui-say">{{ui_voice_hint}}</p>
            <p class="ui-quote">{{ui_voice_said}}</p>
            <div class="ui-tx"><b>Rp50.000</b><span>{{trcat_transport}} &middot; {{trwallet_cash}}</span><button class="btn btn--small" type="button" tabindex="-1">{{ui_save}}</button></div>
          </div>
        </div>
        <div role="tabpanel" id="pan-photo" aria-labelledby="tab-photo" class="pan" hidden>
          <div class="pan__copy"><h3>{{how_photo_t}}</h3><p>{{how_photo_p}}</p></div>
          <div class="phone">
            <div class="ui-receipt"><b>{{ui_receipt_shop}}</b><i></i><i></i><i></i><i class="short"></i><div><span>{{ui_receipt_total}}</span><b>Rp84.500</b></div></div>
            <div class="ui-tx"><b>Rp84.500</b><span>{{ui_receipt_shop}} &middot; {{ui_receipt_items}}</span><button class="btn btn--small" type="button" tabindex="-1">{{ui_save}}</button></div>
          </div>
        </div>
        <div role="tabpanel" id="pan-bank" aria-labelledby="tab-bank" class="pan" hidden>
          <div class="pan__copy"><h3>{{how_bank_t}}</h3><p>{{how_bank_p}}</p></div>
          <div class="phone">
            <p class="ui-say">{{ui_bank_pick}}</p>
            <ul class="ui-rows">
              <li><i class="ph ph-check-square" aria-hidden="true"></i><span>Kedai Kopi</span><b>-Rp32.000</b></li>
              <li><i class="ph ph-check-square" aria-hidden="true"></i><span>Minimarket</span><b>-Rp18.500</b></li>
              <li class="off"><i class="ph ph-square" aria-hidden="true"></i><span>Top up</span><b>-Rp100.000</b></li>
              <li><i class="ph ph-check-square" aria-hidden="true"></i><span>Gaji</span><b class="in">+Rp6.500.000</b></li>
            </ul>
          </div>
        </div>
        <div role="tabpanel" id="pan-notif" aria-labelledby="tab-notif" class="pan" hidden>
          <div class="pan__copy"><h3>{{how_notif_t}}</h3><p>{{how_notif_p}}</p></div>
          <div class="phone">
            <div class="ui-notif"><i class="ph ph-wallet" aria-hidden="true"></i><div><b>{{ui_notif_app}}</b><span>{{ui_notif_text}}</span></div></div>
            <div class="ui-tx"><b>Rp32.000</b><span>{{ui_notif_draft}}</span><button class="btn btn--small" type="button" tabindex="-1">{{ui_notif_save}}</button></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="sec sec--tint" id="data">
  <div class="wrap">
    <h2>{{data_h}}</h2>
    <p class="lead">{{data_sub}}</p>
    <div class="data">
      <div class="data__col data__col--phone">
        <div class="data__head"><img src="{{asset}}assets/minyam/item_dasi_kupu.webp" alt="" width="72" height="72" loading="lazy" /><h3>{{data_phone_h}}</h3></div>
        <ul>
          <li><i class="ph ph-device-mobile" aria-hidden="true"></i>{{data_phone_1}}</li>
          <li><i class="ph ph-wifi-slash" aria-hidden="true"></i>{{data_phone_2}}</li>
          <li><i class="ph ph-google-drive-logo" aria-hidden="true"></i>{{data_phone_3}}</li>
        </ul>
      </div>
      <div class="data__col">
        <h3>{{data_out_h}}</h3>
        <ul>
          <li><i class="ph ph-sparkle" aria-hidden="true"></i>{{data_out_1}}</li>
          <li><i class="ph ph-users-three" aria-hidden="true"></i>{{data_out_2}}</li>
          <li><i class="ph ph-currency-circle-dollar" aria-hidden="true"></i>{{data_out_3}}</li>
        </ul>
      </div>
    </div>
    <p class="data__bottom"><b>{{data_bottom}}</b> <a href="{{path_privacy}}">{{data_privacy}}</a></p>
  </div>
</section>

<section class="sec" id="fitur">
  <div class="wrap">
    <h2>{{feat_h}}</h2>
    <div class="bento">
      <article class="cell cell--wallet"><i class="ph ph-wallet" aria-hidden="true"></i><h3>{{f_wallet_t}}</h3><p>{{f_wallet_p}}</p>
        <div class="mini-wallets"><span>Tunai</span><span>BCA</span><span>GoPay</span><span class="on"><i class="ph ph-users" aria-hidden="true"></i>{{f_wallet_t_short}}</span></div></article>
      <article class="cell cell--budget"><i class="ph ph-chart-pie-slice" aria-hidden="true"></i><h3>{{f_budget_t}}</h3><p>{{f_budget_p}}</p>
        <div class="mini-budget"><div><span>{{ui_budget_food}}</span><span>{{ui_budget_left}}</span></div><meter min="0" max="100" value="58" aria-label="{{ui_budget_food}}"></meter></div></article>
      <article class="cell cell--bill"><i class="ph ph-bell-ringing" aria-hidden="true"></i><h3>{{f_bill_t}}</h3><p>{{f_bill_p}}</p></article>
      <article class="cell cell--report"><i class="ph ph-chart-line-up" aria-hidden="true"></i><h3>{{f_report_t}}</h3><p>{{f_report_p}}</p></article>
      <article class="cell cell--asset"><i class="ph ph-target" aria-hidden="true"></i><h3>{{f_asset_t}}</h3><p>{{f_asset_p}}</p></article>
      <article class="cell cell--biz"><i class="ph ph-storefront" aria-hidden="true"></i><h3>{{f_biz_t}} <span class="badge">{{f_biz_badge}}</span></h3><p>{{f_biz_p}}</p></article>
    </div>
    <p class="more"><a class="btn btn--ghost" href="#semua">{{all_btn_n}}</a></p>
  </div>
</section>

<section class="sec" id="semua">
  <div class="wrap">
    <h2>{{all_h}}</h2>
    <p class="lead">{{all_sub}}</p>
    <div class="finder">
      <label for="allSearch">{{search_label}}</label>
      <input id="allSearch" type="search" placeholder="{{search_ph}}" autocomplete="off" />
      <div class="chips" id="allChips" role="group" aria-label="{{all_h}}">{{all_chips}}</div>
      <p class="note" id="allCount" aria-live="polite">{{all_count_n}}</p>
    </div>
    <div id="allList">{{all_groups}}</div>
    <p class="note" id="allNone" hidden>{{no_result}}</p>
    <p class="more"><button class="btn btn--ghost" id="allMore" type="button">{{show_all_n}}</button></p>
  </div>
</section>

<section class="sec sec--tint" id="minyam">
  <div class="wrap minyam">
    <div class="minyam__stage" aria-label="{{min_stage}}">
      <img id="wearImg" src="{{asset}}assets/minyam/idle.webp" alt="" width="400" height="400" loading="lazy" />
    </div>
    <div class="minyam__copy">
      <h2>{{min_h}}</h2>
      <p class="lead">{{min_p}}</p>
      <div class="streak">
        <div class="streak__num"><i class="ph ph-fire" aria-hidden="true"></i><b id="streakNum">6</b> <span>{{streak_day}}</span></div>
        <button class="btn btn--small" id="streakBtn" type="button">{{streak_btn}}</button>
      </div>
      <p class="pick">{{min_pick}}</p>
      <div class="items" id="items" role="group" aria-label="{{min_pick}}"></div>
    </div>
  </div>
</section>

<section class="sec" id="paket">
  <div class="wrap">
    <h2>{{plans_h}}</h2>
    <p class="lead">{{plans_sub}}</p>
    <div class="plans">
      <article class="plan"><h3>{{p_free}}</h3><p>{{p_free_p}}</p></article>
      <article class="plan"><h3>{{p_pro}}</h3><p>{{p_pro_p}}</p></article>
      <article class="plan plan--max"><h3>{{p_max}}</h3><p>{{p_max_p}}</p></article>
    </div>
    <p class="note">{{plans_note}}</p>
  </div>
</section>

<section class="sec sec--tint" id="faq">
  <div class="wrap faq">
    <h2>{{faq_h}}</h2>
    <div class="faq__list">{{faq_items}}</div>
  </div>
</section>

<section class="dl" id="unduh">
  <div class="wrap dl__in">
    <img class="dl__mascot" src="{{asset}}assets/minyam/joy.webp" alt="" width="200" height="200" loading="lazy" />
    <div>
      <h2>{{dl_h}}</h2>
      <a class="play" href="https://play.google.com/store/apps/details?id=com.artosku" target="_blank" rel="noopener"><img src="{{asset}}assets/google-play-badge.svg" alt="{{play_alt}}" width="160" height="48" loading="lazy" /></a>
      <p class="dl__mail">{{dl_p}} <a href="mailto:contact.artosku@gmail.com">contact.artosku@gmail.com</a></p>
    </div>
  </div>
</section>
</main>

<footer class="foot">
  <div class="wrap foot__in">
    <span>&copy; Artosku. {{foot_made}}</span>
    <nav aria-label="Footer"><a href="{{path_tutorial}}">{{foot_guide}}</a><a href="{{path_privacy}}">{{foot_privacy}}</a><a href="{{path_terms}}">{{foot_terms}}</a><a href="{{other_href}}" hreflang="{{other_lang}}" lang="{{other_lang}}">{{other_label}}</a></nav>
  </div>
</footer>

<script src="{{asset}}js/home.js" defer></script>
</body>
</html>
'''

EXTRA = {
    'id': dict(trcat_food='Makan', trcat_transport='Transport', trwallet_cash='Tunai', f_wallet_t_short='Bersama'),
    'en': dict(trcat_food='Food', trcat_transport='Transport', trwallet_cash='Cash', f_wallet_t_short='Shared'),
}


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


# Entries of the app catalog that are account chores, legal pages or app-store housekeeping, not things the
# app offers: kept out of "all features" (they stay in the tutorial). Applies on every re-run.
EXCLUDE = {
    'kata_sandi', 'keluar_akun', 'hapus_akun', 'reset_akun', 'syarat_ketentuan', 'privasi_syarat', 'cek_pembaruan',
    'kritik_saran', 'ikuti_artosku', 'beri_ulasan', 'catatan_pembaruan', 'ulangi_panduan', 'cari_menu', 'ubah_nama',
    'nonaktifkan_pin',
}
# How many groups show their first feature while the list is collapsed.
COLLAPSED_GROUPS = 9


def load_features(app_dir):
    sys.path.insert(0, os.path.join(ROOT, 'tools'))
    from build_tutorial import load_catalog, group_items
    features, recipes = load_catalog(app_dir)
    groups = []
    for g in group_items(features, []):
        if g['id'] == 'tujuan':
            continue
        g['items'] = [f for f in g['items'] if f['id'] not in EXCLUDE]
        if g['items']:
            groups.append(g)
    return groups


def fill_all(t):
    lang = t['lang']
    groups = FEATURE_GROUPS
    n = sum(len(g['items']) for g in groups)
    t['all_btn_n'] = t['all_btn'].format(n=n)
    t['all_count_n'] = t['all_count'].format(n=n)
    t['all_count_tpl'] = t['all_count']
    chips = [f'<button type="button" class="chip" data-g="all" aria-pressed="true">{esc(t["chip_all"])}</button>']
    out = []
    for gi, g in enumerate(groups):
        name = g['nameId'] if lang == 'id' else g['nameEn']
        chips.append(f'<button type="button" class="chip" data-g="{g["id"]}" aria-pressed="false">{esc(name)}</button>')
        rows = []
        for fi, f in enumerate(g['items']):
            title = f['nameId'] if lang == 'id' else f['nameEn']
            text = f['benefitId'] if lang == 'id' else f['benefitEn']
            plan = 'max' if f['mode'] == 'business' else f['plan']
            badge = ''
            if plan in ('pro', 'max'):
                badge = f' <span class="badge">{esc(t["badge_" + plan])}</span>'
            kw = esc(' '.join(f['allKeywords']))
            hay = esc((title + ' ' + text).lower())
            top = ' data-top="1"' if (fi == 0 and gi < COLLAPSED_GROUPS) else ''
            rows.append(
                f'<li{top} data-s="{hay} {kw.lower()}"><a href="{t["path_tutorial"]}#{f["id"]}"><b>{esc(title)}</b>{badge}'
                f'<span>{esc(text)}</span></a></li>')
        out.append(f'<section class="grp" data-g="{g["id"]}"><h3>{esc(name)}</h3><ul>{"".join(rows)}</ul></section>')
    t['all_chips'] = ''.join(chips)
    t['show_all_n'] = t['show_all'].format(n=n)
    t['all_groups'] = ''.join(out)


def build(t):
    t = dict(t)
    t.update(EXTRA[t['lang']])
    t['faq_items'] = ''.join(
        f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in t['faqs'])

    fill_all(t)

    def sub(m):
        return t[m.group(1)]
    out = re.sub(r'\{\{(\w+)\}\}', sub, TEMPLATE)
    assert '—' not in out and '–' not in out, 'em/en dash found'
    return out


FEATURE_GROUPS = []

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--app', default=os.path.join(os.path.dirname(ROOT), 'acisku'))
    FEATURE_GROUPS[:] = load_features(ap.parse_args().app)
    open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8', newline='\n').write(build(ID))
    os.makedirs(os.path.join(ROOT, 'en'), exist_ok=True)
    open(os.path.join(ROOT, 'en', 'index.html'), 'w', encoding='utf-8', newline='\n').write(build(EN))
    print('built')
