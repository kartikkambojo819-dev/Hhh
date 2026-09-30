import os
from curl_cffi import requests
from bs4 import BeautifulSoup

TARGET_URL = "https://ankergames.net"

print("[*] Downloading site...")
print("[*] Rebranding Anker Games -> Kartik Kamboj...")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

resp = requests.get(
    TARGET_URL,
    headers=headers,
    impersonate="chrome",
    timeout=30
)

if resp.status_code != 200:
    print(f"[!] Website returned HTTP {resp.status_code}")
    exit(1)

soup = BeautifulSoup(resp.text, "html.parser")

# --------------------------------------------------
# PAGE TITLE
# --------------------------------------------------

if soup.title:
    soup.title.string = "Kartik Kamboj - Free PC Games Hub"

# --------------------------------------------------
# REPLACE TEXT BRANDING
# --------------------------------------------------

replacements = {
    "AnkerGames": "Kartik Kamboj",
    "Anker Games": "Kartik Kamboj",
    "ANKER GAMES": "KARTIK KAMBOJ",
    "Anker games": "Kartik Kamboj",
    "ankergames": "kartikkamboj",
    "anker games": "kartik kamboj"
}

for element in soup.find_all(string=True):

    if element.parent and element.parent.name in [
        "style",
        "script",
        "noscript"
    ]:
        continue

    original = str(element)
    updated = original

    for old, new in replacements.items():
        updated = updated.replace(old, new)

    if updated != original:
        element.replace_with(updated)

# --------------------------------------------------
# TOP HEADER BRANDING
# --------------------------------------------------

style_tag = soup.new_tag("style")

style_tag.string = r"""
/* ==================================================
   KARTIK KAMBOJ GLOBAL BRANDING
   ================================================== */

html,
body {
    background: #04050d !important;
    color: #eef1ff !important;
    overflow-x: hidden !important;
}

/* Top website logo / brand */

header img[alt*="Anker"],
header img[alt*="ANKER"],
header img[src*="anker"],
header img[src*="Anker"] {
    display: none !important;
}

/* Any header branding text */

header .logo,
header .brand,
header .site-logo,
header .navbar-brand,
header [class*="logo"],
header [class*="brand"] {
    font-size: clamp(25px, 5vw, 48px) !important;
    font-weight: 900 !important;
    letter-spacing: -1px !important;
    white-space: nowrap !important;
}

/* Create new top branding */

header .logo::after,
header .brand::after,
header .site-logo::after,
header .navbar-brand::after {
    content: "KARTIK KAMBOJ" !important;
    display: inline-block !important;
    font-size: clamp(25px, 5vw, 48px) !important;
    font-weight: 900 !important;
    letter-spacing: -1px !important;
}

/* Generic text containing the old branding */

a[href="/"],
a[href="./"] {
    font-weight: 900 !important;
}

/* --------------------------------------------------
   FOOTER
   -------------------------------------------------- */

footer img[alt*="Anker"],
footer img[alt*="ANKER"],
footer img[src*="anker"],
footer img[src*="Anker"] {
    display: none !important;
}

/* Footer logo containers */

footer .logo,
footer .brand,
footer .site-logo,
footer [class*="logo"],
footer [class*="brand"] {
    font-size: 0 !important;
}

/* New footer branding */

footer .logo::after,
footer .brand::after,
footer .site-logo::after,
footer [class*="logo"]::after,
footer [class*="brand"]::after {
    content: "KARTIK KAMBOJ" !important;
    display: block !important;
    font-size: clamp(28px, 7vw, 58px) !important;
    font-weight: 900 !important;
    letter-spacing: 1px !important;
    line-height: 1.1 !important;
    color: #ffffff !important;
    text-shadow:
        0 0 5px #00aaff,
        0 0 15px #008cff,
        0 0 30px rgba(0,140,255,.7) !important;
}

/* --------------------------------------------------
   BACKGROUND
   -------------------------------------------------- */

#bg-canvas {
    position: fixed !important;
    inset: 0 !important;
    width: 100% !important;
    height: 100% !important;
    z-index: -999999 !important;
    pointer-events: none !important;
}

/* --------------------------------------------------
   MOBILE
   -------------------------------------------------- */

@media (max-width: 600px) {

    header .logo::after,
    header .brand::after,
    header .site-logo::after,
    header .navbar-brand::after {
        font-size: 27px !important;
    }

    footer .logo::after,
    footer .brand::after,
    footer .site-logo::after,
    footer [class*="logo"]::after,
    footer [class*="brand"]::after {
        font-size: 32px !important;
    }
}
"""

if soup.head:
    soup.head.append(style_tag)

# --------------------------------------------------
# REMOVE SMALL UNWANTED CLUTTER
# --------------------------------------------------

keywords = [
    "discord",
    "donation",
    "donations",
    "nebulo",
    "reddit"
]

for el in soup.find_all(["div", "a", "button", "li"]):

    try:
        text = el.get_text(" ", strip=True).lower()
    except Exception:
        continue

    if len(text) < 40 and any(k in text for k in keywords):

        # Don't accidentally remove major page containers
        if el.name in ["button", "a", "li"]:
            el.decompose()

# --------------------------------------------------
# 3D GALAXY BACKGROUND + LINK HANDLING
# --------------------------------------------------

script_tag = soup.new_tag("script")

script_tag.string = r"""
document.addEventListener("DOMContentLoaded", function () {

    /*
     * Open download/file links in a new tab.
     */
    document.addEventListener("click", function(e) {

        const target = e.target.closest("a");

        if (!target || !target.href) return;

        const href = target.href.toLowerCase();

        if (
            href.includes("download") ||
            href.includes("file") ||
            href.includes("mega") ||
            href.includes("drive")
        ) {
            target.setAttribute("target", "_blank");
            target.setAttribute("rel", "noopener noreferrer");
        }
    });

    /*
     * 3D galaxy background
     */

    if (!document.getElementById("bg-canvas")) {

        const canvas = document.createElement("canvas");

        canvas.id = "bg-canvas";

        document.body.prepend(canvas);

        const c = canvas;
        const x = c.getContext("2d");

        let W;
        let H;

        let G = [];
        let F = [];

        const N = 1200;

        let ang = 0;

        let tx = 0;
        let ty = 0;

        let mx = 0;
        let my = 0;

        function rs() {

            W = window.innerWidth;
            H = window.innerHeight;

            const dpr = Math.min(window.devicePixelRatio || 1, 2);

            c.width = W * dpr;
            c.height = H * dpr;

            x.setTransform(
                dpr,
                0,
                0,
                dpr,
                0,
                0
            );
        }

        function init() {

            G = [];
            F = [];

            for (let i = 0; i < N; i++) {

                const d =
                    Math.pow(Math.random(), .65) *
                    800 +
                    10;

                const a =
                    d * .0065 +
                    (i % 3) * 2.09;

                G.push({
                    x: Math.cos(a) * d,
                    z: Math.sin(a) * d,
                    y: (Math.random() - .5) * 100,
                    h: 45 + d / 800 * 235,
                    s: Math.random() * 1.3 + .5
                });
            }

            for (let j = 0; j < 200; j++) {

                F.push({
                    x: Math.random(),
                    y: Math.random(),
                    p: Math.random() * 6.28,
                    s: Math.random() * 1.2 + .3
                });
            }
        }

        function fr(t) {

            mx += (tx - mx) * .04;
            my += (ty - my) * .04;

            x.fillStyle = "rgba(4,5,13,.4)";
            x.fillRect(0, 0, W, H);

            for (let j = 0; j < F.length; j++) {

                const f = F[j];

                x.fillStyle =
                    "rgba(255,255,255," +
                    (.2 + .3 * Math.sin(t / 900 + f.p)) +
                    ")";

                x.fillRect(
                    f.x * W,
                    f.y * H,
                    f.s,
                    f.s
                );
            }

            const fov = Math.max(W, H) * .8;

            const cx = W / 2;
            const cy = H / 2;

            const a = ang + mx * .6;

            const ct = Math.cos(1.0 + my * .35);
            const st = Math.sin(1.0 + my * .35);

            const ca = Math.cos(a);
            const sa = Math.sin(a);

            for (let i = 0; i < G.length; i++) {

                const p = G[i];

                const x1 =
                    p.x * ca -
                    p.z * sa;

                const z1 =
                    p.x * sa +
                    p.z * ca;

                const y2 =
                    p.y * ct -
                    z1 * st;

                const z2 =
                    p.y * st +
                    z1 * ct;

                const dp =
                    z2 + 1300;

                if (dp < 100) continue;

                const k = fov / dp;

                const px =
                    cx + x1 * k;

                const py =
                    cy + y2 * k;

                if (
                    px < 0 ||
                    px > W ||
                    py < 0 ||
                    py > H
                ) {
                    continue;
                }

                x.fillStyle =
                    "hsla(" +
                    p.h +
                    ",85%,72%," +
                    Math.min(1, .25 + k * .55) +
                    ")";

                const sz =
                    Math.max(
                        .5,
                        p.s * k * 1.2
                    );

                x.fillRect(
                    px,
                    py,
                    sz,
                    sz
                );
            }

            ang += .0015;

            requestAnimationFrame(fr);
        }

        window.addEventListener(
            "mousemove",
            function (e) {

                tx =
                    (e.clientX / W - .5) * 2;

                ty =
                    (e.clientY / H - .5) * 2;
            }
        );

        window.addEventListener(
            "resize",
            function () {

                rs();
                init();
            }
        );

        rs();
        init();
        fr(0);
    }
});
"""

if soup.body:
    soup.body.append(script_tag)

# --------------------------------------------------
# SAVE
# --------------------------------------------------

with open(
    "index.html",
    "w",
    encoding="utf-8"
) as f:
    f.write(str(soup))

print("")
print("[+] DONE")
print("[+] Kartik Kamboj branding applied.")
print("[+] Top branding enlarged.")
print("[+] Footer branding changed.")
print("[+] index.html saved.")
