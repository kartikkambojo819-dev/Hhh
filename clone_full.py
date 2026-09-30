import os
import re
from curl_cffi import requests
from bs4 import BeautifulSoup

TARGET_URL = "https://ankergames.net"

print("==============================================")
print("   KARTIK KAMBOJ - MASTER REBRAND SCRIPT")
print("==============================================")

HEADERS = {
    "User-Agent":
    "Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
}

# ------------------------------------------------
# DOWNLOAD ORIGINAL PAGE
# ------------------------------------------------

print("[1/6] Downloading original website...")

try:
    r = requests.get(
        TARGET_URL,
        headers=HEADERS,
        impersonate="chrome",
        timeout=45
    )
except Exception as e:
    print("[!] Download failed:", e)
    raise SystemExit(1)

if r.status_code != 200:
    print("[!] HTTP Error:", r.status_code)
    raise SystemExit(1)

html = r.text

print("[+] Website downloaded.")

# ------------------------------------------------
# PARSE HTML
# ------------------------------------------------

soup = BeautifulSoup(html, "html.parser")

# ------------------------------------------------
# TITLE
# ------------------------------------------------

if soup.title:
    soup.title.string = "Kartik Kamboj - PC Games"

# ------------------------------------------------
# DIRECT TEXT REPLACEMENT
# ------------------------------------------------

print("[2/6] Replacing existing branding...")

TEXT_REPLACEMENTS = {
    "ANKER GAMES": "KARTIK KAMBOJ",
    "ANKERGames": "KARTIK KAMBOJ",
    "Anker Games": "Kartik Kamboj",
    "AnkerGames": "Kartik Kamboj",
    "anker games": "kartik kamboj",
    "ankergames": "kartikkamboj",
    "ANKERGAMES": "KARTIK KAMBOJ",
}

for node in soup.find_all(string=True):

    parent = node.parent

    if parent and parent.name in [
        "script",
        "style",
        "noscript",
        "template"
    ]:
        continue

    old = str(node)
    new = old

    for a, b in TEXT_REPLACEMENTS.items():
        new = new.replace(a, b)

    if new != old:
        node.replace_with(new)

# ------------------------------------------------
# META / ALT / TITLE / ARIA
# ------------------------------------------------

for tag in soup.find_all(True):

    for attr in [
        "alt",
        "title",
        "aria-label",
        "data-title",
        "data-brand",
        "data-name"
    ]:

        if tag.has_attr(attr):

            value = str(tag.get(attr))

            for a, b in TEXT_REPLACEMENTS.items():
                value = value.replace(a, b)

            tag[attr] = value

# ------------------------------------------------
# CSS
# ------------------------------------------------

print("[3/6] Installing master branding CSS...")

css = r"""
/* ==========================================================
   KARTIK KAMBOJ MASTER BRANDING
   ========================================================== */

:root {
    --kk-bg: #04050d;
    --kk-blue: #00aaff;
    --kk-white: #ffffff;
}

/* ----------------------------------------------------------
   GENERAL
   ---------------------------------------------------------- */

html,
body {
    overflow-x: hidden !important;
}

/* ----------------------------------------------------------
   TOP HEADER
   ---------------------------------------------------------- */

/*
   Hide old logo IMAGE only in the header.
*/

header img,
nav img,
.header img,
.navbar img,
[class*="header"] img,
[class*="navbar"] img {
    /*
       Don't hide every image globally.
       The JS below specifically handles the branding image.
    */
}

/* Our replacement top brand */

#kk-top-brand {
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;

    color: #ffffff !important;

    font-family:
        Arial Black,
        Arial,
        Helvetica,
        sans-serif !important;

    font-size: clamp(27px, 5vw, 50px) !important;

    font-weight: 950 !important;

    line-height: 1 !important;

    letter-spacing: -1.5px !important;

    white-space: nowrap !important;

    text-decoration: none !important;

    text-shadow:
        0 0 5px rgba(255,255,255,.7),
        0 0 12px rgba(0,170,255,.8),
        0 0 25px rgba(0,120,255,.55) !important;

    z-index: 999999 !important;

    position: relative !important;
}

/* ----------------------------------------------------------
   BOTTOM LOGO
   ---------------------------------------------------------- */

#kk-footer-brand {
    display: block !important;

    width: 100% !important;

    text-align: center !important;

    color: #ffffff !important;

    font-family:
        Arial Black,
        Arial,
        Helvetica,
        sans-serif !important;

    font-size: clamp(30px, 7vw, 64px) !important;

    font-weight: 950 !important;

    line-height: 1 !important;

    letter-spacing: 1px !important;

    text-shadow:
        0 0 5px #ffffff,
        0 0 12px #00aaff,
        0 0 25px #008cff,
        0 0 40px rgba(0,140,255,.7) !important;

    margin: 10px auto !important;

    position: relative !important;

    z-index: 999999 !important;
}

/* ----------------------------------------------------------
   OLD BRANDING HIDDEN
   ---------------------------------------------------------- */

.kk-old-brand {
    display: none !important;
}

/* ----------------------------------------------------------
   MOBILE
   ---------------------------------------------------------- */

@media (max-width: 600px) {

    #kk-top-brand {
        font-size: 27px !important;
        letter-spacing: -1px !important;
    }

    #kk-footer-brand {
        font-size: 34px !important;
    }
}
"""

style = soup.new_tag("style")
style.string = css

if soup.head:
    soup.head.append(style)
else:
    soup.insert(0, style)

# ------------------------------------------------
# MASTER JAVASCRIPT
# ------------------------------------------------

print("[4/6] Installing runtime branding engine...")

js = r"""
(function () {

"use strict";

const BRAND = "KARTIK KAMBOJ";

/* ==========================================================
   TEXT REPLACEMENT
   ========================================================== */

function replaceBrandText(root) {

    if (!root) return;

    const walker = document.createTreeWalker(
        root,
        NodeFilter.SHOW_TEXT,
        {
            acceptNode: function (node) {

                const p = node.parentElement;

                if (!p) {
                    return NodeFilter.FILTER_REJECT;
                }

                const tag = p.tagName.toLowerCase();

                if (
                    tag === "script" ||
                    tag === "style" ||
                    tag === "noscript" ||
                    tag === "textarea"
                ) {
                    return NodeFilter.FILTER_REJECT;
                }

                return NodeFilter.FILTER_ACCEPT;
            }
        }
    );

    const nodes = [];

    let node;

    while ((node = walker.nextNode())) {
        nodes.push(node);
    }

    nodes.forEach(function (n) {

        let text = n.nodeValue;

        if (!text) return;

        let updated = text;

        updated = updated.replace(
            /ANKER\s*GAMES/gi,
            BRAND
        );

        updated = updated.replace(
            /ANKERGames/gi,
            BRAND
        );

        updated = updated.replace(
            /AnkerGames/gi,
            BRAND
        );

        updated = updated.replace(
            /Anker\s*Games/gi,
            BRAND
        );

        if (updated !== text) {
            n.nodeValue = updated;
        }
    });
}


/* ==========================================================
   ATTRIBUTE REPLACEMENT
   ========================================================== */

function replaceAttributes(root) {

    if (!root) return;

    const elements = root.querySelectorAll("*");

    elements.forEach(function (el) {

        [
            "alt",
            "title",
            "aria-label",
            "data-brand",
            "data-name"
        ].forEach(function (attr) {

            if (!el.hasAttribute(attr)) return;

            let value = el.getAttribute(attr);

            if (!value) return;

            value = value.replace(
                /ANKER\s*GAMES/gi,
                BRAND
            );

            value = value.replace(
                /AnkerGames/gi,
                BRAND
            );

            el.setAttribute(attr, value);
        });
    });
}


/* ==========================================================
   FIND TOP HEADER
   ========================================================== */

function findTopArea() {

    return (
        document.querySelector("header") ||
        document.querySelector("nav") ||
        document.querySelector(".header") ||
        document.querySelector(".navbar") ||
        document.body
    );
}


/* ==========================================================
   FIND FOOTER
   ========================================================== */

function findFooter() {

    return (
        document.querySelector("footer") ||
        document.querySelector(".footer") ||
        document.body
    );
}


/* ==========================================================
   TOP BRAND
   ========================================================== */

function createTopBrand() {

    if (document.getElementById("kk-top-brand")) {
        return;
    }

    const area = findTopArea();

    if (!area) return;

    /*
       Search for elements that visibly contain old branding.
    */

    const all = area.querySelectorAll(
        "img, svg, a, span, div"
    );

    let found = null;

    for (const el of all) {

        const text =
            (
                el.textContent ||
                ""
            ).trim().toUpperCase();

        const src =
            (
                el.getAttribute("src") ||
                ""
            ).toLowerCase();

        const alt =
            (
                el.getAttribute("alt") ||
                ""
            ).toLowerCase();

        if (
            text.includes("ANKER GAMES") ||
            src.includes("anker") ||
            alt.includes("anker")
        ) {
            found = el;
            break;
        }
    }

    /*
       If old logo was found, hide it.
    */

    if (found) {

        found.classList.add("kk-old-brand");

        /*
           If it's a parent container, don't destroy header layout.
        */

        if (
            found.tagName === "IMG" ||
            found.tagName === "SVG"
        ) {
            found.style.display = "none";
        }
    }

    /*
       Create our brand.
    */

    const brand = document.createElement("div");

    brand.id = "kk-top-brand";

    brand.textContent = BRAND;

    /*
       Put it near the beginning of header.
    */

    if (area.firstElementChild) {
        area.insertBefore(
            brand,
            area.firstElementChild
        );
    } else {
        area.appendChild(brand);
    }
}


/* ==========================================================
   FOOTER BRAND
   ========================================================== */

function createFooterBrand() {

    if (document.getElementById("kk-footer-brand")) {
        return;
    }

    const footer = findFooter();

    if (!footer) return;

    const all = footer.querySelectorAll(
        "img, svg, a, span, div"
    );

    let logo = null;

    for (const el of all) {

        const text =
            (
                el.textContent ||
                ""
            ).trim().toUpperCase();

        const src =
            (
                el.getAttribute("src") ||
                ""
            ).toLowerCase();

        const alt =
            (
                el.getAttribute("alt") ||
                ""
            ).toLowerCase();

        if (
            text.includes("ANKER GAMES") ||
            src.includes("anker") ||
            alt.includes("anker")
        ) {
            logo = el;
            break;
        }
    }

    /*
       IMPORTANT:
       If footer has the wizard image, preserve the image
       and place our text over its branding area.
    */

    if (logo) {

        /*
           If it is an image, create a wrapper.
        */

        if (logo.tagName === "IMG") {

            const wrapper =
                document.createElement("div");

            wrapper.style.position = "relative";
            wrapper.style.display = "block";
            wrapper.style.width = "100%";
            wrapper.style.textAlign = "center";

            logo.parentNode.insertBefore(
                wrapper,
                logo
            );

            wrapper.appendChild(logo);

            const replacement =
                document.createElement("div");

            replacement.id = "kk-footer-brand";

            replacement.textContent = BRAND;

            replacement.style.position = "absolute";
            replacement.style.left = "0";
            replacement.style.right = "0";

            /*
               Logo in screenshot has branding near
               lower part, so place replacement there.
            */

            replacement.style.bottom = "8%";

            /*
               Cover original text.
            */

            replacement.style.background =
                "rgba(4,5,13,.96)";

            replacement.style.padding =
                "8px 4px";

            replacement.style.boxSizing =
                "border-box";

            wrapper.appendChild(
                replacement
            );

        } else {

            logo.classList.add(
                "kk-old-brand"
            );

            const replacement =
                document.createElement("div");

            replacement.id =
                "kk-footer-brand";

            replacement.textContent =
                BRAND;

            footer.appendChild(
                replacement
            );
        }

    } else {

        /*
           If no logo was detected,
           append branding anyway.
        */

        const replacement =
            document.createElement("div");

        replacement.id =
            "kk-footer-brand";

        replacement.textContent =
            BRAND;

        footer.appendChild(
            replacement
        );
    }
}


/* ==========================================================
   RUN EVERYTHING
   ========================================================== */

function applyBranding() {

    replaceBrandText(document.body);

    replaceAttributes(document.body);

    createTopBrand();

    createFooterBrand();
}


/* ==========================================================
   PAGE LOAD
   ========================================================== */

function start() {

    applyBranding();

    /*
       Run again because many modern websites
       generate content using JavaScript.
    */

    setTimeout(applyBranding, 300);
    setTimeout(applyBranding, 1000);
    setTimeout(applyBranding, 2500);
    setTimeout(applyBranding, 5000);
}


/* ==========================================================
   MUTATION OBSERVER
   ========================================================== */

const observer =
    new MutationObserver(function () {

        /*
           Debounce slightly.
        */

        clearTimeout(
            window.__kkBrandTimer
        );

        window.__kkBrandTimer =
            setTimeout(
                applyBranding,
                50
            );
    });

observer.observe(
    document.documentElement,
    {
        childList: true,
        subtree: true,
        characterData: true
    }
);


/* ==========================================================
   START
   ========================================================== */

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

})();
"""

script = soup.new_tag("script")
script.string = js

if soup.body:
    soup.body.append(script)

# ------------------------------------------------
# SAVE
# ------------------------------------------------

print("[5/6] Saving index.html...")

with open(
    "index.html",
    "w",
    encoding="utf-8"
) as f:
    f.write(
        "<!DOCTYPE html>\n" +
        str(soup)
    )

print("[+] index.html created.")

# ------------------------------------------------
# VERIFY
# ------------------------------------------------

print("[6/6] Checking generated file...")

with open(
    "index.html",
    "r",
    encoding="utf-8"
) as f:
    final_html = f.read()

checks = [
    "KARTIK KAMBOJ",
    "kk-top-brand",
    "kk-footer-brand",
    "MutationObserver"
]

for item in checks:

    if item in final_html:
        print("[OK] " + item)
    else:
        print("[WARNING] Missing:", item)

print("")
print("==============================================")
print("       MASTER REBRAND COMPLETE")
print("==============================================")
