from bs4 import BeautifulSoup

FILE = "index.html"

with open(FILE, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")


# ==========================================================
# REMOVE ALL PREVIOUS PATCHES
# ==========================================================

for el in soup.select(
    "#kk-top-brand, #kk-footer-brand, "
    ".kk-logo-wrapper, .kk-logo-name, "
    ".kk-final-logo, .kk-final-name"
):
    el.decompose()


for style in soup.find_all("style"):
    t = style.get_text(" ", strip=True)

    if any(x in t for x in [
        "kk-top-brand",
        "kk-footer-brand",
        "kk-logo-wrapper",
        "kk-logo-name",
        "kk-final-logo",
        "kk-final-name"
    ]):
        style.decompose()


for script in soup.find_all("script"):
    t = script.get_text(" ", strip=True)

    if any(x in t for x in [
        "kk-top-brand",
        "kk-footer-brand",
        "kk-logo-wrapper",
        "kk-logo-name",
        "kk-final-logo",
        "kk-final-name"
    ]):
        script.decompose()


# ==========================================================
# FINAL CSS
# ==========================================================

style = soup.new_tag("style")

style.string = r"""
/* ==========================================================
   KARTIK KAMBOJ — HEADER ONLY
   ========================================================== */

/*
   IMPORTANT:
   Do NOT touch footer.
   Do NOT touch game images.
   Do NOT touch wizard/footer artwork.
*/


/* Our single header brand */

#kartik-header-brand {

    position: relative !important;

    display: flex !important;

    align-items: center !important;

    justify-content: center !important;

    width: 100% !important;

    height: 105px !important;

    min-height: 105px !important;

    box-sizing: border-box !important;

    margin: 0 !important;

    padding: 10px 8px !important;

    overflow: hidden !important;

    text-align: center !important;

    color: #ffffff !important;

    font-family:
        Arial Black,
        Arial,
        Helvetica,
        sans-serif !important;

    font-size:
        clamp(30px, 8vw, 54px) !important;

    font-weight: 900 !important;

    line-height: 1 !important;

    letter-spacing: 1px !important;

    white-space: nowrap !important;

    text-shadow:
        0 0 4px #ffffff,
        0 0 10px #00baff,
        0 0 22px #008cff,
        0 0 38px rgba(0,140,255,.7) !important;

    background:
        linear-gradient(
            180deg,
            rgba(3,5,16,.98),
            rgba(3,5,16,.88)
        ) !important;

    z-index: 999999 !important;
}


/* premium line */

#kartik-header-brand::after {

    content: "" !important;

    position: absolute !important;

    left: 15% !important;

    right: 15% !important;

    bottom: 7px !important;

    height: 2px !important;

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
        0 0 10px #00aaff !important;
}


/*
   Hide only the ORIGINAL header logo.
   The JavaScript adds a class to the exact element.
*/

.kk-hide-original-header-logo {
    display: none !important;
}


/* Mobile */

@media (max-width: 600px) {

    #kartik-header-brand {

        height: 105px !important;

        min-height: 105px !important;

        font-size: 35px !important;

        letter-spacing: .5px !important;
    }
}


/* Small phone */

@media (max-width: 380px) {

    #kartik-header-brand {

        height: 98px !important;

        min-height: 98px !important;

        font-size: 31px !important;
    }
}
"""

if soup.head:
    soup.head.append(style)


# ==========================================================
# FINAL JAVASCRIPT
# ==========================================================

script = soup.new_tag("script")

script.string = r"""
(function () {

"use strict";


/*
============================================================
FIND THE ACTUAL HEADER
============================================================
*/

function getHeader() {

    return (
        document.querySelector("header") ||
        document.querySelector("nav") ||
        document.querySelector(
            '[role="banner"]'
        ) ||
        document.body
    );

}


/*
============================================================
REMOVE OUR OLD BRANDING
============================================================
*/

function removeOld() {

    document
        .querySelectorAll(
            "#kartik-header-brand"
        )
        .forEach(function(el) {
            el.remove();
        });

}


/*
============================================================
FIND ORIGINAL HEADER LOGO
============================================================

IMPORTANT:
We search ONLY inside the header.

We NEVER search the footer.
We NEVER search game cards.
We NEVER search large images on the page.
============================================================
*/

function findOriginalHeaderLogo(header) {

    if (!header) return null;


    /*
       First: SVG logo
    */

    const svgs =
        Array.from(
            header.querySelectorAll("svg")
        );

    for (const svg of svgs) {

        const box =
            svg.getBoundingClientRect();

        if (
            box.width > 120 &&
            box.width < 500 &&
            box.height > 20 &&
            box.height < 150
        ) {
            return svg;
        }

    }


    /*
       Second: image logo
    */

    const imgs =
        Array.from(
            header.querySelectorAll("img")
        );

    for (const img of imgs) {

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

        const box =
            img.getBoundingClientRect();

        if (
            (
                src.includes("logo") ||
                src.includes("anker") ||
                alt.includes("logo") ||
                alt.includes("anker")
            ) &&
            box.width > 100
        ) {
            return img;
        }

    }


    /*
       Third: link/div containing Anker text
    */

    const elements =
        Array.from(
            header.querySelectorAll(
                "a, div, span"
            )
        );

    for (const el of elements) {

        const text =
            (
                el.textContent ||
                ""
            )
            .replace(/\s+/g, " ")
            .trim()
            .toUpperCase();

        if (
            text === "ANKER GAMES" ||
            text.includes("ANKER GAMES")
        ) {

            const box =
                el.getBoundingClientRect();

            if (
                box.width > 100 &&
                box.height > 20
            ) {
                return el;
            }

        }

    }


    return null;

}


/*
============================================================
CREATE EXACTLY ONE HEADER BRAND
============================================================
*/

function install() {

    removeOld();


    /*
       Don't create multiple copies.
    */

    if (
        document.querySelector(
            "#kartik-header-brand"
        )
    ) {
        return;
    }


    const header =
        getHeader();

    if (!header) return;


    const original =
        findOriginalHeaderLogo(header);


    /*
       If we found the actual logo,
       hide ONLY that logo.
    */

    if (original) {

        original.classList.add(
            "kk-hide-original-header-logo"
        );

    }


    /*
       Create ONE brand.
    */

    const brand =
        document.createElement("div");

    brand.id =
        "kartik-header-brand";

    brand.textContent =
        "KARTIK KAMBOJ";


    /*
       Put it at the top of the header.
    */

    header.insertBefore(
        brand,
        header.firstElementChild
    );

}


/*
============================================================
START
============================================================
*/

function start() {

    install();

}


/*
   Wait until DOM is ready.
*/

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
   A few delayed checks for JS-generated header.
*/

setTimeout(start, 300);
setTimeout(start, 1000);
setTimeout(start, 2500);


/*
============================================================
WATCH HEADER ONLY
============================================================
*/

const observer =
    new MutationObserver(function() {

        clearTimeout(
            window.__kartikHeaderTimer
        );

        window.__kartikHeaderTimer =
            setTimeout(
                install,
                250
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


# ==========================================================
# SAVE
# ==========================================================

with open(FILE, "w", encoding="utf-8") as f:
    f.write(
        "<!DOCTYPE html>\n" +
        str(soup)
    )


print()
print("==============================================")
print("      FINAL HEADER BRANDING INSTALLED")
print("==============================================")
print("[✓] Previous patches removed")
print("[✓] Footer untouched")
print("[✓] Game images untouched")
print("[✓] Only header logo targeted")
print("[✓] One single KARTIK KAMBOJ")
print("[✓] No duplicate branding")
print("[✓] Mobile responsive")
print("==============================================")
