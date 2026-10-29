"""Isi tulisan tangan Buku Panduan yang BUKAN dari katalog: bagian "Mulai dari sini", pengelompokan, teks antarmuka.

Langkah per fitur tetap hanya dari katalog app (lihat build_tutorial.py). Nama tombol di bagian "Mulai dari sini"
sudah dicocokkan dengan kode app (dashboard_screen.dart: 'Belum ada wallet', 'Buat Contoh', 'Buat Sendiri', 'Total saldo';
en_category.dart: 'Create Samples', 'Create Your Own'; en_shell.dart: 'Home', 'Total balance').
"""

SITE = "https://artosku.my.id"
PLAY = "https://play.google.com/store/apps/details?id=com.artosku"

# Urutan grup. Setiap fitur dimasukkan ke grup pertama yang memuat id-nya; sisa fitur Mode Bisnis masuk
# grup "bisnis", sisanya ke "pengaturan". Fitur baru di katalog otomatis muncul di salah satu dari dua grup itu.
GROUPS = [
    ("catat", "Mencatat uang", "Recording money", [
        "catat_transaksi", "catat_ai_suara", "scan_struk", "tambah_banyak", "impor_mutasi", "catat_notif",
        "catat_notif_setelan", "biaya_transfer", "salin_transaksi", "struk_gabungan"]),
    ("wallet", "Wallet, kategori & merchant", "Wallets, categories & merchants", [
        "wallet", "pocket", "pindah_pocket", "mata_uang", "kategori", "belajar_kategori", "merchant"]),
    ("anggaran", "Anggaran & jatah", "Budgets & allowance", [
        "anggaran", "anggaran_harian", "jatah_harian", "jatah_dikecualikan", "berulang", "periode_laporan"]),
    ("utang", "Utang & cicilan", "Debts & installments", ["utang_piutang", "cicilan", "arisan", "paylater"]),
    ("tabungan", "Tabungan, aset & belanja", "Savings, assets & shopping", [
        "tabungan", "aset", "daftar_belanja", "pemakaian_barang"]),
    ("laporan", "Laporan", "Reports", ["laporan"]),
    ("bersama", "Berbagi dengan orang lain", "Sharing with others", [
        "split", "wallet_bersama", "undang_anggota", "kontak", "saling_kirim"]),
    ("backup", "Backup & pulihkan", "Backup & restore", [
        "backup_drive", "backup_otomatis", "excel", "backup_excel_otomatis", "impor_excel_lama"]),
    ("ai", "AI Chat & AI", "AI Chat & AI", ["ai_chat", "pemakaian_ai", "persetujuan_ai"]),
    ("maskot", "Streak & maskot", "Streak & mascot", ["streak_maskot", "toko_maskot", "koleksi_maskot"]),
    ("pengaturan", "Pengaturan & akun", "Settings & account", []),  # sisa fitur pribadi
    ("tujuan", "Cara cepat untuk tujuan umum", "Quick how-tos for common goals", []),  # resep tujuan umum (pribadi)
    ("bisnis", "Mode Bisnis", "Business Mode", []),       # semua fitur dan resep Mode Bisnis
]

UI = {
    "id": {
        "lang": "id", "path": "/tutorial/", "root": "../", "other": "../en/tutorial/", "other_name": "English",
        "title": "Buku Panduan Artosku — Cara Catat Keuangan di HP",
        "desc": "Cara catat keuangan di HP dengan Artosku: siapkan wallet, catat transaksi pakai AI, atur jatah harian dan anggaran. Langkah singkat, bahasa santai.",
        "og_desc": "Langkah singkat memakai Artosku, dari wallet pertama sampai backup ke Google Drive.",
        "skip": "Langsung ke konten", "nav_main": "Navigasi utama", "nav_mobile": "Navigasi mobile", "nav_footer": "Navigasi footer",
        "nav": [("Fitur", "#fitur"), ("Paket", "#paket"), ("Panduan", None), ("FAQ", "#faq"), ("Kontak", "#kontak")],
        "download": "Download Artosku", "menu": "Buka menu", "theme": "Ganti tema terang atau gelap",
        "h1": "Buku Panduan Artosku", "sub": "Langkah singkat memakai Artosku. Data kamu tetap tersimpan di HP sendiri.",
        "search_ph": "Cari, mis. anggaran, struk, backup", "search_label": "Cari panduan", "toc": "Daftar isi",
        "found": "{n} panduan ditemukan", "empty": "Belum ketemu. Coba kata lain, atau kembali ke <a href=\"#mulai\" id=\"tutReset\">Mulai dari sini</a>.",
        "start": "Mulai dari sini", "where": "Lokasi",
        "cta_h": "Siap mencoba?", "cta_p": "Gratis di Google Play.", "cta": "Download di Play Store",
        "privacy": "Kebijakan Privasi", "terms": "Syarat dan Ketentuan", "made": "Dibuat oleh Andi Pramana.",
        "privacy_href": "privacy.html", "terms_href": "terms.html", "shot_alt": "Layar {name} di Artosku",
    },
    "en": {
        "lang": "en", "path": "/en/tutorial/", "root": "../../", "other": "../../tutorial/", "other_name": "Bahasa Indonesia",
        "title": "Artosku Guide — How to Track Your Money on Your Phone",
        "desc": "How to track your money on your phone with Artosku: set up a wallet, record transactions with AI, set a daily allowance and budgets. Short steps, plain words.",
        "og_desc": "Short steps for using Artosku, from your first wallet to a Google Drive backup.",
        "skip": "Skip to content", "nav_main": "Main navigation", "nav_mobile": "Mobile navigation", "nav_footer": "Footer navigation",
        "nav": [("Features", "#fitur"), ("Plans", "#paket"), ("Guide", None), ("FAQ", "#faq"), ("Contact", "#kontak")],
        "download": "Download Artosku", "menu": "Open menu", "theme": "Switch light or dark theme",
        "h1": "Artosku Guide", "sub": "Short steps for using Artosku. Your data stays on your own phone.",
        "search_ph": "Search, e.g. budget, receipt, backup", "search_label": "Search the guide", "toc": "Contents",
        "found": "{n} guide(s) found", "empty": "Nothing found. Try another word, or go back to <a href=\"#mulai\" id=\"tutReset\">Start here</a>.",
        "start": "Start here", "where": "Where",
        "cta_h": "Ready to try it?", "cta_p": "Free on Google Play.", "cta": "Download on Google Play",
        "privacy": "Privacy Policy", "terms": "Terms and Conditions", "made": "Made by Andi Pramana.",
        "privacy_href": "privacy.html", "terms_href": "terms.html", "shot_alt": "The {name} screen in Artosku",
    },
}

GROUP_NAME_EN_INDEX = 2

# "Mulai dari sini": (judul, isi HTML). Nama tombol persis seperti di app (ID) dan seperti terjemahan app (EN).
START = {
    "id": {
        "lead": "Empat langkah, sekitar lima menit.",
        "steps": [
            ("Siapkan wallet",
             "<p>Wallet itu tempat uangmu: tunai, rekening bank, atau e-wallet. Di Beranda, kalau belum ada wallet, ketuk <b>Buat Contoh</b>. "
             "Wallet Cash, Bank, dan E-Wallet langsung jadi, dan bisa kamu ubah atau hapus nanti. Mau bikin sendiri? Ketuk <b>Buat Sendiri</b>.</p>"),
            ("Catat transaksi pertama",
             "<p><b>Pakai AI:</b> ketuk tombol <b>+</b> di tengah bawah, lalu <b>Catat pakai AI</b>. Ucapkan atau ketik, mis. \"makan siang 25 ribu\". Cek hasilnya, lalu simpan.</p>"
             "<p><b>Manual:</b> ketuk <b>+</b>, pilih Pengeluaran, Pemasukan, atau Transfer. Isi Jumlah, pilih Wallet dan Kategori, lalu ketuk <b>Simpan</b>.</p>"),
            ("Lihat hasilnya di Beranda",
             "<p>Balik ke Beranda. Total saldo kamu sudah ikut berubah. Jatah harian muncul di sini setelah kamu membuatnya (lihat langkah berikutnya).</p>"),
            ("Langkah berikutnya",
             "<p>Coba <a href=\"#jatah_harian\">Jatah harian</a> (boleh jajan berapa per hari sampai gajian), <a href=\"#anggaran\">Anggaran</a> "
             "(batas per kategori), dan <a href=\"#backup_drive\">Backup Google Drive</a> (salinan data di Drive milikmu sendiri).</p>"),
        ],
    },
    "en": {
        "lead": "Four steps, about five minutes.",
        "steps": [
            ("Set up a wallet",
             "<p>A wallet is where your money lives: cash, a bank account or an e-wallet. On Home, if you have no wallet yet, tap <b>Create Samples</b>. "
             "Cash, Bank and E-Wallet wallets are made at once, and you can edit or delete them later. Want to make your own? Tap <b>Create Your Own</b>.</p>"),
            ("Record your first transaction",
             "<p><b>With AI:</b> tap the <b>+</b> button at the bottom middle, then <b>Record with AI</b>. Say or type, e.g. \"lunch 25k\". Check the result, then save.</p>"
             "<p><b>By hand:</b> tap <b>+</b>, pick Expense, Income or Transfer. Fill in the Amount, pick the Wallet and the Category, then tap <b>Save</b>.</p>"),
            ("See the result on Home",
             "<p>Go back to Home. Your total balance has changed. The daily allowance shows up here once you have made one (see the next step).</p>"),
            ("What next",
             "<p>Try <a href=\"#jatah_harian\">Daily allowance</a> (how much you can spend per day until payday), <a href=\"#anggaran\">Budgets</a> "
             "(a limit per category) and <a href=\"#backup_drive\">Backup to Google Drive</a> (a copy of your data in your own Drive).</p>"),
        ],
    },
}
