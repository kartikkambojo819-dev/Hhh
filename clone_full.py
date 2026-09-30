import os
from curl_cffi import requests
from bs4 import BeautifulSoup

TARGET_URL = "https://ankergames.net"
print("[*] Downloading and adding clean professional ad banner...")
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
resp = requests.get(TARGET_URL, headers=headers, impersonate="chrome")

if resp.status_code != 200:
    print(f"[!] Error: {resp.status_code}")
    exit()

soup = BeautifulSoup(resp.text, 'html.parser')

# 1. Title Update
if soup.title:
    soup.title.string = "Kartik Kamboj - Free PC Games Hub"

# 2. Replace Anker text globally across text nodes
for element in soup.find_all(text=True):
    if element.parent.name not in ['style', 'script', '[document]']:
        new_text = element.replace('AnkerGames', 'Kartik Kamboj').replace('Anker Games', 'Kartik Kamboj').replace('ANKER GAMES', 'Kartik Kamboj').replace('ankergames', 'kartikkamboj')
        if new_text != element:
            element.replace_with(new_text)

# 3. Remove unwanted clutter
for el in soup.find_all(['div', 'a', 'button', 'li']):
    text = el.get_text().strip().lower()
    if any(kw in text for kw in ['discord', 'donation', 'donations', 'nebulo', 'reddit']):
        if len(text) < 40:
            el.decompose()

# 4. Inject CSS for 3D background, clean header branding, and a gorgeous modern ad banner style
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
    header img, nav img, .brand-logo, [class*="logo"] img {
        display: none !important;
    }
    .brand-title-fixed-header {
        color: #ffffff !important;
        font-size: 20px !important;
        font-weight: 900 !important;
        text-decoration: none !important;
        display: inline-block !important;
        margin-left: 12px !important;
        letter-spacing: 0.5px;
        white-space: nowrap;
    }
    /* First Promo Banner Style */
    .custom-promo-banner {
        background: linear-gradient(135deg, #ff416c, #ff4b2b);
        color: #ffffff;
        padding: 12px 20px;
        text-align: center;
        font-weight: 700;
        font-size: 14px;
        box-shadow: 0 4px 15px rgba(255, 65, 108, 0.4);
        position: relative;
        z-index: 99;
        margin: 12px auto;
        max-width: 90%;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        text-decoration: none;
        transition: transform 0.2s ease;
    }
    .custom-promo-banner:hover { transform: scale(1.02); }

    /* Second Sleek Ad Network Banner Style (Clean & Premium) */
    .custom-ad-partner-banner {
        background: linear-gradient(135deg, #00c6ff, #0072ff);
        color: #ffffff;
        padding: 12px 20px;
        text-align: center;
        font-weight: 700;
        font-size: 14px;
        box-shadow: 0 4px 15px rgba(0, 114, 255, 0.4);
        position: relative;
        z-index: 99;
        margin: 10px auto 15px auto;
        max-width: 90%;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        text-decoration: none;
        transition: transform 0.2s ease;
    }
    .custom-ad-partner-banner:hover { transform: scale(1.02); }
"""
if soup.head:
    soup.head.append(style_tag)

# 5. Insert Kartik Kamboj title in header
nav_el = soup.find('nav') or soup.find('header')
if nav_el:
    brand_span = soup.new_tag('span')
    brand_span['class'] = 'brand-title-fixed-header'
    brand_span.string = 'Kartik Kamboj'
    nav_el.insert(0, brand_span)

# 6. Insert both promotional banners cleanly at the top of main content
container_div = soup.find('main') or soup.find('div', class_='container') or soup.body
if container_div:
    # First banner (Utility app)
    target_url_banner1 = "https://ultranova-tools.com/preland/storage/ut/privygo_brwsr/utility-app-f/apk/2/index.html?land_id=6792385&p1=https%3A%2F%2Fplay.google.com%2Fstore%2Fapps%2Fdetails%3Fid%3Dcom.privygo.go%26listing%3Dp_1%26referrer%3Dutm_source%253Dall_99_1476223%2526utm_content%253D7089e6b9be67a22383603c1ddbba2ea6%2526utm_medium%253Daffiliate%2526utm_campaign%253Dall_99_1476223_IN_pg%2526PLACEMENT_ID%253D31490188%2526time%253D%257Btime%257D%2526adimp%253D1%2526rl%253Dhttps%25253A%25252F%25252Fmeetsweetmeet.com%25252F%25253Fparams%25253DdisableAd-true%2526rl_t%253D18%25252B%2526rl_i%253Dhttps%25253A%25252F%25252Ffirebasestorage.googleapis.com%25252Fv0%25252Fb%25252Fsb-1-fe340.firebasestorage.app%25252Fo%25252Fic_site_video.png%25253Falt%25253Dmedia%252526token%25253D54d8b5fb-344c-45da-8bf9-f60ad44f762b%2526h_type%253D1%2526subs%253D3"
    banner1 = soup.new_tag('a', href=target_url_banner1, target='_blank')
    banner1['class'] = 'custom-promo-banner'
    banner1.string = '🔥 Recommended Utility App - Click Here to Explore! 🚀'
    container_div.insert(0, banner1)

    # Second banner (New Profitable Rate CPM Network link)
    target_url_banner2 = "https://www.profitableratecpmnetwork.com/dr0ivy208k?key=e7a5a5c92a394c00cedc436f88577345"
    banner2 = soup.new_tag('a', href=target_url_banner2, target='_blank')
    banner2['class'] = 'custom-ad-partner-banner'
    banner2.string = '⭐ High-Speed Mirror Link & Special Offers - Tap Here! 📥'
    container_div.insert(1, banner2)

# 7. Inject 3D Galaxy Script & Download Protection
script_tag = soup.new_tag('script')
script_tag.string = """
document.addEventListener("DOMContentLoaded", function() {
    document.addEventListener('click', function(e) {
        let target = e.target.closest('a');
        if (target && target.href && !target.classList.contains('custom-promo-banner') && !target.classList.contains('custom-ad-partner-banner')) {
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

print("[+] Successfully added both professional banners cleanly!")
