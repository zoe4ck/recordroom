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
    page_title="record room",
    page_icon="♫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CSS
# =========================================================

CSS = """"
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

@st.cache_resource
def get_supabase():
    if create_client is None:
        return None
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
    except Exception:
        return None
    try:
        return create_client(url, key)
    except Exception:
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
    "current_record": None,
    "room_records": [],
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
    st.rerun()

def go_room_service():
    st.session_state.page = "choice"
    st.session_state.choice_mode = None
    st.session_state.room_service_step = "search"
    st.rerun()

def go_my_room():
    st.session_state.page = "my_room"
    st.rerun()

# =========================================================
# AUTH
# =========================================================

def login_user(email, password):
    if supabase is None:
        return False, "Supabase 연결을 확인해 주세요."
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
        message = str(e)
        if "Invalid login credentials" in message:
            return False, "이메일 또는 비밀번호가 올바르지 않습니다."
        return False, "로그인에 실패했습니다. 이메일과 비밀번호를 확인해 주세요."

def signup_user(email, password):
    if supabase is None:
        return False, "Supabase 연결을 확인해 주세요."
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        user = getattr(response, "user", None)
        if user is None:
            return False, "회원가입에 실패했습니다."
        session = getattr(response, "session", None)
        if session is not None:
            st.session_state.logged_in = True
            st.session_state.current_user = user
            return True, "CHECK-IN 완료"
        return True, "회원가입이 완료되었습니다. 이메일 인증 후 CHECK-IN 해주세요."
    except Exception as e:
        message = str(e).strip()
        lower_message = message.lower()

        if "already registered" in lower_message or "user already registered" in lower_message:
            return False, "이미 가입된 이메일입니다."

        if "email signups are disabled" in lower_message:
            return False, "Supabase에서 이메일 회원가입이 비활성화되어 있습니다. Authentication → Providers → Email에서 활성화해 주세요."

        if "invalid api key" in lower_message or "apikey" in lower_message and "invalid" in lower_message:
            return False, "Supabase API KEY가 올바르지 않습니다. Streamlit Secrets의 SUPABASE_KEY를 확인해 주세요."

        if "rate limit" in lower_message:
            return False, f"이메일 발송 제한에 걸렸습니다. 잠시 후 다시 시도해 주세요.\n\n상세 오류: {message}"

        # 원래는 실제 Supabase 오류를 숨겨서 원인을 알 수 없었기 때문에,
        # 이제는 정확한 오류 내용을 화면에 표시합니다.
        return False, f"회원가입 오류: {message}"

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
        '<div class="sidebar-title">MYSTERY HOTEL</div>',
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

def normalize(text):
    if not text:
        return ""
    return re.sub(r"[^0-9a-z가-힣]", "", text.lower())

# =========================================================
# ARTIST ALIASES
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
    "르세라핌": ["LE SSERAFIM"],
    "le sserafim": ["르세라핌"],
}

# =========================================================
# ARTIST SEARCH
# =========================================================

@st.cache_data(ttl=600, show_spinner=False)
def find_artist_tracks(query):
    query = query.strip()
    if not query:
        return []

    nq = normalize(query)
    search_terms = [query]

    for alias in ARTIST_ALIASES.get(query.lower(), []):
        if alias not in search_terms:
            search_terms.append(alias)

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

    exact = [
        artist for artist in candidates
        if normalize(artist.get("artistName", "")) == nq
    ]

    if exact:
        selected = exact[0]
    else:
        selected = None

        for alias in search_terms[1:]:
            alias_normalized = normalize(alias)
            alias_exact = [
                artist for artist in candidates
                if normalize(artist.get("artistName", "")) == alias_normalized
            ]
            if alias_exact:
                selected = alias_exact[0]
                break

        if selected is None:
            contains = [
                artist for artist in candidates
                if nq in normalize(artist.get("artistName", ""))
            ]
            if contains:
                selected = contains[0]

        if selected is None:
            for alias in search_terms[1:]:
                alias_normalized = normalize(alias)
                contains = [
                    artist for artist in candidates
                    if alias_normalized in normalize(artist.get("artistName", ""))
                ]
                if contains:
                    selected = contains[0]
                    break

    if selected is None:
        return []

    artist_id = selected.get("artistId")
    if not artist_id:
        return []

    for country in ["KR", "US"]:
        data = apple_lookup({
            "id": artist_id,
            "entity": "song",
            "country": country,
            "limit": 100
        })

        tracks = [
            item for item in data.get("results", [])
            if item.get("wrapperType") == "track"
            and item.get("kind") == "song"
        ]

        if tracks:
            return tracks

    return []

# =========================================================
# SONG SEARCH
# =========================================================

@st.cache_data(ttl=600, show_spinner=False)
def find_song(query):
    query = query.strip()
    if not query:
        return []

    nq = normalize(query)
    all_results = []

    for country in ["KR", "US"]:
        data = apple_search({
            "term": query,
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

            if track_id and any(
                x.get("trackId") == track_id
                for x in all_results
            ):
                continue

            all_results.append(result)

    if not all_results:
        return []

    exact = [
        result for result in all_results
        if normalize(result.get("trackName", "")) == nq
    ]

    if exact:
        return exact

    partial = [
        result for result in all_results
        if nq in normalize(result.get("trackName", ""))
    ]

    return partial[:30]

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
    artwork = escape(record.get("artwork", ""))
    preview = escape(record.get("preview", ""))

    player_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* {{ box-sizing: border-box; }}
body {{
    margin: 0;
    background: transparent;
    color: #d8ad79;
    font-family: Georgia, serif;
    overflow: hidden;
}}
.wrap {{
    min-height: 540px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}}
.hint {{
    color: #a98a70;
    font-size: 13px;
    letter-spacing: 1.5px;
    margin-bottom: 24px;
    text-align: center;
}}
.record {{
    width: 360px;
    height: 360px;
    border-radius: 50%;
    position: relative;
    cursor: pointer;
    user-select: none;
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
}}
.record.playing {{
    animation: spin 2.6s linear infinite;
}}
.record:before {{
    content: "";
    position: absolute;
    inset: 28px;
    border-radius: 50%;
    border: 1px solid rgba(255,255,255,0.06);
}}
.label {{
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    width: 132px;
    height: 132px;
    border-radius: 50%;
    overflow: hidden;
    background:
        radial-gradient(
            circle,
            #b98555 0%,
            #8f5e3b 48%,
            #6c412a 100%
        );
    box-shadow: 0 0 15px rgba(0,0,0,0.45);
}}
.label img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}}
.hole {{
    position: absolute;
    width: 12px;
    height: 12px;
    background: #17110e;
    border-radius: 50%;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
}}
.info {{
    margin-top: 20px;
    text-align: center;
}}
.title {{
    color: #e0bd91;
    font-size: 23px;
    letter-spacing: 2px;
}}
.artist {{
    color: #a98a70;
    font-size: 14px;
    margin-top: 6px;
}}
.state {{
    color: #c49a70;
    font-size: 12px;
    letter-spacing: 2px;
    margin-top: 12px;
}}
audio {{ display: none; }}
@keyframes spin {{
    from {{ transform: rotate(0deg); }}
    to {{ transform: rotate(360deg); }}
}}
</style>
</head>
<body>
<div class="wrap">
    <div class="hint">CLICK ONCE · PLAY &nbsp;&nbsp; DOUBLE CLICK · STOP</div>

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

    <audio id="audio" preload="metadata">
        <source src="{preview}" type="audio/mpeg">
    </audio>
</div>

<script>
const record = document.getElementById("record");
const audio = document.getElementById("audio");
const state = document.getElementById("state");
let clickTimer = null;

function playRecord() {{
    if (!audio.src) return;

    audio.play().then(() => {{
        record.classList.add("playing");
        state.textContent = "PLAYING";
    }}).catch(() => {{
        state.textContent = "PRESS AGAIN TO PLAY";
    }});
}}

function stopRecord() {{
    audio.pause();
    audio.currentTime = 0;
    record.classList.remove("playing");
    state.textContent = "STOPPED";
}}

record.addEventListener("click", () => {{
    if (clickTimer) clearTimeout(clickTimer);

    clickTimer = setTimeout(() => {{
        if (audio.paused) {{
            playRecord();
        }} else {{
            audio.pause();
            record.classList.remove("playing");
            state.textContent = "PAUSED";
        }}
        clickTimer = null;
    }}, 230);
}});

record.addEventListener("dblclick", (event) => {{
    event.preventDefault();

    if (clickTimer) {{
        clearTimeout(clickTimer);
        clickTimer = null;
    }}

    stopRecord();
}});

audio.addEventListener("ended", () => {{
    record.classList.remove("playing");
    state.textContent = "FINISHED";
}});
</script>
</body>
</html>
"""

    components.html(player_html, height=580, scrolling=False)

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
            '<div class="welcome-title">MYSTERY HOTEL</div>'
            '<div class="welcome-line"></div>'
            '<div class="welcome-description">'
            '음악을 듣고, 발견하고, 잠시 머무는 작은 방'
            '</div></div>',
            unsafe_allow_html=True
        )

        left, center, right = st.columns([2, 1, 2])

        with center:
            if st.button(
                "ENTER HOTEL",
                key="enter_room",
                use_container_width=True
            ):
                st.session_state.main_entered = True
                st.rerun()

    else:

        letter_html = (
            '<div class="letter-wrap">'
            '<div class="letter-paper">'
            '<div class="letter-date">SEPTEMBER 28, 2026</div>'
            '<div class="letter-title">DEAR, GUEST</div>'
            '<div class="letter-body">'
            '이곳에는 조금 오래 머물러도 괜찮습니다.'
            '<br><br>'
            '누군가에게는 스쳐 지나갈 한 곡이, '
            '누군가에게는 오래 기억될 밤이 되기도 하니까요.'
            '<br><br>'
            '이 호텔에서는 당신이 원하는 음악을 찾아 '
            '객실로 가져갈 수 있습니다.'
            '<br><br>'
            '그리고 음악이 필요한 밤에는, '
            '당신만의 방에서 조용히 음악을 틀어보세요.'
            '<br><br>'
            '문은 이미 열려 있습니다.'
            '</div>'
            '<div class="letter-sign">— MYSTERY HOTEL</div>'
            '</div>'
            '</div>'
        )

        st.markdown(letter_html, unsafe_allow_html=True)

        if st.button(
            "← BACK TO LOBBY",
            key="back_main_letter"
        ):
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
            '<div class="section-subtitle">'
            '오늘 밤 객실로 가져갈 음악을 골라보세요.'
            '</div></div>',
            unsafe_allow_html=True
        )

        left, right = st.columns(2, gap="large")

        with left:
            if st.button(
                "노래 듣기",
                key="listen_choice",
                use_container_width=True
            ):
                st.session_state.choice_mode = "listen"
                st.session_state.room_service_step = "search"
                st.rerun()

        with right:
            if st.button(
                "추천받기",
                key="recommend_choice",
                use_container_width=True
            ):
                st.session_state.choice_mode = "recommend"
                st.rerun()

        st.markdown(
            '<div style="text-align:center;color:#76563e;'
            'font-family:Georgia,serif;margin-top:35px;letter-spacing:2px;">'
            'ROOM SERVICE · OPEN ALL NIGHT</div>',
            unsafe_allow_html=True
        )

    elif st.session_state.choice_mode == "listen":

        st.markdown(
            '<div class="room-service-container">'
            '<div class="room-service-title">ROOM SERVICE</div>'
            '<div class="room-service-subtitle">'
            '객실로 가져갈 음악을 검색하세요. 선택한 음악은 MY ROOM의 LP로 이동합니다.'
            '</div></div>',
            unsafe_allow_html=True
        )

        if st.button(
            "← BACK TO ROOM SERVICE",
            key="room_service_back_top",
            use_container_width=True
        ):
            st.session_state.choice_mode = None
            st.session_state.search_results = []
            st.session_state.search_text = ""
            st.rerun()

        st.markdown(
            '<div class="listen-search">',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="result-title">FIND A RECORD</div>',
            unsafe_allow_html=True
        )

        search_col, button_col = st.columns([5, 1])

        with search_col:
            query = st.text_input(
                "SEARCH",
                value=st.session_state.search_text,
                placeholder="예: 아이유 / IU / 지코 / ZICO / Love wins all",
                label_visibility="collapsed",
                key="music_search_input"
            )

        with button_col:
            search_clicked = st.button(
                "SEARCH",
                key="music_search_button",
                use_container_width=True
            )

        search_type = st.radio(
            "검색 기준",
            ["자동", "가수", "곡"],
            horizontal=True,
            label_visibility="collapsed"
        )

        type_map = {
            "자동": "auto",
            "가수": "artist",
            "곡": "song"
        }

        if search_clicked:

            if query.strip():

                st.session_state.search_text = query

                with st.spinner("호텔에서 음악을 찾는 중..."):
                    st.session_state.search_results = search_music(
                        query,
                        type_map[search_type]
                    )

                st.rerun()

        if st.session_state.search_text:
            display_results(st.session_state.search_results)

        st.markdown('</div>', unsafe_allow_html=True)

    else:

        st.markdown(
            '<div class="section-area">'
            '<div class="section-title">RECOMMEND</div>'
            '<div class="section-subtitle">'
            '당신에게 맞는 음악을 찾는 공간입니다.'
            '</div>'
            '<div style="color:#8f7059;font-family:Georgia,serif;margin-top:20px;">'
            'COMING SOON</div></div>',
            unsafe_allow_html=True
        )

        if st.button(
            "← BACK TO ROOM SERVICE",
            key="recommend_back",
            use_container_width=True
        ):
            st.session_state.choice_mode = None
            st.rerun()

# =========================================================
# MY ROOM
# =========================================================

elif st.session_state.page == "my_room":

    if not st.session_state.logged_in:

        st.markdown(
            '<div class="section-area">'
            '<div class="section-title">MY ROOM</div>'
            '<div class="section-subtitle">'
            'YOUR PRIVATE ROOM · CHECK-IN REQUIRED'
            '</div></div>',
            unsafe_allow_html=True
        )

        if supabase is None:
            st.error(
                "Supabase 연결이 되지 않았습니다. "
                "Streamlit Cloud의 Secrets에 SUPABASE_URL과 SUPABASE_KEY가 있는지 확인해 주세요."
            )

        st.markdown(
            '<div class="auth-box">'
            '<div class="auth-title">CHECK-IN</div>'
            '<div class="auth-subtitle">'
            '객실에 들어가려면 ROOM KEY가 필요합니다.'
            '</div></div>',
            unsafe_allow_html=True
        )

        auth_left, auth_right = st.columns(2)

        with auth_left:
            if st.button(
                "CHECK-IN",
                key="auth_login_tab",
                use_container_width=True
            ):
                st.session_state.auth_mode = "login"
                st.rerun()

        with auth_right:
            if st.button(
                "NEW GUEST",
                key="auth_signup_tab",
                use_container_width=True
            ):
                st.session_state.auth_mode = "signup"
                st.rerun()

        email = st.text_input(
            "EMAIL",
            placeholder="guest@example.com",
            key="auth_email"
        )

        password = st.text_input(
            "ROOM KEY",
            type="password",
            placeholder="비밀번호",
            key="auth_password"
        )

        if st.session_state.auth_mode == "signup":
            password_confirm = st.text_input(
                "ROOM KEY AGAIN",
                type="password",
                placeholder="비밀번호를 다시 입력하세요",
                key="auth_password_confirm"
            )
        else:
            password_confirm = ""

        if st.session_state.auth_mode == "login":

            if st.button(
                "ENTER MY ROOM",
                key="login_submit",
                use_container_width=True
            ):

                if not email.strip() or not password:
                    st.warning("이메일과 비밀번호를 입력해 주세요.")
                else:
                    ok, message = login_user(
                        email.strip(),
                        password
                    )

                    if ok:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)

        else:

            if st.button(
                "CREATE ROOM KEY",
                key="signup_submit",
                use_container_width=True
            ):

                if not email.strip() or not password:
                    st.warning("이메일과 비밀번호를 입력해 주세요.")

                elif password != password_confirm:
                    st.warning("두 비밀번호가 일치하지 않습니다.")

                elif len(password) < 6:
                    st.warning("비밀번호는 6자 이상으로 입력해 주세요.")

                else:
                    ok, message = signup_user(
                        email.strip(),
                        password
                    )

                    if ok:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)

        st.write("")

        if st.button(
            "← BACK TO LOBBY",
            key="my_room_back_login",
            use_container_width=True
        ):
            st.session_state.page = "main"
            st.rerun()

    else:

        user_email = ""

        if st.session_state.current_user is not None:
            user_email = getattr(
                st.session_state.current_user,
                "email",
                ""
            ) or ""

        st.markdown(
            '<div class="room-service-container">'
            '<div class="room-service-title">MY ROOM</div>'
            '<div class="room-service-subtitle">'
            'GUEST PRIVATE ROOM'
            '</div></div>',
            unsafe_allow_html=True
        )

        top_left, top_mid, top_right = st.columns([2, 3, 2])

        with top_left:
            st.caption("CHECKED IN")

        with top_mid:
            if user_email:
                st.markdown(
                    '<div style="text-align:center;color:#a98a70;'
                    'font-family:Georgia,serif;letter-spacing:1px;">'
                    + escape(user_email)
                    + '</div>',
                    unsafe_allow_html=True
                )

        with top_right:
            if st.button(
                "CHECK-OUT",
                key="logout_button",
                use_container_width=True
            ):
                logout_user()

        st.markdown(
            '<div class="room-tabs">PLAY YOUR RECORD</div>',
            unsafe_allow_html=True
        )

        render_lp_player(st.session_state.current_record)

        st.markdown(
            '<div class="room-tabs">RECORD CABINET</div>',
            unsafe_allow_html=True
        )

        if not st.session_state.room_records:

            st.markdown(
                '<div class="room-record-empty">'
                '아직 객실로 가져온 음악이 없습니다.<br>'
                'ROOM SERVICE에서 음악을 선택해 주세요.'
                '</div>',
                unsafe_allow_html=True
            )

            if st.button(
                "GO TO ROOM SERVICE",
                key="go_room_service_empty",
                use_container_width=True
            ):
                go_room_service()

        else:

            for index, record in enumerate(
                st.session_state.room_records
            ):

                img_col, info_col, action_col = st.columns(
                    [1, 4, 1.5],
                    vertical_alignment="center"
                )

                with img_col:
                    if record.get("artwork"):
                        st.image(
                            record["artwork"],
                            width=86
                        )

                with info_col:
                    st.markdown(
                        '<div class="room-record-title">'
                        + escape(record.get("track", "RECORD"))
                        + '</div>'
                        '<div class="room-record-meta">'
                        + escape(record.get("artist", ""))
                        + '<br>'
                        + escape(record.get("album", ""))
                        + '</div>',
                        unsafe_allow_html=True
                    )

                with action_col:

                    if st.button(
                        "PLAY ON LP",
                        key=f"cabinet_play_{index}_{record.get('track_id')}",
                        use_container_width=True
                    ):
                        st.session_state.current_record = record
                        st.rerun()

                    if st.button(
                        "RETURN",
                        key=f"cabinet_return_{index}_{record.get('track_id')}",
                        use_container_width=True
                    ):
                        remove_from_room(record.get("track_id"))
                        st.rerun()

                st.markdown(
                    '<div style="height:1px;background:rgba(199,157,109,0.10);'
                    'margin:8px 0 16px 0;"></div>',
                    unsafe_allow_html=True
                )

        st.markdown(
            '<div style="height:40px;"></div>',
            unsafe_allow_html=True
        )

        # FIREPLACE는 MY ROOM에만 존재
        render_fireplace()

        st.markdown(
            '<div style="height:30px;"></div>',
            unsafe_allow_html=True
        )

        if st.button(
            "← BACK TO ROOM SERVICE",
            key="my_room_back_room_service",
            use_container_width=True
        ):
            go_room_service()
