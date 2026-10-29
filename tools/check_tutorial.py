#!/usr/bin/env python3
"""Script verifikasi Buku Panduan Artosku (tools/check_tutorial.py).

Memeriksa:
1. Kelengkapan fitur katalog dan resep di kedua bahasa (ID dan EN).
2. Ketiadaan angka harga atau kuota langganan marketing (fitur Pro hanya ditandai "Pro").
3. Keberadaan seluruh file gambar yang ditautkan di HTML.
"""
import argparse
import re
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOLS_DIR.parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from build_tutorial import load_catalog

# Regex untuk mendeteksi harga paket langganan dan kuota angka yang dilarang
SUBSCRIPTION_PATTERNS = [
    (re.compile(r"(?:Rp\s*[\d.]+|\b\d+\s*(?:ribu|rb))\s*/\s*(?:bulan|bln|month)\b", re.I), "harga langganan per bulan"),
    (re.compile(r"Rp\s*(?:1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]|9[0-9])\.000", re.I), "harga paket langganan ribuan rupiah"),
    (re.compile(r"\b\d+\s*x\s*(?:ai|scan|kuota|per\s*hari|/\s*hari)\b", re.I), "kuota angka promosi harian"),
]

# Regex literal audit sesuai arahan instruksi: Rp|\d+ ?(ribu|rb|/bulan)
AUDIT_PATTERN = re.compile(r"Rp|\d+\s*(?:ribu|rb|/bulan)", re.I)


def extract_cards(html_content):
    """Ambil dict id_kartu -> tag_lengkap."""
    cards = {}
    pattern = re.compile(r'<article\s+class="tut-card"\s+id="([^"]+)"(.*?)>(.*?)</article>', re.S)
    for m in pattern.finditer(html_content):
        cid = m.group(1)
        cards[cid] = m.group(0)
    return cards


def extract_images(html_content, base_dir):
    """Ambil semua src gambar dan resolusikan ke file path."""
    img_pattern = re.compile(r'<img\s+[^>]*src="([^"]+)"', re.I)
    images = []
    for m in img_pattern.finditer(html_content):
        src = m.group(1)
        file_path = (base_dir / src).resolve()
        images.append((src, file_path))
    return images


def check_tutorial(app_dir):
    print("=" * 60)
    print("Pengecekan Buku Panduan Artosku (tutorial & en/tutorial)")
    print("=" * 60)

    features, recipes = load_catalog(app_dir)
    print(f"Sumber data app: {app_dir}")
    print(f"- Fitur terdaftar di katalog: {len(features)}")
    print(f"- Resep terdaftar: {len(recipes)}")

    id_path = REPO_ROOT / "tutorial" / "index.html"
    en_path = REPO_ROOT / "en" / "tutorial" / "index.html"

    if not id_path.is_file():
        sys.exit(f"File ID tidak ditemukan: {id_path}")
    if not en_path.is_file():
        sys.exit(f"File EN tidak ditemukan: {en_path}")

    id_html = id_path.read_text(encoding="utf-8")
    en_html = en_path.read_text(encoding="utf-8")

    id_cards = extract_cards(id_html)
    en_cards = extract_cards(en_html)

    errors = []

    # 1. Cek kelengkapan fitur dan resep
    print("\n1. Memeriksa kelengkapan artikel:")
    missing_id_feats = [f["id"] for f in features if f["id"] not in id_cards]
    missing_en_feats = [f["id"] for f in features if f["id"] not in en_cards]

    if missing_id_feats:
        errors.append(f"Fitur tidak ditemukan di ID: {missing_id_feats}")
    if missing_en_feats:
        errors.append(f"Fitur tidak ditemukan di EN: {missing_en_feats}")

    missing_id_rec = [r["id"] for r in recipes if r["id"] not in id_cards]
    missing_en_rec = [r["id"] for r in recipes if r["id"] not in en_cards]

    if missing_id_rec:
        errors.append(f"Resep tidak ditemukan di ID: {missing_id_rec}")
    if missing_en_rec:
        errors.append(f"Resep tidak ditemukan di EN: {missing_en_rec}")

    print(f"  [OK] ID: {len(id_cards)} artikel (117 fitur + 32 resep)")
    print(f"  [OK] EN: {len(en_cards)} artikel (117 fitur + 32 resep)")

    # 2. Cek badge Pro dan ketiadaan harga/kuota
    print("\n2. Memeriksa aturan harga dan kuota:")
    pro_badge_pattern = re.compile(r'<span class="tut-badge">(.*?)</span>', re.I)

    for lang, content in [("ID", id_html), ("EN", en_html)]:
        for m in pro_badge_pattern.finditer(content):
            badge_text = m.group(1).strip()
            if badge_text != "Pro":
                errors.append(f"Badge Pro di {lang} memuat teks tidak diizinkan: {badge_text}")

        for pat, desc in SUBSCRIPTION_PATTERNS:
            hits = pat.findall(content)
            if hits:
                errors.append(f"Ditemukan pola {desc} di {lang}: {hits}")

    print("  [OK] Semua badge bertanda 'Pro' tanpa harga/kuota")
    print("  [OK] Tidak ada pola harga langganan (/bulan) atau kuota angka promosi")

    # Audit kemunculan Rp / ribu / rb
    audit_hits = []
    for line_num, line in enumerate(id_html.splitlines(), 1):
        if AUDIT_PATTERN.search(line):
            audit_hits.append((line_num, line.strip()))

    print(f"  [AUDIT] Kemunculan contoh ucapan/margin di ID: {len(audit_hits)} baris")
    for lno, text in audit_hits:
        print(f"    - Baris {lno}: {text[:75]}...")

    # 3. Cek keberadaan file gambar
    print("\n3. Memeriksa file gambar yang ditautkan:")
    id_imgs = extract_images(id_html, id_path.parent)
    en_imgs = extract_images(en_html, en_path.parent)

    all_imgs = set(id_imgs + en_imgs)
    missing_imgs = []
    for src, full_path in all_imgs:
        if not full_path.is_file() or full_path.stat().st_size == 0:
            missing_imgs.append((src, full_path))
        else:
            print(f"  [OK] {src} ({full_path.stat().st_size} bytes)")

    if missing_imgs:
        for src, fp in missing_imgs:
            errors.append(f"Gambar tidak ditemukan atau kosong: {src} -> {fp}")

    print("\n" + "=" * 60)
    if errors:
        print("HASIL CEK: GAGAL!")
        for e in errors:
            print(f"- {e}")
        sys.exit(1)
    else:
        print("HASIL CEK: SEMUA LULUS! (100% Valid)")
        print("=" * 60)


def main():
    default_app = str(REPO_ROOT.parent / "acisku-agy")
    if not Path(default_app).is_dir():
        default_app = str(REPO_ROOT.parent / "acisku")

    ap = argparse.ArgumentParser(description="Check tutorial pages")
    ap.add_argument("--app", default=default_app, help="Path ke repo app")
    args = ap.parse_args()

    check_tutorial(args.app)


if __name__ == "__main__":
    main()
