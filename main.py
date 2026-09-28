import streamlit as st
import urllib.parse
import urllib.request
import urllib.error
import json
import re
from textwrap import dedent
from html import escape


# =========================================================
# PAGE SETTING
# =========================================================

st.set_page_config(
    page_title="record room",
    page_icon="♫",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "main"

if "main_entered" not in st.session_state:
    st.session_state.main_entered = False

if "choice_mode" not in st.session_state:
    st.session_state.choice_mode = "select"

if "search_query" not in st.session_state:
    st.session_state.search_query = ""

if "search_results" not in st.session_state:
    st.session_state.search_results = []

if "search_type" not in st.session_state:
    st.session_state.search_type = ""

if "search_artist" not in st.session_state:
    st.session_state.search_artist = None

if "search_error" not in st.session_state:
    st.session_state.search_error = ""


# =========================================================
# HTML RENDER FUNCTION
# =========================================================
# 핵심 수정:
# dedent()를 사용해서 파이썬 들여쓰기가
# Markdown 코드블록으로 인식되는 문제를 방지한다.
# =========================================================

def render_html(content):
    st.markdown(
        dedent(content).strip(),
        unsafe_allow_html=True
    )


# =========================================================
# CSS
# =========================================================

render_html(
    """
    <style>

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

    [data-testid="stAppViewContainer"] {
        min-height: 100vh;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    [data-testid="stToolbar"] {
        display: none !important;
    }

    /* =========================
       SIDEBAR
    ========================= */

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #170d09 0%,
                #120906 50%,
                #0d0705 100%
            ) !important;

        border-right:
            1px solid rgba(190, 145, 92, 0.22);
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 35px;
    }

    .sidebar-brand {
        text-align: center;
        margin-top: 5px;
        margin-bottom: 65px;
    }

    .sidebar-brand-title {
        color: #d9a96f;
        font-family: Georgia, "Times New Roman", serif;
        font-size: 24px;
        letter-spacing: 5px;
        font-weight: 500;
    }

    .sidebar-brand-sub {
        color: #805c3d;
        font-family: Georgia, "Times New Roman", serif;
        font-size: 8px;
        letter-spacing: 4px;
        margin-top: 10px;
    }

    [data-testid="stSidebar"] .stButton {
        width: 100%;
    }

    [data-testid="stSidebar"] .stButton > button {
        background: transparent !important;
        border: none !important;
        border-radius: 0 !important;

        color: #9b704c !important;

        font-family:
            Georgia,
            "Times New Roman",
            serif !important;

        font-size: 13px !important;
        letter-spacing: 4px !important;

        text-align: left !important;

        padding:
            15px 12px 15px 12px !important;

        box-shadow: none !important;

        transition:
            color 0.25s ease,
            background 0.25s ease !important;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        color: #e1b67c !important;

        background:
            linear-gradient(
                90deg,
                rgba(190, 137, 82, 0.10),
                transparent
            ) !important;
    }

    .sidebar-line {
        height: 1px;
        width: 67px;

        background:
            rgba(168, 115, 69, 0.18);

        margin:
            2px 0 22px 20px;
    }


    /* =========================
       MAIN
    ========================= */

    .main .block-container {
        padding-top: 0 !important;
        padding-bottom: 60px !important;

        max-width: 1400px !important;
    }


    /* =========================
       WELCOME
    ========================= */

    .welcome-wrap {
        min-height: 92vh;

        display: flex;
        flex-direction: column;

        justify-content: center;
        align-items: center;

        text-align: center;
    }

    .welcome-small {
        color: #a6784c;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size: 13px;
        letter-spacing: 5px;

        margin-bottom: 22px;
    }

    .welcome-title {
        color: #dcae73;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size:
            clamp(58px, 7vw, 100px);

        letter-spacing: 8px;
        font-weight: 400;

        line-height: 1.05;

        text-shadow:
            0 2px 18px rgba(0, 0, 0, 0.45);
    }

    .welcome-line {
        width: 110px;
        height: 1px;

        background:
            linear-gradient(
                90deg,
                transparent,
                #9c7047,
                transparent
            );

        margin: 28px auto;
    }

    .welcome-description {
        color: #bda087;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size: 15px;

        line-height: 2;

        letter-spacing: 1px;
    }


    /* =========================
       ENTER ROOM
    ========================= */

    .enter-button-wrap {
        display: flex;
        justify-content: center;

        margin-top:
            -170px;

        position: relative;
        z-index: 5;
    }

    .enter-button-wrap .stButton > button {
        min-width: 190px !important;
        height: 52px !important;

        background: transparent !important;

        border:
            1px solid #936b45 !important;

        color: #d6aa75 !important;

        font-family:
            Georgia,
            "Times New Roman",
            serif !important;

        letter-spacing: 4px !important;

        border-radius: 0 !important;

        transition: all 0.25s ease !important;
    }

    .enter-button-wrap .stButton > button:hover {
        background:
            rgba(197, 145, 88, 0.10) !important;

        border-color:
            #d5a66c !important;

        color:
            #efd0a0 !important;

        box-shadow:
            0 0 25px
            rgba(172, 116, 59, 0.15);
    }


    /* =========================
       LETTER
    ========================= */

    .letter-wrap {
        min-height: 92vh;

        display: flex;

        justify-content: center;
        align-items: center;

        padding:
            35px 20px;
    }

    .letter {
        width:
            min(1080px, 90vw);

        min-height:
            650px;

        box-sizing:
            border-box;

        padding:
            72px 90px
            70px 90px;

        position:
            relative;

        background:
            radial-gradient(
                ellipse at center,
                #f7eedb 0%,
                #eee0c4 62%,
                #e2cfac 100%
            );

        border:
            1px solid
            rgba(115, 76, 39, 0.45);

        box-shadow:
            0 30px 70px
            rgba(0, 0, 0, 0.45),
            inset 0 0 45px
            rgba(99, 62, 27, 0.08);

        transform:
            rotate(-0.25deg);
    }

    .letter::before {
        content: "";

        position:
            absolute;

        inset:
            15px;

        border:
            1px solid
            rgba(117, 80, 42, 0.18);

        pointer-events:
            none;
    }

    .letter-date {
        text-align: right;

        color:
            #856344;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size:
            13px;

        letter-spacing:
            1px;

        margin-bottom:
            55px;
    }

    .letter-title {
        color:
            #49301f;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size:
            31px;

        letter-spacing:
            3px;

        margin-bottom:
            42px;
    }

    .letter-body {
        color:
            #49382c;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size:
            17px;

        line-height:
            2.35;

        letter-spacing:
            0.4px;
    }

    .letter-body p {
        margin-bottom:
            25px;
    }

    .letter-sign {
        margin-top:
            65px;

        text-align:
            right;

        color:
            #604531;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size:
            16px;

        line-height:
            1.9;
    }


    /* =========================
       CHOICE
    ========================= */

    .choice-wrap {
        min-height: 92vh;

        display: flex;

        flex-direction:
            column;

        align-items:
            center;

        justify-content:
            center;

        text-align:
            center;
    }

    .choice-heading {
        color:
            #d5a56d;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size:
            44px;

        letter-spacing:
            6px;

        margin-bottom:
            15px;
    }

    .choice-subheading {
        color:
            #96765d;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size:
            14px;

        letter-spacing:
            2px;

        margin-bottom:
            48px;
    }


    /* =========================
       CHOICE BUTTON
    ========================= */

    .paper-button-row {
        display:
            flex;

        justify-content:
            center;

        gap:
            30px;

        width:
            100%;
    }

    .paper-button-row .stButton > button {
        min-width:
            245px !important;

        min-height:
            95px !important;

        padding:
            18px 30px !important;

        border-radius:
            2px !important;

        border:
            1px solid
            rgba(111, 75, 42, 0.45)
            !important;

        background:
            radial-gradient(
                ellipse at center,
                #fbf3e3 0%,
                #ead9b9 100%
            )
            !important;

        color:
            #4c3424 !important;

        font-family:
            Georgia,
            "Times New Roman",
            serif !important;

        font-size:
            21px !important;

        letter-spacing:
            3px !important;

        box-shadow:
            0 15px 35px
            rgba(0, 0, 0, 0.25),
            inset 0 0 20px
            rgba(104, 67, 32, 0.08)
            !important;

        transition:
            all 0.25s ease !important;
    }

    .paper-button-row .stButton > button:hover {
        transform:
            translateY(-4px);

        box-shadow:
            0 20px 40px
            rgba(0, 0, 0, 0.32),
            0 0 25px
            rgba(190, 137, 82, 0.10)
            !important;

        border-color:
            #a77a4e !important;
    }


    /* =========================
       LISTEN
    ========================= */

    .listen-wrap {
        width:
            min(1100px, 90vw);

        margin:
            70px auto 20px auto;
    }

    .listen-heading {
        color:
            #d5a56d;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size:
            42px;

        letter-spacing:
            5px;

        text-align:
            center;

        margin-bottom:
            12px;
    }

    .listen-description {
        color:
            #9d8069;

        text-align:
            center;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size:
            14px;

        letter-spacing:
            1px;

        margin-bottom:
            38px;
    }


    /* =========================
       SEARCH INPUT
    ========================= */

    div[data-testid="stTextInput"] input {
        background:
            rgba(247, 238, 219, 0.96)
            !important;

        color:
            #493528
            !important;

        border:
            1px solid #8d6746
            !important;

        border-radius:
            2px
            !important;

        height:
            52px
            !important;

        font-family:
            "Malgun Gothic",
            Arial,
            sans-serif
            !important;

        font-size:
            15px
            !important;

        box-shadow:
            inset 0 0 15px
            rgba(90, 55, 27, 0.08)
            !important;
    }

    div[data-testid="stTextInput"] input:focus {
        border-color:
            #c09668
            !important;

        box-shadow:
            0 0 0 1px #c09668
            !important;
    }


    /* =========================
       SEARCH BUTTON
    ========================= */

    .search-button-wrap .stButton > button {
        height:
            52px !important;

        width:
            100% !important;

        border-radius:
            2px !important;

        border:
            1px solid #946b45
            !important;

        background:
            #25160f
            !important;

        color:
            #d8aa73
            !important;

        font-family:
            Georgia,
            "Times New Roman",
            serif
            !important;

        letter-spacing:
            3px
            !important;
    }

    .search-button-wrap .stButton > button:hover {
        background:
            #392319
            !important;

        border-color:
            #c39461
            !important;
    }


    /* =========================
       RESULT TITLE
    ========================= */

    .result-heading {
        margin-top:
            55px;

        color:
            #cda072;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size:
            19px;

        letter-spacing:
            2px;

        border-bottom:
            1px solid
            rgba(180, 130, 79, 0.20);

        padding-bottom:
            14px;

        margin-bottom:
            22px;
    }


    /* =========================
       SONG CARD
    ========================= */

    .song-card {
        background:
            linear-gradient(
                135deg,
                rgba(248, 239, 221, 0.98),
                rgba(229, 210, 178, 0.98)
            );

        border:
            1px solid
            rgba(116, 79, 44, 0.40);

        padding:
            22px;

        margin-bottom:
            18px;

        box-shadow:
            0 12px 30px
            rgba(0, 0, 0, 0.20);

        min-height:
            145px;
    }

    .song-name {
        color:
            #392519;

        font-family:
            "Malgun Gothic",
            Arial,
            sans-serif;

        font-size:
            20px;

        font-weight:
            600;

        margin-bottom:
            7px;
    }

    .song-artist {
        color:
            #705039;

        font-size:
            14px;

        margin-bottom:
            5px;
    }

    .song-album {
        color:
            #876b53;

        font-size:
            13px;
    }

    .song-meta {
        color:
            #987b60;

        font-size:
            11px;

        margin-top:
            9px;
    }

    .apple-link {
        display:
            inline-block;

        margin-top:
            12px;

        color:
            #765238 !important;

        text-decoration:
            none !important;

        border-bottom:
            1px solid
            rgba(118, 82, 56, 0.35);

        padding-bottom:
            2px;

        font-size:
            12px;
    }

    .apple-link:hover {
        color:
            #4c301e !important;
    }


    /* =========================
       NOTICE
    ========================= */

    .notice-box {
        margin-top:
            30px;

        padding:
            28px;

        border:
            1px solid
            rgba(157, 112, 72, 0.35);

        background:
            rgba(239, 221, 190, 0.06);

        color:
            #b89b80;

        text-align:
            center;

        line-height:
            1.9;
    }


    /* =========================
       COMING SOON
    ========================= */

    .coming-wrap {
        min-height:
            80vh;

        display:
            flex;

        justify-content:
            center;

        align-items:
            center;

        flex-direction:
            column;
    }

    .coming-title {
        color:
            #d5a56d;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size:
            46px;

        letter-spacing:
            7px;
    }

    .coming-text {
        color:
            #8d715d;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        margin-top:
            18px;

        letter-spacing:
            2px;
    }


    /* =========================
       MOBILE
    ========================= */

    @media (max-width: 800px) {

        .paper-button-row {
            flex-direction:
                column;

            align-items:
                center;
        }

        .letter {
            padding:
                55px 40px
                50px 40px;

            min-height:
                600px;
        }

        .letter-body {
            font-size:
                15px;
        }

        .welcome-title {
            letter-spacing:
                5px;
        }

    }

    </style>
    """
)


# =========================================================
# APPLE API
# =========================================================

ITUNES_SEARCH_URL = "https://itunes.apple.com/search"
ITUNES_LOOKUP_URL = "https://itunes.apple.com/lookup"


def normalize_text(text):
    """
    검색 비교용 정규화
    """

    if not text:
        return ""

    text = str(text).lower()

    text = re.sub(
        r"\([^)]*\)",
        "",
        text
    )

    text = re.sub(
        r"\s+",
        "",
        text
    )

    text = re.sub(
        r"[^0-9a-z가-힣ぁ-んァ-ン一-龥]",
        "",
        text
    )

    return text


def apple_api_request(url, params):

    query = urllib.parse.urlencode(params)

    full_url = (
        url
        + "?"
        + query
    )

    request = urllib.request.Request(
        full_url,
        headers={
            "User-Agent":
                "Mozilla/5.0 record-room"
        }
    )

    try:

        with urllib.request.urlopen(
            request,
            timeout=12
        ) as response:

            raw = response.read()

            return json.loads(
                raw.decode("utf-8")
            )

    except urllib.error.HTTPError as e:

        raise Exception(
            f"Apple API 오류 ({e.code})"
        )

    except urllib.error.URLError:

        raise Exception(
            "Apple 서버에 연결하지 못했습니다."
        )

    except Exception as e:

        raise Exception(
            f"검색 중 오류가 발생했습니다: {e}"
        )


# =========================================================
# EXACT ARTIST SEARCH
# =========================================================

@st.cache_data(
    ttl=600,
    show_spinner=False
)
def find_exact_artist(query):

    data = apple_api_request(
        ITUNES_SEARCH_URL,
        {
            "term": query,
            "country": "KR",
            "media": "music",
            "entity": "musicArtist",
            "limit": 50,
            "lang": "ko_kr"
        }
    )

    artists = data.get(
        "results",
        []
    )

    normalized_query = normalize_text(
        query
    )

    # 오직 완전 일치만 인정
    for artist in artists:

        artist_name = artist.get(
            "artistName",
            ""
        )

        if normalize_text(
            artist_name
        ) == normalized_query:

            return artist

    return None


# =========================================================
# ARTIST SONGS
# =========================================================

@st.cache_data(
    ttl=600,
    show_spinner=False
)
def get_artist_songs(artist_id):

    data = apple_api_request(
        ITUNES_LOOKUP_URL,
        {
            "id": artist_id,
            "entity": "song",
            "country": "KR",
            "limit": 50,
            "sort": "recent"
        }
    )

    results = data.get(
        "results",
        []
    )

    songs = []

    for item in results:

        if item.get(
            "wrapperType"
        ) != "track":

            continue

        if item.get(
            "kind"
        ) != "song":

            continue

        songs.append(item)

    return songs


# =========================================================
# SONG SEARCH
# =========================================================

@st.cache_data(
    ttl=600,
    show_spinner=False
)
def find_song_results(query):

    data = apple_api_request(
        ITUNES_SEARCH_URL,
        {
            "term": query,
            "country": "KR",
            "media": "music",
            "entity": "song",
            "limit": 50,
            "lang": "ko_kr"
        }
    )

    results = data.get(
        "results",
        []
    )

    normalized_query = normalize_text(
        query
    )

    exact_matches = []
    partial_matches = []

    for song in results:

        if song.get(
            "kind"
        ) != "song":

            continue

        track_name = song.get(
            "trackName",
            ""
        )

        normalized_track = normalize_text(
            track_name
        )

        if not normalized_track:
            continue

        # 제목 완전 일치
        if normalized_track == normalized_query:

            exact_matches.append(song)

        # 제목 일부 일치
        elif normalized_query in normalized_track:

            partial_matches.append(song)

    # 완전 일치가 하나라도 존재한다면
    # 완전 일치 위주로 보여준다.
    if exact_matches:
        return exact_matches[:30]

    return partial_matches[:30]


# =========================================================
# MAIN SEARCH
# =========================================================

@st.cache_data(
    ttl=600,
    show_spinner=False
)
def search_music(query):

    query = query.strip()

    if not query:

        return {
            "type": "",
            "artist": None,
            "songs": []
        }

    # -----------------------------------------------------
    # 1. 가수 이름 완전 일치 확인
    # -----------------------------------------------------

    artist = find_exact_artist(
        query
    )

    if artist:

        artist_id = artist.get(
            "artistId"
        )

        if artist_id:

            songs = get_artist_songs(
                artist_id
            )

            return {
                "type": "artist",
                "artist": artist,
                "songs": songs
            }

    # -----------------------------------------------------
    # 2. 가수가 아니면 곡 제목 검색
    # -----------------------------------------------------

    songs = find_song_results(
        query
    )

    return {
        "type": "song",
        "artist": None,
        "songs": songs
    }


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    render_html(
        """
        <div class="sidebar-brand">

            <div class="sidebar-brand-title">
                RECORD ROOM
            </div>

            <div class="sidebar-brand-sub">
                A ROOM FOR MUSIC
            </div>

        </div>
        """
    )

    if st.button(
        "MAIN",
        key="sidebar_main"
    ):

        st.session_state.page = "main"
        st.session_state.main_entered = False
        st.session_state.choice_mode = "select"

        st.rerun()

    render_html(
        """
        <div class="sidebar-line"></div>
        """
    )

    if st.button(
        "CHOICE",
        key="sidebar_choice"
    ):

        st.session_state.page = "choice"
        st.session_state.choice_mode = "select"

        st.rerun()

    render_html(
        """
        <div class="sidebar-line"></div>
        """
    )

    if st.button(
        "—",
        key="sidebar_empty"
    ):

        st.session_state.page = "unknown"

        st.rerun()

    render_html(
        """
        <div class="sidebar-line"></div>
        """
    )


# =========================================================
# MAIN PAGE
# =========================================================

if st.session_state.page == "main":

    # -----------------------------------------------------
    # INITIAL MAIN
    # -----------------------------------------------------

    if not st.session_state.main_entered:

        render_html(
            """
            <div class="welcome-wrap">

                <div class="welcome-small">
                    WELCOME TO
                </div>

                <div class="welcome-title">
                    record room
                </div>

                <div class="welcome-line"></div>

                <div class="welcome-description">
                    음악을 듣고, 발견하고,<br>
                    잠시 머무는 작은 방
                </div>

            </div>
            """
        )

        render_html(
            """
            <div class="enter-button-wrap">
            """
        )

        if st.button(
            "ENTER ROOM",
            key="enter_room"
        ):

            st.session_state.main_entered = True

            st.rerun()

        render_html(
            """
            </div>
            """
        )

    # -----------------------------------------------------
    # LETTER
    # -----------------------------------------------------

    else:

        render_html(
            """
            <div class="letter-wrap">

                <div class="letter">

                    <div class="letter-date">
                        RECORD ROOM
                    </div>

                    <div class="letter-title">
                        Dear visitor,
                    </div>

                    <div class="letter-body">

                        <p>
                            이곳에 들어온 것을 환영합니다.
                        </p>

                        <p>
                            이 방에는 수많은 음악이 있습니다.
                            누군가에게는 오래된 기억이고,
                            누군가에게는 아직 만나지 못한
                            새로운 장면일지도 모릅니다.
                        </p>

                        <p>
                            오늘 어떤 음악을 듣게 될지는
                            아직 아무도 알 수 없습니다.
                        </p>

                        <p>
                            천천히 둘러보세요.
                            듣고 싶은 음악을 찾아도 좋고,
                            우연히 새로운 음악을 발견해도 좋습니다.
                        </p>

                        <p>
                            이곳에서 잠시,
                            당신만의 음악을 찾아가길 바랍니다.
                        </p>

                    </div>

                    <div class="letter-sign">
                        from,<br>
                        record room
                    </div>

                </div>

            </div>
            """
        )


# =========================================================
# CHOICE PAGE
# =========================================================

elif st.session_state.page == "choice":

    # =====================================================
    # CHOICE SELECT
    # =====================================================

    if st.session_state.choice_mode == "select":

        render_html(
            """
            <div class="choice-wrap">

                <div class="choice-heading">
                    CHOICE
                </div>

                <div class="choice-subheading">
                    WHAT WOULD YOU LIKE TO DO?
                </div>

            </div>
            """
        )

        st.markdown(
            "<div class='paper-button-row'>",
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(
            2,
            gap="large"
        )

        with col1:

            if st.button(
                "노래 듣기",
                key="listen_button"
            ):

                st.session_state.choice_mode = "listen"

                st.rerun()

        with col2:

            if st.button(
                "추천받기",
                key="recommend_button"
            ):

                st.session_state.choice_mode = "recommend"

                st.rerun()

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


    # =====================================================
    # LISTEN
    # =====================================================

    elif st.session_state.choice_mode == "listen":

        render_html(
            """
            <div class="listen-wrap">

                <div class="listen-heading">
                    LISTEN
                </div>

                <div class="listen-description">
                    가수 이름 또는 곡 제목을 검색해보세요.
                </div>

            </div>
            """
        )

        search_col1, search_col2 = st.columns(
            [5, 1],
            gap="medium"
        )

        with search_col1:

            query = st.text_input(
                "검색",
                placeholder=
                    "가수 이름 또는 곡 제목을 입력하세요",
                label_visibility="collapsed",
                key="music_search_input"
            )

        with search_col2:

            render_html(
                """
                <div class="search-button-wrap">
                """
            )

            search_clicked = st.button(
                "SEARCH",
                key="music_search_button"
            )

            render_html(
                """
                </div>
                """
            )


        # -------------------------------------------------
        # SEARCH
        # -------------------------------------------------

        if search_clicked:

            clean_query = query.strip()

            if not clean_query:

                st.session_state.search_results = []

                st.session_state.search_type = ""

                st.session_state.search_query = ""

                st.session_state.search_artist = None

                st.session_state.search_error = (
                    "검색어를 입력해주세요."
                )

            else:

                try:

                    with st.spinner(
                        "record room에서 음악을 찾는 중..."
                    ):

                        result = search_music(
                            clean_query
                        )

                    st.session_state.search_results = (
                        result["songs"]
                    )

                    st.session_state.search_type = (
                        result["type"]
                    )

                    st.session_state.search_artist = (
                        result["artist"]
                    )

                    st.session_state.search_query = (
                        clean_query
                    )

                    st.session_state.search_error = ""

                except Exception as e:

                    st.session_state.search_results = []

                    st.session_state.search_error = (
                        str(e)
                    )


        # -------------------------------------------------
        # ERROR
        # -------------------------------------------------

        if st.session_state.search_error:

            render_html(
                f"""
                <div class="notice-box">
                    {escape(st.session_state.search_error)}
                </div>
                """
            )


        # -------------------------------------------------
        # RESULTS
        # -------------------------------------------------

        results = st.session_state.search_results

        if results:

            search_type = (
                st.session_state.search_type
            )

            searched = (
                st.session_state.search_query
            )

            if search_type == "artist":

                artist = (
                    st.session_state.search_artist
                )

                artist_name = (
                    artist.get(
                        "artistName",
                        searched
                    )
                    if artist
                    else searched
                )

                render_html(
                    f"""
                    <div class="result-heading">
                        {escape(artist_name)} — SONGS
                    </div>
                    """
                )

            else:

                render_html(
                    f"""
                    <div class="result-heading">
                        SEARCH RESULTS FOR
                        "{escape(searched)}"
                    </div>
                    """
                )


            # -------------------------------------------------
            # SONG CARDS
            # -------------------------------------------------

            for song in results:

                track_name = escape(
                    song.get(
                        "trackName",
                        "Unknown Song"
                    )
                )

                artist_name = escape(
                    song.get(
                        "artistName",
                        "Unknown Artist"
                    )
                )

                album_name = escape(
                    song.get(
                        "collectionName",
                        "Unknown Album"
                    )
                )

                artwork = song.get(
                    "artworkUrl100",
                    ""
                )

                release_date = song.get(
                    "releaseDate",
                    ""
                )

                if release_date:

                    release_date = escape(
                        release_date[:10]
                    )
                else:

                    release_date = "-"

                track_url = song.get(
                    "trackViewUrl",
                    ""
                )

                preview_url = song.get(
                    "previewUrl",
                    ""
                )


                result_col1, result_col2 = st.columns(
                    [1, 6],
                    gap="medium"
                )


                # ARTWORK
                with result_col1:

                    if artwork:

                        st.image(
                            artwork,
                            width=120
                        )


                # INFO
                with result_col2:

                    apple_link = ""

                    if track_url:

                        safe_url = escape(
                            track_url,
                            quote=True
                        )

                        apple_link = (
                            f'<a '
                            f'class="apple-link" '
                            f'href="{safe_url}" '
                            f'target="_blank">'
                            f'OPEN IN APPLE MUSIC / ITUNES ↗'
                            f'</a>'
                        )

                    render_html(
                        f"""
                        <div class="song-card">

                            <div class="song-name">
                                {track_name}
                            </div>

                            <div class="song-artist">
                                {artist_name}
                            </div>

                            <div class="song-album">
                                {album_name}
                            </div>

                            <div class="song-meta">
                                RELEASE · {release_date}
                            </div>

                            {apple_link}

                        </div>
                        """
                    )

                    if preview_url:

                        st.audio(
                            preview_url
                        )

                render_html(
                    """
                    <div
                        style="
                            height:14px;
                        "
                    ></div>
                    """
                )


        # -------------------------------------------------
        # NO RESULTS
        # -------------------------------------------------

        elif (
            st.session_state.search_query
            and not st.session_state.search_error
        ):

            render_html(
                f"""
                <div class="notice-box">

                    "{escape(
                        st.session_state.search_query
                    )}"

                    에 해당하는 음악을 찾지 못했습니다.

                    <br><br>

                    정확한 가수 이름이나
                    곡 제목을 입력해보세요.

                </div>
                """
            )


    # =====================================================
    # RECOMMEND
    # =====================================================

    elif st.session_state.choice_mode == "recommend":

        render_html(
            """
            <div class="coming-wrap">

                <div class="coming-title">
                    COMING SOON
                </div>

                <div class="coming-text">
                    YOUR NEXT SONG IS WAITING
                </div>

            </div>
            """
        )


# =========================================================
# UNKNOWN PAGE
# =========================================================

else:

    render_html(
        """
        <div class="coming-wrap">

            <div class="coming-title">
                —
            </div>

        </div>
        """
    )
