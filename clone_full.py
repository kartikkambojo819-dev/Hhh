import os
from curl_cffi import requests
from bs4 import BeautifulSoup

TARGET_URL = "https://ankergames.net"
print("[*] Downloading site and applying exact header logo style...")
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
resp = requests.get(TARGET_URL, headers=headers, impersonate="chrome")

if resp.status_code != 200:
    print(f"[!] Error: {resp.status_code}")
    exit()

soup = BeautifulSoup(resp.text, 'html.parser')

if soup.title:
    soup.title.string = "Kartik Kamboj - Free PC Games Hub"

# Replace text references across the site
for element in soup.find_all(text=True):
    if element.parent.name not in ['style', 'script', '[document]']:
        new_text = element.replace('AnkerGames', 'Kartik Kamboj').replace('Anker Games', 'Kartik Kamboj').replace('ANKER GAMES', 'KARTIK KAMBOJ').replace('ankergames', 'kartikkamboj')
        if new_text != element:
            element.replace_with(new_text)

# CSS Styling to inject the exact glowing crown logo and clean background
style_tag = soup.new_tag('style')
style_tag.string = """
    html, body {
        background: #04050d !important; color: #eef1ff !important;
        overflow-x: hidden !important;
    }
    #bg-canvas {
        position: fixed !important; inset: 0 !important;
        width: 100% !important; height: 100% !important;
        z-index: -999999 !important; pointer-events: none !important;
    }
    /* Hide original text logo or images inside the header */
    header img, nav img, .brand-logo, [class*="logo"] img {
        display: none !important;
    }
    /* Exact match for the glowing Kartik Kamboj header logo with crown */
    .exact-kartik-header-logo {
        text-align: center;
        padding: 15px 10px 5px 10px;
        margin: 0 auto;
        display: block;
        width: 100%;
    }
    .crown-icon {
        font-size: 22px;
        color: #00d2ff;
        display: block;
        text-align: center;
        margin-bottom: -6px;
        filter: drop-shadow(0 0 8px #00d2ff);
    }
    .kartik-text-main {
        font-family: 'Impact', 'Arial Black', sans-serif;
        font-size: 32px;
        font-weight: 900;
        font-style: italic;
        text-transform: uppercase;
        background: linear-gradient(180deg, #ffffff 20%, #bfe9ff 50%, #0072ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 2px 10px rgba(0, 114, 255, 0.8));
        letter-spacing: 1.5px;
        line-height: 1.1;
    }
    .kamboj-text-sub {
        font-family: 'Impact', 'Arial Black', sans-serif;
        font-size: 34px;
        font-weight: 900;
        font-style: italic;
        text-transform: uppercase;
        background: linear-gradient(180deg, #ffffff 10%, #6be3ff 50%, #0044cc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 2px 10px rgba(0, 114, 255, 0.8));
        letter-spacing: 2px;
        margin-top: -4px;
        display: block;
    }
    .logo-glow-line {
        height: 3px;
        width: 60%;
        max-width: 250px;
        background: linear-gradient(90deg, transparent, #00d2ff, transparent);
        margin: 8px auto 15px auto;
        box-shadow: 0 0 12px #00d2ff;
    }
"""
if soup.head:
    soup.head.append(style_tag)

# Create the exact header logo HTML structure
logo_container = soup.new_tag('div')
logo_container['class'] = 'exact-kartik-header-logo'

crown_span = soup.new_tag('span')
crown_span['class'] = 'crown-icon'
crown_span.string = '👑'

kartik_span = soup.new_tag('span')
kartik_span['class'] = 'kartik-text-main'
kartik_span.string = 'KARTIK'

br_tag = soup.new_tag('br')

kamboj_span = soup.new_tag('span')
kamboj_span['class'] = 'kamboj-text-sub'
kamboj_span.string = 'KAMBOJ'

line_div = soup.new_tag('div')
line_div['class'] = 'logo-glow-line'

logo_container.append(crown_span)
logo_container.append(kartik_span)
logo_container.append(br_tag)
logo_container.append(kamboj_span)
logo_container.append(line_div)

# Insert the logo right at the top of the main container or body header area
target_insert = soup.find('header') or soup.find('nav') or soup.find('main') or soup.body
if target_insert:
    target_insert.insert(0, logo_container)

# 3D Galaxy Script & Download Protection
script_tag = soup.new_tag('script')
script_tag.string = """
document.addEventListener("DOMContentLoaded", function() {
    document.addEventListener('click', function(e) {
        let target = e.target.closest('a');
        if (target && target.href) {
            let href = target.href.toLowerCase();
            if (href.includes('download') || href.includes('file') || href.includes('mega') || href.includes('drive')) {
                target.setAttribute('target', '_blank');
            }
        }
    });

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

print("[+] Successfully added exact glowing logo and pushed to Git!")
