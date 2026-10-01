from bs4 import BeautifulSoup
from pathlib import Path

FILE = Path("index.html")

if not FILE.exists():
    print("[ERROR] index.html nahi mila")
    raise SystemExit(1)

html = FILE.read_text(encoding="utf-8")
soup = BeautifulSoup(html, "html.parser")


# =========================================================
# REMOVE PREVIOUS 3D PATCHES
# =========================================================

for tag in soup.find_all(["style", "script"]):
    content = tag.get_text(" ", strip=False)

    if any(x in content for x in [
        "kk3d-logo",
        "kk3d-name",
        "kk3d-front",
        "kk3d-layer"
    ]):
        tag.decompose()


for el in soup.find_all(True):

    eid = el.get("id", "")

    if eid in [
        "kk3d-logo",
        "kartik-header-brand",
        "kk-top-brand",
        "kk-final-logo",
        "kk-final-name"
    ]:
        el.decompose()


# =========================================================
# FIND CURRENT KARTIK KAMBOJ ELEMENT
# =========================================================

candidates = []

for el in soup.find_all(True):

    text = el.get_text(" ", strip=True)

    normalized = " ".join(text.upper().split())

    if normalized == "KARTIK KAMBOJ":

        # body/html ko kabhi target nahi karna
        if el.name in ["html", "body", "main"]:
            continue

        # bahut bade container ko ignore
        if len(str(el)) > 30000:
            continue

        candidates.append(el)


# Sabse chhota suitable element choose karo
if candidates:

    candidates.sort(key=lambda x: len(str(x)))
    target = candidates[0]

    print("[OK] Existing KARTIK KAMBOJ element mila:")
    print("    tag =", target.name)
    print("    id  =", target.get("id"))
    print("    cls =", target.get("class"))


else:

    print("[ERROR] Current HTML me exact 'KARTIK KAMBOJ' text nahi mila.")
    print()
    print("Pehle ye command chalao:")
    print()
    print("grep -ni -E 'Kartik|KAMBOJ|ANKER|logo|brand' index.html | head -80")
    print()
    print("Uska output mujhe bhejo.")
    raise SystemExit(1)


# =========================================================
# NEW 3D LOGO
# =========================================================

new_logo = """
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

new_logo = BeautifulSoup(new_logo, "html.parser").div


# =========================================================
# REPLACE ONLY THAT ELEMENT
# =========================================================

target.replace_with(new_logo)


# =========================================================
# CSS
# =========================================================

css = r"""

/* ========================================================
   KARTIK KAMBOJ 3D LOGO
   ======================================================== */

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
            rgba(0,100,255,.18),
            rgba(0,20,60,.05) 55%,
            transparent 78%
        );

    isolation:isolate;

    z-index:20;

    user-select:none;
    -webkit-user-select:none;

    touch-action:pan-y;
}


/* subtle background glow */

#kk3d-logo::before{

    content:"";

    position:absolute;

    left:8%;
    right:8%;

    top:50%;

    height:1px;

    background:
        linear-gradient(
            90deg,
            transparent,
            rgba(0,130,255,.2),
            rgba(0,210,255,.7),
            rgba(0,130,255,.2),
            transparent
        );

    box-shadow:
        0 0 12px rgba(0,160,255,.6);

}


/* stage */

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


/* 3D text */

.kk3d-name{

    --fs:clamp(2.05rem,10vw,4.8rem);
    --step:calc(var(--fs)*.011);

    position:relative;

    display:flex;

    flex-direction:column;

    align-items:center;

    font-family:
        Arial Black,
        Impact,
        sans-serif;

    font-weight:900;

    line-height:.84;

    letter-spacing:.025em;

    transform-style:preserve-3d;

    will-change:transform;

    z-index:5;

}


/* each word */

.kk3d-line{

    position:relative;

    display:block;

    transform-style:preserve-3d;

}


.kk3d-line-second{

    margin-top:4px;

}


.kk3d-front,
.kk3d-layer{

    display:block;

    white-space:nowrap;

}


/* FRONT FACE */

.kk3d-front{

    position:relative;

    background:
        linear-gradient(
            180deg,
            #ffffff 0%,
            #eafaff 25%,
            #62d8ff 52%,
            #008cff 78%,
            #0060e8 100%
        );

    -webkit-background-clip:text;
    background-clip:text;

    color:transparent;

    -webkit-text-fill-color:transparent;

    filter:
        drop-shadow(0 0 4px rgba(255,255,255,.95))
        drop-shadow(0 0 9px rgba(0,190,255,.95))
        drop-shadow(0 0 22px rgba(0,90,255,.75));

}


/* shine */

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

    animation:
        kk3dShine 2.2s 1s ease-out forwards;

    pointer-events:none;

}


@keyframes kk3dShine{

    to{
        background-position:-30% 0;
    }

}


/* depth layers */

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
            calc(205 - var(--t)*45),
            90%,
            calc(42% - var(--t)*20%)
        );

    text-shadow:
        0 0 5px rgba(0,100,255,.5);

}


/* floor glow */

.kk3d-floor{

    position:absolute;

    left:50%;

    bottom:16px;

    width:min(72%,430px);

    height:20px;

    transform:translateX(-50%);

    border-radius:50%;

    background:
        radial-gradient(
            closest-side,
            rgba(0,190,255,.48),
            rgba(30,100,255,.18) 48%,
            transparent 75%
        );

    filter:blur(2px);

}


/* neon line */

#kk3d-logo::after{

    content:"";

    position:absolute;

    width:min(62%,360px);

    height:3px;

    bottom:22px;

    left:50%;

    transform:translateX(-50%);

    border-radius:100%;

    background:
        linear-gradient(
            90deg,
            transparent,
            #008cff 20%,
            #a8f3ff 50%,
            #008cff 80%,
            transparent
        );

    box-shadow:
        0 0 5px #00aaff,
        0 0 14px rgba(0,136,255,.9),
        0 0 28px rgba(0,97,255,.55);

}


/* MOBILE */

@media(max-width:600px){

    #kk3d-logo{

        height:150px;
        min-height:150px;

    }

    .kk3d-name{

        --fs:clamp(
            2rem,
            12vw,
            3.5rem
        );

    }

}


/* SMALL PHONES */

@media(max-width:380px){

    #kk3d-logo{

        height:140px;
        min-height:140px;

    }

    .kk3d-name{

        --fs:clamp(
            1.75rem,
            12vw,
            2.8rem
        );

    }

}


@media(prefers-reduced-motion:reduce){

    .kk3d-front::after{

        animation:none;

    }

}

"""


style = soup.new_tag("style")
style["id"] = "kk3d-logo-style"
style.string = css

if soup.head:
    soup.head.append(style)


# =========================================================
# JAVASCRIPT 3D DEPTH + ANIMATION
# =========================================================

script = r"""
<script id="kk3d-logo-script">

(()=>{

    const logo =
        document.getElementById("kk3d-logo");

    const name =
        logo?.querySelector(".kk3d-name");

    if(!logo || !name) return;


    const reduce =
        window.matchMedia &&
        window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches;


    const N = 24;


    /* CREATE DEPTH */

    name.querySelectorAll(
        ".kk3d-line"
    ).forEach(line=>{

        const front =
            line.querySelector(".kk3d-front");

        if(!front) return;


        for(let i=1;i<=N;i++){

            const layer =
                document.createElement("span");

            const t=i/N;

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


    function move(e){

        const r =
            logo.getBoundingClientRect();

        ty =
            ((e.clientX-r.left)/r.width-.5)*24;

        tx =
            -((e.clientY-r.top)/r.height-.5)*14;

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
        "pointercancel",
        ()=>{
            active=false;
        }
    );


    logo.addEventListener(
        "pointerup",
        e=>{

            if(e.pointerType!=="mouse"){
                active=false;
            }

        }
    );


    const start =
        performance.now();


    function animate(now){

        const seconds =
            (now-start)/1000;


        if(!active){

            if(reduce){

                tx=0;
                ty=0;

            }else{

                ty =
                    Math.sin(
                        seconds*.75
                    )*7;

                tx =
                    Math.cos(
                        seconds*.55
                    )*2.5-1;

            }

        }


        cx +=
            (tx-cx)*.075;

        cy +=
            (ty-cy)*.075;


        name.style.transform =
            "rotateX("+
            cx.toFixed(2)+
            "deg) rotateY("+
            cy.toFixed(2)+
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
            script,
            "html.parser"
        )
    )


# =========================================================
# SAVE
# =========================================================

FILE.write_text(
    str(soup),
    encoding="utf-8"
)

print()
print("==============================================")
print(" SUCCESS")
print("==============================================")
print("Existing KARTIK KAMBOJ logo replace ho gaya.")
print("Claude-style 3D neon logo install ho gaya.")
print("Baaki website ko touch nahi kiya.")
print("==============================================")
