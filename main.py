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
# DESIGN
# =========================================================

CSS = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&family=Noto+Serif+KR:wght@400;500;600&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background:
        radial-gradient(
            circle at 55% 35%,
            #3b281d 0%,
            #24160f 42%,
            #120b08 78%,
            #0b0705 100%
        ) !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

[data-testid="stToolbar"] {
    display: none !important;
}

.main .block-container {
    padding-top: 0 !important;
    max-width: 1400px;
}

/* =========================================================
   SIDEBAR
   ========================================================= */

[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #170d09 0%,
            #120906 55%,
            #0d0705 100%
        ) !important;

    border-right: 1px solid rgba(190,145,92,0.22);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 35px;
}

.sidebar-title {
    color: #d9a96f;
    font-family: "Cormorant Garamond", serif;
    font-size: 24px;
    letter-spacing: 4px;
    text-align: center;
    margin: 0;
}

.sidebar-subtitle {
    color: #805c3d;
    font-family: "Cormorant Garamond", serif;
    font-size: 12px;
    letter-spacing: 3px;
    text-align: center;
    margin-top: 7px;
    margin-bottom: 55px;
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

    font-family: "Cormorant Garamond", serif !important;

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
   MAIN
   ========================================================= */

.welcome-area {
    min-height: 88vh;

    display: flex;

    flex-direction: column;

    justify-content: center;

    align-items: center;

    text-align: center;
}

.welcome-small {
    color: #a6784c;

    font-family: "Cormorant Garamond", serif;

    font-size: 14px;

    letter-spacing: 5px;

    margin-bottom: 18px;
}

.welcome-title {
    color: #dcae73;

    font-family: "Cormorant Garamond", serif;

    font-size: clamp(60px, 7vw, 100px);

    font-weight: 400;

    letter-spacing: 8px;

    line-height: 1;

    margin: 0;
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

    margin-bottom: 28px;
}

/* =========================================================
   ENTER BUTTON
   ========================================================= */

div[data-testid="stButton"] > button {
    background: transparent !important;

    color: #d8ad79 !important;

    border: 1px solid rgba(190,145,92,0.5) !important;

    border-radius: 2px !important;

    font-family: "Cormorant Garamond", serif !important;

    letter-spacing: 3px !important;

    transition: 0.25s ease !important;
}

div[data-testid="stButton"] > button:hover {
    background: rgba(197,145,88,0.08) !important;

    border-color: #d5a66c !important;

    color: #efd7b0 !important;
}

/* =========================================================
   LETTER
   ========================================================= */

.letter-wrap {
    min-height: 88vh;

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

    background:
        radial-gradient(
            ellipse at center,
            #f7eedb 0%,
            #eee0c4 62%,
            #e2cfac 100%
        );

    border: 1px solid rgba(117,80,42,0.18);

    box-shadow:
        0 20px 45px rgba(0,0,0,0.45);

    position: relative;

    color: #49382c;

    font-family: "Noto Serif KR", serif;
}

.letter-paper::before {
    content: "";

    position: absolute;

    inset: 15px;

    border: 1px solid rgba(117,80,42,0.18);

    pointer-events: none;
}

.letter-date {
    color: #856344;

    text-align: right;

    font-family: "Cormorant Garamond", serif;

    font-size: 14px;

    margin-bottom: 50px;
}

.letter-title {
    color: #49301f;

    font-family: "Cormorant Garamond", serif;

    font-size: 34px;

    letter-spacing: 3px;

    margin-bottom: 40px;
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

    font-family: "Cormorant Garamond", serif;

    font-size: 17px;

    line-height: 1.9;

    margin-top: 45px;
}

/* =========================================================
   CHOICE
   ========================================================= */

.section-area {
    min-height: 88vh;

    display: flex;

    flex-direction: column;

    justify-content: center;

    align-items: center;

    text-align: center;
}

.section-title {
    color: #d5a56d;

    font-family: "Cormorant Garamond", serif;

    font-size: 48px;

    letter-spacing: 6px;

    margin: 0 0 12px 0;
}

.section-subtitle {
    color: #96765d;

    font-family: "Noto Serif KR", serif;

    font-size: 14px;

    letter-spacing: 2px;

    margin-bottom: 40px;
}

/* CHOICE 버튼 */

div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] > button {
    min-height: 95px !important;

    background:
        radial-gradient(
            ellipse at center,
            #fbf3e3 0%,
            #ead9b9 100%
        ) !important;

    color: #4c3424 !important;

    border: 1px solid rgba(111,75,42,0.45) !important;

    border-radius: 2px !important;

    font-family: "Noto Serif KR", serif !important;

    font-size: 18px !important;

    letter-spacing: 3px !important;

    box-shadow:
        0 15px 35px rgba(0,0,0,0.25) !important;
}

/* =========================================================
   LISTEN
   ========================================================= */

.listen-title {
    color: #d5a56d;

    font-family: "Cormorant Garamond", serif;

    font-size: 48px;

    letter-spacing: 5px;

    text-align: center;
}

.listen-subtitle {
    color: #9d8069;

    font-family: "Noto Serif KR", serif;

    font-size: 14px;

    text-align: center;

    margin-top: 12px;

    margin-bottom: 38px;
}

.search-button {
    height: 52px;
}

.result-title {
    color: #dca072;

    font-family: "Cormorant Garamond", serif;

    font-size: 28px;

    letter-spacing: 3px;

    margin: 30px 0 15px 0;
}

.result-card {
    display: flex;

    gap: 20px;

    align-items: center;

    text-align: left;

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

    font-family: "Cormorant Garamond", serif;

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

/* =========================================================
   RADIO
   ========================================================= */

[data-testid="stRadio"] label {
    color: #9f8068 !important;
}
</style>
"""

# 핵심:
# CSS를 st.markdown으로 출력하지 않고 st.html로 렌더링
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

    st.rerun()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">RECORD ROOM</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">A ROOM FOR MUSIC</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-rule"></div>',
        unsafe_allow_html=True
    )

    if st.button("MAIN", key="nav_main"):
        go("main")

    if st.button("CHOICE", key="nav_choice"):
        go("choice")

    if st.button("—", key="nav_unknown"):
        go("unknown")


# =========================================================
# APPLE iTUNES SEARCH API
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
# SEARCH ARTIST
# =========================================================

@st.cache_data(ttl=600, show_spinner=False)
def find_artist_tracks(query):

    query = query.strip()

    if not query:
        return []

    normalized_query = normalize(query)

    # -----------------------------------------
    # 1. Apple에서 실제 가수 검색
    # -----------------------------------------

    params = {
        "term": query,
        "country": "US",
        "media": "music",
        "entity": "musicArtist",
        "attribute": "artistTerm",
        "limit": 25
    }

    data = apple_search(params)

    artists = data.get(
        "results",
        []
    )

    exact = [
        artist
        for artist in artists
        if normalize(
            artist.get("artistName", "")
        ) == normalized_query
    ]

    if exact:

        artist = exact[0]

    else:

        partial = [
            artist
            for artist in artists
            if normalized_query in normalize(
                artist.get("artistName", "")
            )
        ]

        if partial:

            artist = partial[0]

        else:

            # -----------------------------------------
            # 한국 스토어 fallback
            # -----------------------------------------

            params["country"] = "KR"

            data = apple_search(params)

            artists = data.get(
                "results",
                []
            )

            exact = [
                artist
                for artist in artists
                if normalize(
                    artist.get("artistName", "")
                ) == normalized_query
            ]

            if exact:

                artist = exact[0]

            else:

                partial = [
                    artist
                    for artist in artists
                    if normalized_query in normalize(
                        artist.get("artistName", "")
                    )
                ]

                if not partial:
                    return []

                artist = partial[0]

    artist_id = artist.get("artistId")

    if not artist_id:
        return []

    # -----------------------------------------
    # 2. artistId로 정확한 곡만 가져오기
    # -----------------------------------------

    lookup_params = {
        "id": artist_id,
        "entity": "song",
        "country": "US",
        "limit": 100
    }

    lookup = apple_lookup(
        lookup_params
    )

    tracks = [
        item
        for item in lookup.get("results", [])
        if item.get("wrapperType") == "track"
    ]

    # 미국 스토어에 없으면 한국 스토어
    if not tracks:

        lookup_params["country"] = "KR"

        lookup = apple_lookup(
            lookup_params
        )

        tracks = [
            item
            for item in lookup.get("results", [])
            if item.get("wrapperType") == "track"
        ]

    return tracks


# =========================================================
# SEARCH SONG
# =========================================================

@st.cache_data(ttl=600, show_spinner=False)
def find_song(query):

    query = query.strip()

    if not query:
        return []

    params = {
        "term": query,
        "country": "US",
        "media": "music",
        "entity": "song",
        "attribute": "songTerm",
        "limit": 50
    }

    data = apple_search(params)

    results = data.get(
        "results",
        []
    )

    normalized_query = normalize(query)

    # 제목 완전 일치
    exact = [
        result
        for result in results
        if normalize(
            result.get("trackName", "")
        ) == normalized_query
    ]

    if exact:
        return exact

    # 제목 부분 일치
    partial = [
        result
        for result in results
        if normalized_query in normalize(
            result.get("trackName", "")
        )
    ]

    return partial[:30]


# =========================================================
# GENERAL SEARCH
# =========================================================

def search_music(query, search_type):

    if search_type == "artist":

        return find_artist_tracks(query)

    if search_type == "song":

        return find_song(query)

    # 자동 검색
    artist_results = find_artist_tracks(query)

    if artist_results:

        return artist_results

    return find_song(query)


# =========================================================
# RESULT DISPLAY
# =========================================================

def display_results(results):

    if not results:

        st.markdown(
            """
            <div class="no-result">
                검색 결과를 찾지 못했습니다.<br>
                가수 이름이나 정확한 곡 제목을 다시 입력해 주세요.
            </div>
            """,
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
            (result.get(
                "releaseDate",
                ""
            ) or "")[:10]
        )

        apple_url = result.get(
            "trackViewUrl",
            ""
        )

        preview_url = result.get(
            "previewUrl",
            ""
        )

        if artwork:

            image_html = (
                '<img src="'
                + escape(artwork)
                + '">'
            )

        else:

            image_html = ""

        if apple_url:

            apple_link = (
                '<a href="'
                + escape(apple_url)
                + '" target="_blank" '
                'style="color:#c89b6b;'
                'text-decoration:none;">'
                'Apple Music ↗'
                '</a>'
            )

        else:

            apple_link = ""

        card_html = (
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
            + apple_link
            + '</div>'
            + '</div>'
            + '</div>'
        )

        st.markdown(
            card_html,
            unsafe_allow_html=True
        )

        if preview_url:

            st.audio(
                preview_url
            )


# =========================================================
# MAIN PAGE
# =========================================================

if st.session_state.page == "main":

    if not st.session_state.main_entered:

        st.markdown(
            """
            <div class="welcome-area">

                <div class="welcome-small">
                    WELCOME TO
                </div>

                <div class="welcome-title">
                    record room
                </div>

                <div class="welcome-line"></div>

                <div class="welcome-description">
                    음악을 듣고, 발견하고, 잠시 머무는 작은 방
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        # 중앙 버튼
        _, center, _ = st.columns(
            [2, 1, 2]
        )

        with center:

            if st.button(
                "ENTER ROOM",
                key="enter_room",
                use_container_width=True
            ):

                st.session_state.main_entered = True

                st.rerun()

    else:

        st.markdown(
            """
            <div class="letter-wrap">

                <div class="letter-paper">

                    <div class="letter-date">
                        SEPTEMBER 28, 2026
                    </div>

                    <div class="letter-title">
                        DEAR, VISITOR
                    </div>

                    <div class="letter-body">

                        이곳에는 조금 오래 머물러도 괜찮습니다.

                        <br><br>

                        누군가에게는 스쳐 지나갈 한 곡이,
                        누군가에게는 오래 기억될 밤이 되기도 하니까요.

                        <br><br>

                        이 방에서는 이름을 알고 찾아온 음악도,
                        우연히 발견한 음악도 천천히 들여다볼 수 있습니다.

                        <br><br>

                        문을 열었으니,
                        이제 당신이 들을 차례입니다.

                    </div>

                    <div class="letter-sign">
                        — record room
                    </div>

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# CHOICE PAGE
# =========================================================

elif st.session_state.page == "choice":

    # -----------------------------------------
    # 선택 화면
    # -----------------------------------------

    if st.session_state.choice_mode is None:

        st.markdown(
            """
            <div class="section-area">

                <div class="section-title">
                    CHOICE
                </div>

                <div class="section-subtitle">
                    오늘은 어떤 방식으로 음악을 만날까요?
                </div>

            </div>
            """,
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

                st.rerun()

        with right:

            if st.button(
                "추천받기",
                key="recommend_choice",
                use_container_width=True
            ):

                st.session_state.choice_mode = "recommend"

                st.rerun()


    # -----------------------------------------
    # 노래 듣기
    # -----------------------------------------

    elif st.session_state.choice_mode == "listen":

        st.markdown(
            """
            <div style="
                padding-top:55px;
                text-align:center;
            ">

                <div class="listen-title">
                    LISTEN
                </div>

                <div class="listen-subtitle">
                    가수 이름 또는 곡 제목을 검색하세요.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        search_col, button_col = st.columns(
            [5, 1],
            gap="small"
        )

        with search_col:

            query = st.text_input(
                "SEARCH",
                value=st.session_state.search_text,
                placeholder="예: 아이유 / Love wins all",
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
                    "record room에서 음악을 찾는 중..."
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


    # -----------------------------------------
    # 추천받기
    # -----------------------------------------

    else:

        st.markdown(
            """
            <div class="section-area">

                <div class="section-title">
                    RECOMMEND
                </div>

                <div class="section-subtitle">
                    당신에게 맞는 음악을 찾는 공간입니다.
                </div>

                <div style="
                    color:#8f7059;
                    font-family:Georgia,serif;
                    margin-top:20px;
                ">
                    COMING SOON
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# UNKNOWN PAGE
# =========================================================

else:

    st.markdown(
        """
        <div class="section-area">

            <div class="section-title">
                —
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )
