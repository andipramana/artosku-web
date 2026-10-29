#!/usr/bin/env python3
"""Membangun Buku Panduan statis (ID dan EN) dari katalog AI Chat app Artosku.

Sumber data tunggal:
- acisku-agy/lib/features/ai_chat/ (feature_catalog*.dart, feature_steps*.dart, feature_recipes.dart).
Dibaca strictly read-only tanpa modifikasi pada app.

Output:
- tutorial/index.html (Bahasa Indonesia)
- en/tutorial/index.html (English)

Menghasilkan file secara deterministik.
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path

# Impor konfigurasi konten tulisan tangan
TOOLS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOLS_DIR.parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from tutorial_content import GROUPS, START, UI

CATALOG_DIR = Path("lib/features/ai_chat")
CATALOG_FILES = [
    "feature_catalog.dart",
    "feature_subfeatures.dart",
    "feature_personal_settings.dart",
    "feature_business.dart",
]
STEP_FILES = [
    "feature_steps.dart",
    "feature_personal_settings_steps.dart",
    "feature_business_steps.dart",
]
RECIPE_FILE = "feature_recipes.dart"

FEATURE_SHOTS = {
    "catat_transaksi": {
        "file": "tutorial_step2_transaction.png",
        "w": 360,
        "h": 760,
        "alt_id": "Form transaksi dengan tombol Simpan disorot",
        "alt_en": "Transaction form with Save button highlighted",
    },
    "catat_ai_suara": {
        "file": "tutorial_step3_ai.png",
        "w": 360,
        "h": 412,
        "alt_id": "Layar Catat pakai AI dengan hasil dan tombol Simpan Semua disorot",
        "alt_en": "Record with AI screen with results and Save All button highlighted",
    },
    "jatah_harian": {
        "file": "tutorial_step4_allowance.png",
        "w": 360,
        "h": 521,
        "alt_id": "Layar Jatah Harian kosong dengan tombol Buat jatah harian disorot",
        "alt_en": "Empty Daily Allowance screen with Create daily allowance button highlighted",
    },
}


# ----------------------------------------------------------------------------
# Pembaca literal Dart
# ----------------------------------------------------------------------------

class Call:
    def __init__(self, name, args, pos):
        self.name, self.args, self.pos = name, args, pos


class Ident:
    def __init__(self, name):
        self.name = name


class Spread:
    def __init__(self, name):
        self.name = name


class Rec:
    def __init__(self, fields):
        self.fields = fields


TOKEN_RE = re.compile(
    r"""
    (?P<ws>\s+|//[^\n]*|/\*.*?\*/)
  | (?P<str>r?'(?:\\.|[^'\\])*'|r?"(?:\\.|[^"\\])*")
  | (?P<num>-?\d+(?:\.\d+)?)
  | (?P<id>[A-Za-z_$][A-Za-z0-9_$]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*)
  | (?P<spread>\.\.\.)
  | (?P<p>[()\[\]{},:;=<>?+\-*/])
  | (?P<x>.)
    """,
    re.X | re.S,
)

ESCAPES = {"n": "\n", "t": "\t", "'": "'", '"': '"', "\\": "\\", "$": "$"}


def tokenize(src):
    pos, out = 0, []
    while pos < len(src):
        m = TOKEN_RE.match(src, pos)
        if not m:
            raise SyntaxError("karakter tidak dikenal di %d: %r" % (pos, src[pos:pos + 30]))
        pos = m.end()
        kind = m.lastgroup
        if kind in ("ws", "x"):
            continue
        out.append((kind, m.group(kind), m.start()))
    return out


def unquote(raw, consts):
    is_raw = raw.startswith("r")
    body = raw[1:] if is_raw else raw
    body = body[1:-1]
    if is_raw:
        return body
    out, i = [], 0
    while i < len(body):
        c = body[i]
        if c == "\\" and i + 1 < len(body):
            n = body[i + 1]
            out.append(ESCAPES.get(n, n))
            i += 2
        elif c == "$":
            m = re.match(r"\$\{(\w+)\}|\$(\w+)", body[i:])
            if not m:
                out.append(c)
                i += 1
                continue
            name = m.group(1) or m.group(2)
            if name not in consts:
                raise KeyError("konstanta string tidak dikenal: $" + name)
            out.append(consts[name])
            i += m.end()
        else:
            out.append(c)
            i += 1
    return "".join(out)


class Parser:
    def __init__(self, src):
        self.src = src
        self.toks = tokenize(src)
        self.i = 0
        self.consts = {}

    def peek(self, k=0):
        j = self.i + k
        return self.toks[j] if j < len(self.toks) else (None, None, None)

    def eat(self, val=None):
        t = self.toks[self.i]
        if val is not None and t[1] != val:
            raise SyntaxError("harap %r, dapat %r di %d" % (val, t[1], t[2]))
        self.i += 1
        return t

    def value(self):
        k, v, pos = self.peek()
        if k == "str":
            parts = []
            while self.peek()[0] == "str":
                parts.append(unquote(self.eat()[1], self.consts))
            s = "".join(parts)
            while self.peek()[1] == "+" and self.peek(1)[0] == "str":
                self.eat()
                s += unquote(self.eat()[1], self.consts)
            return s
        if k == "num":
            return float(self.eat()[1])
        if k == "spread":
            self.eat()
            return Spread(self.eat()[1])
        if v == "<":
            depth = 0
            while True:
                t = self.eat()[1]
                depth += (t == "<") - (t == ">")
                if depth == 0:
                    break
            return self.value()
        if v == "[":
            self.eat()
            items = []
            while self.peek()[1] != "]":
                items.append(self.value())
                if self.peek()[1] == ",":
                    self.eat()
            self.eat("]")
            return items
        if v == "{":
            self.eat()
            items = []
            while self.peek()[1] != "}":
                key = self.value()
                if self.peek()[1] == ":":
                    self.eat()
                    items.append((key, self.value()))
                else:
                    items.append((None, key))
                if self.peek()[1] == ",":
                    self.eat()
            self.eat("}")
            return items
        if k == "id":
            name = self.eat()[1]
            if self.peek()[1] == "(":
                self.eat()
                args, pos_args = {}, []
                while self.peek()[1] != ")":
                    if self.peek()[0] == "id" and self.peek(1)[1] == ":":
                        key = self.eat()[1]
                        self.eat(":")
                        args[key] = self.value()
                    else:
                        pos_args.append(self.value())
                    if self.peek()[1] == ",":
                        self.eat()
                self.eat(")")
                args["_pos"] = pos_args
                return Call(name, args, pos)
            return Ident(name)
        if v == "(":
            self.eat()
            fields = {}
            while self.peek()[1] != ")":
                key = self.eat()[1]
                self.eat(":")
                fields[key] = self.value()
                if self.peek()[1] == ",":
                    self.eat()
            self.eat(")")
            return Rec(fields)
        raise SyntaxError("nilai tak terduga %r di %d" % (v, pos))


def parse_file(path):
    src = Path(path).read_text(encoding="utf-8")
    p = Parser(src)
    top = {}
    for m in re.finditer(r"^const\s+(_\w+)\s*=\s*('(?:\\.|[^'\\])*')\s*;", src, re.M):
        p.consts[m.group(1)] = unquote(m.group(2), p.consts)
    for m in re.finditer(r"^const\s+(?:([^=;]*?)\s+)?(\w+)\s*=\s*", src, re.M):
        name = m.group(2)
        if name.startswith("_") and name in p.consts:
            continue
        start = next((i for i, t in enumerate(p.toks) if t[2] >= m.end()), None)
        if start is None:
            continue
        p.i = start
        try:
            top[name] = p.value()
        except Exception as e:
            raise RuntimeError("%s: gagal membaca %s: %s" % (path, name, e))
    return top, p.consts


def ident_name(v):
    return v.name.split(".")[-1] if isinstance(v, Ident) else None


# ----------------------------------------------------------------------------
# Muat Katalog dan Resep
# ----------------------------------------------------------------------------

def load_catalog(app_dir):
    base = Path(app_dir) / CATALOG_DIR
    if not base.is_dir():
        sys.exit("Folder katalog tidak ditemukan: %s (pakai --app untuk menunjuk folder app)" % base)
    tops = {}
    for f in CATALOG_FILES + STEP_FILES:
        t, _ = parse_file(base / f)
        for k, v in t.items():
            tops.setdefault(k, v)

    features = []
    for listname in ("_baseFeatures", "subFeatures", "personalSettingsFeatures", "businessFeatures"):
        if listname not in tops:
            sys.exit("Daftar %s tidak ditemukan di katalog" % listname)
        for c in tops[listname]:
            if not isinstance(c, Call) or c.name != "AppFeature":
                raise RuntimeError("isi %s bukan AppFeature (%r)" % (listname, c))
            a = c.args
            features.append({
                "id": a["id"],
                "emoji": a.get("emoji", ""),
                "nameId": a["nameId"],
                "nameEn": a["nameEn"],
                "benefitId": a["benefitId"],
                "benefitEn": a["benefitEn"],
                "keywords": list(a.get("keywords", [])),
                "menuId": a.get("menuId"),
                "menuEn": a.get("menuEn"),
                "route": a.get("route"),
                "mode": ident_name(a.get("mode")) or "both",
                "plan": ident_name(a.get("plan")) or "free",
                "parent": a.get("parent"),
                "action": ident_name(a.get("action")),
                "source": listname,
                "isRecipe": False,
            })

    steps = {}
    for name in ("featureSteps", "personalSettingsSteps", "businessFeatureSteps"):
        for k, v in tops.get(name, []):
            if k is None:
                continue
            steps[k] = {"id": list(v.fields["id"]), "en": list(v.fields["en"])}

    def kwmap(name):
        return {k: list(v) for k, v in tops.get(name, []) if k is not None}

    extra = kwmap("featureExtraKeywords")
    sub = kwmap("featureSubMenuKeywords")

    out = []
    for f in features:
        s = steps.get(f["id"])
        f["stepsId"] = s["id"] if s else []
        f["stepsEn"] = s["en"] if s else []
        if s and len(s["id"]) != len(s["en"]):
            print("PERINGATAN: langkah ID/EN beda jumlah: %s" % f["id"], file=sys.stderr)
        kws = f["keywords"] + extra.get(f["id"], []) + sub.get(f["id"], [])
        seen, uniq = set(), []
        for k in kws:
            if k.lower() not in seen:
                seen.add(k.lower())
                uniq.append(k)
        f["allKeywords"] = uniq
        out.append(f)

    # Muat resep (tujuan umum)
    recipes = []
    recipe_path = base / RECIPE_FILE
    if recipe_path.is_file():
        t_recipe, _ = parse_file(recipe_path)
        raw_recipes = t_recipe.get("appRecipes", [])
        for r in raw_recipes:
            if isinstance(r, Call) and r.name == "AppRecipe":
                a = r.args
                phrases = list(a.get("phrases", []))
                recipes.append({
                    "id": a["id"],
                    "nameId": a["nameId"],
                    "nameEn": a["nameEn"],
                    "benefitId": "",
                    "benefitEn": "",
                    "keywords": phrases,
                    "allKeywords": phrases,
                    "stepsId": list(a.get("stepsId", [])),
                    "stepsEn": list(a.get("stepsEn", [])),
                    "featureIds": list(a.get("featureIds", [])),
                    "mode": ident_name(a.get("mode")) or "both",
                    "plan": ident_name(a.get("plan")) or "free",
                    "isRecipe": True,
                })

    return out, recipes


def group_items(features, recipes):
    feat_map = {f["id"]: f for f in features}
    assigned_feats = set()
    groups_data = []

    for gid, name_id, name_en, ids in GROUPS:
        items = []
        if gid == "bisnis":
            for f in features:
                if f["mode"] == "business":
                    items.append(f)
                    assigned_feats.add(f["id"])
            for r in recipes:
                if r["mode"] == "business":
                    items.append(r)
        elif gid == "pengaturan":
            for f in features:
                if f["id"] not in assigned_feats and f["mode"] != "business":
                    items.append(f)
                    assigned_feats.add(f["id"])
        elif gid == "tujuan":
            for r in recipes:
                if r["mode"] != "business":
                    items.append(r)
        else:
            for fid in ids:
                if fid in feat_map:
                    items.append(feat_map[fid])
                    assigned_feats.add(fid)

        if items:
            groups_data.append({
                "id": gid,
                "nameId": name_id,
                "nameEn": name_en,
                "items": items,
            })
    return groups_data


# ----------------------------------------------------------------------------
# Perender HTML
# ----------------------------------------------------------------------------

def render_card(item, lang, root):
    title = html.escape(item["nameId"] if lang == "id" else item["nameEn"])
    intro = html.escape(item["benefitId"] if lang == "id" else item["benefitEn"])
    steps = item["stepsId"] if lang == "id" else item["stepsEn"]
    kw_str = html.escape(" ".join(item["allKeywords"]))

    badge = ' <span class="tut-badge">Pro</span>' if item.get("plan") in ("pro", "max") else ""

    lines = [
        f'      <article class="tut-card" id="{item["id"]}" data-title="{title}" data-keywords="{kw_str}">',
        f'        <h3>{title}{badge}</h3>',
    ]
    if intro:
        lines.append(f'        <p class="tut-intro">{intro}</p>')
    if steps:
        lines.append('        <ol>')
        for s in steps:
            lines.append(f'          <li>{html.escape(s)}</li>')
        lines.append('        </ol>')

    if item["id"] in FEATURE_SHOTS:
        shot = FEATURE_SHOTS[item["id"]]
        alt = shot["alt_id"] if lang == "id" else shot["alt_en"]
        lines.append(
            f'        <figure class="tut-shot"><img src="{root}assets/tutorial/{shot["file"]}" '
            f'alt="{html.escape(alt)}" width="{shot["w"]}" height="{shot["h"]}" loading="lazy" /></figure>'
        )

    lines.append('      </article>')
    return "\n".join(lines)


def render_start_section(lang, root):
    start_info = START[lang]
    lead = html.escape(start_info["lead"])
    h_title = "Mulai dari sini" if lang == "id" else "Start here"

    lines = [
        f'    <section class="tut-start" id="mulai" aria-labelledby="mulai-h">',
        f'      <h2 id="mulai-h">{h_title}</h2>',
        f'      <p class="tut-lead">{lead}</p>',
        f'      <ol class="tut-steps">',
    ]

    for i, (title, html_body) in enumerate(start_info["steps"]):
        lines.append('        <li>')
        lines.append(f'          <h3>{html.escape(title)}</h3>')
        lines.append(f'          {html_body}')
        if i == 0:
            alt = "Layar Beranda kosong dengan tombol Buat Contoh disorot" if lang == "id" else "Empty Home screen with Create Samples button highlighted"
            shot_html = (
                f'          <figure class="tut-shot"><img src="{root}assets/tutorial/tutorial_step1_wallet.png" '
                f'alt="{alt}" width="360" height="577" loading="lazy" /></figure>'
            )
            lines.append(shot_html)
        lines.append('        </li>')

    lines.append('      </ol>')
    lines.append('    </section>')
    return "\n".join(lines)


def render_page(groups, lang, template_str):
    ui = UI[lang]
    root = ui["root"]

    # Nav links
    nav_links = []
    nav_links_mobile = []
    for label, target in ui["nav"]:
        if target is None:
            nav_links.append(f'      <a href="./" aria-current="page">{label}</a>')
            nav_links_mobile.append(f'    <a href="./">{label}</a>')
        else:
            href = f"{root}{target}" if lang == "id" else f"{root}en/{target}"
            nav_links.append(f'      <a href="{href}">{label}</a>')
            nav_links_mobile.append(f'    <a href="{href}">{label}</a>')
    nav_links_html = "\n".join(nav_links)
    nav_links_mobile_html = "\n".join(nav_links_mobile)

    # Footer links
    footer_links = []
    for label, target in ui["nav"]:
        if target is None:
            footer_links.append(f'      <a href="./">{label}</a>')
        else:
            href = f"{root}{target}" if lang == "id" else f"{root}en/{target}"
            footer_links.append(f'      <a href="{href}">{label}</a>')
    footer_links_html = "\n".join(footer_links)

    # TOC
    start_label = ui["start"]
    toc_links = [f'        <a href="#mulai">{start_label}</a>']
    for g in groups:
        gname = g["nameId"] if lang == "id" else g["nameEn"]
        toc_links.append(f'        <a href="#g-{g["id"]}">{html.escape(gname)}</a>')
    toc_html = "\n".join(toc_links)

    # Start section
    start_html = render_start_section(lang, root)

    # Groups section
    groups_blocks = []
    for g in groups:
        gid = g["id"]
        gname = html.escape(g["nameId"] if lang == "id" else g["nameEn"])
        lines = [
            f'    <section class="tut-group" id="g-{gid}" aria-labelledby="h-g-{gid}">',
            f'      <h2 id="h-g-{gid}">{gname}</h2>',
        ]
        for item in g["items"]:
            lines.append(render_card(item, lang, root))
        lines.append('    </section>')
        groups_blocks.append("\n".join(lines))
    groups_html = "\n\n".join(groups_blocks)

    # Ganti token template
    replacements = {
        "{{LANG}}": ui["lang"],
        "{{TITLE}}": ui["title"],
        "{{DESC}}": ui["desc"],
        "{{CANONICAL}}": f"https://artosku.my.id{ui['path']}",
        "{{OG_DESC}}": ui["og_desc"],
        "{{ROOT}}": root,
        "{{OTHER_HREF}}": ui["other"],
        "{{OTHER_LANG}}": "en" if lang == "id" else "id",
        "{{OTHER_NAME}}": ui["other_name"],
        "{{SKIP_LINK_TEXT}}": ui["skip"],
        "{{NAV_MAIN_LABEL}}": ui["nav_main"],
        "{{NAV_MOBILE_LABEL}}": ui["nav_mobile"],
        "{{NAV_FOOTER_LABEL}}": ui["nav_footer"],
        "{{NAV_LINKS_HTML}}": nav_links_html,
        "{{NAV_LINKS_MOBILE_HTML}}": nav_links_mobile_html,
        "{{FOOTER_LINKS_HTML}}": footer_links_html,
        "{{THEME_TOGGLE_LABEL}}": ui["theme"],
        "{{DOWNLOAD_LABEL}}": ui["download"],
        "{{MENU_TOGGLE_LABEL}}": ui["menu"],
        "{{HERO_H1}}": ui["h1"],
        "{{HERO_P}}": ui["sub"],
        "{{SEARCH_PLACEHOLDER}}": ui["search_ph"],
        "{{SEARCH_LABEL}}": ui["search_label"],
        "{{TOC_LABEL}}": ui["toc"],
        "{{TOC_LINKS_HTML}}": toc_html,
        "{{START_SECTION_HTML}}": start_html,
        "{{GROUPS_HTML}}": groups_html,
        "{{EMPTY_SEARCH_HTML}}": ui["empty"],
        "{{CTA_H2}}": ui["cta_h"],
        "{{CTA_P}}": ui["cta_p"],
        "{{CTA_BTN}}": ui["cta"],
        "{{PRIVACY_TEXT}}": ui["privacy"],
        "{{PRIVACY_HREF}}": f"{root}{ui['privacy_href']}",
        "{{TERMS_TEXT}}": ui["terms"],
        "{{TERMS_HREF}}": f"{root}{ui['terms_href']}",
        "{{MADE_BY}}": ui["made"],
    }

    out = template_str
    for k, v in replacements.items():
        out = out.replace(k, v)
    return out


# ----------------------------------------------------------------------------
# Main CLI
# ----------------------------------------------------------------------------

def build_all(app_dir):
    features, recipes = load_catalog(app_dir)
    groups = group_items(features, recipes)

    template_file = TOOLS_DIR / "tutorial_template.html"
    template_str = template_file.read_text(encoding="utf-8")

    id_html = render_page(groups, "id", template_str)
    en_html = render_page(groups, "en", template_str)

    id_out = REPO_ROOT / "tutorial" / "index.html"
    en_out = REPO_ROOT / "en" / "tutorial" / "index.html"

    id_out.parent.mkdir(parents=True, exist_ok=True)
    en_out.parent.mkdir(parents=True, exist_ok=True)

    id_out.write_text(id_html, encoding="utf-8", newline="\n")
    en_out.write_text(en_html, encoding="utf-8", newline="\n")

    total_articles = sum(len(g["items"]) for g in groups)
    print(f"Buku Panduan dibangun dari: {app_dir}")
    print(f"- Fitur: {len(features)}, Resep: {len(recipes)}, Total artikel per bahasa: {total_articles}")
    print(f"- ID: {id_out} ({len(id_html)} byte)")
    print(f"- EN: {en_out} ({len(en_html)} byte)")
    return features, recipes, groups


def main():
    default_app = str(REPO_ROOT.parent / "acisku-agy")
    if not Path(default_app).is_dir():
        default_app = str(REPO_ROOT.parent / "acisku")

    ap = argparse.ArgumentParser(description="Build Artosku Tutorial pages")
    ap.add_argument("--app", default=default_app, help="Path ke repo app acisku/acisku-agy")
    args = ap.parse_args()

    build_all(args.app)


if __name__ == "__main__":
    main()
