"""Screenshots every Mode Bisnis tab (ID/EN x light/dark x 360/1280) with headless Chrome.
Usage: python tools/render_bisnis_tabs.py OUT_DIR   (needs Pillow). 360 wide is rendered inside an iframe because
headless Chrome will not make a window narrower than about 500 px."""
import os, subprocess, sys
from PIL import Image

CH = os.environ.get('CHROME', 'C:/Program Files/Google/Chrome/Application/chrome.exe')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'bisnis_tabs')
os.makedirs(OUT, exist_ok=True)
TABS = ['kasir', 'stok', 'po', 'piutang', 'laporan', 'tutup']  # button ids are btab-<name>; resolved by index below


def shot(rel, w, theme, idx, name):
    src = open(os.path.join(ROOT, rel), encoding='utf-8').read()
    if theme == 'dark':
        src = src.replace('var t="light"', 'var t="dark"', 1)
    css = '<style>*,*::before,*::after{animation:none!important;transition:none!important}main>section:not(#bisnis),.foot,header.nav{display:none!important}</style></head>'
    js = ('<script>window.addEventListener("load",function(){setTimeout(function(){'
          'var t=document.querySelectorAll("#bisnis .how--biz [role=tab]")[%d];if(t)t.click();'
          'var h=document.querySelector("#bisnis .how--biz");if(h)h.scrollIntoView();},300);});</script></body>') % idx
    src = src.replace('</head>', css, 1).replace('</body>', js, 1)
    d = os.path.dirname(rel)
    page = (d + '/' if d else '') + '_tab_tmp.html'
    open(os.path.join(ROOT, page), 'w', encoding='utf-8').write(src)
    harness = os.path.join(ROOT, '_tab_h.html')
    H = 1500
    open(harness, 'w').write("<!doctype html><body style='margin:0'><iframe src='%s' style='width:%dpx;height:%dpx;border:0;display:block'></iframe>" % (page, w, H))
    out = os.path.join(OUT, name)
    try:
        subprocess.run([CH, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--virtual-time-budget=9000',
                        '--window-size=%d,%d' % (max(w, 500), H), '--screenshot=' + out, 'file:///' + ROOT + '/_tab_h.html'], capture_output=True)
    finally:
        os.remove(os.path.join(ROOT, page)); os.remove(harness)
    im = Image.open(out).convert('RGB')
    bg = im.getpixel((2, im.size[1] - 1)); px = im.load(); y = im.size[1] - 1
    while y > 0 and all(px[x, y] == bg for x in range(0, min(w, im.size[0]), max(1, w // 40))):
        y -= 1
    im.crop((0, 0, min(w, im.size[0]), min(im.size[1], y + 24))).save(out)


for lang, rel in (('id', 'index.html'), ('en', 'en/index.html')):
    for i, t in enumerate(TABS):
        for theme in ('light', 'dark'):
            for w in (360, 1280):
                shot(rel, w, theme, i, 'tab%d_%s_%s_%s_%d.png' % (i + 1, t, lang, theme, w))
print('done', OUT)
