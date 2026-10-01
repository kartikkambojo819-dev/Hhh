from bs4 import BeautifulSoup
from pathlib import Path

FILE = Path("index.html")

if not FILE.exists():
    print("[ERROR] index.html nahi mila.")
    raise SystemExit(1)

html = FILE.read_text(encoding="utf-8")
soup = BeautifulSoup(html, "html.parser")

# ============================================================
# 1. PURANE KARTIK BRAND PATCHES KO REMOVE KARO
# ============================================================

old_ids = [
    "kk-top-brand",
    "kk-footer-brand",
    "kartik-header-brand",
    "kk-final-logo",
    "kk-final-name"
]

old_classes = [
    "kk-logo-wrapper",
    "kk-logo-name",
    "kk-hide-original-header-logo"
]

for element in soup.find_all(True):
    if element.get("id") in old_ids:
        element.decompose()
        continue

    classes = element.get("class", [])
    if any(c in old_classes for c in classes):
        element.decompose()

# Purane injected style/script blocks hatao
for tag in soup.find_all(["style", "script"]):
    content = tag.string or tag.get_text()
    if any(x in content for x in [
        "kk-top-brand",
        "kk-footer-brand",
        "kartik-header-brand",
        "kk-final-logo",
        "kk-final-name",
        "kk3d-logo"
    ]):
        tag.decompose()

# ============================================================
# 2. HEADER LOGO KI JAGAH 3D LOGO INSERT KARNA
# ============================================================

logo_html = """
<div id="kk3d-logo" aria-label="Kartik Kamboj">
    <div class="kk3d-stage">

        <div class="kk3d-floor"></div>

        <div class="kk3d-name">

            <div class="kk3d-line">
                <span class="kk3d-front">KARTIK</span>
            </div>

            <div class="kk3d-line kk3d-line-second">
                <span class="kk3d-front">KAMBOJ</span>
            </div>

        </div>

    </div>
</div>
"""

logo = BeautifulSoup(logo_html, "html.parser").div

# ------------------------------------------------------------
# Existing custom header brand mile to usko replace karo
# ------------------------------------------------------------

existing = soup.find(id="kartik-header-brand")

if existing:
    existing.replace_with(logo)
    print("[OK] Existing Kartik header brand replace kar diya.")

else:
    # --------------------------------------------------------
    # Header / nav dhoondo
    # --------------------------------------------------------
    header = soup.find("header")

    if not header:
        header = soup.find(attrs={"role": "banner"})

    if not header:
        # Common navbar selectors
        for selector in ["nav", ".navbar", ".header", ".site-header"]:
            found = soup.select_one(selector)
            if found:
                header = found
                break

    if not header:
        print("[ERROR] Header nahi mila.")
        print("File modify nahi ki gayi.")
        raise SystemExit(1)

    # --------------------------------------------------------
    # Logo candidate dhoondo
    # Strong logo/brand selectors first
    # --------------------------------------------------------

    candidate = None

    strong_selectors = [
        '[class*="logo"]',
        '[id*="logo"]',
        '[class*="brand"]',
        '[id*="brand"]',
        'a[href="/"] img',
        'a[href="/"] svg'
    ]

    for selector in strong_selectors:
        try:
            found = header.select_one(selector)
        except Exception:
            found = None

        if found:
            candidate = found

            # Agar img/svg ke andar hai to uska parent link/container replace karo
            if found.name in ["img", "svg"]:
                if found.parent and found.parent.name in ["a", "div", "span"]:
                    candidate = found.parent

            break

    if not candidate:
        print("[ERROR] Header logo identify nahi hua.")
        print("File modify nahi ki gayi.")
        raise SystemExit(1)

    candidate.replace_with(logo)

    print("[OK] Original header logo replace kar diya.")


# ============================================================
# 3. 3D LOGO CSS
# ============================================================

css = r"""
/* ==========================================================
   KARTIK KAMBOJ — 3D HEADER LOGO
   Sirf existing website ke header logo area ke liye
   ========================================================== */

#kk3d-logo{
    position:relative;
    width:100%;
    height:155px;
    min-height:155px;
    display:flex;
    align-items:center;
    justify-content:center;
    overflow:hidden;
    background:
        radial-gradient(
            65% 70% at 50% 45%,
            rgba(58,31,120,.45) 0%,
            rgba(58,31,120,.08) 52%,
            transparent 75%
        ),
        linear-gradient(
            180deg,
            #050817 0%,
            #020511 100%
        );
    isolation:isolate;
    z-index:5;
    -webkit-user-select:none;
    user-select:none;
    touch-action:pan-y;
}

#kk3d-logo::before{
    content:"";
    position:absolute;
    left:8%;
    right:8%;
    top:50%;
    height:1px;
    background:linear-gradient(
        90deg,
        transparent,
        rgba(0,149,255,.25),
        rgba(0,213,255,.75),
        rgba(0,149,255,.25),
        transparent
    );
    box-shadow:0 0 15px rgba(0,174,255,.5);
    opacity:.8;
}

.kk3d-stage{
    position:relative;
    width:100%;
    height:100%;
    display:flex;
    align-items:center;
    justify-content:center;
    perspective:1200px;
    perspective-origin:50% 45%;
}

.kk3d-floor{
    position:absolute;
    left:50%;
    bottom:16px;
    width:min(72%,430px);
    height:20px;
    transform:translateX(-50%);
    border-radius:50%;
    pointer-events:none;

    background:
        radial-gradient(
            closest-side,
            rgba(0,191,255,.48),
            rgba(35,113,255,.18) 48%,
            transparent 75%
        );

    filter:blur(2px);
}

.kk3d-name{
    --fs:clamp(2.15rem,10vw,4.8rem);
    --step:calc(var(--fs)*.011);
    --grow:1;

    position:relative;
    display:flex;
    flex-direction:column;
    align-items:center;

    font-family:
        "Arial Black",
        Impact,
        system-ui,
        sans-serif;

    font-weight:900;
    line-height:.83;
    letter-spacing:.025em;

    transform-style:preserve-3d;
    will-change:transform;

    z-index:3;
}

.kk3d-line{
    position:relative;
    display:block;
    transform-style:preserve-3d;
    transform:translateZ(calc(var(--fs)*.02));
}

.kk3d-line-second{
    margin-top:4px;
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
            #dff6ff 28%,
            #46cfff 58%,
            #0077ff 100%
        );

    -webkit-background-clip:text;
    background-clip:text;

    color:transparent;
    -webkit-text-fill-color:transparent;

    filter:
        drop-shadow(0 0 4px rgba(255,255,255,.9))
        drop-shadow(0 0 10px rgba(0,183,255,.9))
        drop-shadow(0 0 22px rgba(0,88,255,.7));
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
                var(--grow) *
                -1
            )
        );

    color:hsl(
        calc(205 - var(--t)*55),
        90%,
        calc(42% - var(--t)*20%)
    );

    text-shadow:
        0 0 5px rgba(0,112,255,.45);
}

/* top shine */
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

    animation:kk3dShine 2.2s 1s ease-out forwards;

    pointer-events:none;
}

@keyframes kk3dShine{
    to{
        background-position:-30% 0;
    }
}

/* BLUE NEON LINE */
#kk3d-logo::after{
    content:"";
    position:absolute;

    width:min(62%,360px);
    height:3px;

    bottom:22px;
    left:50%;

    transform:translateX(-50%);

    background:
        linear-gradient(
            90deg,
            transparent,
            #008cff 20%,
            #8eeeff 50%,
            #008cff 80%,
            transparent
        );

    box-shadow:
        0 0 5px #00aaff,
        0 0 14px rgba(0,136,255,.9),
        0 0 28px rgba(0,97,255,.55);

    border-radius:100%;
}

/* MOBILE */
@media(max-width:600px){

    #kk3d-logo{
        height:150px;
        min-height:150px;
    }

    .kk3d-name{
        --fs:clamp(2rem,12vw,3.5rem);
        line-height:.84;
    }

    .kk3d-line-second{
        margin-top:3px;
    }

    .kk3d-floor{
        bottom:17px;
        width:75%;
    }
}

/* VERY SMALL PHONES */
@media(max-width:380px){

    #kk3d-logo{
        height:138px;
        min-height:138px;
    }

    .kk3d-name{
        --fs:clamp(1.75rem,12vw,2.8rem);
    }
}

/* REDUCED MOTION */
@media(prefers-reduced-motion:reduce){

    .kk3d-front::after{
        animation:none;
        background-position:-30% 0;
    }
}
"""

style_tag = soup.new_tag("style")
style_tag["id"] = "kk3d-logo-style"
style_tag.string = css

if soup.head:
    soup.head.append(style_tag)
else:
    soup.insert(0, style_tag)


# ============================================================
# 4. 3D DEPTH + MOUSE/TOUCH ANIMATION
# ============================================================

js = r"""
<script id="kk3d-logo-script">
(()=>{
    const logo = document.getElementById("kk3d-logo");
    const name = logo?.querySelector(".kk3d-name");

    if(!logo || !name) return;

    const reduce =
        window.matchMedia &&
        window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    const N = 22;

    /* Depth layers */
    name.querySelectorAll(".kk3d-line").forEach(line=>{

        const front = line.querySelector(".kk3d-front");

        if(!front) return;

        /* duplicate layer sirf ek baar */
        if(line.querySelector(".kk3d-layer")) return;

        for(let i=1;i<=N;i++){

            const layer =
                document.createElement("span");

            const t=i/N;

            layer.className="kk3d-layer";

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
                t
            );

            line.insertBefore(
                layer,
                front
            );
        }
    });


    let tx=0;
    let ty=0;
    let cx=0;
    let cy=0;
    let active=false;

    const aim=(e)=>{

        const r =
            logo.getBoundingClientRect();

        ty =
            ((e.clientX-r.left)/r.width-.5)*24;

        tx =
            -((e.clientY-r.top)/r.height-.5)*14;

        active=true;
    };


    logo.addEventListener(
        "pointermove",
        aim,
        {passive:true}
    );

    logo.addEventListener(
        "pointerdown",
        aim,
        {passive:true}
    );

    logo.addEventListener(
        "pointerleave",
        ()=>{
            active=false;
        }
    );

    logo.addEventListener(
        "pointercancel",
        ()=>{
            active=false;
        }
    );

    logo.addEventListener(
        "pointerup",
        (e)=>{
            if(e.pointerType!=="mouse"){
                active=false;
            }
        }
    );


    const start =
        performance.now();


    function frame(now){

        const s =
            (now-start)/1000;

        if(!active){

            if(reduce){

                tx=0;
                ty=0;

            }else{

                ty =
                    Math.sin(s*.75)*7;

                tx =
                    Math.cos(s*.55)*2.5-1;
            }
        }


        cx +=
            (tx-cx)*.075;

        cy +=
            (ty-cy)*.075;


        name.style.transform =
            `rotateX(${cx.toFixed(2)}deg)
             rotateY(${cy.toFixed(2)}deg)`;


        requestAnimationFrame(frame);
    }


    requestAnimationFrame(frame);

})();
</script>
"""

if soup.body:
    soup.body.append(
        BeautifulSoup(js, "html.parser")
    )
else:
    soup.append(
        BeautifulSoup(js, "html.parser")
    )


# ============================================================
# 5. SAVE
# ============================================================

FILE.write_text(
    str(soup),
    encoding="utf-8"
)

print()
print("==============================================")
print("  KARTIK KAMBOJ 3D LOGO INSTALLED")
print("==============================================")
print("[+] Sirf header logo replace hua")
print("[+] Existing website layout same rahega")
print("[+] Game cards same rahenge")
print("[+] Menu / theme / profile same rahenge")
print("[+] 3D depth + neon animation enabled")
print("[+] Mobile responsive")
print()
