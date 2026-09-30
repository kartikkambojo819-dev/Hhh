from bs4 import BeautifulSoup

FILE = "index.html"

with open(FILE, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# =========================================================
# OLD LOWER "KARTIK KAMBOJ" COMPLETELY REMOVE
# =========================================================

for el in soup.select("#kk-footer-brand"):
    el.decompose()

# Remove previous footer-brand styles/scripts if necessary
style = soup.new_tag("style")

style.string = r"""
/* ================================================
   REMOVE LOWER KARTIK KAMBOJ
   ================================================ */

#kk-footer-brand {
    display: none !important;
}


/* ================================================
   WIZARD LOGO REPLACEMENT
   ================================================ */

.kk-logo-wrapper {
    position: relative !important;
    display: block !important;
    width: 100% !important;
    max-width: 650px !important;
    margin: 20px auto !important;
    overflow: hidden !important;
}

.kk-logo-wrapper img {
    display: block !important;
    width: 100% !important;
    height: auto !important;
}


/*
   Cover the original ANKER GAMES text
   inside the wizard logo.
*/

.kk-logo-name {
    position: absolute !important;

    left: 7% !important;
    right: 7% !important;

    bottom: 5% !important;

    height: 17% !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;

    text-align: center !important;

    background: #050713 !important;

    color: #ffffff !important;

    font-family:
        Arial Black,
        Arial,
        Helvetica,
        sans-serif !important;

    font-size: clamp(
        25px,
        7vw,
        58px
    ) !important;

    font-weight: 1000 !important;

    letter-spacing: 1px !important;

    line-height: 1 !important;

    white-space: nowrap !important;

    text-shadow:
        0 0 3px #ffffff,
        0 0 8px #00b7ff,
        0 0 18px #008cff,
        0 0 30px rgba(0,140,255,.8) !important;

    border-radius: 8px !important;

    z-index: 50 !important;
}


/* Blue outline/glow */

.kk-logo-name::after {
    content: "" !important;

    position: absolute !important;

    inset: 0 !important;

    border-radius: 8px !important;

    box-shadow:
        0 0 8px rgba(0,180,255,.9),
        inset 0 0 8px rgba(0,150,255,.35) !important;

    pointer-events: none !important;
}


/* Small phones */

@media (max-width: 420px) {

    .kk-logo-name {
        font-size: 25px !important;
        letter-spacing: .5px !important;
        left: 7% !important;
        right: 7% !important;
        height: 17% !important;
    }
}
"""

if soup.head:
    soup.head.append(style)


# =========================================================
# JAVASCRIPT
# =========================================================

script = soup.new_tag("script")

script.string = r"""
(function () {

"use strict";

function installKartikLogo() {

    /*
       Remove EVERY old lower branding element.
    */

    document
        .querySelectorAll("#kk-footer-brand")
        .forEach(function(el) {
            el.remove();
        });


    /*
       Find the wizard logo.
    */

    const images =
        document.querySelectorAll("img");

    let logo = null;

    images.forEach(function(img) {

        if (logo) return;

        const src =
            (img.getAttribute("src") || "")
            .toLowerCase();

        const alt =
            (img.getAttribute("alt") || "")
            .toLowerCase();

        /*
           Detect Anker logo image.
        */

        if (
            src.includes("anker") ||
            alt.includes("anker")
        ) {
            logo = img;
        }
    });


    /*
       If not detected by filename,
       look for large images near footer.
    */

    if (!logo) {

        images.forEach(function(img) {

            if (logo) return;

            const rect =
                img.getBoundingClientRect();

            if (
                rect.width > 250 &&
                rect.height > 200
            ) {
                logo = img;
            }

        });

    }


    if (!logo) return;


    /*
       Don't create duplicate overlay.
    */

    if (
        logo.parentElement &&
        logo.parentElement.classList.contains(
            "kk-logo-wrapper"
        )
    ) {
        return;
    }


    /*
       Create wrapper.
    */

    const wrapper =
        document.createElement("div");

    wrapper.className =
        "kk-logo-wrapper";


    logo.parentNode.insertBefore(
        wrapper,
        logo
    );

    wrapper.appendChild(logo);


    /*
       Create replacement text INSIDE
       the original logo area.
    */

    const name =
        document.createElement("div");

    name.className =
        "kk-logo-name";

    name.textContent =
        "KARTIK KAMBOJ";


    wrapper.appendChild(name);

}


function run() {

    installKartikLogo();

}


/*
   Initial loading.
*/

if (
    document.readyState === "loading"
) {

    document.addEventListener(
        "DOMContentLoaded",
        run
    );

} else {

    run();

}


/*
   Run again because the site can
   dynamically load its footer/logo.
*/

setTimeout(run, 500);
setTimeout(run, 1500);
setTimeout(run, 3000);
setTimeout(run, 5000);


/*
   Watch dynamic changes.
*/

const observer =
    new MutationObserver(function() {

        clearTimeout(
            window.__kkLogoTimer
        );

        window.__kkLogoTimer =
            setTimeout(
                run,
                200
            );

    });


observer.observe(
    document.documentElement,
    {
        childList: true,
        subtree: true
    }
);

})();
"""

if soup.body:
    soup.body.append(script)


# =========================================================
# SAVE
# =========================================================

with open(FILE, "w", encoding="utf-8") as f:
    f.write(
        "<!DOCTYPE html>\n" +
        str(soup)
    )

print("")
print("==============================================")
print("       LOGO REBRANDING COMPLETE")
print("==============================================")
print("[✓] Lower KARTIK KAMBOJ removed")
print("[✓] Original wizard logo preserved")
print("[✓] ANKER GAMES area replaced")
print("[✓] KARTIK KAMBOJ placed inside logo")
print("[✓] Responsive mobile design")
print("==============================================")
