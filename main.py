import streamlit as st
import streamlit.components.v1 as components
import urllib.parse
import urllib.request
import json
import re
from html import escape


# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="record hotel",
    page_icon="♫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CSS
# =========================================================

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&family=Noto+Serif+KR:wght@400;500;600&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 55% 35%, #3b281d 0%, #24160f 42%, #120b08 78%, #0b0705 100%)
        !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

[data-testid="stToolbar"] {
    display: none !important;
}

.main .block-container {
    padding-top: 0 !important;
    max-width: 1400px !important;
}

/* =========================================================
   SIDEBAR
   ========================================================= */

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #170d09 0%, #120906 55%, #0d0705 100%) !important;
    border-right: 1px solid rgba(190,145,92,0.22);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 35px;
}

.sidebar-title {
    color: #d9a96f;
    font-family: "Cormorant Garamond", Georgia, serif;
    font-size: 24px;
    letter-spacing: 4px;
    text-align: center;
}

.sidebar-subtitle {
    color: #805c3d;
    font-family: "Cormorant Garamond", Georgia, serif;
    font-size: 12px;
    letter-spacing: 3px;
    text-align: center;
    margin-top: 7px;
    margin-bottom: 45px;
}

.sidebar-rule {
    width: 67px;
    height: 1px;
    background: #65452f;
    margin: 0 auto 18px auto;
}

[data-testid="stSidebar"] .stButton {
    margin: 0 !important;
}

[data-testid="stSidebar"] .stButton > button {
    width: 100% !important;
    background: transparent !important;
    border: 0 !important;
    box-shadow: none !important;
    color: #9b704c !important;
    font-family: "Cormorant Garamond", Georgia, serif !important;
    font-size: 15px !important;
    letter-spacing: 4px !important;
    text-align: left !important;
    padding: 14px 12px !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    color: #e1b67c !important;
    background: rgba(190,137,82,0.08) !important;
}

/* =========================================================
   COMMON BUTTON
   ========================================================= */

div[data-testid="stButton"] > button {
    min-height: 44px !important;
    width: 100% !important;
    padding: 0.55rem 1rem !important;
    line-height: 1.25 !important;
    white-space: normal !important;
    background: transparent !important;
    color: #d8ad79 !important;
    border: 1px solid rgba(190,145,92,0.5) !important;
    border-radius: 2px !important;
    font-family: "Cormorant Garamond", Georgia, serif !important;
    letter-spacing: 3px !important;
    transition: 0.25s ease !important;
}

div[data-testid="stButton"] > button:hover {
    background: rgba(197,145,88,0.08) !important;
    border-color: #d5a66c !important;
    color: #efd7b0 !important;
}

/* =========================================================
   MAIN
   ========================================================= */

.welcome-area {
    min-height: 82vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
}

.welcome-small {
    color: #a6784c;
    font-family: "Cormorant Garamond", Georgia, serif;
    font-size: 14px;
    letter-spacing: 5px;
    margin-bottom: 18px;
}

.welcome-title {
    color: #dcae73;
    font-family: "Cormorant Garamond", Georgia, serif;
    font-size: clamp(58px, 7vw, 100px);
    font-weight: 400;
    letter-spacing: 8px;
    line-height: 1;
}

.welcome-line {
    width: 110px;
    height: 1px;
    background: #9c7047;
    margin: 28px auto;
}

.welcome-description {
    color: #bda087;
    font-family: "Noto Serif KR", serif;
    font-size: 15px;
    line-height: 2;
    letter-spacing: 1px;
}

/* =========================================================
   LETTER
   ========================================================= */

.letter-wrap {
    min-height: 86vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 35px 20px;
}

.letter-paper {
    width: min(1080px, 90vw);
    min-height: 650px;
    box-sizing: border-box;
    padding: 72px 90px;
    background: radial-gradient(ellipse at center, #f7eedb 0%, #eee0c4 62%, #e2cfac 100%);
    border: 1px solid rgba(117,80,42,0.18);
    box-shadow: 0 20px 45px rgba(0,0,0,0.45);
    position: relative;
    color: #49382c;
}

.letter-paper:before {
    content: "";
    position: absolute;
    inset: 15px;
    border: 1px solid rgba(117,80,42,0.18);
    pointer-events: none;
}

.letter-date {
    color: #856344;
    text-align: right;
    font-family: "Cormorant Garamond", Georgia, serif;
    font-size: 14px;
    margin-bottom: 48px;
}

.letter-title {
    color: #49301f;
    font-family: "Cormorant Garamond", Georgia, serif;
    font-size: 34px;
    letter-spacing: 3px;
    margin-bottom: 38px;
}

.letter-body {
    color: #49382c;
    font-family: "Noto Serif KR", serif;
    font-size: 17px;
    line-height: 2.25;
    letter-spacing: 0.2px;
}

.letter-sign {
    color: #604531;
    text-align: right;
    font-family: "Cormorant Garamond", Georgia, serif;
    font-size: 17px;
    line-height: 1.9;
    margin-top: 45px;
}

/* =========================================================
   CHOICE
   ========================================================= */

.section-area {
    min-height: auto;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding-top: clamp(38px, 7vh, 76px);
    margin-bottom: 22px;
}

.section-title {
    color: #d5a56d;
    font-family: "Cormorant Garamond", Georgia, serif;
    font-size: 48px;
    letter-spacing: 6px;
    margin-bottom: 12px;
}

.section-subtitle {
    color: #96765d;
    font-family: "Noto Serif KR", serif;
    font-size: 14px;
    letter-spacing: 2px;
    margin-bottom: 0;
    line-height: 1.15;
}

.choice-paper-button button {
    min-height: 95px !important;
    background: radial-gradient(ellipse at center, #fbf3e3 0%, #ead9b9 100%) !important;
    color: #4c3424 !important;
    border: 1px solid rgba(111,75,42,0.45) !important;
    border-radius: 2px !important;
    font-family: "Noto Serif KR", serif !important;
    font-size: 18px !important;
    letter-spacing: 3px !important;
    box-shadow: 0 15px 35px rgba(0,0,0,0.25) !important;
}

/* =========================================================
   ROOM SERVICE
   ========================================================= */

.room-service-container {
    width: min(1100px, 90vw);
    margin: 0 auto;
    padding-top: 45px;
}

.room-service-title {
    color: #d5a56d;
    font-family: "Cormorant Garamond", Georgia, serif;
    font-size: 48px;
    letter-spacing: 6px;
    text-align: center;
}

.room-service-subtitle {
    color: #96765d;
    font-family: "Noto Serif KR", serif;
    font-size: 14px;
    text-align: center;
    margin-top: 8px;
}

/* =========================================================
   RECORD PLAYER
   ========================================================= */

.record-stage {
    min-height: 470px;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
}

.record-player {
    width: 370px;
    height: 370px;
    border-radius: 50%;
    background:
        repeating-radial-gradient(
            circle,
            #17110e 0px,
            #17110e 3px,
            #211813 4px,
            #211813 6px
        );
    box-shadow:
        0 0 0 10px rgba(47,31,22,0.75),
        0 25px 55px rgba(0,0,0,0.6);
    position: relative;
}

.record-player:before {
    content: "";
    position: absolute;
    inset: 28px;
    border-radius: 50%;
    border: 1px solid rgba(255,255,255,0.06);
}

.record-label {
    width: 125px;
    height: 125px;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    border-radius: 50%;
    background:
        radial-gradient(
            circle,
            #b98555 0%,
            #8f5e3b 48%,
            #6c412a 100%
        );
    box-shadow: 0 0 15px rgba(0,0,0,0.45);
}

.record-hole {
    width: 12px;
    height: 12px;
    background: #17110e;
    border-radius: 50%;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
}

.record-ring {
    position: absolute;
    width: 92px;
    height: 92px;
    border-radius: 50%;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    border: 1px solid rgba(240,204,160,0.3);
}

.record-label-text {
    position: absolute;
    width: 100%;
    text-align: center;
    top: 31px;
    color: #ead1af;
    font-family: "Cormorant Garamond", Georgia, serif;
    font-size: 12px;
    letter-spacing: 2px;
}

.record-caption {
    text-align: center;
    color: #b99676;
    font-family: "Noto Serif KR", serif;
    margin-top: 15px;
}

/* =========================================================
   FIREPLACE
   ========================================================= */

.fireplace-container {
    width: min(1100px, 90vw);
    margin: 0 auto;
    padding-top: 40px;
}

.fireplace-title {
    color: #d5a56d;
    font-family: "Cormorant Garamond", Georgia, serif;
    font-size: 48px;
    letter-spacing: 6px;
    text-align: center;
}

.fireplace-subtitle {
    color: #96765d;
    font-family: "Noto Serif KR", serif;
    text-align: center;
    font-size: 14px;
    margin-top: 8px;
}

.fireplace {
    width: min(720px, 80vw);
    height: 350px;
    margin: 55px auto 25px auto;
    background:
        radial-gradient(
            ellipse at 50% 100%,
            #8a4424 0%,
            #542617 28%,
            #27130d 58%,
            #110a07 100%
        );
    border: 16px solid #3b261a;
    box-shadow:
        inset 0 0 40px rgba(0,0,0,0.7),
        0 25px 60px rgba(0,0,0,0.5);
    position: relative;
    overflow: hidden;
}

.fire {
    position: absolute;
    bottom: 30px;
    left: 50%;
    width: 130px;
    height: 190px;
    transform: translateX(-50%);
    background:
        radial-gradient(
            ellipse at center bottom,
            #f2a34d 0%,
            #d8642f 35%,
            #7b2f1b 62%,
            transparent 72%
        );
    border-radius: 50% 50% 35% 35%;
    filter: blur(1px);
    animation: flame 1.4s infinite alternate ease-in-out;
}

.fire-small {
    position: absolute;
    bottom: 35px;
    left: 50%;
    width: 65px;
    height: 110px;
    transform: translateX(-50%);
    background:
        radial-gradient(
            ellipse at center bottom,
            #ffe0a3 0%,
            #f19a43 40%,
            #bd4825 70%,
            transparent 75%
        );
    border-radius: 50% 50% 35% 35%;
    animation: flameSmall 0.9s infinite alternate ease-in-out;
}

.wood {
    position: absolute;
    bottom: 27px;
    left: 50%;
    width: 210px;
    height: 22px;
    background: #24140e;
    transform: translateX(-50%) rotate(4deg);
    border-radius: 8px;
}

.wood.two {
    transform: translateX(-50%) rotate(-7deg);
}

@keyframes flame {
    from {
        transform: translateX(-50%) scaleY(0.95) rotate(-2deg);
    }
    to {
        transform: translateX(-50%) scaleY(1.08) rotate(2deg);
    }
}

@keyframes flameSmall {
    from {
        transform: translateX(-50%) scaleY(0.9);
    }
    to {
        transform: translateX(-50%) scaleY(1.1);
    }
}

.fireplace-note {
    text-align: center;
    color: #a17f63;
    font-family: "Noto Serif KR", serif;
    line-height: 2;
}

/* =========================================================
   SEARCH
   ========================================================= */

.listen-search {
    width: min(1000px, 90vw);
    margin: 30px auto 0 auto;
}

.result-title {
    color: #dca072;
    font-family: "Cormorant Garamond", Georgia, serif;
    font-size: 28px;
    letter-spacing: 3px;
    margin: 35px 0 15px 0;
}

.result-card {
    display: flex;
    gap: 20px;
    align-items: center;
    background: rgba(247,238,219,0.06);
    border: 1px solid rgba(199,157,109,0.25);
    padding: 18px;
    margin: 12px 0;
    border-radius: 4px;
}

.result-card img {
    width: 90px;
    height: 90px;
    object-fit: cover;
}

.result-name {
    color: #e0bd91;
    font-family: "Cormorant Garamond", Georgia, serif;
    font-size: 23px;
}

.result-meta {
    color: #a98a70;
    font-family: "Noto Serif KR", serif;
    font-size: 13px;
    line-height: 1.8;
}

.no-result {
    color: #9b7960;
    text-align: center;
    margin-top: 35px;
    font-family: "Noto Serif KR", serif;
    font-size: 15px;
    line-height: 2;
}

[data-testid="stTextInput"] input {
    background: #f3ead9 !important;
    color: #49382c !important;
    border: 1px solid #8d6746 !important;
    border-radius: 2px !important;
    font-family: "Noto Serif KR", serif !important;
}

[data-testid="stRadio"] label {
    color: #a98a70 !important;
}

/* =========================================================
   BACK BUTTON
   ========================================================= */

.back-button {
    margin-top: 20px;
}


/* =========================================================
   RECORD HOTEL POLISH PASS — layout + luxury cocktail styling
   Kept inside this single Python file; no separate HTML/CSS files.
   ========================================================= */
.main .block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2.4rem !important;
}

/* Bring ROOM SERVICE buttons up, closer to the title and subtitle. */
.section-area {
    min-height: 0 !important;
    padding-top: clamp(30px, 5vh, 58px) !important;
    margin-bottom: 20px !important;
}
.section-title {
    font-size: clamp(36px, 4vw, 48px) !important;
    letter-spacing: 5px !important;
    line-height: 1.15 !important;
    margin: 0 0 10px !important;
}
.section-subtitle {
    margin: 0 !important;
    line-height: 1.8 !important;
    letter-spacing: 1px !important;
}
.section-area + div[data-testid="stHorizontalBlock"] {
    gap: 22px !important;
    max-width: 1060px;
    margin: 0 auto !important;
}
.section-area + div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] > button {
    min-height: 54px !important;
    font-size: 15px !important;
    letter-spacing: 3px !important;
    background: linear-gradient(135deg, rgba(111,72,43,.20), rgba(45,27,19,.55)) !important;
    border: 1px solid rgba(207,157,99,.48) !important;
    box-shadow: 0 8px 22px rgba(0,0,0,.13), inset 0 1px rgba(255,255,255,.025) !important;
}
.section-area + div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, rgba(156,99,57,.30), rgba(64,37,25,.72)) !important;
    transform: translateY(-1px);
}

/* MY ROOM check-in gate: centered, compact, and visually grouped. */
.auth-box {
    margin: 16px auto 8px !important;
    padding: 25px 30px !important;
    max-width: 520px !important;
    background: linear-gradient(145deg, rgba(247,238,219,.075), rgba(247,238,219,.025)) !important;
    border-color: rgba(199,157,109,.32) !important;
    box-shadow: 0 16px 38px rgba(0,0,0,.22) !important;
}
.auth-subtitle { margin: 5px 0 8px !important; }

/* Cocktail menu cards: editorial hotel-bar styling. */
.cocktail-header {
    padding: 18px 0 24px !important;
}
.cocktail-kicker {
    color: #a17b59 !important;
    font-size: 11px !important;
    letter-spacing: 4.5px !important;
}
.cocktail-title {
    font-size: clamp(40px, 5vw, 58px) !important;
    letter-spacing: 6px !important;
    text-shadow: 0 4px 24px rgba(219,151,91,.08);
}
.cocktail-subtitle {
    margin-top: 10px !important;
    color: #b79a80 !important;
    letter-spacing: .5px !important;
}
.order-slip {
    min-height: 355px !important;
    padding: 22px 15px 20px !important;
    border: 1px solid rgba(211,170,121,.34) !important;
    border-radius: 3px !important;
    background: linear-gradient(155deg, rgba(255,240,220,.075), rgba(54,34,24,.22) 54%, rgba(14,9,7,.28)) !important;
    box-shadow: 0 18px 42px rgba(0,0,0,.22), inset 0 1px rgba(255,255,255,.035) !important;
    transition: transform .22s ease, border-color .22s ease, box-shadow .22s ease;
}
.order-slip:hover {
    transform: translateY(-3px);
    border-color: rgba(224,177,123,.65) !important;
    box-shadow: 0 23px 48px rgba(0,0,0,.3), 0 0 25px rgba(210,155,97,.055) !important;
}
.order-slip:before { inset: 8px !important; border-color: rgba(211,170,121,.14) !important; }
.slip-no { color: #997453 !important; letter-spacing: 2.5px !important; }
.slip-label { color: #f0d5b3 !important; font-size: 15px !important; margin-top: 12px !important; }
.slip-drink { color: #dfb17c !important; font-size: 14px !important; letter-spacing: 1.8px !important; }
.slip-desc { color: #b2957c !important; font-size: 11px !important; }
.order-slip div[data-testid="stButton"] > button { margin-top: 10px !important; }

/* Miniature glass composition. All decorative parts stay clipped inside the glass. */
.mini-drink { transform: scale(1.05); margin-top: 16px !important; margin-bottom: 8px !important; filter: drop-shadow(0 12px 12px rgba(0,0,0,.26)) !important; }
.mini-glass { backdrop-filter: blur(2px); box-shadow: inset 7px 0 13px rgba(255,255,255,.08), inset -7px 0 12px rgba(0,0,0,.08), 0 8px 18px rgba(0,0,0,.18) !important; }
.mini-rim { border-color: rgba(255,244,229,.82) !important; box-shadow: 0 0 8px rgba(255,255,255,.07) !important; }
.mini-pink .mini-glass {
    height: 58px !important; bottom: 37px !important; width: 88px !important; left: 12px !important;
    border-radius: 0 0 46px 46px !important;
    background: linear-gradient(90deg, rgba(255,255,255,.24), rgba(255,255,255,.025) 42%, rgba(255,255,255,.15)) !important;
}
.mini-pink .mini-liquid { background: linear-gradient(180deg,#ffdce6 0%,#f29db8 42%,#bd557d 100%) !important; box-shadow: inset 0 3px 8px rgba(255,255,255,.22); }
.mini-green .mini-liquid { background: linear-gradient(180deg,#d8ffc9 0%,#8fe4a0 35%,#3a9b65 100%) !important; }
.mini-orange .mini-liquid { background: linear-gradient(180deg,#ffe9ad 0%,#ffb84e 45%,#e96b20 100%) !important; }
.mini-navy .mini-liquid { background: linear-gradient(180deg,#91b4ec 0%,#4c669f 45%,#171e42 100%) !important; }
.mini-cocktail-olive { background: radial-gradient(circle at 30% 25%, #fff0bd, #c8a76a 52%, #78603b) !important; border: 1px solid rgba(255,255,255,.55); box-shadow: 0 0 0 3px rgba(255,255,255,.07), inset 2px 2px 4px rgba(255,255,255,.45) !important; }
.mini-pick { background: linear-gradient(#fff0c8,#c59b62) !important; }

/* Large cocktail scene: more glass-like reflections, restrained luxury colors. */
.drink-stage { min-height: 410px !important; padding: 0 0 8px !important; }
.drink-visual {
    height: 365px !important;
    filter: drop-shadow(0 20px 24px rgba(0,0,0,.24));
}
.glass {
    border-color: rgba(255,238,220,.7) !important;
    background: linear-gradient(90deg, rgba(255,255,255,.19), rgba(255,255,255,.025) 24%, rgba(255,255,255,.015) 70%, rgba(255,255,255,.14)) !important;
    box-shadow: 0 24px 50px rgba(0,0,0,.25), inset 9px 0 15px rgba(255,255,255,.08), inset -9px 0 15px rgba(0,0,0,.07) !important;
}
.glass .liquid { opacity: .96 !important; }
.glass-rim { border-color: rgba(255,245,231,.82) !important; box-shadow: 0 0 10px rgba(255,255,255,.1) !important; }
.glass-shine { background: linear-gradient(180deg, rgba(255,255,255,.34), rgba(255,255,255,.025)) !important; width: 10px !important; left: 20px !important; filter: blur(1.5px) !important; }
.drink-scene.pink .glass {
    width: 238px !important; height: 160px !important; margin-top: 35px !important;
    border-radius: 0 0 119px 119px !important;
    background: linear-gradient(90deg, rgba(255,255,255,.22), rgba(255,255,255,.02) 40%, rgba(255,255,255,.12)) !important;
}
.drink-scene.pink .liquid { background: linear-gradient(180deg,#ffdce6 0%,#f19ab6 35%,#c95c84 72%,#963b62 100%) !important; }
.drink-scene.green .glass { width: 170px !important; height: 255px !important; border-radius: 8px 8px 36px 36px !important; }
.drink-scene.green .liquid { background: linear-gradient(180deg,#d9ffc8 0%,#9ce7a3 28%,#57bf7c 68%,#2d8154 100%) !important; }
.drink-scene.orange .glass { width: 210px !important; height: 205px !important; border-radius: 12px 12px 54px 54px !important; }
.drink-scene.orange .liquid { background: linear-gradient(180deg,#fff0b9 0%,#ffd077 24%,#ff9e34 65%,#d9581b 100%) !important; }
.drink-scene.navy .glass { width: 218px !important; height: 200px !important; border-radius: 12px 12px 44px 44px !important; }
.drink-scene.navy .liquid { background: linear-gradient(180deg,#9ab8ef 0%,#526fae 28%,#2d3e75 62%,#11172f 100%) !important; }
/* Keep garnishes inside the glass boundary, including at full fill. */
.melon-ice-cream { top: 15px !important; width: 64px !important; height: 34px !important; }
.drink-straw { top: 18px !important; height: 62px !important; }
.drink-cherry { top: 24px !important; width: 15px !important; height: 15px !important; }
.orange-half.one { top: 18px !important; right: 8px !important; width: 54px !important; height: 32px !important; }
.orange-half.two { top: 56px !important; bottom: auto !important; left: 17px !important; width: 44px !important; height: 25px !important; }
.pink-olive { top: 18px !important; width: 20px !important; height: 20px !important; }
.pink-pick { top: 8px !important; height: 37px !important; }
.navy-garnish { top: 22px !important; left: 15px !important; width: 52px !important; }
.drink-name { margin-top: 34px !important; font-size: 17px !important; letter-spacing: 3.5px !important; }
.drink-state { color: #a98768 !important; letter-spacing: 2.5px !important; }
.concierge-card {
    border-radius: 3px !important;
    padding: 22px 24px !important;
    background: linear-gradient(145deg, rgba(255,240,220,.075), rgba(54,34,24,.18)) !important;
    border-color: rgba(211,170,121,.3) !important;
}
.concierge-title { font-size: 20px !important; line-height: 1.65 !important; }
.recommendation-title { font-size: 24px !important; letter-spacing: 3.5px !important; }

@media (max-width: 900px) {
    .section-area { padding-top: 28px !important; margin-bottom: 16px !important; }
    .section-area + div[data-testid="stHorizontalBlock"] { gap: 12px !important; }
    .cocktail-header { padding: 14px 0 18px !important; }
    .order-slip { min-height: 320px !important; }
    .drink-visual { transform: scale(.9); transform-origin: center top; margin-bottom: -18px; }
}
@media (max-width: 700px) {
    .section-title { font-size: 34px !important; letter-spacing: 3px !important; }
    .section-subtitle { padding: 0 14px; font-size: 12px !important; }
    .order-slip { min-height: 270px !important; }
    .drink-visual { transform: scale(.78); transform-origin: center top; margin-bottom: -48px; }
    .drink-name { margin-top: 10px !important; }
}

</style>

<style>
.record-selected-note {
    text-align: center;
    color: #b99676;
    font-family: "Noto Serif KR", serif;
    margin: 8px 0 20px 0;
    line-height: 1.8;
}
.room-record-card {
    background: rgba(247,238,219,0.055);
    border: 1px solid rgba(199,157,109,0.24);
    padding: 16px;
    margin: 12px 0;
    border-radius: 4px;
}
.room-record-card img {
    width: 86px;
    height: 86px;
    object-fit: cover;
    border: 1px solid rgba(199,157,109,0.25);
}
.room-record-title {
    color: #e0bd91;
    font-family: "Cormorant Garamond", Georgia, serif;
    font-size: 21px;
    letter-spacing: 2px;
}
.room-record-meta {
    color: #a98a70;
    font-family: "Noto Serif KR", serif;
    font-size: 13px;
    line-height: 1.8;
}
.auth-box {
    width: min(520px, 90vw);
    margin: 18px auto 0 auto;
    padding: 28px 34px;
    background: rgba(247,238,219,0.055);
    border: 1px solid rgba(199,157,109,0.28);
    box-shadow: 0 20px 50px rgba(0,0,0,0.35);
}
.auth-title {
    color: #d5a56d;
    font-family: "Cormorant Garamond", Georgia, serif;
    font-size: 42px;
    letter-spacing: 5px;
    text-align: center;
}
.auth-subtitle {
    color: #96765d;
    font-family: "Noto Serif KR", serif;
    text-align: center;
    margin: 8px 0 18px 0;
    line-height: 1.8;
}
.room-tabs {
    color: #c49a70;
    font-family: "Cormorant Garamond", Georgia, serif;
    letter-spacing: 3px;
    text-align: center;

    margin: 20px 0;
}

/* =========================================================
   COCKTAIL BAR
   ========================================================= */
.cocktail-header {
    width: min(1120px, 92vw);
    margin: 0 auto;
    padding: 34px 0 24px;
    text-align: center;
}
.cocktail-kicker {
    color:#806047;
    font-family:"Cormorant Garamond",Georgia,serif;
    letter-spacing:4px;
    font-size:12px;
    line-height:1.4;
}
.cocktail-title {
    color:#d5a56d;
    font-family:"Cormorant Garamond",Georgia,serif;
    font-size:56px;
    letter-spacing:7px;
    line-height:1.12;
    margin-top:12px;
    margin-bottom:0;
}
.cocktail-subtitle {
    color:#96765d;
    font-family:"Noto Serif KR",serif;
    font-size:14px;
    line-height:1.85;
    margin:16px auto 0;
    max-width:650px;
}
.order-slip {
    min-height:330px;
    padding:22px 18px 18px;
    border:1px solid rgba(199,157,109,.3);
    background:linear-gradient(180deg, rgba(247,238,219,.065), rgba(247,238,219,.025));
    position:relative;
    text-align:center;
    box-shadow:0 15px 35px rgba(0,0,0,.18);
    overflow:hidden;
}
.order-slip:before {
    content:"";
    position:absolute;
    inset:8px;
    border:1px dashed rgba(199,157,109,.16);
    pointer-events:none;
}
.slip-no {
    color:#806047;
    font-family:Georgia,serif;
    font-size:10px;
    letter-spacing:2px;
}
.slip-label {
    color:#e0bd91;
    font-family:"Noto Serif KR",serif;
    font-size:16px;
    line-height:1.5;
    margin-top:16px;
}
.slip-drink {
    color:#c49a70;
    font-family:"Cormorant Garamond",Georgia,serif;
    font-size:15px;
    letter-spacing:2px;
    margin-top:7px;
}
.slip-desc {
    color:#92735d;
    font-family:"Noto Serif KR",serif;
    font-size:11px;
    line-height:1.8;
    margin:8px auto 0;
    max-width:190px;
}
.mini-drink {
    position:relative;
    width:88px;
    height:112px;
    margin:18px auto 2px;
}
.mini-glass {
    position:absolute;
    left:12px;
    bottom:3px;
    width:64px;
    height:84px;
    border:1.5px solid rgba(240,228,211,.58);
    border-top:0;
    border-radius:5px 5px 19px 19px;
    overflow:hidden;
    background:linear-gradient(90deg, rgba(255,255,255,.10), rgba(255,255,255,.02), rgba(255,255,255,.08));
    box-shadow:0 10px 18px rgba(0,0,0,.22), inset 0 0 8px rgba(255,255,255,.06);
}
.mini-liquid {
    position:absolute;
    inset:auto 0 0 0;
    height:66%;
    opacity:.88;
}
.mini-pink .mini-liquid { background:linear-gradient(180deg,#da93aa,#a94f70); }
.mini-green .mini-liquid { background:linear-gradient(180deg,#84d38a,#49a968); }
.mini-orange .mini-liquid { background:linear-gradient(180deg,#ffc06a,#ef761b); }
.mini-navy .mini-liquid { background:linear-gradient(180deg,#4969a0,#1d274f); }
.mini-ice {
    position:absolute;
    width:19px;
    height:19px;
    border:1px solid rgba(255,255,255,.28);
    background:rgba(255,255,255,.13);
    transform:rotate(12deg);
}
.mini-ice.a { top:34px; left:12px; }
.mini-ice.b { top:42px; right:10px; transform:rotate(-14deg); }
.mini-scoop {
    position:absolute;
    z-index:4;
    left:24px;
    top:2px;
    width:42px;
    height:35px;
    border-radius:50%;
    background:radial-gradient(circle at 35% 28%, #fffdf2 0%, #fff3d3 55%, #e5d2aa 100%);
    box-shadow:0 5px 10px rgba(0,0,0,.2);
}
.mini-straw {
    position:absolute;
    z-index:5;
    right:20px;
    top:0;
    width:3px;
    height:58px;
    background:#e9a0a8;
    transform:rotate(16deg);
    transform-origin:bottom center;
    border-radius:3px;
}
.mini-cherry {
    position:absolute;
    z-index:6;
    left:18px;
    top:3px;
    width:10px;
    height:10px;
    border-radius:50%;
    background:#b63f4e;
    box-shadow:0 0 0 2px rgba(255,255,255,.12);
}
.mini-citrus {
    position:absolute;
    z-index:6;
    right:6px;
    top:8px;
    width:24px;
    height:24px;
    border-radius:50%;
    background:radial-gradient(circle, #ffe2a0 0 33%, #f5a33f 35% 72%, #fff0c9 74% 82%, #df7d20 84%);
}
.mini-moon {
    position:absolute;
    z-index:6;
    left:23px;
    top:20px;
    width:32px;
    height:32px;
    border-radius:50%;
    box-shadow:0 0 18px rgba(121,153,225,.55);
    background:radial-gradient(circle at 36% 30%, #96aedd, #334b83 58%, #1a2448 100%);
}
/* refined cocktail glass details */
.mini-drink { width:112px; height:138px; margin:14px auto 0; position:relative; filter:drop-shadow(0 10px 12px rgba(0,0,0,.22)); }
.mini-glass { position:absolute; left:18px; bottom:18px; width:76px; height:84px; border:1.5px solid rgba(245,232,213,.65); border-top:0; border-radius:7px 7px 24px 24px; overflow:hidden; background:linear-gradient(90deg,rgba(255,255,255,.16),rgba(255,255,255,.025),rgba(255,255,255,.12)); box-shadow:inset 8px 0 15px rgba(255,255,255,.06),inset -8px 0 12px rgba(0,0,0,.08); }
.mini-rim { position:absolute; z-index:10; left:18px; top:34px; width:76px; height:13px; border:1.5px solid rgba(245,232,213,.68); border-radius:50%; background:rgba(255,255,255,.035); }
.mini-liquid { position:absolute; left:0; right:0; bottom:0; opacity:.92; border-radius:0 0 20px 20px; }
.mini-stem { position:absolute; left:50%; bottom:7px; width:3px; height:22px; transform:translateX(-50%); background:rgba(235,218,192,.65); }
.mini-base { position:absolute; left:50%; bottom:1px; width:48px; height:7px; transform:translateX(-50%); border:1.5px solid rgba(235,218,192,.65); border-radius:50%; }
.mini-pink .mini-glass { height:62px; bottom:36px; width:84px; left:14px; border-radius:0 0 42px 42px; }
.mini-pink .mini-rim { width:84px; left:14px; top:32px; }
.mini-pink .mini-liquid { background:linear-gradient(180deg,#ffd0dc,#df779a 55%,#a8446b); }
.mini-green .mini-glass { height:92px; width:68px; left:22px; border-radius:5px 5px 22px 22px; }
.mini-green .mini-rim { width:68px; left:22px; top:25px; }
.mini-green .mini-liquid { background:linear-gradient(180deg,#b8f2a9,#62c976 55%,#2f9958); }
.mini-orange .mini-glass { height:72px; width:82px; left:15px; border-radius:7px 7px 28px 28px; }
.mini-orange .mini-rim { width:82px; left:15px; top:43px; }
.mini-orange .mini-liquid { background:linear-gradient(180deg,#ffd995,#ffac3b 48%,#ec7018); }
.mini-navy .mini-glass { height:70px; width:82px; left:15px; border-radius:8px 8px 25px 25px; }
.mini-navy .mini-rim { width:82px; left:15px; top:44px; }
.mini-navy .mini-liquid { background:linear-gradient(180deg,#6f91d2,#354d91 52%,#171f4d); }
.mini-scoop { position:absolute; z-index:20; left:29px; top:-9px; width:55px; height:39px; border-radius:50%; background:radial-gradient(circle at 34% 25%,#fffef7,#fff0cc 62%,#d9c394); box-shadow:0 5px 10px rgba(0,0,0,.24); }
.mini-cherry { position:absolute; z-index:22; left:24px; top:-11px; width:11px; height:11px; border-radius:50%; background:radial-gradient(circle at 30% 25%,#f08089,#a52d43 65%,#671a2b); }
.mini-straw { position:absolute; z-index:21; right:18px; top:-17px; width:3px; height:68px; border-radius:3px; background:linear-gradient(#ef9a9f,#db5d76); transform:rotate(13deg); transform-origin:bottom; }
.mini-bubbles { position:absolute; inset:0; z-index:12; }
.mini-bubbles i { position:absolute; width:4px; height:4px; border-radius:50%; background:rgba(255,255,255,.45); }
.mini-bubbles i:nth-child(1){left:25px;bottom:35px}.mini-bubbles i:nth-child(2){left:44px;bottom:52px}.mini-bubbles i:nth-child(3){right:20px;bottom:25px}
.mini-orange-half { position:absolute; z-index:20; width:38px; height:22px; border-radius:38px 38px 0 0; background:radial-gradient(circle at 50% 100%,#ffe7a2 0 32%,#ffb447 34% 68%,#e86d18 70% 100%); box-shadow:0 4px 8px rgba(0,0,0,.2); }
.mini-orange-half:after { content:""; position:absolute; left:18px; top:3px; width:1px; height:17px; background:rgba(255,239,188,.65); transform:rotate(28deg); }
.mini-orange-half { right:4px; top:20px; transform:rotate(13deg); }
.mini-orange-half.second { left:5px; right:auto; top:62px; width:28px; height:17px; transform:rotate(-18deg); }
.mini-leaf { position:absolute; z-index:21; right:23px; top:12px; width:20px; height:10px; border-radius:100% 0 100% 0; background:linear-gradient(135deg,#83a85c,#456b40); transform:rotate(-20deg); }
.mini-cocktail-olive { position:absolute; z-index:20; left:36px; top:30px; width:13px; height:13px; border-radius:50%; background:#b5b86d; box-shadow:inset 3px 2px 4px rgba(255,255,255,.28); }
.mini-pick { position:absolute; z-index:19; left:43px; top:9px; width:2px; height:47px; background:#e9c78d; transform:rotate(-10deg); }
.mini-blue-glow { position:absolute; z-index:15; left:31px; top:47px; width:45px; height:30px; border-radius:50%; background:radial-gradient(circle,#91b8ff,rgba(60,89,155,.2) 70%,transparent); filter:blur(4px); }
.mini-lemon-twist { position:absolute; z-index:21; right:11px; top:30px; width:30px; height:10px; border:3px solid #f5c75d; border-left-color:transparent; border-bottom-color:transparent; border-radius:50%; transform:rotate(18deg); }
.mini-star { position:absolute; z-index:22; left:33px; top:49px; color:#dbe6ff; font-size:12px; text-shadow:0 0 9px #89aaff; }

.selected-order {
    width:min(900px,92vw);
    margin:0 auto 14px;
    text-align:center;
}
.selected-order-small {
    color:#805c3d;
    font-family:Georgia,serif;
    font-size:10px;
    letter-spacing:3px;
    line-height:1.4;
}
.selected-order-title {
    color:#dcae73;
    font-family:"Noto Serif KR",serif;
    font-size:28px;
    line-height:1.45;
    margin-top:5px;
}
.selected-order-sub {
    color:#96765d;
    font-family:"Noto Serif KR",serif;
    font-size:13px;
    line-height:1.8;
    margin-top:2px;
}
.drink-stage {
    min-height:540px;
    display:flex;
    align-items:center;
    justify-content:center;
    padding:8px 0 14px;
}
.drink-visual {
    position:relative;
    width:300px;
    height:430px;
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
}
.glass {
    position:relative;
    width:190px;
    height:270px;
    margin-top:22px;
    border:2px solid rgba(226,208,178,.57);
    border-top:0;
    border-radius:10px 10px 52px 52px;
    overflow:visible;
    background:linear-gradient(90deg,rgba(255,255,255,.11),rgba(255,255,255,.025),rgba(255,255,255,.09));
    box-shadow:0 28px 55px rgba(0,0,0,.35), inset 0 0 20px rgba(255,255,255,.05);
}
.glass .liquid {
    position:absolute;
    left:0;
    right:0;
    bottom:0;
    border-radius:0 0 48px 48px;
    transition:height .4s ease;
    opacity:.9;
    overflow:hidden;
}
.glass .liquid:after {
    content:"";
    position:absolute;
    inset:0;
    background:radial-gradient(circle at 20% 28%, rgba(255,255,255,.28) 0 1px, transparent 2px), radial-gradient(circle at 68% 45%, rgba(255,255,255,.18) 0 1px, transparent 2px), radial-gradient(circle at 48% 70%, rgba(255,255,255,.16) 0 1px, transparent 2px);
    background-size:40px 45px, 52px 55px, 64px 62px;
    opacity:.6;
}
.drink-scene.green .liquid { background:linear-gradient(180deg,#a4ec9d 0%,#68ca79 46%,#3ca45f 100%); }
.drink-scene.orange .liquid { background:linear-gradient(180deg,#ffd98f 0%,#ffad3c 42%,#f17b19 100%); }
.drink-scene.pink .liquid { background:linear-gradient(180deg,#f4b1c0 0%,#dc7f9b 42%,#b24e76 100%); }
.drink-scene.navy .liquid { background:linear-gradient(180deg,#708dc4 0%,#40598f 40%,#202c59 100%); }
.glass-shine {
    position:absolute;
    z-index:9;
    top:25px;
    left:28px;
    width:18px;
    height:205px;
    border-radius:50%;
    background:rgba(255,255,255,.14);
    filter:blur(2px);
    pointer-events:none;
}
.glass-rim {
    position:absolute;
    z-index:10;
    left:-1px;
    right:-1px;
    top:-1px;
    height:17px;
    border:2px solid rgba(236,226,214,.58);
    border-radius:50%;
    background:rgba(255,255,255,.03);
    box-shadow:0 2px 7px rgba(0,0,0,.16);
}
.glass-foot {
    position:absolute;
    left:50%;
    bottom:-35px;
    width:3px;
    height:38px;
    transform:translateX(-50%);
    background:rgba(226,208,178,.55);
}
.glass-base {
    position:absolute;
    left:50%;
    bottom:-43px;
    width:112px;
    height:10px;
    transform:translateX(-50%);
    border:2px solid rgba(226,208,178,.55);
    border-radius:50%;
}
.drink-scene.green .glass {
    width:174px;
    height:285px;
    border-radius:5px 5px 38px 38px;
}
.drink-scene.green .glass-foot,
.drink-scene.green .glass-base { display:block; }
.drink-scene.orange .glass {
    width:220px;
    height:220px;
    margin-top:45px;
    border-radius:11px 11px 56px 56px;
}
.drink-scene.orange .glass-foot,
.drink-scene.orange .glass-base { display:none; }
.drink-scene.pink .glass {
    width:225px;
    height:170px;
    margin-top:58px;
    border-radius:0 0 110px 110px;
    transform:perspective(200px) rotateX(-3deg);
}
.drink-scene.pink .glass-foot,
.drink-scene.pink .glass-base { display:block; }
.pink-olive {
    position:absolute;
    z-index:14;
    left:50%;
    top:22px;
    width:24px;
    height:24px;
    transform:translateX(-50%);
    border-radius:50%;
    background:radial-gradient(circle at 32% 25%,#d7d99b 0%,#a8ad63 48%,#68703d 100%);
    box-shadow:inset 3px 2px 4px rgba(255,255,255,.28), 0 4px 8px rgba(0,0,0,.22);
}
.pink-olive:after {
    content:"";
    position:absolute;
    left:8px;
    top:8px;
    width:7px;
    height:7px;
    border-radius:50%;
    background:rgba(90,60,35,.45);
}
.pink-pick {
    position:absolute;
    z-index:13;
    left:50%;
    top:8px;
    width:2px;
    height:46px;
    transform:translateX(-50%) rotate(-9deg);
    transform-origin:bottom center;
    background:#e5c98e;
    border-radius:2px;
}
/* 실제 음료에서는 잔 안쪽에서만 보이도록 합니다. */
.glass { overflow:hidden !important; isolation:isolate; }
.glass .liquid { left:2px !important; right:2px !important; bottom:2px !important; max-height:calc(100% - 18px); }
.glass .glass-rim { z-index:20; pointer-events:none; }
.glass-foot, .glass-base { overflow:visible !important; }
/* 가니시는 잔 위로 튀어나오지 않고 잔 안쪽에서 보이도록 */
.melon-ice-cream { top:18px !important; width:72px; height:42px; z-index:12; }
.melon-ice-cream:after { bottom:0; width:54px; }
.drink-straw { top:18px !important; height:72px !important; left:66%; }
.drink-cherry { top:24px !important; left:35%; }
.drink-cherry:after { display:none; }
.orange-half.one { top:18px !important; right:8px; width:64px; height:36px; }
.orange-half.two { top:58px !important; bottom:auto; left:20px; width:52px; height:29px; }
.orange-leaf { display:none; }
.navy-garnish { top:24px !important; left:18px; width:60px; height:13px; }

.drink-scene.navy .glass {
    width:230px;
    height:205px;
    margin-top:44px;
    border-radius:12px 12px 46px 46px;
}
.drink-scene.navy .glass-foot,
.drink-scene.navy .glass-base { display:none; }
.melon-ice-cream {
    position:absolute;
    z-index:12;
    top:-35px;
    left:50%;
    width:98px;
    height:72px;
    transform:translateX(-50%);
    border-radius:54% 54% 45% 45%;
    background:radial-gradient(circle at 34% 24%, #fffef7 0%, #fff2d0 55%, #dfcca2 100%);
    box-shadow:0 8px 16px rgba(0,0,0,.24);
}
.melon-ice-cream:after {
    content:"";
    position:absolute;
    left:50%;
    bottom:-4px;
    width:65px;
    height:12px;
    transform:translateX(-50%);
    border-radius:50%;
    background:rgba(218,194,150,.55);
}
.drink-straw {
    position:absolute;
    z-index:13;
    top:-56px;
    left:63%;
    width:4px;
    height:112px;
    border-radius:4px;
    background:linear-gradient(180deg,#ec8f9c,#dd5f76);
    transform:rotate(12deg);
    transform-origin:bottom center;
}
.drink-cherry {
    position:absolute;
    z-index:14;
    top:-45px;
    left:38%;
    width:18px;
    height:18px;
    border-radius:50%;
    background:radial-gradient(circle at 30% 25%, #e77c83, #ae3147 62%, #762033 100%);
    box-shadow:0 4px 8px rgba(0,0,0,.2);
}
.drink-cherry:after {
    content:"";
    position:absolute;
    width:30px;
    height:22px;
    top:-16px;
    left:9px;
    border-top:2px solid #6b8156;
    border-radius:50%;
    transform:rotate(28deg);
}
.orange-half {
    position:absolute;
    z-index:14;
    width:88px;
    height:48px;
    border-radius:88px 88px 0 0;
    background:radial-gradient(circle at 50% 100%, #ffe8a6 0 34%, #ffb84c 36% 69%, #f47b20 71% 88%, #fff1c6 90% 94%, #df6b17 95%);
    box-shadow:0 8px 16px rgba(0,0,0,.22);
}
.orange-half:after {
    content:""; position:absolute; left:50%; bottom:4px; width:2px; height:39px;
    background:rgba(255,240,190,.7); transform:translateX(-50%) rotate(25deg);
    box-shadow:-15px 8px 0 -0.5px rgba(255,240,190,.5), 15px 8px 0 -0.5px rgba(255,240,190,.5);
}
.orange-half.one { right:8px; top:-20px; transform:rotate(15deg); }
.orange-half.two { left:20px; bottom:12px; width:60px; height:34px; opacity:.95; transform:rotate(-18deg); }
.orange-leaf {
    position:absolute;
    z-index:14;
    left:37px;
    top:-22px;
    width:42px;
    height:22px;
    border-radius:100% 0 100% 0;
    background:linear-gradient(135deg,#7eac58,#406b40);
    transform:rotate(-20deg);
}
.melon-straw-line {
    position:absolute;
    z-index:15;
    left:50%;
    top:-52px;
    width:4px;
    height:150px;
    border-radius:4px;
    background:linear-gradient(180deg,#f3c67a,#db8b41);
    transform:translateX(-50%) rotate(-13deg);
    transform-origin:bottom center;
}
.bubbles {
    position:absolute;
    z-index:11;
    inset:0;
    pointer-events:none;
}
.bubbles span { position:absolute; border-radius:50%; background:rgba(255,255,255,.35); box-shadow:0 0 7px rgba(255,255,255,.24); }
.bubbles .b1 { width:7px; height:7px; left:28%; top:33%; }
.bubbles .b2 { width:4px; height:4px; left:42%; top:26%; }
.bubbles .b3 { width:6px; height:6px; left:63%; top:43%; }
.bubbles .b4 { width:3px; height:3px; left:73%; top:30%; }
.navy-garnish {
    position:absolute;
    z-index:14;
    left:16px;
    top:8px;
    width:75px;
    height:17px;
    border-radius:70% 30% 70% 30%;
    background:linear-gradient(90deg,#f8e3a2,#f3b54e);
    transform:rotate(-17deg);
    box-shadow:0 6px 13px rgba(0,0,0,.2);
}
.navy-garnish:after {
    content:"";
    position:absolute;
    width:28px;
    height:7px;
    left:11px;
    top:5px;
    border-radius:50%;
    background:#fff1bd;
}
.stars { position:absolute; inset:0; z-index:13; pointer-events:none; }
.stars span { position:absolute; color:rgba(220,229,255,.75); font-size:16px; text-shadow:0 0 12px rgba(160,187,255,.8); }
.stars .s1 { top:35px; left:34px; }
.stars .s2 { top:75px; right:44px; font-size:12px; }
.stars .s3 { bottom:43px; left:62px; font-size:11px; }
.drink-name {
    color:#dcae73;
    font-family:"Cormorant Garamond",Georgia,serif;
    letter-spacing:3px;
    font-size:18px;
    line-height:1.3;
    margin-top:66px;
    text-align:center;
}
.drink-state {
    color:#896951;
    font-family:Georgia,serif;
    font-size:10px;
    letter-spacing:3px;
    margin-top:6px;
    text-align:center;
}
.concierge-card {
    padding:25px 26px 23px;
    border:1px solid rgba(199,157,109,.25);
    background:linear-gradient(180deg, rgba(247,238,219,.065), rgba(247,238,219,.025));
    box-shadow:0 20px 45px rgba(0,0,0,.22);
    margin-bottom:18px;
}
.concierge-label {
    color:#805c3d;
    font-family:Georgia,serif;
    font-size:11px;
    letter-spacing:3px;
    line-height:1.4;
}
.concierge-title {
    color:#dcae73;
    font-family:"Noto Serif KR",serif;
    font-size:21px;
    line-height:1.75;
    margin-top:10px;
}
.concierge-copy {
    color:#96765d;
    font-family:"Noto Serif KR",serif;
    font-size:12px;
    line-height:1.9;
    margin-top:12px;
}
.compact-recommendations {
    max-height:510px;
    overflow-y:auto;
    padding-right:5px;
}
.compact-recommendation {
    border-top:1px solid rgba(199,157,109,.16);
    padding:13px 0 14px;
}
.compact-recommendation:first-child { border-top:0; }
.compact-rec-title {
    color:#e0bd91;
    font-family:"Cormorant Garamond",Georgia,serif;
    font-size:18px;
    line-height:1.4;
}
.compact-rec-meta {
    color:#9c7b63;
    font-family:"Noto Serif KR",serif;
    font-size:11px;
    line-height:1.7;
    margin-top:2px;
}
.recommendation-title {
    color:#dca072;
    font-family:"Cormorant Garamond",Georgia,serif;
    font-size:25px;
    letter-spacing:4px;
    margin:2px 0 7px;
}
.ai-note {
    color:#76563e;
    font-family:Georgia,serif;
    font-size:9px;
    letter-spacing:2px;
    margin-bottom:5px;
}
.drink-controls {
    width:min(340px, 90vw);
    margin:0 auto;
}

@media (max-width: 1050px) {
    .cocktail-title { font-size:48px; }
    .drink-stage { min-height:520px; }
}

@media (max-width: 900px) {
    .cocktail-title { font-size:42px; }
    .cocktail-header { padding-top:26px; padding-bottom:18px; }
    .drink-stage { min-height:430px; }
    .drink-visual { transform:scale(.9); transform-origin:center; margin-bottom:-18px; }
}

@media (max-width: 700px) {
    .room-service-container, .listen-search, .fireplace-container { width:92vw; }
    .room-service-title, .fireplace-title { font-size:38px; }
    .section-title { font-size:38px; }
    .cocktail-title { font-size:34px; letter-spacing:4px; }
    .cocktail-subtitle { padding:0 20px; }
    .order-slip { min-height:285px; margin-bottom:10px; }
    .slip-label { margin-top:15px; font-size:15px; }
    .letter-paper { padding:50px 35px; min-height:auto; }
    .letter-body { font-size:15px; }
    .drink-visual { transform:scale(.82); margin-bottom:-35px; }
    .drink-stage { min-height:380px; padding-bottom:0; }
}
/* Final visual spacing and cocktail refinement */
.order-slip {
    min-height: 372px !important;
    padding: 27px 18px 24px !important;
    margin-bottom: 18px !important;
    background: linear-gradient(145deg, rgba(255,244,229,.095), rgba(69,42,30,.34) 48%, rgba(16,10,8,.34)) !important;
    border-color: rgba(220,177,128,.42) !important;
}
.order-slip div[data-testid="stButton"] { margin-top: 18px !important; }
.order-slip div[data-testid="stButton"] > button {
    min-height: 48px !important;
    margin-top: 0 !important;
    letter-spacing: 3px !important;
    background: linear-gradient(135deg, rgba(105,68,43,.26), rgba(28,17,13,.66)) !important;
}
.cocktail-header { padding: 26px 0 34px !important; }
.cocktail-subtitle { margin-top: 15px !important; line-height: 2 !important; }
.mini-drink { margin-top: 25px !important; margin-bottom: 15px !important; transform: scale(1.12); }
.slip-drink { margin-top: 15px !important; }
.slip-desc { margin-top: 12px !important; line-height: 2 !important; }
.drink-visual { filter: drop-shadow(0 24px 28px rgba(0,0,0,.32)) !important; }
.glass {
    backdrop-filter: blur(3px) !important;
    border-color: rgba(255,245,232,.82) !important;
    box-shadow: 0 28px 54px rgba(0,0,0,.28), inset 10px 0 17px rgba(255,255,255,.13), inset -10px 0 18px rgba(0,0,0,.11), inset 0 0 0 1px rgba(255,255,255,.08) !important;
}
.glass .liquid { transition: height .28s ease, background .28s ease; }
.glass .bubble-dot { position:absolute; z-index:5; width:5px; height:5px; border-radius:50%; background:radial-gradient(circle at 30% 25%,rgba(255,255,255,.95),rgba(255,255,255,.18) 72%); box-shadow:0 0 7px rgba(255,255,255,.2); pointer-events:none; }
.bubbles { position:absolute; inset:0; overflow:hidden; border-radius:inherit; pointer-events:none; }
.drink-straw { z-index:18 !important; filter:drop-shadow(1px 1px 1px rgba(0,0,0,.16)); }
.melon-ice-cream { box-shadow: inset 5px 3px 8px rgba(255,255,255,.65), inset -4px -4px 8px rgba(194,165,120,.2), 0 7px 13px rgba(0,0,0,.18) !important; }
.melon-ice-cream.half-gone { opacity:.55 !important; transform:translateY(12px) scale(.82) !important; transition:all .2s ease; }
.orange-half { box-shadow: inset 0 0 0 2px rgba(255,243,203,.72), 0 5px 12px rgba(0,0,0,.2) !important; }
.pink-olive { box-shadow: inset 4px 3px 5px rgba(255,255,255,.7), inset -3px -3px 5px rgba(120,39,70,.2), 0 4px 8px rgba(0,0,0,.2) !important; }
.drink-name { margin-top: 26px !important; }
.drink-state { margin-top: 8px !important; }
@media (max-width: 900px) {
    .order-slip { min-height: 340px !important; margin-bottom: 18px !important; }
    .cocktail-header { padding-bottom: 26px !important; }
}
@media (max-width: 700px) {
    .order-slip { min-height: 300px !important; margin-bottom: 16px !important; }
    .mini-drink { margin-top: 18px !important; transform: scale(1.02); }
}

<style>
/* COCKTAIL BAR final art direction: more breathing room and clear, connected glassware. */
.cocktail-header {
    width: min(1180px, 94vw) !important;
    margin: 0 auto !important;
    padding: 34px 0 48px !important;
}
.cocktail-kicker { font-size: 11px !important; letter-spacing: 4.5px !important; color: #a98563 !important; }
.cocktail-title {
    margin-top: 15px !important;
    font-size: clamp(42px, 5vw, 60px) !important;
    letter-spacing: 6.5px !important;
    line-height: 1.16 !important;
}
.cocktail-subtitle {
    margin: 18px auto 0 !important;
    max-width: 720px !important;
    font-size: 14px !important;
    line-height: 2 !important;
    letter-spacing: .6px !important;
    color: #c2a287 !important;
}
/* Explicitly create a gap between the menu card and its Streamlit button element. */
[data-testid="stVerticalBlock"] > [data-testid="stElementContainer"]:has(.order-slip) {
    margin-bottom: 23px !important;
}
[data-testid="stColumn"] [data-testid="stVerticalBlock"] { row-gap: 13px !important; }
.order-slip {
    box-sizing: border-box !important;
    min-height: 425px !important;
    height: 425px !important;
    padding: 25px 18px 24px !important;
    margin: 0 !important;
    overflow: hidden !important;
    border-radius: 5px !important;
    border: 1px solid rgba(218,177,133,.40) !important;
    background: linear-gradient(155deg, rgba(255,242,224,.09), rgba(63,39,28,.25) 52%, rgba(16,10,8,.36)) !important;
    box-shadow: 0 18px 40px rgba(0,0,0,.24), inset 0 1px rgba(255,255,255,.045) !important;
}
.order-slip:before { inset: 9px !important; border-color: rgba(218,177,133,.16) !important; }
.slip-no { font-size: 10px !important; color: #a17f60 !important; letter-spacing: 3px !important; }
.slip-label {
    min-height: 48px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    margin: 14px auto 0 !important;
    max-width: 250px !important;
    font-size: 15px !important;
    line-height: 1.8 !important;
    letter-spacing: .3px !important;
    color: #f3debf !important;
}
.slip-drink { margin-top: 8px !important; font-size: 13px !important; line-height: 1.5 !important; letter-spacing: 2px !important; }
.slip-desc {
    min-height: 44px !important;
    margin: 9px auto 0 !important;
    max-width: 245px !important;
    font-size: 11px !important;
    line-height: 1.9 !important;
    color: #b69a81 !important;
}
[data-testid="stColumn"] div[data-testid="stButton"] { margin-top: 0 !important; }
[data-testid="stColumn"] div[data-testid="stButton"] > button {
    min-height: 52px !important;
    letter-spacing: 3px !important;
    background: linear-gradient(135deg, rgba(92,58,39,.42), rgba(24,15,11,.82)) !important;
    border-color: rgba(213,167,117,.55) !important;
    box-shadow: 0 8px 22px rgba(0,0,0,.16) !important;
}
[data-testid="stColumn"] div[data-testid="stButton"] > button:hover { transform: translateY(-1px); border-color: #eac18e !important; }
.mini-drink {
    width: 100% !important;
    height: 190px !important;
    margin: 2px auto 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    filter: drop-shadow(0 12px 15px rgba(0,0,0,.22)) !important;
    transform: none !important;
    position: relative !important;
    z-index: 1 !important;
}
.cocktail-svg { display: block; overflow: visible; }
.cocktail-svg.mini { width: 146px !important; height: 190px !important; max-width: 100% !important; }
.cocktail-svg.hero { width: min(300px, 100%) !important; height: auto !important; max-height: 390px !important; margin: 0 auto !important; }
.drink-visual {
    width: 100% !important;
    height: auto !important;
    min-height: 0 !important;
    margin: 0 auto !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    filter: drop-shadow(0 20px 24px rgba(0,0,0,.28)) !important;
    transform: none !important;
}
.drink-name { margin-top: 7px !important; font-size: 16px !important; letter-spacing: 3.2px !important; line-height: 1.8 !important; }
.drink-state { margin-top: 3px !important; font-size: 10px !important; letter-spacing: 2.5px !important; }
.selected-order { margin: 7px auto 25px !important; }
.selected-order-title { margin-top: 9px !important; font-size: clamp(22px, 2vw, 28px) !important; line-height: 1.6 !important; }
.selected-order-sub { margin-top: 7px !important; line-height: 1.9 !important; }
.concierge-card { padding: 27px 28px !important; margin-bottom: 24px !important; }
.recommendation-title { margin-top: 20px !important; }
@media (max-width: 1150px) {
    .order-slip { min-height: 405px !important; height: 405px !important; padding-left: 12px !important; padding-right: 12px !important; }
    .mini-drink { height: 172px !important; }
    .cocktail-svg.mini { height: 172px !important; }
}
@media (max-width: 700px) {
    .cocktail-header { padding: 23px 0 30px !important; }
    .cocktail-title { font-size: 36px !important; letter-spacing: 4px !important; }
    .cocktail-subtitle { padding: 0 16px !important; margin-top: 14px !important; }
    .order-slip { min-height: 390px !important; height: 390px !important; }
    .mini-drink { height: 170px !important; }
    .cocktail-svg.mini { height: 170px !important; }
    .cocktail-svg.hero { width: min(265px, 100%) !important; }
}
</style>
</style>
"""

try:
    st.html(CSS)
except Exception:
    st.markdown(CSS, unsafe_allow_html=True)

# Final responsive visual corrections. Kept separate so these overrides reliably win.
POLISH_CSS = r"""
<style>
/* Consistent, legible section heading and more breathing room before actions. */
.section-area { min-height: 0 !important; padding-top: clamp(34px, 5vh, 58px) !important; margin: 0 auto 0 !important; text-align: center !important; }
.section-area .section-title, .cocktail-header .cocktail-title { color: #d9ad75 !important; font-family: "Cormorant Garamond", Georgia, serif !important; font-weight: 400 !important; letter-spacing: 5px !important; line-height: 1.2 !important; }
.section-area .section-subtitle { color: #aa8667 !important; line-height: 1.9 !important; margin-top: 12px !important; }
.room-service-buttons-spacer { height: 34px !important; width: 100%; line-height: 0 !important; }

/* Mood menu: compact cards, centered type and clearly separated order buttons. */
.cocktail-header { width: min(1180px, 94vw) !important; padding: 25px 0 35px !important; margin: 0 auto !important; text-align: center !important; }
.cocktail-kicker { color: #a98563 !important; font-size: 10px !important; letter-spacing: 4px !important; }
.cocktail-title { color: #dcb47c !important; font-family: "Cormorant Garamond", Georgia, serif !important; font-size: clamp(38px, 4.3vw, 52px) !important; font-weight: 400 !important; letter-spacing: 5px !important; line-height: 1.15 !important; text-align: center !important; }
.cocktail-subtitle { color: #c0a087 !important; font-size: 13px !important; margin: 15px auto 0 !important; max-width: 680px !important; line-height: 1.9 !important; text-align: center !important; }
.order-slip { height: 360px !important; min-height: 360px !important; box-sizing: border-box !important; padding: 18px 14px 16px !important; margin: 0 !important; overflow: hidden !important; border: 1px solid rgba(211,170,121,.34) !important; border-radius: 4px !important; background: linear-gradient(155deg, rgba(255,240,220,.065), rgba(54,34,24,.20) 54%, rgba(14,9,7,.28)) !important; box-shadow: 0 12px 28px rgba(0,0,0,.19), inset 0 1px rgba(255,255,255,.03) !important; }
.order-slip:before { inset: 7px !important; border-color: rgba(211,170,121,.12) !important; }
.slip-no { color: #957353 !important; text-align: center !important; font-size: 9px !important; letter-spacing: 2.4px !important; }
.slip-label { display: block !important; min-height: 0 !important; margin: 10px auto 0 !important; max-width: 240px !important; color: #f0d7b8 !important; text-align: center !important; font-size: 14px !important; line-height: 1.6 !important; letter-spacing: 0 !important; }
.mini-drink { display: flex !important; width: 100% !important; height: 198px !important; align-items: center !important; justify-content: center !important; margin: 7px auto 0 !important; transform: none !important; filter: drop-shadow(0 7px 9px rgba(0,0,0,.20)) !important; overflow: visible !important; }
.cocktail-svg.mini { display: block !important; width: 158px !important; height: 198px !important; max-width: 100% !important; margin: 0 auto !important; overflow: visible !important; }
.slip-drink { color: #d9b182 !important; text-align: center !important; margin: 6px auto 0 !important; font-size: 12px !important; line-height: 1.5 !important; letter-spacing: 1.5px !important; }
.slip-desc { min-height: 0 !important; max-width: 245px !important; margin: 5px auto 0 !important; color: #aa8b71 !important; font-size: 10px !important; line-height: 1.6 !important; text-align: center !important; }
.cocktail-order-button-gap { height: 10px !important; min-height: 10px !important; width: 100%; line-height: 0 !important; }
[data-testid="stColumn"] div[data-testid="stButton"] > button { min-height: 46px !important; letter-spacing: 2.5px !important; border-color: rgba(213,167,117,.48) !important; background: linear-gradient(135deg, rgba(92,58,39,.34), rgba(24,15,11,.80)) !important; }

/* Selected drink: smaller overall glass, connected stem/base retained in the SVG. */
.selected-order { margin: 4px auto 16px !important; }
.selected-order-title { color: #dcb47c !important; font-size: clamp(20px, 2vw, 25px) !important; line-height: 1.45 !important; }
.drink-stage { min-height: 0 !important; padding: 0 !important; }
.drink-visual { width: 100% !important; height: auto !important; min-height: 0 !important; margin: 0 auto !important; filter: drop-shadow(0 12px 18px rgba(0,0,0,.24)) !important; }
.cocktail-svg.hero { display: block !important; width: min(225px, 100%) !important; height: auto !important; max-height: 300px !important; margin: 0 auto !important; }
.drink-name { color: #dcb47c !important; margin-top: 8px !important; font-size: 14px !important; letter-spacing: 1.5px !important; line-height: 1.6 !important; text-align: center !important; }
.drink-state { margin-top: 2px !important; color: #a98768 !important; font-size: 9px !important; letter-spacing: 2px !important; text-align: center !important; }
.concierge-card { padding: 21px 22px !important; }

@media (max-width: 1050px) {
  .order-slip { height: 348px !important; min-height: 348px !important; padding-left: 10px !important; padding-right: 10px !important; }
  .mini-drink { height: 184px !important; }
  .cocktail-svg.mini { width: 148px !important; height: 185px !important; }
}
@media (max-width: 700px) {
  .room-service-buttons-spacer { height: 26px !important; }
  .cocktail-header { padding: 20px 0 25px !important; }
  .cocktail-title { font-size: 34px !important; letter-spacing: 3px !important; }
  .order-slip { height: 334px !important; min-height: 334px !important; padding: 16px 9px 14px !important; }
  .mini-drink { height: 172px !important; }
  .cocktail-svg.mini { width: 138px !important; height: 172px !important; }
  .slip-label { font-size: 12px !important; }
  .slip-desc { font-size: 9px !important; }
  .cocktail-svg.hero { width: min(210px, 100%) !important; }
}
</style>
"""
st.markdown(POLISH_CSS, unsafe_allow_html=True)

# =========================================================
# SUPABASE
# =========================================================

try:
    from supabase import create_client
except Exception:
    create_client = None

SUPABASE_CONFIG_ERROR = ""
SUPABASE_URL_VALUE = ""

@st.cache_resource
def get_supabase():
    global SUPABASE_CONFIG_ERROR, SUPABASE_URL_VALUE

    SUPABASE_CONFIG_ERROR = ""
    SUPABASE_URL_VALUE = ""

    if create_client is None:
        SUPABASE_CONFIG_ERROR = "supabase 패키지가 설치되어 있지 않습니다. requirements.txt에 supabase를 추가해 주세요."
        return None

    try:
        url = str(st.secrets["SUPABASE_URL"]).strip()
        key = str(st.secrets["SUPABASE_KEY"]).strip()
        SUPABASE_URL_VALUE = url
    except Exception:
        SUPABASE_CONFIG_ERROR = "Streamlit Secrets에 SUPABASE_URL과 SUPABASE_KEY가 없습니다."
        return None

    # Project URL이 아닌 Supabase 대시보드 주소를 넣는 실수를 방지합니다.
    if (
        not url.startswith("https://")
        or "supabase.com/dashboard" in url
        or "/dashboard/" in url
        or ".supabase.co" not in url
    ):
        SUPABASE_CONFIG_ERROR = (
            "SUPABASE_URL이 올바른 Project URL이 아닙니다. "
            "Supabase → Project Settings → API → Project URL의 "
            "https://프로젝트주소.supabase.co 형태를 넣어 주세요."
        )
        return None

    if not key:
        SUPABASE_CONFIG_ERROR = "SUPABASE_KEY가 비어 있습니다."
        return None

    try:
        return create_client(url, key)
    except Exception as e:
        SUPABASE_CONFIG_ERROR = f"Supabase 연결 오류: {e}"
        return None

supabase = get_supabase()

# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "page": "main",
    "main_entered": False,
    "choice_mode": None,
    "room_service_step": "search",
    "search_text": "",
    "search_results": [],
    "logged_in": False,
    "current_user": None,
    "auth_mode": "login",
    "my_room_checkin_open": False,
    "current_record": None,
    "room_records": [],
    "my_room_view": "fireplace",
    "cocktail_mood": None,
    "cocktail_sips": 0,
    "cocktail_recommendations": [],
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =========================================================
# NAVIGATION
# =========================================================

def go(page):
    st.session_state.page = page
    if page != "main":
        st.session_state.main_entered = False
    if page != "choice":
        st.session_state.choice_mode = None
    if page != "my_room":
        st.session_state.my_room_checkin_open = False
    if page != "choice":
        st.session_state.cocktail_mood = None
        st.session_state.cocktail_sips = 0
        st.session_state.cocktail_recommendations = []
    st.rerun()

def go_room_service():
    st.session_state.page = "choice"
    st.session_state.choice_mode = None
    st.session_state.room_service_step = "search"
    st.session_state.cocktail_mood = None
    st.session_state.cocktail_sips = 0
    st.session_state.cocktail_recommendations = []
    st.rerun()

def go_my_room():
    st.session_state.page = "my_room"
    st.rerun()

# =========================================================
# AUTH
# =========================================================

def _auth_error_message(message, action="회원가입"):
    """Supabase의 오류를 사용자가 알아보기 쉽게 변환합니다."""
    text = str(message).strip()
    lower = text.lower()

    if "already registered" in lower or "user already registered" in lower:
        return "이미 가입된 이메일입니다."

    if "email signups are disabled" in lower:
        return "Supabase에서 이메일 회원가입이 비활성화되어 있습니다. Authentication → Providers → Email에서 활성화해 주세요."

    if "invalid api key" in lower or ("apikey" in lower and "invalid" in lower):
        return "Supabase API KEY가 올바르지 않습니다. Streamlit Secrets의 SUPABASE_KEY를 확인해 주세요."

    if "rate limit" in lower or "email rate limit" in lower:
        return "이메일 발송 제한에 걸렸습니다. 잠시 후 다시 시도해 주세요."

    # Supabase URL이 잘못되어 HTML 페이지가 JSON 대신 반환되는 경우
    # 현재 화면에서 보였던 pydantic 'Invalid JSON' 오류를 사람이 이해할 수 있게 바꿉니다.
    if "invalid json" in lower and "doctype html" in lower:
        return (
            "SUPABASE_URL이 잘못되었습니다. 지금 Supabase API가 JSON 대신 HTML 페이지를 반환했습니다. "
            "Streamlit Secrets의 SUPABASE_URL에는 Supabase Dashboard 주소가 아니라 "
            "Project Settings → API → Project URL(https://프로젝트주소.supabase.co)을 넣어 주세요."
        )

    if "fetch failed" in lower or "connection" in lower or "connect" in lower:
        return f"Supabase 연결에 실패했습니다. SUPABASE_URL과 SUPABASE_KEY를 확인해 주세요.\n\n상세 오류: {text}"

    return f"{action} 오류: {text}"


def login_user(email, password):
    if supabase is None:
        return False, SUPABASE_CONFIG_ERROR or "Supabase 연결을 확인해 주세요."
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        user = getattr(response, "user", None)
        if user is None:
            return False, "로그인 정보를 확인해 주세요."
        st.session_state.logged_in = True
        st.session_state.current_user = user
        return True, "CHECK-IN 완료"
    except Exception as e:
        message = str(e).strip()
        lower_message = message.lower()
        if "invalid login credentials" in lower_message:
            return False, "이메일 또는 비밀번호가 올바르지 않습니다."
        if "email not confirmed" in lower_message:
            return False, "이메일 인증이 아직 완료되지 않았습니다. 가입한 이메일의 인증 메일을 확인해 주세요."
        return False, _auth_error_message(message, "로그인")


def signup_user(email, password):
    if supabase is None:
        return False, SUPABASE_CONFIG_ERROR or "Supabase 연결을 확인해 주세요."
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        user = getattr(response, "user", None)
        if user is None:
            return False, "회원가입에 실패했습니다. Supabase 응답에 사용자 정보가 없습니다."

        session = getattr(response, "session", None)
        if session is not None:
            st.session_state.logged_in = True
            st.session_state.current_user = user
            return True, "CHECK-IN 완료"

        return True, "회원가입이 완료되었습니다. 이메일 인증 후 CHECK-IN 해주세요."
    except Exception as e:
        return False, _auth_error_message(str(e), "회원가입")


def logout_user():
    if supabase is not None:
        try:
            supabase.auth.sign_out()
        except Exception:
            pass
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.current_record = None
    st.session_state.room_records = []
    st.rerun()

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown(
        '<div class="sidebar-title">RECORD HOTEL</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="sidebar-subtitle">A QUIET PLACE FOR MUSIC</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="sidebar-rule"></div>',
        unsafe_allow_html=True
    )

    if st.button("MAIN", key="nav_main"):
        go("main")

    if st.button("ROOM SERVICE", key="nav_choice"):
        go("choice")

    if st.button("MY ROOM", key="nav_my_room"):
        go("my_room")

# =========================================================
# APPLE API
# =========================================================

@st.cache_data(ttl=600, show_spinner=False)
def apple_search(params):
    url = "https://itunes.apple.com/search?" + urllib.parse.urlencode(params)
    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "record-room/1.0"}
        )
        with urllib.request.urlopen(request, timeout=12) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception:
        return {"resultCount": 0, "results": []}

@st.cache_data(ttl=600, show_spinner=False)
def apple_lookup(params):
    url = "https://itunes.apple.com/lookup?" + urllib.parse.urlencode(params)
    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "record-room/1.0"}
        )
        with urllib.request.urlopen(request, timeout=12) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception:
        return {"resultCount": 0, "results": []}

# =========================================================
# KOREA POPULAR CHART
# =========================================================

@st.cache_data(ttl=900, show_spinner=False)
def korea_top_chart():
    """Apple Music 대한민국 Top 100을 받아 검색 결과의 인기순 정렬에 사용합니다."""
    urls = [
        "https://rss.applemarketingtools.com/api/v2/kr/music/most-played/100/songs.json",
        "https://itunes.apple.com/kr/rss/topsongs/limit=100/json",
    ]

    for url in urls:
        try:
            request = urllib.request.Request(
                url,
                headers={"User-Agent": "record-room/1.0"}
            )
            with urllib.request.urlopen(request, timeout=12) as response:
                data = json.loads(response.read().decode("utf-8"))

            results = data.get("feed", {}).get("results", [])
            if not results:
                results = data.get("results", [])

            if results:
                return results[:100]
        except Exception:
            continue

    return []


def artist_names_equivalent(name_a, name_b):
    na = normalize(name_a)
    nb = normalize(name_b)
    if not na or not nb:
        return False
    if na == nb:
        return True

    for key, aliases in ARTIST_ALIASES.items():
        group = {normalize(key)}
        group.update(normalize(alias) for alias in aliases)
        if na in group and nb in group:
            return True

    return False


def korea_chart_rank(track):
    title = normalize(track.get("trackName") or track.get("name") or "")
    artist = track.get("artistName", "")
    if not title:
        return 9999

    for rank, item in enumerate(korea_top_chart(), start=1):
        chart_title = normalize(item.get("name") or item.get("trackName") or "")
        chart_artist = item.get("artistName", "")
        if chart_title == title and artist_names_equivalent(artist, chart_artist):
            return rank

    return 9999


def popularity_sort_key(track):
    chart_rank = korea_chart_rank(track)
    release_date = track.get("releaseDate", "") or ""
    release_score = 0
    if release_date:
        try:
            release_score = -int(release_date[:10].replace("-", ""))
        except Exception:
            release_score = 0
    return (0 if chart_rank < 9999 else 1, chart_rank, release_score)


def rank_by_korea_popularity(results, limit=None):
    ranked = sorted(results, key=popularity_sort_key)
    return ranked[:limit] if limit else ranked

def normalize(text):
    if not text:
        return ""
    return re.sub(r"[^0-9a-z가-힣]", "", text.lower())

# =========================================================
# SEARCH ALIASES
# =========================================================

ARTIST_ALIASES = {
    "아이유": ["IU"],
    "iu": ["아이유"],
    "지코": ["ZICO", "Zico"],
    "zico": ["지코"],
    "뉴진스": ["NewJeans"],
    "newjeans": ["뉴진스"],
    "방탄소년단": ["BTS"],
    "bts": ["방탄소년단"],
    "블랙핑크": ["BLACKPINK"],
    "blackpink": ["블랙핑크"],
    "에스파": ["aespa"],
    "aespa": ["에스파"],
    "아이브": ["IVE"],
    "ive": ["아이브"],
    "세븐틴": ["SEVENTEEN"],
    "seventeen": ["세븐틴"],
    "르세라핌": ["LE SSERAFIM", "LE SSERAFIM"],
    "le sserafim": ["르세라핌"],
    "보이넥스트도어": ["BOYNEXTDOOR", "BOY NEXT DOOR"],
    "boynextdoor": ["보이넥스트도어", "BOYNEXTDOOR"],
    "boy next door": ["보이넥스트도어", "BOYNEXTDOOR"],
    "투모로우바이투게더": ["TOMORROW X TOGETHER", "TXT"],
    "txt": ["TOMORROW X TOGETHER", "투모로우바이투게더"],
    "스트레이키즈": ["Stray Kids"],
    "straykids": ["스트레이키즈", "Stray Kids"],
    "엔하이픈": ["ENHYPEN"],
    "enhypen": ["엔하이픈"],
    "르세라핌": ["LE SSERAFIM"],
    "아이들": ["(G)I-DLE", "G I-DLE", "여자아이들"],
    "여자아이들": ["(G)I-DLE", "아이들"],
    "gidle": ["(G)I-DLE", "여자아이들"],
    "빅뱅": ["BIGBANG"],
    "bigbang": ["빅뱅"],
    "악뮤": ["AKMU", "악동뮤지션"],
    "akmu": ["악뮤", "AKMU"],
}

# Apple Music/iTunes의 동명이인 아티스트를 피하기 위한 대표 아티스트 ID입니다.
# 특히 IU는 같은 이름을 쓰는 다른 아티스트가 검색되는 경우가 있어 ID로 고정합니다.
KNOWN_ARTIST_IDS = {
    "아이유": 409076743,
    "iu": 409076743,
}

PREFERRED_ARTIST_NAMES = {
    "아이유": ["아이유", "IU"],
    "iu": ["아이유", "IU"],
    "지코": ["ZICO", "지코"],
    "zico": ["ZICO", "지코"],
    "뉴진스": ["NewJeans", "뉴진스"],
    "newjeans": ["NewJeans", "뉴진스"],
    "보이넥스트도어": ["BOYNEXTDOOR", "보이넥스트도어"],
    "boynextdoor": ["BOYNEXTDOOR", "보이넥스트도어"],
    "방탄소년단": ["BTS", "방탄소년단"],
    "bts": ["BTS", "방탄소년단"],
    "블랙핑크": ["BLACKPINK", "블랙핑크"],
    "blackpink": ["BLACKPINK", "블랙핑크"],
    "에스파": ["aespa", "에스파"],
    "aespa": ["aespa", "에스파"],
}


SONG_ALIASES = {
    "러브 윈즈 올": ["Love wins all"],
    "love wins all": ["러브 윈즈 올"],
    "러브윈즈올": ["Love wins all"],
}


def expand_search_terms(query, alias_map):
    query = query.strip()
    terms = [query]
    lower = query.lower()
    normalized = normalize(query)

    for key, aliases in alias_map.items():
        if lower == key.lower() or normalized == normalize(key):
            for alias in aliases:
                if alias not in terms:
                    terms.append(alias)
            break

    return terms


# =========================================================
# ARTIST SEARCH
# =========================================================

@st.cache_data(ttl=600, show_spinner=False)
def find_artist_tracks(query):
    query = query.strip()
    if not query:
        return []

    search_terms = expand_search_terms(query, ARTIST_ALIASES)
    nq = normalize(query)
    candidates = []

    for search_term in search_terms:
        for country in ["KR", "US"]:
            data = apple_search({
                "term": search_term,
                "country": country,
                "media": "music",
                "entity": "musicArtist",
                "attribute": "artistTerm",
                "limit": 50
            })

            for artist in data.get("results", []):
                artist_id = artist.get("artistId")
                artist_name = artist.get("artistName", "")
                if not artist_id or not artist_name:
                    continue
                if not any(x.get("artistId") == artist_id for x in candidates):
                    candidates.append(artist)

    # musicArtist 검색이 한글 검색에서 비어 있는 경우 곡 검색으로 아티스트를 역추적합니다.
    if not candidates:
        for search_term in search_terms:
            for country in ["KR", "US"]:
                data = apple_search({
                    "term": search_term,
                    "country": country,
                    "media": "music",
                    "entity": "song",
                    "attribute": "artistTerm",
                    "limit": 100
                })
                for song in data.get("results", []):
                    artist_id = song.get("artistId")
                    artist_name = song.get("artistName", "")
                    if not artist_id or not artist_name:
                        continue
                    if not any(x.get("artistId") == artist_id for x in candidates):
                        candidates.append({
                            "artistId": artist_id,
                            "artistName": artist_name
                        })

    if not candidates:
        return []

    # -----------------------------------------------------
    # 0. 대표 아티스트 ID가 있으면 이름 검색 결과보다 ID를 우선합니다.
    # -----------------------------------------------------
    known_id = None
    for key, artist_id in KNOWN_ARTIST_IDS.items():
        if normalize(key) == normalize(query):
            known_id = artist_id
            break

    if known_id is not None:
        canonical = [
            artist for artist in candidates
            if artist.get("artistId") == known_id
        ]
        if canonical:
            selected = canonical[0]
        else:
            # 검색 결과에 ID가 빠져도 직접 lookup하면 정확한 아티스트를 확보할 수 있습니다.
            lookup_data = apple_lookup({
                "id": known_id,
                "entity": "song",
                "country": "KR",
                "limit": 100
            })
            canonical_tracks = [
                item for item in lookup_data.get("results", [])
                if item.get("wrapperType") == "track"
                and item.get("kind") == "song"
            ]
            if canonical_tracks:
                return rank_by_korea_popularity(canonical_tracks, limit=30)
            selected = None
    else:
        selected = None

    # 원래 검색어 → 공식/대표 표기 → 별칭 → 부분 일치 순서로 정확도를 높입니다.
    preferred_names = PREFERRED_ARTIST_NAMES.get(lower := query.lower(), [])
    preferred_normalized = [normalize(name) for name in preferred_names]

    if selected is None and preferred_normalized:
        preferred = [
            artist for artist in candidates
            if normalize(artist.get("artistName", "")) in preferred_normalized
        ]
        if preferred:
            selected = preferred[0]

    if selected is None:
        exact = [
            artist for artist in candidates
            if normalize(artist.get("artistName", "")) == nq
        ]
        if exact:
            selected = exact[0]

    if selected is None:
        for alias in search_terms[1:]:
            alias_normalized = normalize(alias)
            exact_alias = [
                artist for artist in candidates
                if normalize(artist.get("artistName", "")) == alias_normalized
            ]
            if exact_alias:
                selected = exact_alias[0]
                break

    if selected is None:
        for term in search_terms:
            nt = normalize(term)
            contains = [
                artist for artist in candidates
                if nt and nt in normalize(artist.get("artistName", ""))
            ]
            if contains:
                selected = contains[0]
                break

    if selected is None:
        return []

    artist_id = selected.get("artistId")
    if not artist_id:
        return []

    all_tracks = []
    for country in ["KR", "US"]:
        data = apple_lookup({
            "id": artist_id,
            "entity": "song",
            "country": country,
            "limit": 100
        })
        for item in data.get("results", []):
            if item.get("wrapperType") == "track" and item.get("kind") == "song":
                track_id = item.get("trackId")
                if track_id and any(x.get("trackId") == track_id for x in all_tracks):
                    continue
                all_tracks.append(item)

    # 대한민국에서 현재 많이 듣는 곡을 먼저 보여주고,
    # 그 뒤에 최신 발매곡을 보완합니다. 그래서 "아이유"처럼
    # 동명이인의 듣보 아티스트가 검색 상단을 차지하는 문제를 줄입니다.
    return rank_by_korea_popularity(all_tracks, limit=30)


# =========================================================
# SONG SEARCH
# =========================================================

@st.cache_data(ttl=600, show_spinner=False)
def find_song(query):
    query = query.strip()
    if not query:
        return []

    search_terms = expand_search_terms(query, SONG_ALIASES)
    all_results = []

    for search_term in search_terms:
        for country in ["KR", "US"]:
            data = apple_search({
                "term": search_term,
                "country": country,
                "media": "music",
                "entity": "song",
                "attribute": "songTerm",
                "limit": 100
            })
            for result in data.get("results", []):
                track_name = result.get("trackName", "")
                if not track_name:
                    continue
                track_id = result.get("trackId")
                if track_id and any(x.get("trackId") == track_id for x in all_results):
                    continue
                all_results.append(result)

    if not all_results:
        return []

    # 원문 정확 일치
    for term in search_terms:
        nt = normalize(term)
        exact = [
            result for result in all_results
            if normalize(result.get("trackName", "")) == nt
        ]
        if exact:
            return rank_by_korea_popularity(exact, limit=30)

    # 제목에 검색어가 포함되는 결과
    partial = []
    for term in search_terms:
        nt = normalize(term)
        if not nt:
            continue
        partial.extend([
            result for result in all_results
            if nt in normalize(result.get("trackName", ""))
        ])

    unique = []
    seen = set()
    for result in partial:
        track_id = result.get("trackId")
        if track_id in seen:
            continue
        seen.add(track_id)
        unique.append(result)

    return rank_by_korea_popularity(unique, limit=30)


# =========================================================
# GENERAL SEARCH
# =========================================================

def search_music(query, mode):
    query = query.strip()
    if not query:
        return []

    if mode == "artist":
        return find_artist_tracks(query)
    if mode == "song":
        return find_song(query)

    artist_results = find_artist_tracks(query)
    if artist_results:
        return artist_results
    return find_song(query)


# =========================================================
# AI COCKTAIL RECOMMENDATION
# =========================================================

MOOD_CONFIG = {
    "sad": {
        "label": "조금 위로가 필요해요",
        "drink": "핑크 칵테일",
        "color": "pink",
        "description": "마음을 가라앉히고 천천히 쉬어 가는 음악",
        "fallback": ["Korean sad ballad", "Korean emotional R&B", "IU ballad", "Korean indie melancholy"],
    },
    "refresh": {
        "label": "산뜻하게 기분 전환",
        "drink": "멜론 소다",
        "color": "green",
        "description": "가볍고 청량한 분위기로 전환하는 음악",
        "fallback": ["K-pop refreshing", "Korean upbeat pop", "Korean pop summer", "K-pop bright"],
    },
    "excited": {
        "label": "신나는 노래가 필요해요",
        "drink": "오렌지 주스",
        "color": "orange",
        "description": "리듬을 타면서 기분을 끌어올리는 음악",
        "fallback": ["K-pop dance", "Korean hip hop", "K-pop party", "Korean upbeat R&B"],
    },
    "quiet": {
        "label": "조용히 쉬고 싶어요",
        "drink": "네이비 칵테일",
        "color": "navy",
        "description": "차분하게 집중하고 편하게 쉴 수 있는 음악",
        "fallback": ["Korean indie acoustic", "Korean chill R&B", "Korean lo-fi", "Korean soft pop"],
    },
}


def cocktail_visual_html(color, fill=100, mini=False):
    """Inline SVG cocktail illustration with connected bowl, stem and base.

    Liquid, bubbles and in-glass details are clipped to the bowl. Garnishes are
    progressively removed after each sip; the melon soda's long straw remains.
    """
    color = color if color in {"pink", "green", "orange", "navy"} else "pink"
    height = 100 if mini else max(0, min(100, int(fill)))
    sips = 0 if mini else max(0, min(6, round((100 - height) / 17)))
    uid = f"rh-{color}-{'mini' if mini else 'hero'}"

    # Bowl geometry, stem and base are a single visual assembly. Each liquid is clipped
    # to its own glass silhouette so none can spill outside the vessel.
    specs = {
        "pink": {
            "body": "M 30 80 C 40 126 74 164 120 174 C 166 164 200 126 210 80 Q 120 60 30 80 Z",
            "rim_y": 80, "rim_rx": 90, "rim_ry": 11,
            "floor": 171, "usable": 88, "left": 30, "width": 180,
            "stem": "M 116 170 L 117 251 Q 120 256 123 251 L 124 170 Z",
            "base_y": 260, "base_rx": 39, "base_ry": 6,
            "shine": "M 48 91 C 58 124 79 150 98 159",
        },
        "green": {
            "body": "M 70 68 Q 120 57 170 68 L 158 201 Q 156 215 140 220 L 100 220 Q 84 215 82 201 Z",
            "rim_y": 68, "rim_rx": 51, "rim_ry": 10,
            "floor": 214, "usable": 137, "left": 70, "width": 100,
            "stem": "M 116 217 L 117 267 Q 120 270 123 267 L 124 217 Z",
            "base_y": 278, "base_rx": 45, "base_ry": 6,
            "shine": "M 82 82 L 91 193 Q 92 205 101 209",
        },
        "orange": {
            "body": "M 48 116 Q 120 98 192 116 C 188 158 176 198 153 214 Q 120 229 87 214 C 64 198 52 158 48 116 Z",
            "rim_y": 116, "rim_rx": 72, "rim_ry": 12,
            "floor": 219, "usable": 94, "left": 49, "width": 142,
            "stem": "M 116 217 L 117 269 Q 120 272 123 269 L 124 217 Z",
            "base_y": 280, "base_rx": 46, "base_ry": 6,
            "shine": "M 62 128 C 68 166 77 191 94 204",
        },
        "navy": {
            "body": "M 34 80 Q 120 52 206 80 L 128 155 Q 120 163 112 155 Z",
            "rim_y": 80, "rim_rx": 86, "rim_ry": 12,
            "floor": 156, "usable": 67, "left": 36, "width": 168,
            "stem": "M 117 157 L 118 238 Q 120 241 122 238 L 123 157 Z",
            "base_y": 250, "base_rx": 48, "base_ry": 6,
            "shine": "M 49 82 Q 87 72 113 82 L 118 105",
        },
    }
    s = specs[color]
    liquid_h = s["usable"] * height / 100.0
    liquid_top = s["floor"] - liquid_h
    top_width = s["rim_rx"] * 2 * (0.88 if color == "navy" else 0.96)
    bottom_width = {"pink": 22, "green": 56, "orange": 58, "navy": 16}[color]
    frac = min(1.0, max(0.0, (liquid_top - (s["floor"] - s["usable"])) / s["usable"])) if s["usable"] else 0
    surface_w = bottom_width + (top_width - bottom_width) * frac
    surface_left = 120 - surface_w / 2

    liquid_colors = {
        "pink": ("#ffe5ed", "#ee94b2", "#b94070"),
        "green": ("#e0ffd5", "#83dfa0", "#26965d"),
        "orange": ("#fff0bb", "#ffb33e", "#e75f19"),
        "navy": ("#b6d0ff", "#536fb2", "#151c43"),
    }
    c1, c2, c3 = liquid_colors[color]
    bubble_positions = [(0.24, .20), (.69, .34), (.43, .52), (.78, .66), (.29, .76), (.57, .26), (.61, .86), (.18, .48)]
    # Small, fine carbonation bubbles; fewer as the drink is sipped.
    bubble_count = 0 if height <= 0 else min(5, max(1, round(height / 21)))
    bubbles_svg = []
    if liquid_h > 6:
        interior_left = s["left"] + 6
        interior_w = s["width"] - 12
        for i, (xp, yp) in enumerate(bubble_positions[:bubble_count]):
            bx = interior_left + interior_w * xp
            by = s["floor"] - max(4, liquid_h * yp)
            radius = (1.05, 1.25, 0.95, 1.15, 1.0, 0.9, 1.2, 0.85)[i]
            bubbles_svg.append(
                f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="{radius}" '
                'fill="#fff9f1" fill-opacity=".48" stroke="#ffffff" stroke-opacity=".16" stroke-width=".45"/>'
            )
    bubbles = ''.join(bubbles_svg)

    liquid_block = ""
    if height > 0 and liquid_h > 0:
        liquid_block = (
            f'<rect x="0" y="{liquid_top:.2f}" width="240" height="{liquid_h + 7:.2f}" '
            f'fill="url(#{uid}-liquid)" opacity=".98"/>'
            f'<path d="M {surface_left:.1f} {liquid_top:.1f} Q 120 {liquid_top + 3:.1f} '
            f'{surface_left + surface_w:.1f} {liquid_top:.1f}" fill="none" stroke="#fff9ee" '
            'stroke-opacity=".46" stroke-width="1.6"/>'
            + bubbles
        )

    # Decorations are layered intentionally and have discrete stages tied to each sip.
    garnish = ""
    sparkles = ""
    if color == "pink":
        if sips < 1:
            garnish += (
                '<path d="M 111 52 L 136 112" stroke="#edcf91" stroke-width="3.2" stroke-linecap="round"/>'
                '<path d="M 112 54 L 136 112" stroke="#fff0c8" stroke-width=".9" stroke-linecap="round"/>'
            )
        if sips < 2:
            garnish += (
                '<circle cx="135" cy="105" r="9.5" fill="url(#' + uid + '-pearl)" stroke="#fff0da" stroke-width="1.2"/>'
                '<circle cx="132" cy="102" r="2.6" fill="#fff8f4" fill-opacity=".78"/>'
            )
    elif color == "green":
        # This long straw is intentionally retained for every sip state.
        garnish += (
            '<path d="M 157 13 L 132 109" stroke="#e87f95" stroke-width="8" stroke-linecap="round"/>'
            '<path d="M 156 14 L 133 105" stroke="#ffe2df" stroke-width="2" stroke-linecap="round"/>'
        )
        if sips < 1:
            # Full scoop and cherry overlap slightly so they read as one garnish on the rim.
            garnish += (
                '<path d="M 73 72 C 70 53 86 37 107 37 C 130 37 144 53 142 73 '
                'Q 109 88 73 72 Z" fill="url(#' + uid + '-cream)" stroke="#fff9e9" stroke-width="1.5"/>'
                '<path d="M 80 65 Q 108 76 136 66" fill="none" stroke="#e9d9b8" stroke-width="1.6" stroke-opacity=".68"/>'
                '<circle cx="135" cy="66" r="9.5" fill="url(#' + uid + '-cherry)" stroke="#f5b8af" stroke-width="1.1"/>'
                '<path d="M 134 57 Q 142 49 150 54" fill="none" stroke="#7a9659" stroke-width="2.1" stroke-linecap="round"/>'
            )
        elif sips < 2:
            garnish += (
                '<path d="M 89 73 Q 100 62 115 69 L 130 74 Q 108 82 89 73 Z" '
                'fill="url(#' + uid + '-cream)" stroke="#fff9e9" stroke-width="1.1" opacity=".70"/>'
            )
    elif color == "orange":
        if sips < 2:
            # One modest citrus wheel sits directly on the bowl's rim; no detached garnish.
            garnish += (
                '<g transform="translate(171 113) rotate(10)">'
                '<circle r="19" fill="#e9671b" stroke="#ffcd74" stroke-width="2.0"/>'
                '<circle r="15.8" fill="#fff0b9"/>'
                '<circle r="13.7" fill="url(#' + uid + '-liquid)" stroke="#f28b2d" stroke-width="1.15"/>'
                '<path d="M 0 0 L 0 -13 M 0 0 L 11.8 6.5 M 0 0 L -11.8 6.5 M 0 0 L 0 13" stroke="#fff2c5" stroke-width="1.15" stroke-linecap="round"/>'
                '<circle r="2.0" fill="#fff3cf"/>'
                '</g>'
            )
    else:  # navy
        if sips < 2:
            # A single fine lemon twist sits across the rim; no loose pick or floating dot.
            garnish += (
                '<path d="M 151 80 C 157 66 176 65 185 78 C 177 84 163 84 155 78" '
                'fill="#ffd46e" stroke="#fff0b2" stroke-width="1.25" stroke-linejoin="round"/>'
                '<path d="M 158 78 Q 170 72 179 78" fill="none" stroke="#fff6d3" stroke-width="1.4" stroke-linecap="round"/>'
            )
        # Fine, sparse glints fade with the liquid level.
        star_specs = [(91, .30, 1.45), (145, .49, 1.2), (111, .68, 1.05)]
        count = 0 if height < 8 else (1 if height < 34 else (2 if height < 62 else 3))
        for sx, yf, rr in star_specs[:count]:
            sy = s["floor"] - max(5, liquid_h * yf)
            sparkles += (
                f'<path d="M {sx} {sy-rr*2:.1f} L {sx+rr*.55:.1f} {sy-rr*.55:.1f} '
                f'L {sx+rr*2:.1f} {sy:.1f} L {sx+rr*.55:.1f} {sy+rr*.55:.1f} '
                f'L {sx} {sy+rr*2:.1f} L {sx-rr*.55:.1f} {sy+rr*.55:.1f} '
                f'L {sx-rr*2:.1f} {sy:.1f} L {sx-rr*.55:.1f} {sy-rr*.55:.1f} Z" '
                'fill="#e3eaff" fill-opacity=".84"/>'
            )

    bubble_gradient = {
        "pink": ("#fff2f6", "#e7a0b7", "#b73e70"),
        "green": ("#f2ffdf", "#a3efb5", "#2a9a62"),
        "orange": ("#fff4c9", "#ffc15c", "#eb6b1e"),
        "navy": ("#e0eaff", "#8ca9e7", "#283d80"),
    }[color]
    g1, g2, g3 = bubble_gradient
    rim_y = s["rim_y"]
    rim_rx, rim_ry = s["rim_rx"], s["rim_ry"]
    base_y, base_rx, base_ry = s["base_y"], s["base_rx"], s["base_ry"]
    top_y = rim_y
    glass_shape = s["body"]
    stem = s["stem"]

    # Draw base and stem first so the bowl visibly joins them rather than floating above them.
    svg = (
        f'<svg class="cocktail-svg {"mini" if mini else "hero"}" viewBox="0 0 240 300" width="{158 if mini else 240}" height="{198 if mini else 300}" '
        'role="img" aria-label="' + {"pink":"Pink cocktail", "green":"Melon soda", "orange":"Orange juice", "navy":"Navy cocktail"}[color] + '">' 
        '<defs>'
        f'<linearGradient id="{uid}-liquid" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{c1}"/><stop offset=".45" stop-color="{c2}"/><stop offset="1" stop-color="{c3}"/></linearGradient>'
        f'<linearGradient id="{uid}-glass" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#ffffff" stop-opacity=".30"/><stop offset=".22" stop-color="#ffffff" stop-opacity=".035"/>'
        '<stop offset=".76" stop-color="#ffffff" stop-opacity=".02"/><stop offset="1" stop-color="#ffffff" stop-opacity=".19"/></linearGradient>'
        f'<linearGradient id="{uid}-stem" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#cbbba5" stop-opacity=".68"/><stop offset=".45" stop-color="#fff2dc" stop-opacity=".9"/>'
        '<stop offset="1" stop-color="#a18d77" stop-opacity=".74"/></linearGradient>'
        f'<radialGradient id="{uid}-pearl" cx="30%" cy="25%">'
        '<stop offset="0" stop-color="#fffef8"/><stop offset=".55" stop-color="#f7dfc5"/><stop offset="1" stop-color="#c68b91"/></radialGradient>'
        f'<radialGradient id="{uid}-cream" cx="32%" cy="20%">'
        '<stop offset="0" stop-color="#fffef3"/><stop offset=".62" stop-color="#fff0c8"/><stop offset="1" stop-color="#dbc59a"/></radialGradient>'
        f'<radialGradient id="{uid}-cherry" cx="25%" cy="20%">'
        '<stop offset="0" stop-color="#ff9aa0"/><stop offset=".55" stop-color="#d9364f"/><stop offset="1" stop-color="#781c35"/></radialGradient>'
        f'<clipPath id="{uid}-clip"><path d="{glass_shape}"/></clipPath>'
        '</defs>'
        f'<ellipse cx="120" cy="{base_y + 4}" rx="{base_rx + 6}" ry="4" fill="#000000" fill-opacity=".20"/>'
        f'<path d="{stem}" fill="url(#{uid}-stem)" stroke="#f2dfc7" stroke-opacity=".58" stroke-width=".8"/>'
        f'<ellipse cx="120" cy="{base_y}" rx="{base_rx}" ry="{base_ry}" fill="#281911" fill-opacity=".56" stroke="#e8d7c0" stroke-opacity=".78" stroke-width="1.7"/>'
        f'<ellipse cx="120" cy="{base_y-1}" rx="{base_rx-7}" ry="{max(2,base_ry-2)}" fill="none" stroke="#fff1da" stroke-opacity=".26" stroke-width="1"/>'
        f'<g clip-path="url(#{uid}-clip)">'
        + liquid_block + sparkles +
        '</g>'
        f'<path d="{glass_shape}" fill="url(#{uid}-glass)" fill-opacity=".42" stroke="#f5e7d5" stroke-opacity=".88" stroke-width="2" stroke-linejoin="round"/>'
        f'<path d="{s["shine"]}" fill="none" stroke="#fffdf6" stroke-opacity=".62" stroke-width="3.1" stroke-linecap="round"/>'
        f'<ellipse cx="120" cy="{top_y}" rx="{rim_rx}" ry="{rim_ry}" fill="#ffffff" fill-opacity=".045" stroke="#fff6e9" stroke-opacity=".88" stroke-width="2"/>'
        f'<ellipse cx="120" cy="{top_y+1}" rx="{rim_rx-4}" ry="{max(2,rim_ry-3)}" fill="none" stroke="#ffffff" stroke-opacity=".26" stroke-width="1"/>'
        + garnish +
        '</svg>'
    )
    if mini:
        return f'<div class="mini-drink mini-{color}">{svg}</div>'
    return f'<div class="drink-visual drink-scene {color}" data-sips="{sips}">{svg}</div>'


def get_openai_key():
    try:
        key = str(st.secrets["OPENAI_API_KEY"]).strip()
        return key
    except Exception:
        return ""


def extract_response_text(data):
    pieces = []
    for item in data.get("output", []) if isinstance(data, dict) else []:
        if not isinstance(item, dict):
            continue
        for content in item.get("content", []) or []:
            if isinstance(content, dict) and content.get("type") in ("output_text", "text"):
                text_value = content.get("text", "")
                if text_value:
                    pieces.append(str(text_value))
    return "\n".join(pieces).strip()


@st.cache_data(ttl=1800, show_spinner=False)
def ai_search_terms(mood_key):
    config = MOOD_CONFIG[mood_key]
    api_key = get_openai_key()

    if not api_key:
        return config["fallback"], False

    system_prompt = (
        "You are the music concierge of a Korean mystery hotel. "
        "The user has selected a mood. Generate exactly 5 concise search phrases "
        "that can be sent to the Apple iTunes music search API. "
        "Prefer real Korean/English genres, artists, or music styles rather than abstract adjectives. "
        "Do not invent song titles. Return only 5 lines, one search phrase per line, with no numbering."
    )
    user_prompt = (
        f"Mood: {config['label']}\n"
        f"Description: {config['description']}\n"
        "Create five useful search phrases for finding songs that fit this mood."
    )

    body = json.dumps({
        "model": "gpt-5.6-luna",
        "input": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "max_output_tokens": 180,
    }).encode("utf-8")

    request = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            data = json.loads(response.read().decode("utf-8"))
        text = extract_response_text(data)
        terms = []
        for line in text.splitlines():
            line = re.sub(r"^[\s\-•\d\.\)]+", "", line).strip()
            if line and line not in terms:
                terms.append(line)
        if len(terms) >= 2:
            return terms[:5], True
    except Exception:
        pass

    curated_fallbacks = {
        "sad": ["IU Through the Night", "AKMU How can I love the heartbreak", "BOL4 To My Youth", "Taeyeon Fine", "Paul Kim Me After You"],
        "refresh": ["NewJeans Super Shy", "IVE After LIKE", "DAY6 Time of Our Life", "ZICO Any Song", "LE SSERAFIM Perfect Night"],
        "excited": ["aespa Supernova", "BLACKPINK Shut Down", "ZICO SPOT", "BTS Dynamite", "SEVENTEEN Super"],
        "quiet": ["wave to earth seasons", "DEAN instagram", "Colde Your Dog Loves You", "BIBI Restless", "IU 밤편지"],
    }
    return curated_fallbacks.get(mood_key, config["fallback"]), False


@st.cache_data(ttl=1800, show_spinner=False)
def get_ai_recommendations(mood_key):
    terms, used_ai = ai_search_terms(mood_key)
    results = []

    for term in terms:
        data = apple_search({
            "term": term,
            "country": "KR",
            "media": "music",
            "entity": "song",
            "limit": 25,
        })
        for item in data.get("results", []):
            if not item.get("trackName") or not item.get("artistName"):
                continue
            if not item.get("previewUrl"):
                continue
            track_id = item.get("trackId")
            if track_id and any(x.get("trackId") == track_id for x in results):
                continue
            results.append(item)
            if len(results) >= 35:
                break
        if len(results) >= 35:
            break

    if results:
        return rank_by_korea_popularity(results, limit=8), used_ai

    # KR 검색이 부족하면 US 검색도 보완합니다.
    for term in terms:
        data = apple_search({
            "term": term,
            "country": "US",
            "media": "music",
            "entity": "song",
            "limit": 25,
        })
        for item in data.get("results", []):
            if not item.get("trackName") or not item.get("artistName") or not item.get("previewUrl"):
                continue
            track_id = item.get("trackId")
            if track_id and any(x.get("trackId") == track_id for x in results):
                continue
            results.append(item)
            if len(results) >= 35:
                break
        if len(results) >= 35:
            break

    return rank_by_korea_popularity(results, limit=8), used_ai

# =========================================================
# RECORD HELPERS
# =========================================================

def record_data(result):
    return {
        "track_id": result.get("trackId"),
        "track": result.get("trackName", "제목 없음"),
        "artist": result.get("artistName", "아티스트 없음"),
        "album": result.get("collectionName", "앨범 정보 없음"),
        "artwork": result.get("artworkUrl600")
                    or result.get("artworkUrl100", ""),
        "preview": result.get("previewUrl", ""),
        "apple_url": result.get("trackViewUrl", ""),
    }

def add_to_room(result):
    record = record_data(result)

    if not record["preview"]:
        st.warning(
            "이 곡은 Apple Music 미리듣기를 제공하지 않아 LP에서 재생할 수 없습니다."
        )
        return

    existing_ids = [
        x.get("track_id")
        for x in st.session_state.room_records
    ]

    if record["track_id"] not in existing_ids:
        st.session_state.room_records.append(record)

    st.session_state.current_record = record

def remove_from_room(track_id):
    st.session_state.room_records = [
        x for x in st.session_state.room_records
        if x.get("track_id") != track_id
    ]

    if (
        st.session_state.current_record
        and st.session_state.current_record.get("track_id") == track_id
    ):
        st.session_state.current_record = (
            st.session_state.room_records[-1]
            if st.session_state.room_records
            else None
        )

# =========================================================
# RESULT DISPLAY
# =========================================================

def display_results(results):
    if not results:
        st.markdown(
            '<div class="no-result">'
            '검색 결과를 찾지 못했습니다.<br>'
            '가수 이름이나 정확한 곡 제목을 다시 입력해 주세요.'
            '</div>',
            unsafe_allow_html=True
        )
        return

    st.markdown(
        '<div class="result-title">SEARCH RESULT</div>',
        unsafe_allow_html=True
    )

    for index, result in enumerate(results[:30]):

        artwork = result.get("artworkUrl100", "")
        track = escape(result.get("trackName", "제목 없음"))
        artist = escape(result.get("artistName", "아티스트 없음"))
        album = escape(result.get("collectionName", "앨범 정보 없음"))
        date = escape((result.get("releaseDate", "") or "")[:10])
        apple_url = result.get("trackViewUrl", "")
        preview_url = result.get("previewUrl", "")

        col_img, col_info, col_action = st.columns(
            [1, 4, 1.5],
            vertical_alignment="center"
        )

        with col_img:
            if artwork:
                st.image(artwork, width=90)

        with col_info:
            st.markdown(
                '<div class="result-name">' + track + '</div>',
                unsafe_allow_html=True
            )

            link_html = ""
            if apple_url:
                link_html = (
                    '<a href="' + escape(apple_url)
                    + '" target="_blank" '
                    'style="color:#c89b6b;text-decoration:none;">'
                    'Apple Music ↗</a>'
                )

            st.markdown(
                '<div class="result-meta">'
                + artist + '<br>'
                + album + ' · ' + date + '<br>'
                + link_html + '</div>',
                unsafe_allow_html=True
            )

        with col_action:
            if preview_url:
                if st.button(
                    "TAKE TO MY ROOM",
                    key=f"take_record_{index}_{result.get('trackId')}",
                    use_container_width=True
                ):
                    add_to_room(result)
                    st.session_state.page = "my_room"
                    st.rerun()
            else:
                st.caption("LP 재생 불가")

        # 검색 결과의 미리듣기는 유지하되,
        # 실제 LP 재생은 MY ROOM에서 한다.
        if preview_url:
            st.audio(preview_url)

        st.markdown(
            '<div style="height:1px;background:rgba(199,157,109,0.10);'
            'margin:14px 0 20px 0;"></div>',
            unsafe_allow_html=True
        )

# =========================================================
# LP PLAYER
# =========================================================

def render_lp_player(record):

    if not record:
        st.markdown(
            '<div class="record-stage">'
            '<div class="record-player">'
            '<div class="record-label">'
            '<div class="record-label-text">EMPTY<br>RECORD</div>'
            '<div class="record-ring"></div>'
            '<div class="record-hole"></div>'
            '</div></div></div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<div class="record-caption">'
            'ROOM SERVICE에서 음악을 가져오면 이곳에서 재생할 수 있습니다.'
            '</div>',
            unsafe_allow_html=True
        )
        return

    title = escape(record.get("track", "RECORD"))
    artist = escape(record.get("artist", ""))
    artwork = escape(record.get("artwork", ""), quote=True)
    preview = escape(record.get("preview", ""), quote=True)

    player_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* {{ box-sizing: border-box; }}
html, body {{ margin:0; padding:0; background:transparent; }}
body {{ color:#d8ad79; font-family:Georgia, serif; overflow:hidden; }}
.wrap {{ min-height:500px; display:flex; flex-direction:column; align-items:center; justify-content:center; }}
.hint {{ color:#a98a70; font-size:13px; letter-spacing:1.5px; margin-bottom:22px; text-align:center; }}
.record {{ width:min(360px, 70vw); height:min(360px, 70vw); border-radius:50%; position:relative; cursor:pointer; user-select:none; touch-action:manipulation;
    background:repeating-radial-gradient(circle,#17110e 0px,#17110e 3px,#211813 4px,#211813 6px);
    box-shadow:0 0 0 10px rgba(47,31,22,.75),0 25px 55px rgba(0,0,0,.6); }}
.record.playing {{ animation:spin 2.6s linear infinite; }}
.record:before {{ content:""; position:absolute; inset:28px; border-radius:50%; border:1px solid rgba(255,255,255,.06); }}
.label {{ position:absolute; left:50%; top:50%; transform:translate(-50%,-50%); width:132px; height:132px; border-radius:50%; overflow:hidden;
    background:radial-gradient(circle,#b98555 0%,#8f5e3b 48%,#6c412a 100%); box-shadow:0 0 15px rgba(0,0,0,.45); }}
.label img {{ width:100%; height:100%; object-fit:cover; display:block; }}
.hole {{ position:absolute; width:12px; height:12px; background:#17110e; border-radius:50%; left:50%; top:50%; transform:translate(-50%,-50%); }}
.info {{ margin-top:20px; text-align:center; max-width:80vw; }}
.title {{ color:#e0bd91; font-size:23px; letter-spacing:2px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }}
.artist {{ color:#a98a70; font-size:14px; margin-top:6px; }}
.state {{ color:#c49a70; font-size:12px; letter-spacing:2px; margin-top:12px; }}
audio {{ display:none; }}
@keyframes spin {{ from {{ transform:rotate(0deg); }} to {{ transform:rotate(360deg); }} }}
</style>
</head>
<body>
<div class="wrap">
<div class="hint">CLICK ONCE · PLAY / PAUSE &nbsp;&nbsp; DOUBLE CLICK · STOP</div>
<div class="record" id="record">
    <div class="label">
        <img src="{artwork}" onerror="this.style.display='none'">
        <div class="hole"></div>
    </div>
</div>
<div class="info">
    <div class="title">{title}</div>
    <div class="artist">{artist}</div>
    <div class="state" id="state">STOPPED</div>
</div>
<audio id="audio" preload="auto" playsinline></audio>
</div>
<script>
const record = document.getElementById("record");
const audio = document.getElementById("audio");
const state = document.getElementById("state");
let clickTimer = null;

// Apple의 preview는 AAC/M4A인 경우가 많아서 audio/mp4로 직접 연결합니다.
audio.src = {json.dumps(record.get("preview", ""))};
audio.load();

function playRecord() {{
    if (!audio.src) {{ state.textContent = "NO PREVIEW"; return; }}
    const promise = audio.play();
    if (promise !== undefined) {{
        promise.then(() => {{
            record.classList.add("playing");
            state.textContent = "PLAYING";
        }}).catch(() => {{
            state.textContent = "PRESS AGAIN TO PLAY";
            record.classList.remove("playing");
        }});
    }}
}}

function pauseRecord() {{
    audio.pause();
    record.classList.remove("playing");
    state.textContent = "PAUSED";
}}

function stopRecord() {{
    audio.pause();
    try {{ audio.currentTime = 0; }} catch(e) {{}}
    record.classList.remove("playing");
    state.textContent = "STOPPED";
}}

record.addEventListener("click", () => {{
    if (clickTimer) clearTimeout(clickTimer);
    clickTimer = setTimeout(() => {{
        if (audio.paused) playRecord();
        else pauseRecord();
        clickTimer = null;
    }}, 230);
}});

record.addEventListener("dblclick", (event) => {{
    event.preventDefault();
    if (clickTimer) {{ clearTimeout(clickTimer); clickTimer = null; }}
    stopRecord();
}});

audio.addEventListener("ended", () => {{
    record.classList.remove("playing");
    state.textContent = "FINISHED";
}});

audio.addEventListener("error", () => {{
    record.classList.remove("playing");
    state.textContent = "PREVIEW UNAVAILABLE";
}});
</script>
</body>
</html>
"""

    components.html(player_html, height=540, scrolling=False)

# =========================================================
# FIREPLACE
# =========================================================

def render_fireplace():

    st.markdown(
        '<div class="fireplace-container">'
        '<div class="fireplace-title">FIREPLACE</div>'
        '<div class="fireplace-subtitle">불빛을 바라보며 잠시 쉬어가세요.</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="fireplace">'
        '<div class="wood"></div>'
        '<div class="wood two"></div>'
        '<div class="fire"></div>'
        '<div class="fire-small"></div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="fireplace-note">'
        '이곳에서는 아무것도 하지 않아도 괜찮습니다.<br>'
        '불멍을 하거나, 아래의 소리를 틀어두고 천천히 쉬어가세요.'
        '</div>',
        unsafe_allow_html=True
    )

    ambient_html = """
<!DOCTYPE html>
<html>
<head>
<style>
body {
    margin:0;
    background:transparent;
    font-family:Georgia, serif;
}
.row {
    display:flex;
    gap:10px;
    justify-content:center;
    flex-wrap:wrap;
    padding:12px 0;
}
button {
    background:rgba(247,238,219,.05);
    color:#c49a70;
    border:1px solid rgba(190,145,92,.45);
    padding:11px 18px;
    cursor:pointer;
    font-family:Georgia, serif;
    letter-spacing:2px;
}
button:hover {
    background:rgba(197,145,88,.10);
}
#status {
    text-align:center;
    color:#96765d;
    font-size:12px;
    letter-spacing:2px;
    margin-top:8px;
}
</style>
</head>
<body>
<div class="row">
    <button id="fire">FIREPLACE</button>
    <button id="rain">RAIN</button>
    <button id="white">WHITE NOISE</button>
    <button id="stop">STOP</button>
</div>
<div id="status">AMBIENT OFF</div>

<script>
let ctx = null;
let master = null;
let source = null;
let gain = null;
let timer = null;

function setup() {
    if (!ctx) {
        ctx = new (window.AudioContext || window.webkitAudioContext)();
        master = ctx.createGain();
        master.gain.value = 0.055;
        master.connect(ctx.destination);
    }
    if (ctx.state === "suspended") ctx.resume();
}

function stopAll() {
    if (source) {
        try { source.stop(); } catch(e) {}
        source = null;
    }
    if (gain) {
        try { gain.disconnect(); } catch(e) {}
        gain = null;
    }
    if (timer) {
        clearInterval(timer);
        timer = null;
    }
    document.getElementById("status").textContent = "AMBIENT OFF";
}

function noiseBuffer() {
    const length = ctx.sampleRate * 2;
    const buffer = ctx.createBuffer(1, length, ctx.sampleRate);
    const data = buffer.getChannelData(0);

    for (let i = 0; i < length; i++) {
        data[i] = Math.random() * 2 - 1;
    }

    return buffer;
}

function playNoise(type) {
    setup();
    stopAll();

    source = ctx.createBufferSource();
    source.buffer = noiseBuffer();
    source.loop = true;

    gain = ctx.createGain();
    gain.gain.value = type === "white" ? 0.12 : 0.07;

    const filter = ctx.createBiquadFilter();

    if (type === "rain") {
        filter.type = "lowpass";
        filter.frequency.value = 2200;
    } else {
        filter.type = "lowpass";
        filter.frequency.value = 900;
    }

    source.connect(filter);
    filter.connect(gain);
    gain.connect(master);
    source.start();

    document.getElementById("status").textContent =
        type === "rain" ? "RAIN PLAYING" : "WHITE NOISE PLAYING";
}

function playFire() {
    setup();
    stopAll();

    const osc = ctx.createOscillator();
    const fireGain = ctx.createGain();

    osc.type = "sine";
    osc.frequency.value = 65;
    fireGain.gain.value = 0.02;

    osc.connect(fireGain);
    fireGain.connect(master);
    osc.start();

    source = osc;
    gain = fireGain;

    timer = setInterval(() => {
        if (!ctx) return;

        const crack = ctx.createOscillator();
        const crackGain = ctx.createGain();

        crack.type = "triangle";
        crack.frequency.value = 100 + Math.random() * 900;

        crackGain.gain.setValueAtTime(0.0001, ctx.currentTime);
        crackGain.gain.exponentialRampToValueAtTime(
            0.035 + Math.random() * 0.025,
            ctx.currentTime + 0.01
        );
        crackGain.gain.exponentialRampToValueAtTime(
            0.0001,
            ctx.currentTime + 0.09
        );

        crack.connect(crackGain);
        crackGain.connect(master);
        crack.start();
        crack.stop(ctx.currentTime + 0.1);
    }, 700);

    document.getElementById("status").textContent = "FIREPLACE PLAYING";
}

document.getElementById("fire").onclick = playFire;
document.getElementById("rain").onclick = () => playNoise("rain");
document.getElementById("white").onclick = () => playNoise("white");
document.getElementById("stop").onclick = stopAll;
</script>
</body>
</html>
"""

    components.html(ambient_html, height=100, scrolling=False)

# =========================================================
# MAIN
# =========================================================

if st.session_state.page == "main":

    if not st.session_state.main_entered:
        st.markdown(
            '<div class="welcome-area">'
            '<div class="welcome-small">WELCOME TO</div>'
            '<div class="welcome-title">RECORD HOTEL</div>'
            '<div class="welcome-line"></div>'
            '<div class="welcome-description">'
            '음악을 듣고, 발견하고, 잠시 머무는 작은 방'
            '</div></div>',
            unsafe_allow_html=True
        )
        left, center, right = st.columns([2, 1, 2])
        with center:
            if st.button("ENTER HOTEL", key="enter_room", use_container_width=True):
                st.session_state.main_entered = True
                st.rerun()
    else:
        letter_html = (
            '<div class="letter-wrap"><div class="letter-paper">'
            '<div class="letter-date">SEPTEMBER 28, 2026</div>'
            '<div class="letter-title">DEAR, GUEST</div>'
            '<div class="letter-body">'
            '이곳에는 조금 오래 머물러도 괜찮습니다.<br><br>'
            '누군가에게는 스쳐 지나갈 한 곡이, 누군가에게는 오래 기억될 밤이 되기도 하니까요.<br><br>'
            '이 호텔에서는 당신이 원하는 음악을 찾아 객실로 가져갈 수 있습니다.<br><br>'
            '그리고 음악이 필요한 밤에는, 당신만의 방에서 조용히 음악을 틀어보세요.<br><br>'
            '문은 이미 열려 있습니다.'
            '</div><div class="letter-sign">— RECORD HOTEL</div>'
            '</div></div>'
        )
        st.markdown(letter_html, unsafe_allow_html=True)
        if st.button("← BACK TO LOBBY", key="back_main_letter"):
            st.session_state.main_entered = False
            st.rerun()

# =========================================================
# ROOM SERVICE
# =========================================================

elif st.session_state.page == "choice":

    if st.session_state.choice_mode is None:
        st.markdown(
            '<div class="section-area">'
            '<div class="section-title">ROOM SERVICE</div>'
            '<div class="section-subtitle">오늘 밤 객실로 가져갈 음악을 골라보세요.</div>'
            '</div>',
            unsafe_allow_html=True
        )
        st.markdown('<div class="room-service-buttons-spacer"></div>', unsafe_allow_html=True)
        left, right = st.columns(2, gap="large")
        with left:
            if st.button("노래 듣기", key="listen_choice", use_container_width=True):
                st.session_state.choice_mode = "listen"
                st.session_state.room_service_step = "search"
                st.rerun()
        with right:
            if st.button("추천받기", key="recommend_choice", use_container_width=True):
                st.session_state.choice_mode = "recommend"
                st.session_state.cocktail_mood = None
                st.session_state.cocktail_sips = 0
                st.session_state.cocktail_recommendations = []
                st.rerun()
        st.markdown(
            '<div style="text-align:center;color:#76563e;font-family:Georgia,serif;'
            'margin-top:35px;letter-spacing:2px;">ROOM SERVICE · OPEN ALL NIGHT</div>',
            unsafe_allow_html=True
        )

    elif st.session_state.choice_mode == "listen":
        st.markdown(
            '<div class="room-service-container">'
            '<div class="room-service-title">ROOM SERVICE</div>'
            '<div class="room-service-subtitle">객실로 가져갈 음악을 검색하세요. 선택한 음악은 MY ROOM의 LP로 이동합니다.</div>'
            '</div>',
            unsafe_allow_html=True
        )
        if st.button("← BACK TO ROOM SERVICE", key="room_service_back_top", use_container_width=True):
            st.session_state.choice_mode = None
            st.session_state.search_results = []
            st.session_state.search_text = ""
            st.rerun()

        st.markdown('<div class="listen-search">', unsafe_allow_html=True)
        st.markdown('<div class="result-title">FIND A RECORD</div>', unsafe_allow_html=True)
        search_col, button_col = st.columns([5, 1])
        with search_col:
            query = st.text_input(
                "SEARCH", value=st.session_state.search_text,
                placeholder="예: 아이유 / IU / 보이넥스트도어 / BOYNEXTDOOR / Love wins all",
                label_visibility="collapsed", key="music_search_input"
            )
        with button_col:
            search_clicked = st.button("SEARCH", key="music_search_button", use_container_width=True)

        search_type = st.radio("검색 기준", ["자동", "가수", "곡"], horizontal=True, label_visibility="collapsed")
        type_map = {"자동": "auto", "가수": "artist", "곡": "song"}

        if search_clicked and query.strip():
            st.session_state.search_text = query
            with st.spinner("호텔에서 음악을 찾는 중..."):
                st.session_state.search_results = search_music(query, type_map[search_type])
            st.rerun()

        if st.session_state.search_text:
            display_results(st.session_state.search_results)
        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.choice_mode == "recommend":
        # ---------------- COCKTAIL BAR ----------------
        st.markdown(
            '<div class="cocktail-header">'
            '<div class="cocktail-kicker">ROOM SERVICE · NIGHT CONCIERGE</div>'
            '<div class="cocktail-title">COCKTAIL BAR</div>'
            '<div class="cocktail-subtitle">오늘의 기분을 한 잔 골라주세요. 음악은 그 다음에 고를게요.</div>'
            '</div>',
            unsafe_allow_html=True
        )

        if st.session_state.cocktail_mood is None:
            mood_cols = st.columns(4, gap="medium")
            for col, (key, config) in zip(mood_cols, MOOD_CONFIG.items()):
                with col:
                    mini_visual = cocktail_visual_html(config["color"], mini=True)
                    st.markdown(
                        f'<div class="order-slip {config["color"]}">'
                        f'<div class="slip-no">ORDER NO. {list(MOOD_CONFIG).index(key)+1:02d}</div>'
                        f'<div class="slip-label">{config["label"]}</div>'
                        + mini_visual
                        + f'<div class="slip-drink">{config["drink"]}</div>'
                        + f'<div class="slip-desc">{config["description"]}</div>'
                        + '</div>',
                        unsafe_allow_html=True
                    )
                    st.markdown('<div class="cocktail-order-button-gap"></div>', unsafe_allow_html=True)
                    if st.button("ORDER THIS", key=f"order_mood_{key}", use_container_width=True):
                        st.session_state.cocktail_mood = key
                        st.session_state.cocktail_sips = 0
                        st.session_state.cocktail_recommendations = []
                        st.session_state.cocktail_recommendation_requested = False
                        st.rerun()

        else:
            if st.button("← BACK TO COCKTAIL BAR", key="cocktail_back_top", use_container_width=True):
                st.session_state.cocktail_mood = None
                st.session_state.cocktail_sips = 0
                st.session_state.cocktail_recommendations = []
                st.rerun()

            mood_key = st.session_state.cocktail_mood
            config = MOOD_CONFIG[mood_key]
            sips = st.session_state.cocktail_sips
            fill = max(0, 100 - sips * 17)

            st.markdown(
                f'<div class="selected-order">'
                f'<div class="selected-order-small">ROOM SERVICE ORDER</div>'
                f'<div class="selected-order-title">{config["label"]}</div>'
                f'<div class="selected-order-sub">{config["description"]}</div>'
                '</div>',
                unsafe_allow_html=True
            )

            # 칵테일과 마시기 버튼을 먼저 보여줍니다. 추천은 사용자가 원할 때 시작합니다.
            # Streamlit의 동기 실행 특성상 추천 API 호출 중 화면 상호작용을 막지 않도록
            # 음료를 먼저 제공하고 추천 요청은 별도 버튼으로 분리했습니다.
            recs = st.session_state.cocktail_recommendations
            drink_col, info_col = st.columns([1.02, 1.28], gap="large", vertical_alignment="top")

            with drink_col:
                st.markdown(
                    cocktail_visual_html(config["color"], fill=fill),
                    unsafe_allow_html=True
                )

                st.markdown(
                    f'<div class="drink-name">{config["drink"]}</div>'
                    f'<div class="drink-state">{("FULL" if sips == 0 else f"{fill}% REMAINING")}</div>',
                    unsafe_allow_html=True
                )

                st.write("")
                sip_col, refill_col = st.columns(2, gap="small")
                with sip_col:
                    if st.button("TAKE A SIP", key="take_sip", use_container_width=True):
                        if sips < 6:
                            st.session_state.cocktail_sips += 1
                        st.rerun()
                with refill_col:
                    if st.button("다시 먹기", key="refill_drink", use_container_width=True):
                        st.session_state.cocktail_sips = 0
                        st.rerun()

            with info_col:
                st.markdown(
                    '<div class="concierge-card">'
                    '<div class="concierge-label">NIGHT CONCIERGE</div>'
                    '<div class="concierge-title">오늘의 한 잔 옆에<br>어울리는 레코드를 골랐어요.</div>'
                    '<div class="concierge-copy">현재 대한민국에서 인기 있는 음악을 우선으로, 선택한 기분과 장르에 맞는 실제 Apple 음악 카탈로그의 곡을 골라옵니다.</div>'
                    '</div>',
                    unsafe_allow_html=True
                )

                if not st.session_state.cocktail_recommendations:
                    st.markdown(
                        '<div class="ai-note" style="font-size:11px;line-height:1.8;margin:8px 0 12px;">'
                        '칵테일을 먼저 즐겨보세요. 준비되면 아래 버튼으로 오늘의 레코드를 불러올 수 있어요.'
                        '</div>',
                        unsafe_allow_html=True
                    )
                    if st.button("오늘의 노래 추천받기", key="start_cocktail_recommendations", use_container_width=True):
                        with st.spinner("CONCIERGE IS CHOOSING RECORDS..."):
                            recs, used_ai = get_ai_recommendations(mood_key)
                        st.session_state.cocktail_recommendations = recs
                        st.session_state.cocktail_ai_used = used_ai
                        st.session_state.cocktail_recommendation_requested = True
                        st.rerun()

                st.markdown(
                    '<div class="recommendation-title">TONIGHT\'S RECORDS</div>',
                    unsafe_allow_html=True
                )
                if recs and st.session_state.get("cocktail_ai_used", False):
                    st.markdown('<div class="ai-note">AI CONCIERGE · MOOD MATCHED · KOREA POPULAR FIRST</div>', unsafe_allow_html=True)
                elif recs:
                    st.markdown('<div class="ai-note">CONCIERGE · FALLBACK MENU · KOREA POPULAR FIRST</div>', unsafe_allow_html=True)

                if recs:
                    for index, result in enumerate(recs[:5]):
                        artwork = result.get("artworkUrl100", "")
                        track = escape(result.get("trackName", "제목 없음"))
                        artist = escape(result.get("artistName", "아티스트 없음"))
                        album = escape(result.get("collectionName", "앨범 정보 없음"))

                        with st.container(border=True):
                            image_col, text_col = st.columns([0.8, 3.4], gap="small", vertical_alignment="center")
                            with image_col:
                                if artwork:
                                    st.image(artwork, width=68)
                            with text_col:
                                st.markdown(
                                    f'<div class="compact-rec-title">{track}</div>'
                                    f'<div class="compact-rec-meta">{artist}<br>{album}</div>',
                                    unsafe_allow_html=True
                                )

                            if result.get("previewUrl"):
                                st.audio(result["previewUrl"])

                            if st.button(
                                "TAKE TO MY ROOM",
                                key=f"cocktail_take_{index}_{result.get('trackId')}",
                                use_container_width=True
                            ):
                                add_to_room(result)
                                st.session_state.my_room_view = "lp"
                                st.session_state.page = "my_room"
                                st.rerun()
                elif st.session_state.get("cocktail_recommendation_requested", False):
                    st.markdown(
                        '<div class="no-result" style="margin-top:20px;">'
                        '오늘 밤에 맞는 레코드를 찾지 못했어요.<br>'
                        '다시 추천을 요청하면 다른 레코드를 찾아볼게요.'
                        '</div>',
                        unsafe_allow_html=True
                    )

            st.write("")
            if st.button("← BACK TO ROOM SERVICE", key="recommend_back", use_container_width=True):
                go_room_service()

# =========================================================
# MY ROOM
# =========================================================

elif st.session_state.page == "my_room":

    if not st.session_state.logged_in:
        st.markdown(
            '<div class="section-area" style="margin-bottom:30px;">'
            '<div class="section-title">MY ROOM</div></div>',
            unsafe_allow_html=True
        )

        if not st.session_state.my_room_checkin_open:
            st.markdown(
                '<div class="auth-box" style="margin-top:0;">'
                '<div class="auth-subtitle">객실에 들어가려면 먼저 CHECK-IN이 필요합니다.</div>'
                '</div>', unsafe_allow_html=True
            )
            gate_left, gate_center, gate_right = st.columns([2,1,2])
            with gate_center:
                if st.button("CHECK-IN", key="open_checkin", use_container_width=True):
                    st.session_state.my_room_checkin_open = True
                    st.session_state.auth_mode = "login"
                    st.rerun()
            if st.button("← BACK TO LOBBY", key="my_room_back_gate", use_container_width=True):
                st.session_state.page = "main"
                st.session_state.my_room_checkin_open = False
                st.rerun()
        else:
            st.markdown(
                '<div class="auth-box"><div class="auth-title">CHECK-IN</div>'
                '<div class="auth-subtitle">ROOM KEY를 입력하거나 새로운 GUEST로 등록하세요.</div></div>',
                unsafe_allow_html=True
            )
            auth_left, auth_right = st.columns(2)
            with auth_left:
                if st.button("CHECK-IN", key="auth_login_tab", use_container_width=True):
                    st.session_state.auth_mode = "login"
                    st.rerun()
            with auth_right:
                if st.button("NEW GUEST", key="auth_signup_tab", use_container_width=True):
                    st.session_state.auth_mode = "signup"
                    st.rerun()

            if supabase is None and SUPABASE_CONFIG_ERROR:
                st.error(SUPABASE_CONFIG_ERROR)
            email = st.text_input("EMAIL", placeholder="guest@example.com", key="auth_email")
            password = st.text_input("ROOM KEY", type="password", placeholder="비밀번호", key="auth_password")
            password_confirm = ""
            if st.session_state.auth_mode == "signup":
                password_confirm = st.text_input("ROOM KEY AGAIN", type="password", placeholder="비밀번호를 다시 입력하세요", key="auth_password_confirm")

            if st.session_state.auth_mode == "login":
                if st.button("ENTER MY ROOM", key="login_submit", use_container_width=True):
                    if not email.strip() or not password:
                        st.warning("이메일과 비밀번호를 입력해 주세요.")
                    else:
                        ok, message = login_user(email.strip(), password)
                        if ok:
                            st.session_state.my_room_view = "fireplace"
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
            else:
                if st.button("CREATE ROOM KEY", key="signup_submit", use_container_width=True):
                    if not email.strip() or not password:
                        st.warning("이메일과 비밀번호를 입력해 주세요.")
                    elif password != password_confirm:
                        st.warning("두 비밀번호가 일치하지 않습니다.")
                    elif len(password) < 6:
                        st.warning("비밀번호는 6자 이상으로 입력해 주세요.")
                    else:
                        ok, message = signup_user(email.strip(), password)
                        if ok:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)

            if st.button("← BACK", key="my_room_back_auth", use_container_width=True):
                st.session_state.my_room_checkin_open = False
                st.rerun()

    else:
        user_email = ""
        if st.session_state.current_user is not None:
            user_email = getattr(st.session_state.current_user, "email", "") or ""

        st.markdown(
            '<div class="room-service-container">'
            '<div class="room-service-title">MY ROOM</div>'
            '<div class="room-service-subtitle">GUEST PRIVATE ROOM</div>'
            '</div>', unsafe_allow_html=True
        )

        top_left, top_mid, top_right = st.columns([2,3,2])
        with top_left:
            st.caption("CHECKED IN")
        with top_mid:
            if user_email:
                st.markdown(
                    '<div style="text-align:center;color:#a98a70;font-family:Georgia,serif;letter-spacing:1px;">'
                    + escape(user_email) + '</div>', unsafe_allow_html=True
                )
        with top_right:
            if st.button("CHECK-OUT", key="logout_button", use_container_width=True):
                logout_user()

        view = st.session_state.my_room_view

        if view == "fireplace":
            render_fireplace()
            st.markdown('<div style="height:25px;"></div>', unsafe_allow_html=True)
            nav_left, nav_center, nav_right = st.columns([1,2,1])
            with nav_center:
                if st.button("GO TO LP PLAYER →", key="go_lp_from_fire", use_container_width=True):
                    st.session_state.my_room_view = "lp"
                    st.rerun()
            if st.button("← BACK TO ROOM SERVICE", key="my_room_back_fire", use_container_width=True):
                go_room_service()

        else:
            st.markdown('<div class="room-tabs">PLAY YOUR RECORD</div>', unsafe_allow_html=True)
            render_lp_player(st.session_state.current_record)

            st.markdown('<div class="room-tabs">RECORD CABINET</div>', unsafe_allow_html=True)
            if not st.session_state.room_records:
                st.markdown(
                    '<div class="room-record-empty">아직 객실로 가져온 음악이 없습니다.<br>ROOM SERVICE에서 음악을 선택해 주세요.</div>',
                    unsafe_allow_html=True
                )
                if st.button("GO TO ROOM SERVICE", key="go_room_service_empty", use_container_width=True):
                    go_room_service()
            else:
                for index, record in enumerate(st.session_state.room_records):
                    img_col, info_col, action_col = st.columns([1,4,1.5], vertical_alignment="center")
                    with img_col:
                        if record.get("artwork"):
                            st.image(record["artwork"], width=86)
                    with info_col:
                        st.markdown(
                            '<div class="room-record-title">' + escape(record.get("track", "RECORD")) + '</div>'
                            '<div class="room-record-meta">' + escape(record.get("artist", "")) + '<br>' + escape(record.get("album", "")) + '</div>',
                            unsafe_allow_html=True
                        )
                    with action_col:
                        if st.button("PLAY ON LP", key=f"cabinet_play_{index}_{record.get('track_id')}", use_container_width=True):
                            st.session_state.current_record = record
                            st.rerun()
                        if st.button("RETURN", key=f"cabinet_return_{index}_{record.get('track_id')}", use_container_width=True):
                            remove_from_room(record.get("track_id"))
                            st.rerun()
                    st.markdown('<div style="height:1px;background:rgba(199,157,109,0.10);margin:8px 0 16px 0;"></div>', unsafe_allow_html=True)

            st.markdown('<div style="height:25px;"></div>', unsafe_allow_html=True)
            nav_left, nav_center, nav_right = st.columns([1,2,1])
            with nav_center:
                if st.button("← BACK TO FIREPLACE", key="back_to_fireplace", use_container_width=True):
                    st.session_state.my_room_view = "fireplace"
                    st.rerun()
            if st.button("← BACK TO ROOM SERVICE", key="my_room_back_lp", use_container_width=True):
                go_room_service()

