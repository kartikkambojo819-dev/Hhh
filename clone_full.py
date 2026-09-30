import os
from curl_cffi import requests
from bs4 import BeautifulSoup
import urllib.parse

TARGET_URL = "https://ankergames.net"
OUTPUT_DIR = "."

print("[*] Bypassing Cloudflare and downloading full site...")
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
resp = requests.get(TARGET_URL, headers=headers, impersonate="chrome")

if resp.status_code != 200:
    print(f"[!] Error: {resp.status_code}")
    exit()

soup = BeautifulSoup(resp.text, 'html.parser')

# 1. Rebranding & Title Update
if soup.title:
    soup.title.string = "Kartik Kamboj - Free PC Games Hub"

for text_node in soup.find_all(text=True):
    if 'AnkerGames' in text_node or 'Anker Games' in text_node:
        new_text = text_node.replace('AnkerGames', 'Kartik Kamboj').replace('Anker Games', 'Kartik Kamboj')
        text_node.replace_with(new_text)

# 2. Unwanted elements removal (Discord, Donations, Nebulo, Reddit)
for el in soup.find_all(['div', 'a', 'button', 'li']):
    text = el.get_text().strip().lower()
    if any(kw in text for kw in ['discord', 'donation', 'donations', 'nebulo', 'reddit']):
        if len(text) < 40:
            el.decompose()

# 3. Injecting 3D Galaxy background & CSS fixes so design never breaks
style_tag = soup.new_tag('style')
style_tag.string = """
    *{box-sizing:border-box}
    html, body {
        width: 100%; max-width: 100%; overflow-x: hidden;
        background: #04050d !important; color: #eef1ff !important;
        font-family: system-ui, -apple-system, sans-serif !important;
    }
    #bg-canvas {
        position: fixed !important; inset: 0 !important;
        width: 100% !important; height: 100% !important;
        z-index: -999999 !important; pointer-events: none !important;
    }
    nav img, header img, [class*="logo"] img { display: none !important; }
    .brand-title-fixed {
        color: #ffffff !important; font-size: 18px !important;
        font-weight: 900 !important; text-decoration: none !important;
        margin-left: 8px; white-space: nowrap;
    }
"""
if soup.head:
    soup.head.append(style_tag)

# 4. Fix Brand Name in Navbar
navBrand = soup.find('nav') or soup.find('header')
if navBrand:
    for img in navBrand.find_all('img'):
        img['style'] = 'display:none !important;'
    span = soup.new_tag('span')
    span['class'] = 'brand-title-fixed'
    span.string = 'Kartik Kamboj'
    navBrand.append(span)

# 5. Injecting 3D Galaxy Script
script_tag = soup.new_tag('script')
script_tag.string = """
document.addEventListener("DOMContentLoaded", function() {
    if (!document.getElementById('bg-canvas')) {
        const canvas = document.createElement('canvas');
        canvas.id = 'bg-canvas';
        document.body.prepend(canvas);
        var c = canvas, x = c.getContext('2d'), W, H, G = [], F = [], N = 1200, ang = 0, tx = 0, ty = 0, mx = 0, my = 0;
        function rs(){ W = window.innerWidth; H = window.innerHeight; c.width = W * window.devicePixelRatio; c.height = H * window.devicePixelRatio; x.setTransform(window.devicePixelRatio,0,0,window.devicePixelRatio,0,0); }
        function init(){
            G = []; F = [];
            for(var i = 0; i < N; i++){
                var d = Math.pow(Math.random(), .65) * 800 + 10, a = d * .0065 + (i % 3) * 2.09;
                G.push({x: Math.cos(a)*d, z: Math.sin(a)*d, y: (Math.random()-.5)*100, h: 45 + d/800*235, s: Math.random()*1.3+.5});
            }
            for(var j = 0; j < 200; j++) F.push({x: Math.random(), y: Math.random(), p: Math.random()*6.28, s: Math.random()*1.2+.3});
        }
        function fr(t){
            mx += (tx - mx) * .04; my += (ty - my) * .04;
            x.fillStyle = 'rgba(4,5,13,.4)'; x.fillRect(0,0,W,H);
            for(var j = 0; j < F.length; j++){ var f = F[j]; x.fillStyle = 'rgba(255,255,255,'+(.2+.3*Math.sin(t/900+f.p))+')'; x.fillRect(f.x*W, f.y*H, f.s, f.s); }
            var fov = Math.max(W,H)*.8, cx = W/2, cy = H/2;
            var a = ang + mx*.6, ct = Math.cos(1.0+my*.35), st = Math.sin(1.0+my*.35), ca = Math.cos(a), sa = Math.sin(a);
            for(var i = 0; i < G.length; i++){
                var p = G[i], x1 = p.x*ca - p.z*sa, z1 = p.x*sa + p.z*ca, y2 = p.y*ct - z1*st, z2 = p.y*st + z1*ct, dp = z2 + 1300;
                if(dp < 100) continue;
                var k = fov/dp, px = cx + x1*k, py = cy + y2*k;
                if(px < 0 || px > W || py < 0 || py > H) continue;
                x.fillStyle = 'hsla('+p.h+',85%,72%,'+Math.min(1, .25+k*.55)+')';
                var sz = Math.max(.5, p.s*k*1.2);
                x.fillRect(px, py, sz, sz);
            }
            ang += .0015; requestAnimationFrame(fr);
        }
        window.addEventListener('mousemove', e => { tx = (e.clientX/W-.5)*2; ty = (e.clientY/H-.5)*2; });
        window.addEventListener('resize', () => { rs(); init(); });
        rs(); init(); fr(0);
    }
});
"""
if soup.body:
    soup.body.append(script_tag)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(str(soup))

print("[+] Successfully generated clean fixed index.html!")
