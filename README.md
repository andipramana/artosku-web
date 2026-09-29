# Artosku — Landing Page

Landing page statis (HTML/CSS/JS biasa, tanpa build step) untuk Artosku, di-host lewat GitHub Pages.

## Menjalankan lokal

Tidak perlu instalasi apa pun — cukup jalankan server statis apa saja dari folder ini, misalnya:

```
python -m http.server 8080
```

lalu buka `http://localhost:8080`.

## Struktur

```
index.html        # semua konten & struktur halaman
css/styles.css     # semua styling, token warna/tipografi di :root
js/main.js         # parallax, scroll reveal, navbar glass, tilt 3D, menu mobile, form kontak
assets/            # gambar (layer parallax, logo, og-cover)
downloads/artosku.apk  # file APK yang didownload dari tombol "Download Artosku"
CNAME              # domain custom: artosku.my.id
```

## Mengaktifkan GitHub Pages

Repo ini sudah berisi `index.html` di root, jadi tinggal:

1. Buka **Settings → Pages** di repo GitHub.
2. Source: **Deploy from a branch**, branch **main**, folder **/ (root)**.
3. Simpan — halaman tersedia di `https://artosku.my.id` (domain custom, lihat file `CNAME`).

## Update tombol "Download APK"

Tombol download mengarah langsung ke `downloads/artosku.apk` di repo ini (bukan GitHub Release) — jadi update-nya cukup timpa file itu:

1. Build APK dari project Flutter `artosku` (`flutter build apk --release`), hasilnya ada di `build/app/outputs/flutter-apk/app-release.apk`.
2. Copy file itu ke `downloads/artosku.apk` di repo ini (timpa yang lama, nama file harus tetap persis `artosku.apk`).
3. Commit & push — begitu GitHub Pages selesai deploy ulang, tombol download otomatis mengarah ke versi terbaru.

Catatan: karena APK disimpan langsung di repo (bukan GitHub Release), setiap versi yang pernah di-commit tetap tersimpan di riwayat git selamanya — ukuran repo akan terus bertambah tiap kali APK-nya diupdate. Untuk project sekecil ini itu masih wajar, tapi kalau suatu saat ukurannya jadi masalah, pertimbangkan pindah ke GitHub Release (link `releases/latest/download/artosku.apk`) sebagai gantinya.

## Catatan konten

Beberapa bagian dari brief awal sengaja tidak dipakai supaya halaman ini tidak menampilkan klaim yang tidak benar:

- **Tidak ada badge Google Play / App Store** — Artosku belum rilis di sana, tombol download mengarah langsung ke file APK.
- **Tidak ada angka statistik (jumlah download, rating, dsb.)** — belum ada data nyata untuk itu.
- **Tidak ada testimoni palsu** — diganti dengan catatan singkat dari pembuat aplikasi.

Kalau nanti ada data nyata (rilis di Play Store, jumlah pengguna, testimoni asli), bagian-bagian itu bisa ditambahkan.
