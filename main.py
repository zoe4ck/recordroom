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
    min-height: 82vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
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
    margin-bottom: 40px;
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
    width:min(760px,82vw);
    height:390px;
    margin:48px auto 28px;
    position:relative;
    overflow:hidden;
    border:1px solid rgba(215,166,105,.28);
    border-radius:18px;
    background:
        radial-gradient(ellipse at 50% 82%, rgba(255,122,38,.22) 0 12%, transparent 38%),
        linear-gradient(180deg,#17100c 0%,#0d0907 55%,#070504 100%);
    box-shadow:0 25px 70px rgba(0,0,0,.55), inset 0 0 70px rgba(0,0,0,.78);
}
.fireplace:before {
    content:"";
    position:absolute;
    left:50%;
    bottom:42px;
    width:330px;
    height:220px;
    transform:translateX(-50%);
    border-radius:50%;
    background:radial-gradient(ellipse,rgba(255,157,68,.38) 0 12%,rgba(230,83,28,.18) 34%,transparent 72%);
    filter:blur(15px);
    animation:hearthGlow 2.4s ease-in-out infinite alternate;
}
.fireplace:after {
    content:"";
    position:absolute;
    left:50%;
    top:48px;
    width:500px;
    height:280px;
    transform:translateX(-50%);
    border:18px solid #241913;
    border-bottom-width:26px;
    border-radius:50% 50% 10px 10px;
    box-shadow:inset 0 0 0 1px rgba(216,169,111,.12), inset 0 0 30px rgba(0,0,0,.65), 0 8px 25px rgba(0,0,0,.35);
    pointer-events:none;
}
.wood {
    position:absolute;
    z-index:5;
    bottom:52px;
    left:50%;
    width:235px;
    height:25px;
    transform:translateX(-50%) rotate(8deg);
    border-radius:16px;
    background:linear-gradient(180deg,#75452b,#32180f 70%);
    border:1px solid rgba(215,151,88,.25);
    box-shadow:0 5px 8px rgba(0,0,0,.5), inset 0 4px 5px rgba(255,184,104,.1);
}
.wood.two { transform:translateX(-50%) rotate(-9deg); bottom:61px; }
.wood:after {
    content:"";
    position:absolute;
    right:7px;
    top:4px;
    width:14px;
    height:14px;
    border-radius:50%;
    border:2px solid rgba(40,18,10,.5);
}
.fire {
    position:absolute;
    z-index:4;
    left:50%;
    bottom:67px;
    width:160px;
    height:205px;
    transform:translateX(-50%);
    background:radial-gradient(ellipse at 50% 86%,#fff4c4 0 7%,#ffc65d 18%,#f47a2c 43%,rgba(177,52,20,.5) 62%,transparent 76%);
    clip-path:polygon(50% 0,61% 22%,55% 37%,78% 27%,70% 49%,94% 45%,77% 73%,63% 100%,37% 100%,20% 74%,6% 48%,29% 54%,22% 28%,44% 40%);
    filter:blur(.35px);
    animation:flame 1.25s ease-in-out infinite alternate;
    transform-origin:50% 100%;
}
.fire-small {
    position:absolute;
    z-index:6;
    left:50%;
    bottom:72px;
    width:82px;
    height:145px;
    transform:translateX(-50%);
    background:radial-gradient(ellipse at 50% 84%,#fffdf0 0 11%,#ffe27f 25%,#ff9636 55%,transparent 75%);
    clip-path:polygon(50% 0,66% 29%,59% 46%,79% 38%,68% 67%,55% 100%,43% 100%,28% 68%,18% 48%,40% 54%,33% 31%);
    animation:flameSmall .82s ease-in-out infinite alternate;
}
.fire-core {
    position:absolute;
    z-index:7;
    left:50%;
    bottom:74px;
    width:40px;
    height:91px;
    transform:translateX(-50%);
    background:linear-gradient(180deg,#fffef0,#ffe99a 52%,#ffb34d);
    clip-path:polygon(50% 0,72% 35%,64% 56%,82% 51%,63% 100%,39% 100%,22% 61%,42% 55%,32% 32%);
    animation:flameCore .65s ease-in-out infinite alternate;
}
.ember {
    position:absolute;
    z-index:8;
    width:4px;
    height:4px;
    border-radius:50%;
    background:#ffc16c;
    box-shadow:0 0 10px rgba(255,118,39,.95);
    animation:ember 2.8s infinite ease-out;
}
.ember.e1{left:43%;bottom:115px}.ember.e2{left:58%;bottom:125px;animation-delay:.8s}.ember.e3{left:48%;bottom:145px;animation-delay:1.4s}.ember.e4{left:63%;bottom:95px;animation-delay:2s}
@keyframes hearthGlow{from{opacity:.72;transform:translateX(-50%) scale(.94)}to{opacity:1;transform:translateX(-50%) scale(1.08)}}
@keyframes flameCore{from{transform:translateX(-50%) scale(.92,.96)}to{transform:translateX(-50%) scale(1.05,1.08)}}
@keyframes ember{0%{opacity:0;transform:translateY(10px) scale(.6)}25%{opacity:1}100%{opacity:0;transform:translateY(-90px) translateX(15px) scale(.15)}}
@keyframes flame{from{transform:translateX(-50%) scaleY(.94) rotate(-2deg)}to{transform:translateX(-50%) scaleY(1.08) rotate(2deg)}}
@keyframes flameSmall{from{transform:translateX(-50%) scaleY(.9)}to{transform:translateX(-50%) scaleY(1.08)}}

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
    margin: 50px auto 0 auto;
    padding: 42px 48px;
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
    margin: 10px 0 30px 0;
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
    padding: 48px 0 28px;
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
    line-height:1.05;
    margin-top:8px;
}
.cocktail-subtitle {
    color:#96765d;
    font-family:"Noto Serif KR",serif;
    font-size:14px;
    line-height:1.9;
    margin:12px auto 0;
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
    width:300px;
    height:174px;
    margin:8px auto 0;
    position:relative;
    overflow:visible;
}
/* 메뉴 미리보기와 실제 음료가 완전히 같은 그래픽을 사용하도록 합니다. */
.mini-drink .drink-visual {
    width:300px;
    height:430px;
    transform:scale(.40);
    transform-origin:top center;
}

.mini-drink .mini-rim,
.mini-drink .mini-stem,
.mini-drink .mini-base,
.mini-drink .mini-glass,
.mini-drink .mini-liquid,
.mini-drink .mini-scoop,
.mini-drink .mini-cherry,
.mini-drink .mini-straw,
.mini-drink .mini-orange-half,
.mini-drink .mini-leaf,
.mini-drink .mini-cocktail-olive,
.mini-drink .mini-pick,
.mini-drink .mini-blue-glow,
.mini-drink .mini-lemon-twist,
.mini-drink .mini-star,
.mini-drink .mini-bubbles { display:none; }

.selected-order {
    width:min(900px,92vw);
    margin:0 auto 14px;
}
.drink-visual {
    position:relative;
    width:300px;
    height:430px;
    display:flex;
    align-items:center;
    justify-content:center;
    margin:0 auto;
}
.glass {
    position:relative;
    width:190px;
    height:270px;
    margin-top:22px;
    border:1.5px solid rgba(236,223,204,.62);
    border-top:0;
    border-radius:10px 10px 52px 52px;
    overflow:hidden;
    isolation:isolate;
    background:linear-gradient(105deg,rgba(255,255,255,.14),rgba(255,255,255,.025) 35%,rgba(255,255,255,.08));
    box-shadow:0 24px 55px rgba(0,0,0,.36), inset 8px 0 18px rgba(255,255,255,.055), inset -8px 0 15px rgba(0,0,0,.10);
}
.glass .liquid {
    position:absolute;
    left:0; right:0; bottom:0;
    border-radius:0 0 48px 48px;
    transition:height .42s ease;
    opacity:.92;
    overflow:hidden;
}
.glass .liquid:after {
    content:"";
    position:absolute;
    inset:0;
    background:radial-gradient(circle at 25% 28%,rgba(255,255,255,.28) 0 1px,transparent 2px),radial-gradient(circle at 68% 46%,rgba(255,255,255,.20) 0 1px,transparent 2px);
    opacity:.65;
}
.glass-shine {
    position:absolute;
    z-index:20;
    top:28px;
    left:24px;
    width:15px;
    height:185px;
    border-radius:50%;
    background:linear-gradient(180deg,rgba(255,255,255,.22),rgba(255,255,255,0));
    filter:blur(1px);
    pointer-events:none;
}
.glass-rim {
    position:absolute;
    z-index:30;
    left:-1px; right:-1px; top:-1px;
    height:18px;
    border:1.5px solid rgba(240,229,214,.65);
    border-radius:50%;
    background:rgba(255,255,255,.035);
}
.glass-foot {
    position:absolute;
    left:50%; bottom:27px;
    width:3px; height:48px;
    transform:translateX(-50%);
    background:rgba(226,208,178,.55);
}
.glass-base {
    position:absolute;
    left:50%; bottom:17px;
    width:112px; height:10px;
    transform:translateX(-50%);
    border:1.5px solid rgba(226,208,178,.55);
    border-radius:50%;
}

/* GREEN MELON SODA — 실제 카페의 투명한 하이볼 느낌 */
.drink-scene.green .glass {
    width:166px;
    height:286px;
    border-radius:9px 9px 44px 44px;
    background:linear-gradient(105deg,rgba(255,255,255,.18),rgba(255,255,255,.025) 40%,rgba(255,255,255,.10));
}
.drink-scene.green .liquid { background:linear-gradient(180deg,#b9ef9b 0%,#67cf72 35%,#31a75a 100%); }
.drink-scene.green .glass-foot { bottom:29px; }
.drink-scene.green .glass-base { bottom:18px; }
.melon-ice-cream {
    position:absolute; z-index:25; top:14px; left:50%;
    width:76px; height:47px; transform:translateX(-50%);
    border-radius:50%;
    background:radial-gradient(circle at 34% 24%,#fffef8,#fff3d5 58%,#d9c49b 100%);
    box-shadow:0 4px 12px rgba(0,0,0,.28);
}
.drink-straw {
    position:absolute; z-index:26; top:10px; left:60%;
    width:4px; height:70px; border-radius:4px;
    background:linear-gradient(#f0a0a8,#dc6078);
    transform:rotate(11deg); transform-origin:bottom;
}
.drink-cherry {
    position:absolute; z-index:27; top:23px; left:34%;
    width:17px; height:17px; border-radius:50%;
    background:radial-gradient(circle at 30% 25%,#ef8089,#a72c44 65%,#671a2b);
}
.bubbles { position:absolute; z-index:15; inset:0; pointer-events:none; }
.bubbles span { position:absolute; border-radius:50%; background:rgba(255,255,255,.40); box-shadow:0 0 8px rgba(255,255,255,.22); }
.bubbles .b1{width:6px;height:6px;left:25%;top:37%}.bubbles .b2{width:4px;height:4px;left:42%;top:27%}.bubbles .b3{width:7px;height:7px;left:62%;top:45%}.bubbles .b4{width:4px;height:4px;left:72%;top:32%}.bubbles .b5{width:3px;height:3px;left:53%;top:58%}

/* ORANGE JUICE — 둥근 주스 글라스 + 컵 안쪽 반달 오렌지 */
.drink-scene.orange .glass {
    width:214px; height:230px; margin-top:40px;
    border-radius:13px 13px 64px 64px;
}
.drink-scene.orange .liquid { background:linear-gradient(180deg,#ffd77d 0%,#ffad37 42%,#ef7118 100%); }
.orange-half {
    position:absolute; z-index:25;
    width:66px; height:38px;
    border-radius:66px 66px 0 0;
    background:radial-gradient(circle at 50% 100%,#fff0b4 0 31%,#ffb84b 34% 70%,#ec701b 72% 100%);
    box-shadow:0 4px 10px rgba(0,0,0,.22);
}
.orange-half:after {
    content:""; position:absolute; left:50%; bottom:4px; width:2px; height:28px;
    background:rgba(255,239,186,.75); transform:translateX(-50%) rotate(25deg);
}
.orange-half.one { right:26px; top:22px; transform:rotate(12deg); }
.orange-half.two { left:26px; top:38px; width:50px; height:29px; transform:rotate(-15deg); }

/* PINK COCKTAIL — 깔끔한 마티니 잔 */
.drink-scene.pink .glass {
    width:226px; height:172px; margin-top:55px;
    border-radius:0 0 112px 112px;
    transform:perspective(220px) rotateX(-2deg);
}
.drink-scene.pink .liquid { background:linear-gradient(180deg,#f7c2d0 0%,#dc809e 45%,#ad4c73 100%); }
.drink-scene.pink .glass-foot { bottom:27px; }
.drink-scene.pink .glass-base { bottom:17px; }
.pink-foam {
    position:absolute; z-index:25; left:18%; right:18%; top:10px; height:20px;
    border-radius:50%; background:radial-gradient(circle at 35% 30%,#fff8fa,#f5c6d4 58%,#d77d9d 100%);
}
.pink-cherry {
    position:absolute; z-index:26; left:48%; top:13px;
    width:13px; height:13px; border-radius:50%;
    background:radial-gradient(circle at 30% 25%,#ef7e88,#a52d45 65%,#681a2b);
}

/* NAVY COCKTAIL — 낮은 쿠페 잔 */
.drink-scene.navy .glass {
    width:230px; height:205px; margin-top:43px;
    border-radius:12px 12px 52px 52px;
}
.drink-scene.navy .liquid { background:linear-gradient(180deg,#6e8fce 0%,#405b9d 42%,#1d2858 100%); }
.navy-garnish {
    position:absolute; z-index:25; left:50%; top:16px;
    width:52px; height:18px; transform:translateX(-50%) rotate(-7deg);
    border-radius:50%; background:linear-gradient(90deg,#f4dfa2,#e7b85d);
    box-shadow:0 4px 10px rgba(0,0,0,.2);
}
.stars { position:absolute; inset:0; z-index:16; pointer-events:none; }
.stars span { position:absolute; color:rgba(226,235,255,.70); font-size:13px; text-shadow:0 0 10px rgba(150,180,255,.75); }
.stars .s1{top:56px;left:30px}.stars .s2{top:90px;right:42px;font-size:10px}.stars .s3{bottom:45px;left:58px;font-size:9px}

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
    .cocktail-header { padding-top:30px; }
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
</style>
"""

try:
    st.html(CSS)
except Exception:
    st.markdown(CSS, unsafe_allow_html=True)

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
        "label": "슬퍼요",
        "drink": "PINK COCKTAIL",
        "color": "pink",
        "description": "조금 천천히, 감정을 그대로 두는 밤",
        "fallback": ["Korean sad ballad", "Korean emotional R&B", "IU ballad", "Korean indie melancholy"],
    },
    "refresh": {
        "label": "기분전환이 필요해요",
        "drink": "GREEN MELON SODA",
        "color": "green",
        "description": "답답한 기분을 조금 가볍게 바꾸는 시간",
        "fallback": ["K-pop refreshing", "Korean upbeat pop", "Korean pop summer", "K-pop bright"],
    },
    "excited": {
        "label": "신나요",
        "drink": "ORANGE JUICE",
        "color": "orange",
        "description": "지금의 텐션을 그대로 이어가는 밤",
        "fallback": ["K-pop dance", "Korean hip hop", "K-pop party", "Korean upbeat R&B"],
    },
    "quiet": {
        "label": "조용한 게 좋아요",
        "drink": "NAVY COCKTAIL",
        "color": "navy",
        "description": "말없이 음악만 곁에 두고 싶은 밤",
        "fallback": ["Korean indie acoustic", "Korean chill R&B", "Korean lo-fi", "Korean soft pop"],
    },
}


def cocktail_visual_html(color, fill=100, mini=False):
    """실제 음료와 메뉴 미리보기가 같은 HTML 그래픽을 사용하도록 합니다."""
    height = max(0, min(100, fill))
    eaten = height < 100

    if color == "green":
        garnish = ""
        if not eaten:
            garnish = (
                '<div class="melon-ice-cream"></div>'
                '<div class="drink-straw"></div>'
                '<div class="drink-cherry"></div>'
            )
        common = (
            f'<div class="glass soda-glass">'
            f'<div class="liquid" style="height:{height}%;"></div>'
            f'<div class="glass-rim"></div>'
            f'<div class="bubbles"><span class="b1"></span><span class="b2"></span><span class="b3"></span><span class="b4"></span><span class="b5"></span></div>'
            f'{garnish}'
            f'<div class="glass-shine"></div>'
            f'</div><div class="glass-foot"></div><div class="glass-base"></div>'
        )
    elif color == "orange":
        garnish = ""
        if not eaten:
            garnish = '<div class="orange-half one"></div><div class="orange-half two"></div>'
        common = (
            f'<div class="glass orange-glass">'
            f'<div class="liquid" style="height:{height}%;"></div>'
            f'<div class="glass-rim"></div>{garnish}'
            f'<div class="glass-shine"></div></div>'
        )
    elif color == "pink":
        garnish = '<div class="pink-foam"></div><div class="pink-cherry"></div>' if not eaten else ''
        common = (
            f'<div class="glass pink-glass">'
            f'<div class="liquid" style="height:{height}%;"></div>'
            f'<div class="glass-rim"></div>{garnish}'
            f'<div class="glass-shine"></div></div>'
            f'<div class="glass-foot"></div><div class="glass-base"></div>'
        )
    else:
        garnish = '<div class="navy-garnish"></div>' if not eaten else ''
        common = (
            f'<div class="glass navy-glass">'
            f'<div class="liquid" style="height:{height}%;"></div>'
            f'<div class="glass-rim"></div>{garnish}'
            f'<div class="stars"><span class="s1">✦</span><span class="s2">✧</span><span class="s3">✦</span></div>'
            f'<div class="glass-shine"></div></div>'
        )

    if mini:
        return f'<div class="mini-drink"><div class="drink-visual drink-scene {color}">{common}</div></div>'

    return f'<div class="drink-visual drink-scene {color}">{common}</div>'


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

    return config["fallback"], False


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
            if len(results) >= 12:
                break
        if len(results) >= 12:
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
            if len(results) >= 12:
                break
        if len(results) >= 12:
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
        '<div class="fire-small"></div><div class="fire-core"></div><i class="ember e1"></i><i class="ember e2"></i><i class="ember e3"></i><i class="ember e4"></i>'
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
                    if st.button("ORDER THIS", key=f"order_mood_{key}", use_container_width=True):
                        st.session_state.cocktail_mood = key
                        st.session_state.cocktail_sips = 0
                        st.session_state.cocktail_recommendations = []
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

            # 추천은 음료를 고르는 즉시 불러오고, 화면 오른쪽에 고정해서 보여줍니다.
            if not st.session_state.cocktail_recommendations:
                with st.spinner("CONCIERGE IS CHOOSING RECORDS..."):
                    recs, used_ai = get_ai_recommendations(mood_key)
                st.session_state.cocktail_recommendations = recs
                st.session_state.cocktail_ai_used = used_ai

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

                st.markdown(
                    '<div class="recommendation-title">TONIGHT\'S RECORDS</div>',
                    unsafe_allow_html=True
                )
                if st.session_state.get("cocktail_ai_used", False):
                    st.markdown('<div class="ai-note">AI CONCIERGE · MOOD MATCHED · KOREA POPULAR FIRST</div>', unsafe_allow_html=True)
                else:
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
                else:
                    st.markdown(
                        '<div class="no-result" style="margin-top:20px;">'
                        '오늘 밤에 맞는 레코드를 찾지 못했어요.<br>'
                        '다시 주문하면 다른 메뉴를 찾아볼게요.'
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

