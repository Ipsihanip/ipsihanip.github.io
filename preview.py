import sys, threading, functools, http.server, socketserver, json, os
from playwright.sync_api import sync_playwright

ROOT = "/workspace/work/ipsihanip-web"
OUT = "/workspace/attachments/2026-11-22"
os.makedirs(OUT, exist_ok=True)

class S(socketserver.TCPServer):
    allow_reuse_address = True
httpd = S(("127.0.0.1", 0), functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT))
httpd.RequestHandlerClass.log_message = lambda *a: None
PORT = httpd.server_address[1]
threading.Thread(target=httpd.serve_forever, daemon=True).start()

prefix = sys.argv[1] if len(sys.argv) > 1 else "portal"

PROBE = """() => {
  const r = el => { if(!el) return null; const b = el.getBoundingClientRect();
    return [Math.round(b.left), Math.round(b.right), Math.round(b.top), Math.round(b.height)]; };
  const d = document.documentElement;
  const over = [...document.querySelectorAll('body *')].filter(el => {
    const b = el.getBoundingClientRect();
    return b.width > 0 && (b.right > innerWidth + 0.5 || b.left < -0.5);
  }).slice(0, 8).map(el => el.tagName + '.' + (el.className && el.className.toString().slice(0,30))
     + '|' + Math.round(el.getBoundingClientRect().left) + '..' + Math.round(el.getBoundingClientRect().right));
  const cards = [...document.querySelectorAll('.card')].map(c => {
    const b = c.getBoundingClientRect();
    return {top: Math.round(b.top), left: Math.round(b.left), w: Math.round(b.width), h: Math.round(b.height)};
  });
  return {theme: d.getAttribute('data-theme'), scrollW: d.scrollWidth, clientW: d.clientWidth,
    scrollH: d.scrollHeight,
    header: r(document.querySelector('header.top')), brand: r(document.querySelector('.brand')),
    switch: r(document.querySelector('.theme-switch')),
    h1: r(document.querySelector('.hero h1')), lede: r(document.querySelector('.lede')),
    cards, tips: r(document.querySelector('.tips')),
    channels: r(document.querySelector('.channels')), note: r(document.querySelector('.note')),
    over};
}"""

with sync_playwright() as p:
    b = p.chromium.launch()
    cases = [("390-dark", 390, 844, "dark"), ("390-light", 390, 844, "light"),
             ("1440-dark", 1440, 900, "dark"), ("1440-light", 1440, 900, "light"),
             ("768-dark", 768, 1024, "dark")]
    for name, w, h, theme in cases:
        mobile = w < 700
        ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=2,
                            is_mobile=mobile, has_touch=mobile)
        pg = ctx.new_page()
        pg.add_init_script(f"try{{localStorage.setItem('ipsihanip-theme','{theme}')}}catch(e){{}}")
        pg.goto(f"http://127.0.0.1:{PORT}/index.html", wait_until="networkidle")
        pg.wait_for_timeout(500)
        info = pg.evaluate(PROBE)
        print(name, json.dumps(info, ensure_ascii=False), flush=True)
        pg.screenshot(path=f"{OUT}/{prefix}-{name}.png", animations="disabled", full_page=(theme=="dark" and w==390) or False)
        pg.screenshot(path=f"{OUT}/{prefix}-{name}-viewport.png", animations="disabled")
        ctx.close()
    b.close()
httpd.shutdown()
