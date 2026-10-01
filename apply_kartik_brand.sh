#!/data/data/com.termux/files/usr/bin/bash

set -e

FILE="index.html"

if [ ! -f "$FILE" ]; then
    echo "[ERROR] index.html nahi mila."
    exit 1
fi

cp "$FILE" "${FILE}.backup"

python3 - <<'PY'
from bs4 import BeautifulSoup
from pathlib import Path

file = Path("index.html")
html = file.read_text(encoding="utf-8")
soup = BeautifulSoup(html, "html.parser")

# ============================================================
# REMOVE ONLY OUR OLD HEADER PATCHES
# ============================================================

for tag in soup.find_all(["style", "script"]):
    txt = tag.get_text(" ", strip=False)

    if any(x in txt for x in [
        "kk3d-logo",
        "kk3d-stage",
        "kk3d-name",
        "kk3d-front",
        "kk3d-layer"
    ]):
        tag.decompose()

old = soup.find(id="kk3d-logo")
if old:
    old.decompose()


# ============================================================
# FIND REAL TOP NAVIGATION
# ============================================================

header = soup.find("header")

if not header:
    header = soup.find("nav")

if not header:
    # fallback: common top navigation containers
    for selector in [
        ".navbar",
        ".site-header",
        ".header",
        "[role='banner']"
    ]:
        found = soup.select_one(selector)
        if found:
            header = found
            break

if not header:
    print("[ERROR] Top header/navigation nahi mila.")
    print("[BACKUP] index.html.backup ban chuka hai.")
    raise SystemExit(1)


# ============================================================
# FIND LOGO INSIDE TOP HEADER
# Footer ko intentionally search nahi karna.
# ============================================================

candidates = []

for a in header.find_all("a"):

    imgs = a.find_all("img")
    svgs = a.find_all("svg")

    classes = " ".join(a.get("class", []))
    aid = a.get("id", "")

    score = 0

    text = a.get_text(" ", strip=True).lower()

    if "logo" in classes.lower():
        score += 100

    if "brand" in classes.lower():
        score += 90

    if "logo" in aid.lower():
        score += 100

    if "brand" in aid.lower():
        score += 90

    for img in imgs:

        src = (img.get("src") or "").lower()
        alt = (img.get("alt") or "").lower()
        iclass = " ".join(img.get("class", [])).lower()

        if "logo" in src:
            score += 80

        if "logo" in alt:
            score += 80

        if "anker" in src:
            score += 100

        if "anker" in alt:
            score += 100

        if "brand" in iclass:
            score += 60

    if svgs:
        score += 15

    # Home link with an image is often the site logo
    href = (a.get("href") or "").strip()

    if href in ["/", "#"]:
        score += 35

    if imgs or svgs:
        score += 20

    # Hamburger/menu buttons usually have aria-label containing menu
    aria = (a.get("aria-label") or "").lower()

    if "menu" in aria or "search" in aria or "theme" in aria:
        score -= 100

    if score > 0:
        candidates.append((score, a))


if not candidates:
    print("[ERROR] Header logo candidate nahi mila.")
    print("[BACKUP] index.html.backup ban chuka hai.")
    raise SystemExit(1)


candidates.sort(
    key=lambda x: x[0],
    reverse=True
)

score, target = candidates[0]

print("[OK] Header logo found.")
print("[OK] Score:", score)
print("[OK] Tag:", target.name)
print("[OK] Classes:", target.get("class"))
print("[OK] Href:", target.get("href"))


# ============================================================
# NEW KARTIK KAMBOJ 3D LOGO
# ============================================================

logo_html = """
<div id="kk3d-logo" aria-label="Kartik Kamboj">

    <div class="kk3d-stage">

        <div class="kk3d-floor"></div>

        <div class="kk3d-name">

            <div class="kk3d-line">
                <span class="kk3d-front">KARTIK</span>
            </div>

            <div class="kk3d-line second">
                <span class="kk3d-front">KAMBOJ</span>
            </div>

        </div>

    </div>

</div>
"""

new_logo = BeautifulSoup(
    logo_html,
    "html.parser"
).find(id="kk3d-logo")


# Replace ONLY header logo
target.replace_with(new_logo)


# ============================================================
# CSS
# ============================================================

css = r"""
/* =========================================================
   KARTIK KAMBOJ — HEADER 3D BRAND
   ========================================================= */

#kk3d-logo{
    position:relative;
    width:clamp(180px,42vw,360px);
    height:92px;
    flex:0 1 auto;

    display:flex;
    align-items:center;
    justify-content:center;

    overflow:hidden;

    background:
        radial-gradient(
            70% 80% at 50% 45%,
            rgba(0,125,255,.18),
            transparent 72%
        );

    border-radius:12px;

    isolation:isolate;

    user-select:none;
    -webkit-user-select:none;

    touch-action:pan-y;

    z-index:30;
}

.kk3d-stage{
    position:relative;

    width:100%;
    height:100%;

    display:flex;
    align-items:center;
    justify-content:center;

    perspective:1100px;
    perspective-origin:50% 45%;
}

.kk3d-name{
    --fs:clamp(1.45rem,5.5vw,3rem);
    --step:calc(var(--fs)*.012);

    position:relative;

    display:flex;
    flex-direction:column;
    align-items:center;

    font-family:
        Arial Black,
        Impact,
        sans-serif;

    font-weight:900;
    line-height:.82;

    letter-spacing:.035em;

    transform-style:preserve-3d;

    will-change:transform;

    z-index:5;
}

.kk3d-line{
    position:relative;
    display:block;
    transform-style:preserve-3d;
}

.kk3d-line.second{
    margin-top:3px;
}

.kk3d-front,
.kk3d-layer{
    display:block;
    white-space:nowrap;
}

.kk3d-front{
    position:relative;

    background:
        linear-gradient(
            180deg,
            #ffffff 0%,
            #e9fbff 23%,
            #62d8ff 48%,
            #008cff 75%,
            #005de8 100%
        );

    -webkit-background-clip:text;
    background-clip:text;

    color:transparent;
    -webkit-text-fill-color:transparent;

    filter:
        drop-shadow(0 0 3px rgba(255,255,255,.9))
        drop-shadow(0 0 8px rgba(0,190,255,.95))
        drop-shadow(0 0 17px rgba(0,85,255,.75));
}

.kk3d-front::after{
    content:"";

    position:absolute;
    inset:0;

    background:
        linear-gradient(
            110deg,
            transparent 35%,
            rgba(255,255,255,.95) 49%,
            transparent 62%
        );

    background-size:220% 100%;
    background-position:130% 0;

    -webkit-background-clip:text;
    background-clip:text;

    animation:kk3dShine 2.4s 1s ease-out forwards;

    pointer-events:none;
}

@keyframes kk3dShine{
    to{
        background-position:-30% 0;
    }
}

.kk3d-layer{
    position:absolute;
    inset:0;

    pointer-events:none;

    transform:
        translateZ(
            calc(
                var(--i) *
                var(--step) *
                -1
            )
        );

    color:
        hsl(
            calc(210 - var(--t)*45),
            90%,
            calc(43% - var(--t)*20%)
        );

    text-shadow:
        0 0 5px rgba(0,105,255,.5);
}

.kk3d-floor{
    position:absolute;

    left:50%;
    bottom:8px;

    width:72%;
    height:13px;

    transform:translateX(-50%);

    border-radius:50%;

    background:
        radial-gradient(
            closest-side,
            rgba(0,190,255,.5),
            rgba(30,100,255,.15) 50%,
            transparent 75%
        );

    filter:blur(2px);
}

#kk3d-logo::after{
    content:"";

    position:absolute;

    width:62%;
    height:2px;

    left:50%;
    bottom:9px;

    transform:translateX(-50%);

    border-radius:100%;

    background:
        linear-gradient(
            90deg,
            transparent,
            #008cff,
            #a8f3ff,
            #008cff,
            transparent
        );

    box-shadow:
        0 0 6px #00aaff,
        0 0 14px rgba(0,136,255,.75);
}

@media(max-width:600px){

    #kk3d-logo{
        width:190px;
        height:82px;
    }

    .kk3d-name{
        --fs:clamp(1.35rem,7vw,2.3rem);
    }
}

@media(max-width:380px){

    #kk3d-logo{
        width:170px;
        height:76px;
    }

    .kk3d-name{
        --fs:1.28rem;
    }
}
"""

style = soup.new_tag("style")
style["id"] = "kk3d-logo-style"
style.string = css

if soup.head:
    soup.head.append(style)


# ============================================================
# JAVASCRIPT
# ============================================================

js = r"""
<script id="kk3d-logo-script">
(()=>{

    const logo =
        document.getElementById("kk3d-logo");

    if(!logo) return;

    const name =
        logo.querySelector(".kk3d-name");

    if(!name) return;

    const reduce =
        window.matchMedia &&
        window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches;

    const N = 20;


    /* 3D DEPTH */

    name.querySelectorAll(".kk3d-line")
    .forEach(line=>{

        const front =
            line.querySelector(".kk3d-front");

        if(!front) return;

        for(let i=1;i<=N;i++){

            const layer =
                document.createElement("span");

            layer.className =
                "kk3d-layer";

            layer.setAttribute(
                "aria-hidden",
                "true"
            );

            layer.textContent =
                front.textContent;

            layer.style.setProperty(
                "--i",
                i
            );

            layer.style.setProperty(
                "--t",
                i/N
            );

            line.insertBefore(
                layer,
                front
            );
        }
    });


    let rx=0;
    let ry=0;

    let targetX=0;
    let targetY=0;

    let active=false;


    function move(e){

        const r =
            logo.getBoundingClientRect();

        targetY =
            ((e.clientX-r.left)/r.width-.5)*18;

        targetX =
            -((e.clientY-r.top)/r.height-.5)*10;

        active=true;
    }


    logo.addEventListener(
        "pointermove",
        move,
        {passive:true}
    );

    logo.addEventListener(
        "pointerdown",
        move,
        {passive:true}
    );

    logo.addEventListener(
        "pointerleave",
        ()=>{
            active=false;
        }
    );

    logo.addEventListener(
        "pointerup",
        ()=>{
            active=false;
        }
    );


    const start =
        performance.now();


    function animate(now){

        const t =
            (now-start)/1000;

        if(!active && !reduce){

            targetY =
                Math.sin(t*.8)*5;

            targetX =
                Math.cos(t*.55)*2;
        }

        if(reduce){

            targetX=0;
            targetY=0;
        }

        rx +=
            (targetX-rx)*.08;

        ry +=
            (targetY-ry)*.08;

        name.style.transform =
            "rotateX("+
            rx.toFixed(2)+
            "deg) rotateY("+
            ry.toFixed(2)+
            "deg)";

        requestAnimationFrame(
            animate
        );
    }

    requestAnimationFrame(
        animate
    );

})();
</script>
"""

if soup.body:
    soup.body.append(
        BeautifulSoup(
            js,
            "html.parser"
        )
    )


# ============================================================
# SAVE
# ============================================================

file.write_text(
    str(soup),
    encoding="utf-8"
)

print()
print("==============================================")
print("   KARTIK 3D HEADER INSTALLED")
print("==============================================")
print("[OK] Header logo replaced")
print("[OK] Footer untouched")
print("[OK] Game cards untouched")
print("[OK] Menu untouched")
print("[OK] 3D animation added")
print("[OK] Backup: index.html.backup")
print("==============================================")
PY

echo
echo "[1/2] Branding installed."
echo
echo "[2/2] Git push..."

git add index.html

git commit -m "Replace header logo with Kartik Kamboj 3D branding" || true

git push origin main --force

echo
echo "=============================================="
echo " DONE — GitHub par push ho gaya"
echo "=============================================="
