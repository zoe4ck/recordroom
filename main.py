import streamlit as st
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
"""

try:
    st.html(CSS)
except Exception:
    st.markdown(CSS, unsafe_allow_html=True)


# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "main"

if "main_entered" not in st.session_state:
    st.session_state.main_entered = False

if "choice_mode" not in st.session_state:
    st.session_state.choice_mode = None

if "room_service_step" not in st.session_state:
    st.session_state.room_service_step = "record"

if "search_text" not in st.session_state:
    st.session_state.search_text = ""

if "search_results" not in st.session_state:
    st.session_state.search_results = []


def go(page):

    st.session_state.page = page

    if page != "main":
        st.session_state.main_entered = False

    if page != "choice":
        st.session_state.choice_mode = None

    if page != "choice":
        st.session_state.room_service_step = "record"

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

    if st.button("MY ROOM", key="nav_unknown"):
        go("unknown")


# =========================================================
# APPLE API
# =========================================================

@st.cache_data(ttl=600, show_spinner=False)
def apple_search(params):

    url = (
        "https://itunes.apple.com/search?"
        + urllib.parse.urlencode(params)
    )

    try:

        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "record-room/1.0"
            }
        )

        with urllib.request.urlopen(
            request,
            timeout=12
        ) as response:

            return json.loads(
                response.read().decode("utf-8")
            )

    except Exception:

        return {
            "resultCount": 0,
            "results": []
        }


@st.cache_data(ttl=600, show_spinner=False)
def apple_lookup(params):

    url = (
        "https://itunes.apple.com/lookup?"
        + urllib.parse.urlencode(params)
    )

    try:

        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "record-room/1.0"
            }
        )

        with urllib.request.urlopen(
            request,
            timeout=12
        ) as response:

            return json.loads(
                response.read().decode("utf-8")
            )

    except Exception:

        return {
            "resultCount": 0,
            "results": []
        }


def normalize(text):

    if not text:
        return ""

    return re.sub(
        r"[^0-9a-z가-힣]",
        "",
        text.lower()
    )


# =========================================================
# KOREAN / ENGLISH ARTIST ALIASES
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
    "르세라핌": ["LE SSERAFIM"],
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

    # -----------------------------------------------------
    # 검색할 후보 단어
    # -----------------------------------------------------

    search_terms = [query]

    for alias in ARTIST_ALIASES.get(
        query.lower(),
        []
    ):

        if alias not in search_terms:
            search_terms.append(alias)

    candidates = []

    # -----------------------------------------------------
    # Apple Music Artist 검색
    # -----------------------------------------------------

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

            for artist in data.get(
                "results",
                []
            ):

                artist_id = artist.get(
                    "artistId"
                )

                artist_name = artist.get(
                    "artistName",
                    ""
                )

                if not artist_id or not artist_name:
                    continue

                if not any(
                    x.get("artistId") == artist_id
                    for x in candidates
                ):

                    candidates.append(
                        artist
                    )

    if not candidates:

        # -------------------------------------------------
        # Artist 검색이 안 될 경우
        # Song + artistTerm으로 다시 검색
        # -------------------------------------------------

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

                for song in data.get(
                    "results",
                    []
                ):

                    artist_id = song.get(
                        "artistId"
                    )

                    artist_name = song.get(
                        "artistName",
                        ""
                    )

                    if not artist_id or not artist_name:
                        continue

                    if not any(
                        x.get("artistId") == artist_id
                        for x in candidates
                    ):

                        candidates.append({
                            "artistId": artist_id,
                            "artistName": artist_name
                        })

    if not candidates:
        return []

    # -----------------------------------------------------
    # 1. 정확히 일치
    # -----------------------------------------------------

    exact = [
        artist
        for artist in candidates
        if normalize(
            artist.get(
                "artistName",
                ""
            )
        ) == nq
    ]

    if exact:

        selected = exact[0]

    else:

        # -------------------------------------------------
        # 2. alias와 정확히 일치
        # -------------------------------------------------

        selected = None

        for alias in search_terms[1:]:

            alias_normalized = normalize(
                alias
            )

            alias_exact = [
                artist
                for artist in candidates
                if normalize(
                    artist.get(
                        "artistName",
                        ""
                    )
                ) == alias_normalized
            ]

            if alias_exact:

                selected = alias_exact[0]
                break

        # -------------------------------------------------
        # 3. 부분 일치
        # -------------------------------------------------

        if selected is None:

            contains = [
                artist
                for artist in candidates
                if nq in normalize(
                    artist.get(
                        "artistName",
                        ""
                    )
                )
            ]

            if contains:

                selected = contains[0]

        # -------------------------------------------------
        # 4. alias 부분 일치
        # -------------------------------------------------

        if selected is None:

            for alias in search_terms[1:]:

                alias_normalized = normalize(
                    alias
                )

                contains = [
                    artist
                    for artist in candidates
                    if alias_normalized in normalize(
                        artist.get(
                            "artistName",
                            ""
                        )
                    )
                ]

                if contains:

                    selected = contains[0]
                    break

    if selected is None:
        return []

    # -----------------------------------------------------
    # Artist ID
    # -----------------------------------------------------

    artist_id = selected.get(
        "artistId"
    )

    if not artist_id:
        return []

    # -----------------------------------------------------
    # Artist ID로 실제 곡 목록 조회
    # -----------------------------------------------------

    for country in ["KR", "US"]:

        data = apple_lookup({
            "id": artist_id,
            "entity": "song",
            "country": country,
            "limit": 100
        })

        tracks = [
            item
            for item in data.get(
                "results",
                []
            )
            if item.get(
                "wrapperType"
            ) == "track"
            and item.get(
                "kind"
            ) == "song"
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

        for result in data.get(
            "results",
            []
        ):

            track_name = result.get(
                "trackName",
                ""
            )

            if not track_name:
                continue

            track_id = result.get(
                "trackId"
            )

            if track_id and any(
                x.get(
                    "trackId"
                ) == track_id
                for x in all_results
            ):
                continue

            all_results.append(
                result
            )

    if not all_results:
        return []

    # 정확한 제목
    exact = [
        result
        for result in all_results
        if normalize(
            result.get(
                "trackName",
                ""
            )
        ) == nq
    ]

    if exact:
        return exact

    # 부분 일치
    partial = [
        result
        for result in all_results
        if nq in normalize(
            result.get(
                "trackName",
                ""
            )
        )
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

        return find_artist_tracks(
            query
        )

    if mode == "song":

        return find_song(
            query
        )

    artist_results = find_artist_tracks(
        query
    )

    if artist_results:

        return artist_results

    return find_song(
        query
    )


# =========================================================
# RESULT DISPLAY
# =========================================================

def display_results(results):

    if not results:

        st.markdown(
            '<div class="no-result">검색 결과를 찾지 못했습니다.<br>가수 이름이나 정확한 곡 제목을 다시 입력해 주세요.</div>',
            unsafe_allow_html=True
        )

        return

    st.markdown(
        '<div class="result-title">SEARCH RESULT</div>',
        unsafe_allow_html=True
    )

    for result in results[:30]:

        artwork = result.get(
            "artworkUrl100",
            ""
        )

        track = escape(
            result.get(
                "trackName",
                "제목 없음"
            )
        )

        artist = escape(
            result.get(
                "artistName",
                "아티스트 없음"
            )
        )

        album = escape(
            result.get(
                "collectionName",
                "앨범 정보 없음"
            )
        )

        date = escape(
            (
                result.get(
                    "releaseDate",
                    ""
                )
                or ""
            )[:10]
        )

        apple_url = result.get(
            "trackViewUrl",
            ""
        )

        preview_url = result.get(
            "previewUrl",
            ""
        )

        image_html = ""

        if artwork:

            image_html = (
                '<img src="'
                + escape(artwork)
                + '">'
            )

        link_html = ""

        if apple_url:

            link_html = (
                '<a href="'
                + escape(apple_url)
                + '" target="_blank" '
                'style="color:#c89b6b;text-decoration:none;">'
                'Apple Music ↗'
                '</a>'
            )

        card = (
            '<div class="result-card">'
            + image_html
            + '<div>'
            + '<div class="result-name">'
            + track
            + '</div>'
            + '<div class="result-meta">'
            + artist
            + '<br>'
            + album
            + ' · '
            + date
            + '<br>'
            + link_html
            + '</div>'
            + '</div>'
            + '</div>'
        )

        st.markdown(
            card,
            unsafe_allow_html=True
        )

        if preview_url:

            st.audio(
                preview_url
            )


# =========================================================
# MAIN
# =========================================================

if st.session_state.page == "main":

    # -----------------------------------------------------
    # MAIN 첫 화면
    # -----------------------------------------------------

    if not st.session_state.main_entered:

        st.markdown(
            '<div class="welcome-area"><div class="welcome-small">WELCOME TO</div><div class="welcome-title">MYSTERY HOTEL</div><div class="welcome-line"></div><div class="welcome-description">음악을 듣고, 발견하고, 잠시 머무는 작은 방</div></div>',
            unsafe_allow_html=True
        )

        left, center, right = st.columns(
            [2, 1, 2]
        )

        with center:

            if st.button(
                "ENTER HOTEL",
                key="enter_room",
                use_container_width=True
            ):

                st.session_state.main_entered = True

                st.rerun()

    # -----------------------------------------------------
    # 편지
    # -----------------------------------------------------

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

        st.markdown(
            letter_html,
            unsafe_allow_html=True
        )

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

    # =====================================================
    # 처음 ROOM SERVICE에 들어온 화면
    # =====================================================

    if st.session_state.choice_mode is None:

        st.markdown(
            '<div class="section-area"><div class="section-title">ROOM SERVICE</div><div class="section-subtitle">오늘 밤 객실로 가져갈 음악을 골라보세요.</div></div>',
            unsafe_allow_html=True
        )

        left, right = st.columns(
            2,
            gap="large"
        )

        with left:

            if st.button(
                "노래 듣기",
                key="listen_choice",
                use_container_width=True
            ):

                st.session_state.choice_mode = "listen"
                st.session_state.room_service_step = "record"

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
            '<div style="text-align:center;color:#76563e;font-family:Georgia,serif;margin-top:35px;letter-spacing:2px;">ROOM SERVICE · OPEN ALL NIGHT</div>',
            unsafe_allow_html=True
        )


    # =====================================================
    # 노래 듣기
    # =====================================================

    elif st.session_state.choice_mode == "listen":

        # -------------------------------------------------
        # RECORD PLAYER
        # -------------------------------------------------

        if st.session_state.room_service_step == "record":

            st.markdown(
                '<div class="room-service-container"><div class="room-service-title">RECORD ROOM</div><div class="room-service-subtitle">당신의 객실에서 음악을 재생할 레코드입니다.</div></div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="record-stage"><div class="record-player"><div class="record-label"><div class="record-label-text">RECORD<br>ROOM</div><div class="record-ring"></div><div class="record-hole"></div></div></div></div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="record-caption">Your record is waiting.</div>',
                unsafe_allow_html=True
            )

            st.write("")

            col1, col2 = st.columns(
                [1, 1]
            )

            with col1:

                if st.button(
                    "← BACK",
                    key="record_back",
                    use_container_width=True
                ):

                    st.session_state.choice_mode = None
                    st.session_state.room_service_step = "record"

                    st.rerun()

            with col2:

                if st.button(
                    "NEXT → FIREPLACE",
                    key="record_next",
                    use_container_width=True
                ):

                    st.session_state.room_service_step = "fireplace"

                    st.rerun()

            # ---------------------------------------------
            # 검색
            # ---------------------------------------------

            st.markdown(
                '<div class="listen-search">',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="result-title">FIND A RECORD</div>',
                unsafe_allow_html=True
            )

            search_col, button_col = st.columns(
                [5, 1]
            )

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

                    with st.spinner(
                        "호텔에서 음악을 찾는 중..."
                    ):

                        st.session_state.search_results = search_music(
                            query,
                            type_map[search_type]
                        )

                    st.rerun()

            if st.session_state.search_text:

                display_results(
                    st.session_state.search_results
                )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )


        # -------------------------------------------------
        # FIREPLACE
        # -------------------------------------------------

        else:

            st.markdown(
                '<div class="fireplace-container"><div class="fireplace-title">FIREPLACE</div><div class="fireplace-subtitle">불빛을 바라보며 잠시 쉬어가세요.</div></div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="fireplace"><div class="wood"></div><div class="wood two"></div><div class="fire"></div><div class="fire-small"></div></div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="fireplace-note">이곳에서는 아무것도 하지 않아도 괜찮습니다.<br>불멍을 하거나, 아래의 소리를 틀어두고 천천히 쉬어가세요.</div>',
                unsafe_allow_html=True
            )

            st.write("")

            sound_col1, sound_col2, sound_col3 = st.columns(
                3
            )

            with sound_col1:

                st.markdown(
                    '<div style="text-align:center;color:#c49a70;font-family:Georgia,serif;letter-spacing:2px;margin-bottom:10px;">FIREPLACE</div>',
                    unsafe_allow_html=True
                )

                # 외부 오디오 URL이 필요하므로
                # 실제 백색소음 파일은 다음 단계에서 연결
                st.caption(
                    "🔥 벽난로 소리는 다음 단계에서 연결할 수 있어요."
                )

            with sound_col2:

                st.markdown(
                    '<div style="text-align:center;color:#c49a70;font-family:Georgia,serif;letter-spacing:2px;margin-bottom:10px;">RAIN</div>',
                    unsafe_allow_html=True
                )

                st.caption(
                    "🌧️ 빗소리"
                )

            with sound_col3:

                st.markdown(
                    '<div style="text-align:center;color:#c49a70;font-family:Georgia,serif;letter-spacing:2px;margin-bottom:10px;">WHITE NOISE</div>',
                    unsafe_allow_html=True
                )

                st.caption(
                    "〰️ 백색소음"
                )

            st.write("")

            if st.button(
                "← BACK TO RECORD ROOM",
                key="fireplace_back",
                use_container_width=True
            ):

                st.session_state.room_service_step = "record"

                st.rerun()


    # =====================================================
    # 추천받기
    # =====================================================

    else:

        st.markdown(
            '<div class="section-area"><div class="section-title">RECOMMEND</div><div class="section-subtitle">당신에게 맞는 음악을 찾는 공간입니다.</div><div style="color:#8f7059;font-family:Georgia,serif;margin-top:20px;">COMING SOON</div></div>',
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

else:

    st.markdown(
        '<div class="section-area"><div class="section-title">MY ROOM</div><div class="section-subtitle">YOUR PRIVATE ROOM</div><div style="color:#8f7059;font-family:Georgia,serif;margin-top:20px;">CHECK-IN REQUIRED</div></div>',
        unsafe_allow_html=True
    )
