"""Contrast check for the landing page (WCAG AA). For ID/EN x light/dark: opens the page in headless Chrome, clicks every tab
(all tab groups), and for every visible text element in the page computes text colour vs the effective background
(alpha composited over its ancestors). Normal text needs 4.5:1, large text (>=24px, or >=18.66px bold) 3:1.
Exit code 1 if anything fails. Usage: python tools/check_contrast.py [--shots DIR]
Needs Google Chrome (path below). With --shots it also saves a screenshot of every business tab (1280 wide, 360 via iframe)."""
import json, os, re, subprocess, sys, tempfile

CH = os.environ.get('CHROME', 'C:/Program Files/Google/Chrome/Application/chrome.exe')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')

JS = r"""
(function(){
function parse(c){var m=c.match(/rgba?\(([^)]+)\)/);if(!m)return null;var p=m[1].split(/[ ,\/]+/).filter(Boolean).map(Number);return {r:p[0],g:p[1],b:p[2],a:p.length>3?p[3]:1};}
function over(f,b){var a=f.a;return {r:f.r*a+b.r*(1-a),g:f.g*a+b.g*(1-a),b:f.b*a+b.b*(1-a),a:1};}
function lum(c){function f(v){v/=255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4);}return 0.2126*f(c.r)+0.7152*f(c.g)+0.0722*f(c.b);}
function ratio(a,b){var x=lum(a),y=lum(b);return (Math.max(x,y)+0.05)/(Math.min(x,y)+0.05);}
function bgOf(el){var chain=[];for(var e=el;e&&e.nodeType===1;e=e.parentElement){var cs=getComputedStyle(e);var c=parse(cs.backgroundColor);if(c&&c.a>0){chain.push(c);if(c.a>=1)break;}}
  var base={r:255,g:255,b:255,a:1};for(var i=chain.length-1;i>=0;i--)base=over(chain[i],base);return base;}
function opacityOf(el){var o=1;for(var e=el;e&&e.nodeType===1;e=e.parentElement){o*=parseFloat(getComputedStyle(e).opacity);}return o;}
function visible(el){for(var e=el;e&&e.nodeType===1;e=e.parentElement){var cs=getComputedStyle(e);if(cs.display==='none'||cs.visibility==='hidden')return false;}return el.getClientRects().length>0;}
function scan(label,out){
  var all=document.body.querySelectorAll('*');
  for(var i=0;i<all.length;i++){var el=all[i];
    if(['SCRIPT','STYLE','svg','path','IMG','NOSCRIPT'].indexOf(el.tagName)>=0)continue;
    var own='';for(var n=el.firstChild;n;n=n.nextSibling){if(n.nodeType===3)own+=n.nodeValue;}
    own=own.trim();if(!own&&!(el.tagName==='INPUT'||el.tagName==='TEXTAREA'))continue;
    if(el.tagName==='INPUT'||el.tagName==='TEXTAREA'){if(!el.value&&!el.placeholder)continue;}
    if(!visible(el))continue;
    var cs=getComputedStyle(el);var fg=parse(cs.color);if(!fg)continue;
    var bg=bgOf(el);var op=opacityOf(el);var f=over({r:fg.r,g:fg.g,b:fg.b,a:fg.a*op},bg);
    var size=parseFloat(cs.fontSize),bold=parseInt(cs.fontWeight,10)>=700;
    var need=(size>=24||(size>=18.66&&bold))?3:4.5;var r=ratio(f,bg);
    if(r<need){out.push({where:label,text:(own||el.value||'').slice(0,40),tag:el.tagName.toLowerCase()+(el.className&&typeof el.className==='string'?'.'+el.className.split(' ')[0]:''),ratio:Math.round(r*100)/100,need:need});}
  }}
window.addEventListener('load',function(){setTimeout(function(){
  var out=[],n=0;
  var groups=document.querySelectorAll('[role=tablist]');
  scan('initial',out);
  groups.forEach(function(g,gi){var tabs=g.querySelectorAll('[role=tab]');tabs.forEach(function(t,ti){t.click();n++;scan('tablist'+gi+'/'+(t.textContent||'').trim().slice(0,24),out);});});
  var pay=document.querySelectorAll('#posPay .chip');if(pay[1]){pay[1].click();document.getElementById('posMake').click();scan('pos-qris',out);}
  var pre=document.createElement('pre');pre.id='__res';pre.textContent=JSON.stringify({tabs:n,fails:out});document.body.appendChild(pre);
},600);});
})();
"""


def run_page(rel, theme):
    src = open(os.path.join(ROOT, rel), encoding='utf-8').read()
    if theme == 'dark':
        src = src.replace('var t="light"', 'var t="dark"', 1)
    # reduced motion keeps the demos still and fast
    src = src.replace('</head>', '<style>*,*::before,*::after{animation:none!important;transition:none!important}</style></head>', 1)
    src = src.replace('</body>', '<script>' + JS + '</script></body>', 1)
    d = os.path.dirname(rel)
    tmp = os.path.join(ROOT, d, '_contrast_tmp.html')
    open(tmp, 'w', encoding='utf-8').write(src)
    try:
        r = subprocess.run([CH, '--headless=new', '--disable-gpu', '--window-size=1280,900', '--virtual-time-budget=12000',
                            '--dump-dom', 'file:///' + ROOT + '/' + (d + '/' if d else '') + '_contrast_tmp.html'],
                           capture_output=True, text=True, encoding='utf-8')
    finally:
        os.remove(tmp)
    m = re.search(r'<pre id="__res">(.*?)</pre>', r.stdout, re.S)
    if not m:
        return None
    import html
    return json.loads(html.unescape(m.group(1)))


def main():
    bad = 0
    for rel in ('index.html', 'en/index.html'):
        for theme in ('light', 'dark'):
            res = run_page(rel, theme)
            if res is None:
                print('%s %s: no result (page script failed)' % (rel, theme)); bad += 1; continue
            seen = set(); fails = []
            for f in res['fails']:
                k = (f['tag'], f['text'], f['ratio'])
                if k not in seen:
                    seen.add(k); fails.append(f)
            print('%s %s: %d tabs clicked, %d contrast failures' % (rel, theme, res['tabs'], len(fails)))
            for f in fails[:25]:
                print('   [%s] <%s> "%s" ratio %s (need %s)' % (f['where'], f['tag'], f['text'], f['ratio'], f['need']))
            bad += len(fails)
    if bad:
        print('FAIL'); sys.exit(1)
    print('OK: all text passes AA')


if __name__ == '__main__':
    main()
