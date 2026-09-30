from bs4 import BeautifulSoup

FILE = "index.html"

with open(FILE, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")


# =========================================================
# 1. REMOVE ALL PREVIOUS KARTIK BRANDING WE CREATED
# =========================================================

for selector in [
    "#kk-top-brand",
    "#kk-footer-brand",
    ".kk-logo-name",
    ".kk-logo-wrapper"
]:
    for el in soup.select(selector):
        el.decompose()


# =========================================================
# 2. REMOVE OLD BRANDING CSS / SCRIPTS FROM OUR PATCHES
# =========================================================

for style in soup.find_all("style"):
    txt = style.get_text(" ", strip=True)

    if any(x in txt for x in [
        "kk-top-brand",
        "kk-footer-brand",
        "kk-logo-name",
        "kk-logo-wrapper"
    ]):
        style.decompose()


for script in soup.find_all("script"):
    txt = script.get_text(" ", strip=True)

    if any(x in txt for x in [
        "kk-top-brand",
        "kk-footer-brand",
        "kk-logo-name",
        "kk-logo-wrapper"
    ]):
        script.decompose()


# =========================================================
# 3. CLEAN PREMIUM LOGO CSS
# =========================================================

style = soup.new_tag("style")

style.string = r"""
/* =====================================================
   FINAL KARTIK KAMBOJ LOGO
   ===================================================== */

/* Never show the old separately-added top branding */
#kk-top-brand,
#kk-footer-brand {
    display: none !important;
}


/* -----------------------------------------------------
   WIZARD LOGO CONTAINER
   ----------------------------------------------------- */

.kk-final-logo {
    position: relative !important;

    display: block !important;

    width: min(650px, 94vw) !important;

    margin: 25px auto 30px !important;

    overflow: hidden !important;

    text-align: center !important;
}


/* Keep original wizard artwork */
.kk-final-logo img {
    display: block !important;

    width: 100% !important;

    height: auto !important;

    margin: 0 auto !important;
}


/* -----------------------------------------------------
   ONE SINGLE KARTIK KAMBOJ
   -----------------------------------------------------

   This occupies the original ANKER GAMES area.
   Height is intentionally around 3 normal text lines.
   ----------------------------------------------------- */

.kk-final-name {

    position: absolute !important;

    left: 6% !important;
    right: 6% !important;

    bottom: 4% !important;

    height: 96px !important;

    display: flex !important;

    align-items: center !important;

    justify-content: center !important;

    box-sizing: border-box !important;

    padding: 8px 10px !important;

    overflow: hidden !important;

    background:
        linear-gradient(
            180deg,
            rgba(3,5,16,.97),
            rgba(3,5,16,.99)
        ) !important;

    border-radius: 12px !important;

    color: #ffffff !important;

    font-family:
        Arial Black,
        Arial,
        Helvetica,
        sans-serif !important;

    font-size: clamp(
        24px,
        6.5vw,
        52px
    ) !important;

    font-weight: 1000 !important;

    line-height: 1 !important;

    letter-spacing: 1px !important;

    white-space: nowrap !important;

    text-align: center !important;

    z-index: 100 !important;

    text-shadow:
        0 0 3px #ffffff,
        0 0 8px #00bfff,
        0 0 16px #0099ff,
        0 0 30px rgba(0,145,255,.8) !important;

    box-shadow:
        0 0 8px rgba(0,180,255,.8),
        0 0 22px rgba(0,120,255,.45),
        inset 0 0 12px rgba(0,120,255,.2) !important;
}


/* Thin premium blue line */

.kk-final-name::after {

    content: "" !important;

    position: absolute !important;

    left: 8% !important;

    right: 8% !important;

    bottom: 7px !important;

    height: 2px !important;

    border-radius: 50% !important;

    background:
        linear-gradient(
            90deg,
            transparent,
            #00aaff,
            #ffffff,
            #00aaff,
            transparent
        ) !important;

    box-shadow:
        0 0 8px #00aaff !important;
}


/* -----------------------------------------------------
   MOBILE
   ----------------------------------------------------- */

@media (max-width: 600px) {

    .kk-final-logo {
        width: 94vw !important;

        margin-top: 25px !important;

        margin-bottom: 28px !important;
    }

    .kk-final-name {

        left: 6% !important;
        right: 6% !important;

        height: 82px !important;

        font-size: 26px !important;

        letter-spacing: .5px !important;

        padding-left: 4px !important;
        padding-right: 4px !important;
    }
}


/* -----------------------------------------------------
   VERY SMALL PHONES
   ----------------------------------------------------- */

@media (max-width: 380px) {

    .kk-final-name {

        height: 76px !important;

        font-size: 22px !important;
    }
}
"""

if soup.head:
    soup.head.append(style)


# =========================================================
# 4. JAVASCRIPT
# =========================================================

script = soup.new_tag("script")

script.string = r"""
(function () {

"use strict";


function removeOldBranding() {

    [
        "#kk-top-brand",
        "#kk-footer-brand",
        ".kk-logo-name",
        ".kk-logo-wrapper"
    ].forEach(function(selector) {

        document
            .querySelectorAll(selector)
            .forEach(function(el) {

                el.remove();

            });

    });

}


/*
 * Find the wizard logo.
 *
 * We deliberately don't replace every image.
 * We look for an image whose filename/alt contains
 * branding terms, otherwise use the large logo-like
 * image in the lower section.
 */

function findWizardLogo() {

    const imgs =
        Array.from(
            document.querySelectorAll("img")
        );


    /* First try filename/alt */

    let found =
        imgs.find(function(img) {

            const src =
                (
                    img.getAttribute("src") ||
                    ""
                ).toLowerCase();

            const alt =
                (
                    img.getAttribute("alt") ||
                    ""
                ).toLowerCase();

            return (
                src.includes("anker") ||
                src.includes("wizard") ||
                alt.includes("anker") ||
                alt.includes("wizard")
            );

        });


    if (found) {
        return found;
    }


    /*
     * Look for a large image appearing
     * in the lower/footer portion.
     */

    const candidates =
        imgs.filter(function(img) {

            const r =
                img.getBoundingClientRect();

            return (
                r.width > 250 &&
                r.height > 180
            );

        });


    /*
     * Prefer the largest portrait-ish logo.
     */

    candidates.sort(function(a, b) {

        const ar =
            a.getBoundingClientRect();

        const br =
            b.getBoundingClientRect();

        return (
            (br.width * br.height) -
            (ar.width * ar.height)
        );

    });


    return candidates[0] || null;
}


function installFinalLogo() {

    removeOldBranding();


    /*
     * Don't duplicate.
     */

    if (
        document.querySelector(
            ".kk-final-logo"
        )
    ) {
        return;
    }


    const logo =
        findWizardLogo();


    if (!logo) {
        return;
    }


    /*
     * Create wrapper.
     */

    const wrapper =
        document.createElement("div");

    wrapper.className =
        "kk-final-logo";


    /*
     * Put wrapper exactly where
     * original logo was.
     */

    logo.parentNode.insertBefore(
        wrapper,
        logo
    );

    wrapper.appendChild(logo);


    /*
     * ONE SINGLE NAME.
     */

    const name =
        document.createElement("div");

    name.className =
        "kk-final-name";

    name.textContent =
        "KARTIK KAMBOJ";


    wrapper.appendChild(name);
}


/* -----------------------------------------------------
   START
   ----------------------------------------------------- */

function start() {

    installFinalLogo();

}


if (
    document.readyState ===
    "loading"
) {

    document.addEventListener(
        "DOMContentLoaded",
        start
    );

} else {

    start();

}


/*
 * Wait for dynamically loaded content.
 */

setTimeout(start, 500);
setTimeout(start, 1500);
setTimeout(start, 3000);
setTimeout(start, 5000);

})();
"""

if soup.body:
    soup.body.append(script)


# =========================================================
# 5. SAVE
# =========================================================

with open(FILE, "w", encoding="utf-8") as f:
    f.write(
        "<!DOCTYPE html>\n" +
        str(soup)
    )


print()
print("==============================================")
print("       FINAL LOGO FIX COMPLETE")
print("==============================================")
print()
print("[✓] Old top Kartik Kamboj removed")
print("[✓] Old lower Kartik Kamboj removed")
print("[✓] Wizard logo preserved")
print("[✓] One single KARTIK KAMBOJ added")
print("[✓] Name placed in original logo-name area")
print("[✓] 3-line-height logo area")
print("[✓] Mobile responsive")
print()
print("==============================================")
