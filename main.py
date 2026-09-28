import streamlit as st
import urllib.parse
import urllib.request
import urllib.error
import json
import re


# =========================================================
# 기본 설정
# =========================================================

st.set_page_config(
    page_title="record room",
    page_icon="♫",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# Session State
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

if "search_error" not in st.session_state:
    st.session_state.search_error = ""


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    /* -----------------------------------------------------
       전체 화면
    ----------------------------------------------------- */

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

    /* -----------------------------------------------------
       Sidebar
    ----------------------------------------------------- */

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #170d09 0%,
                #120906 50%,
                #0d0705 100%
            ) !important;

        border-right: 1px solid rgba(190, 145, 92, 0.22);
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

    /* Sidebar buttons */

    [data-testid="stSidebar"] .stButton {
        width: 100%;
        margin: 0;
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
        background: rgba(168, 115, 69, 0.18);
        margin: 2px 0 22px 20px;
    }

    /* -----------------------------------------------------
       Main 영역
    ----------------------------------------------------- */

    .main .block-container {
        padding-top: 0 !important;
        padding-bottom: 60px !important;
        max-width: 1400px !important;
    }

    /* -----------------------------------------------------
       MAIN 첫 화면
    ----------------------------------------------------- */

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

        font-size: clamp(58px, 7vw, 100px);

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

        margin-bottom: 40px;
    }

    /* -----------------------------------------------------
       ENTER ROOM
    ----------------------------------------------------- */

    .enter-space {
        display: flex;
        justify-content: center;
        margin-top: 10px;
    }

    .enter-space .stButton > button {
        min-width: 190px !important;
        height: 52px !important;

        background: transparent !important;

        border: 1px solid #936b45 !important;

        color: #d6aa75 !important;

        font-family:
            Georgia,
            "Times New Roman",
            serif !important;

        letter-spacing: 4px !important;

        border-radius: 0 !important;

        transition:
            all 0.25s ease !important;
    }

    .enter-space .stButton > button:hover {
        background: rgba(197, 145, 88, 0.10) !important;

        border-color: #d5a66c !important;

        color: #efd0a0 !important;

        box-shadow:
            0 0 25px rgba(172, 116, 59, 0.15);
    }

    /* -----------------------------------------------------
       편지
    ----------------------------------------------------- */

    .letter-wrap {
        min-height: 92vh;

        display: flex;

        justify-content: center;
        align-items: center;

        padding: 35px 20px;
    }

    .letter {
        width: min(1080px, 90vw);

        min-height: 650px;

        box-sizing: border-box;

        padding:
            72px 90px
            70px 90px;

        position: relative;

        background:
            radial-gradient(
                ellipse at center,
                #f7eedb 0%,
                #eee0c4 62%,
                #e2cfac 100%
            );

        border:
            1px solid rgba(115, 76, 39, 0.45);

        box-shadow:
            0 30px 70px rgba(0, 0, 0, 0.45),
            inset 0 0 45px rgba(99, 62, 27, 0.08);

        transform: rotate(-0.25deg);
    }

    .letter::before {
        content: "";

        position: absolute;

        inset: 15px;

        border:
            1px solid rgba(117, 80, 42, 0.18);

        pointer-events: none;
    }

    .letter-date {
        text-align: right;

        color: #856344;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size: 13px;

        letter-spacing: 1px;

        margin-bottom: 55px;
    }

    .letter-title {
        color: #49301f;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size: 31px;

        letter-spacing: 3px;

        margin-bottom: 42px;
    }

    .letter-body {
        color: #49382c;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size: 17px;

        line-height: 2.35;

        letter-spacing: 0.4px;
    }

    .letter-body p {
        margin-bottom: 25px;
    }

    .letter-sign {
        margin-top: 65px;

        text-align: right;

        color: #604531;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size: 16px;

        line-height: 1.9;
    }

    /* -----------------------------------------------------
       CHOICE
    ----------------------------------------------------- */

    .choice-wrap {
        min-height: 92vh;

        display: flex;

        flex-direction: column;

        align-items: center;

        justify-content: center;

        text-align: center;
    }

    .choice-heading {
        color: #d5a56d;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size: 44px;

        letter-spacing: 6px;

        margin-bottom: 15px;
    }

    .choice-subheading {
        color: #96765d;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size: 14px;

        letter-spacing: 2px;

        margin-bottom: 48px;
    }

    .paper-button-area {
        display: flex;

        justify-content: center;

        gap: 30px;

        width: 100%;
    }

    .paper-button-area .stButton > button {
        min-width: 245px !important;

        min-height: 95px !important;

        padding: 18px 30px !important;

        border-radius: 2px !important;

        border:
            1px solid rgba(111, 75, 42, 0.45)
            !important;

        background:
            radial-gradient(
                ellipse at center,
                #fbf3e3 0%,
                #ead9b9 100%
            )
            !important;

        color: #4c3424 !important;

        font-family:
            Georgia,
            "Times New Roman",
            serif !important;

        font-size: 21px !important;

        letter-spacing: 3px !important;

        box-shadow:
            0 15px 35px rgba(0, 0, 0, 0.25),
            inset 0 0 20px rgba(104, 67, 32, 0.08) !important;

        transition:
            all 0.25s ease !important;
    }

    .paper-button-area .stButton > button:hover {
        transform: translateY(-4px);

        box-shadow:
            0 20px 40px rgba(0, 0, 0, 0.32),
            0 0 25px rgba(190, 137, 82, 0.10) !important;

        border-color: #a77a4e !important;
    }

    /* -----------------------------------------------------
       검색 화면
    ----------------------------------------------------- */

    .listen-wrap {
        width: min(1100px, 90vw);

        margin:
            70px auto
            60px auto;
    }

    .listen-heading {
        color: #d5a56d;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size: 42px;

        letter-spacing: 5px;

        text-align: center;

        margin-bottom: 12px;
    }

    .listen-description {
        color: #9d8069;

        text-align: center;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size: 14px;

        letter-spacing: 1px;

        margin-bottom: 38px;
    }

    /* Search box */

    .search-label {
        color: #c7a27f;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size: 13px;

        letter-spacing: 2px;

        margin-bottom: 8px;
    }

    div[data-testid="stTextInput"] input {
        background:
            rgba(247, 238, 219, 0.96) !important;

        color: #493528 !important;

        border:
            1px solid #8d6746 !important;

        border-radius: 2px !important;

        height: 52px !important;

        font-family:
            Georgia,
            "Malgun Gothic",
            sans-serif !important;

        font-size: 15px !important;

        box-shadow:
            inset 0 0 15px rgba(90, 55, 27, 0.08) !important;
    }

    div[data-testid="stTextInput"] input:focus {
        border-color: #c09668 !important;

        box-shadow:
            0 0 0 1px #c09668 !important;
    }

    /* Search button */

    .search-button .stButton > button {
        height: 52px !important;

        width: 100% !important;

        border-radius: 2px !important;

        border: 1px solid #946b45 !important;

        background: #25160f !important;

        color: #d8aa73 !important;

        font-family:
            Georgia,
            "Times New Roman",
            serif !important;

        letter-spacing: 3px !important;

        transition: all 0.25s ease !important;
    }

    .search-button .stButton > button:hover {
        background: #392319 !important;

        border-color: #c39461 !important;
    }

    /* -----------------------------------------------------
       검색 결과
    ----------------------------------------------------- */

    .result-heading {
        margin-top: 55px;

        color: #cda072;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size: 19px;

        letter-spacing: 2px;

        border-bottom:
            1px solid rgba(180, 130, 79, 0.20);

        padding-bottom: 14px;

        margin-bottom: 22px;
    }

    .song-card {
        background:
            linear-gradient(
                135deg,
                rgba(248, 239, 221, 0.98),
                rgba(229, 210, 178, 0.98)
            );

        border:
            1px solid rgba(116, 79, 44, 0.40);

        padding: 20px;

        margin-bottom: 16px;

        box-shadow:
            0 12px 30px rgba(0, 0, 0, 0.20);
    }

    .song-name {
        color: #392519;

        font-family:
            Georgia,
            "Malgun Gothic",
            sans-serif;

        font-size: 20px;

        font-weight: 600;

        margin-bottom: 7px;
    }

    .song-artist {
        color: #705039;

        font-family:
            Georgia,
            "Malgun Gothic",
            sans-serif;

        font-size: 14px;

        margin-bottom: 5px;
    }

    .song-album {
        color: #876b53;

        font-family:
            Georgia,
            "Malgun Gothic",
            sans-serif;

        font-size: 13px;
    }

    .song-meta {
        color: #987b60;

        font-size: 11px;

        margin-top: 9px;
    }

    .apple-link {
        display: inline-block;

        margin-top: 12px;

        color: #765238 !important;

        text-decoration: none !important;

        border-bottom:
            1px solid rgba(118, 82, 56, 0.35);

        padding-bottom: 2px;

        font-size: 12px;
    }

    .apple-link:hover {
        color: #4c301e !important;
    }

    /* -----------------------------------------------------
       검색 결과 없음 / 오류
    ----------------------------------------------------- */

    .notice-box {
        margin-top: 30px;

        padding: 28px;

        border:
            1px solid rgba(157, 112, 72, 0.35);

        background:
            rgba(239, 221, 190, 0.06);

        color: #b89b80;

        text-align: center;

        font-family:
            Georgia,
            "Malgun Gothic",
            sans-serif;

        line-height: 1.9;
    }

    /* -----------------------------------------------------
       추천 placeholder
    ----------------------------------------------------- */

    .coming-wrap {
        min-height: 80vh;

        display: flex;

        justify-content: center;

        align-items: center;

        flex-direction: column;
    }

    .coming-title {
        color: #d5a56d;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size: 46px;

        letter-spacing: 7px;
    }

    .coming-text {
        color: #8d715d;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        margin-top: 18px;

        letter-spacing: 2px;
    }

    /* -----------------------------------------------------
       모바일
    ----------------------------------------------------- */

    @media (max-width: 800px) {

        .paper-button-area {
            flex-direction: column;

            align-items: center;
        }

        .letter {
            padding:
                55px 40px
                50px 40px;

            min-height: 600px;
        }

        .letter-body {
            font-size: 15px;
        }

        .welcome-title {
            letter-spacing: 5px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# Apple iTunes Search API
# =========================================================

ITUNES_SEARCH_URL = "https://itunes.apple.com/search"
ITUNES_LOOKUP_URL = "https://itunes.apple.com/lookup"


def normalize_text(text):
    """
    검색 비교용 정규화.
    대소문자, 공백, 일부 특수문자를 제거해서 비교한다.
    """

    if not text:
        return ""

    text = str(text).lower()

    # 괄호 안의 일부 부가 정보 제거에 도움
    text = re.sub(r"\([^)]*\)", "", text)

    # 공백 제거
    text = re.sub(r"\s+", "", text)

    # 특수문자 제거
    text = re.sub(
        r"[^0-9a-z가-힣ぁ-んァ-ン一-龥]",
        "",
        text
    )

    return text


def apple_api_request(url, params):
    """
    Apple API 요청.
    requests 라이브러리를 사용하지 않고
    Python 기본 urllib만 사용.
    """

    query = urllib.parse.urlencode(params)

    full_url = url + "?" + query

    request = urllib.request.Request(
        full_url,
        headers={
            "User-Agent":
                "Mozilla/5.0 record-room-streamlit-app"
        }
    )

    try:

        with urllib.request.urlopen(
            request,
            timeout=12
        ) as response:

            raw = response.read()

            data = json.loads(
                raw.decode("utf-8")
            )

            return data

    except urllib.error.HTTPError as e:

        raise Exception(
            f"Apple API HTTP 오류: {e.code}"
        )

    except urllib.error.URLError:

        raise Exception(
            "Apple Music/iTunes 서버에 연결할 수 없습니다."
        )

    except Exception as e:

        raise Exception(
            f"검색 데이터를 불러오지 못했습니다: {e}"
        )


# =========================================================
# 정확한 아티스트 검색
# =========================================================

@st.cache_data(ttl=600, show_spinner=False)
def find_exact_artist(query):

    data = apple_api_request(
        ITUNES_SEARCH_URL,
        {
            "term": query,
            "country": "KR",
            "media": "music",
            "entity": "musicArtist",
            "limit": 20,
            "lang": "ko_kr"
        }
    )

    artists = data.get(
        "results",
        []
    )

    normalized_query = normalize_text(query)

    # -----------------------------------------------------
    # 1순위: 아티스트 이름 완전 일치
    # -----------------------------------------------------

    for artist in artists:

        artist_name = artist.get(
            "artistName",
            ""
        )

        if normalize_text(
            artist_name
        ) == normalized_query:

            return artist

    # -----------------------------------------------------
    # 2순위: 아주 가까운 경우
    # -----------------------------------------------------

    for artist in artists:

        artist_name = artist.get(
            "artistName",
            ""
        )

        normalized_artist = normalize_text(
            artist_name
        )

        if (
            normalized_query
            and normalized_artist
            and (
                normalized_query
                in normalized_artist
                or normalized_artist
                in normalized_query
            )
        ):
            return artist

    return None


# =========================================================
# 아티스트의 곡 가져오기
# =========================================================

@st.cache_data(ttl=600, show_spinner=False)
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

        # artist 자체 정보는 제외
        if item.get("wrapperType") != "track":
            continue

        if item.get("kind") != "song":
            continue

        songs.append(item)

    return songs


# =========================================================
# 정확한 곡 제목 검색
# =========================================================

@st.cache_data(ttl=600, show_spinner=False)
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

    normalized_query = normalize_text(query)

    scored = []

    for song in results:

        if song.get("kind") != "song":
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

        # -------------------------------------------------
        # 검색 정확도 점수
        # -------------------------------------------------

        score = 0

        # 제목 완전 일치
        if normalized_track == normalized_query:
            score += 1000

        # 제목이 검색어로 시작
        elif normalized_track.startswith(
            normalized_query
        ):
            score += 500

        # 제목에 검색어 포함
        elif normalized_query in normalized_track:
            score += 250

        else:
            # 제목이 완전히 무관하면 제외
            continue

        # 같은 제목이면 아티스트 이름도 비교
        artist_name = song.get(
            "artistName",
            ""
        )

        if normalize_text(
            artist_name
        ) == normalized_query:
            score += 20

        scored.append(
            (
                score,
                song
            )
        )

    # 정확도가 높은 순서
    scored.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return [
        song
        for score, song in scored
    ][:30]


# =========================================================
# 검색 메인 함수
# =========================================================

@st.cache_data(ttl=600, show_spinner=False)
def search_music(query):

    query = query.strip()

    if not query:
        return {
            "type": "",
            "artist": None,
            "songs": []
        }

    # -----------------------------------------------------
    # STEP 1
    # 검색어가 정확한 아티스트인지 먼저 확인
    # -----------------------------------------------------

    artist = find_exact_artist(query)

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
    # STEP 2
    # 정확한 아티스트가 아니라면 곡 제목 검색
    # -----------------------------------------------------

    songs = find_song_results(query)

    return {
        "type": "song",
        "artist": None,
        "songs": songs
    }


# =========================================================
# Sidebar
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand">

            <div class="sidebar-brand-title">
                RECORD ROOM
            </div>

            <div class="sidebar-brand-sub">
                A ROOM FOR MUSIC
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "MAIN",
        key="sidebar_main"
    ):

        st.session_state.page = "main"

        st.session_state.main_entered = False

        st.session_state.choice_mode = "select"

        st.rerun()

    st.markdown(
        '<div class="sidebar-line"></div>',
        unsafe_allow_html=True
    )

    if st.button(
        "CHOICE",
        key="sidebar_choice"
    ):

        st.session_state.page = "choice"

        st.session_state.choice_mode = "select"

        st.rerun()

    st.markdown(
        '<div class="sidebar-line"></div>',
        unsafe_allow_html=True
    )

    if st.button(
        "—",
        key="sidebar_empty"
    ):

        st.session_state.page = "unknown"

        st.rerun()

    st.markdown(
        '<div class="sidebar-line"></div>',
        unsafe_allow_html=True
    )


# =========================================================
# MAIN PAGE
# =========================================================

if st.session_state.page == "main":

    # -----------------------------------------------------
    # 처음 MAIN 화면
    # -----------------------------------------------------

    if not st.session_state.main_entered:

        st.markdown(
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
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="enter-space">',
            unsafe_allow_html=True
        )

        if st.button(
            "ENTER ROOM",
            key="enter_room"
        ):

            st.session_state.main_entered = True

            st.rerun()

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

    # -----------------------------------------------------
    # ENTER ROOM 이후 편지
    # -----------------------------------------------------

    else:

        st.markdown(
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
                            누군가에게는 아직 만나지 못한 새로운 장면일지도 모릅니다.
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
            """,
            unsafe_allow_html=True
        )


# =========================================================
# CHOICE PAGE
# =========================================================

elif st.session_state.page == "choice":

    # =====================================================
    # CHOICE 선택 화면
    # =====================================================

    if st.session_state.choice_mode == "select":

        st.markdown(
            """
            <div class="choice-wrap">

                <div class="choice-heading">
                    CHOICE
                </div>

                <div class="choice-subheading">
                    WHAT WOULD YOU LIKE TO DO?
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="paper-button-area">',
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
            '</div>',
            unsafe_allow_html=True
        )


    # =====================================================
    # 노래 듣기
    # =====================================================

    elif st.session_state.choice_mode == "listen":

        st.markdown(
            """
            <div class="listen-wrap">

                <div class="listen-heading">
                    LISTEN
                </div>

                <div class="listen-description">
                    가수 이름 또는 곡 제목을 검색해보세요.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        # -------------------------------------------------
        # 검색 영역
        # -------------------------------------------------

        search_col1, search_col2 = st.columns(
            [5, 1],
            gap="medium"
        )

        with search_col1:

            query = st.text_input(
                "검색",
                placeholder="가수 이름 또는 곡 제목을 입력하세요",
                label_visibility="collapsed",
                key="music_search_input"
            )

        with search_col2:

            st.markdown(
                '<div class="search-button">',
                unsafe_allow_html=True
            )

            search_clicked = st.button(
                "SEARCH",
                key="music_search_button"
            )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )


        # -------------------------------------------------
        # 검색 실행
        # -------------------------------------------------

        if search_clicked:

            clean_query = query.strip()

            if not clean_query:

                st.session_state.search_results = []

                st.session_state.search_type = ""

                st.session_state.search_error = (
                    "검색어를 입력해주세요."
                )

            else:

                try:

                    with st.spinner(
                        "record room에서 음악을 찾는 중..."
                    ):

                        search_data = search_music(
                            clean_query
                        )

                    st.session_state.search_results = (
                        search_data["songs"]
                    )

                    st.session_state.search_type = (
                        search_data["type"]
                    )

                    st.session_state.search_artist = (
                        search_data["artist"]
                    )

                    st.session_state.search_query = (
                        clean_query
                    )

                    st.session_state.search_error = ""

                except Exception as e:

                    st.session_state.search_results = []

                    st.session_state.search_error = str(e)


        # -------------------------------------------------
        # 검색 오류
        # -------------------------------------------------

        if st.session_state.search_error:

            st.markdown(
                f"""
                <div class="notice-box">
                    {st.session_state.search_error}
                </div>
                """,
                unsafe_allow_html=True
            )


        # -------------------------------------------------
        # 검색 결과
        # -------------------------------------------------

        results = st.session_state.search_results

        if results:

            search_type = (
                st.session_state.search_type
            )

            searched = (
                st.session_state.search_query
            )

            # -------------------------------------------------
            # 아티스트 검색 결과
            # -------------------------------------------------

            if search_type == "artist":

                artist = st.session_state.get(
                    "search_artist",
                    None
                )

                artist_name = (
                    artist.get(
                        "artistName",
                        searched
                    )
                    if artist
                    else searched
                )

                st.markdown(
                    f"""
                    <div class="result-heading">
                        {artist_name} — SONGS
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # -------------------------------------------------
            # 곡 검색 결과
            # -------------------------------------------------

            else:

                st.markdown(
                    f"""
                    <div class="result-heading">
                        SEARCH RESULTS FOR "{searched}"
                    </div>
                    """,
                    unsafe_allow_html=True
                )


            # -------------------------------------------------
            # 곡 카드
            # -------------------------------------------------

            for song in results:

                track_name = song.get(
                    "trackName",
                    "Unknown Song"
                )

                artist_name = song.get(
                    "artistName",
                    "Unknown Artist"
                )

                album_name = song.get(
                    "collectionName",
                    "Unknown Album"
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

                    release_date = (
                        release_date[:10]
                    )

                track_url = song.get(
                    "trackViewUrl",
                    ""
                )

                preview_url = song.get(
                    "previewUrl",
                    ""
                )


                # 카드 시작

                card_col1, card_col2 = st.columns(
                    [1, 5],
                    gap="medium"
                )

                with card_col1:

                    if artwork:

                        st.image(
                            artwork,
                            width=100
                        )

                with card_col2:

                    st.markdown(
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

                            {
                                f'<a class="apple-link" href="{track_url}" target="_blank">OPEN IN APPLE MUSIC / ITUNES ↗</a>'
                                if track_url
                                else ""
                            }

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # Apple의 30초 preview
                    if preview_url:

                        st.audio(
                            preview_url
                        )

                st.markdown(
                    "<div style='height:10px'></div>",
                    unsafe_allow_html=True
                )


        # -------------------------------------------------
        # 검색 결과 없음
        # -------------------------------------------------

        elif (
            st.session_state.search_query
            and not st.session_state.search_error
        ):

            st.markdown(
                f"""
                <div class="notice-box">

                    "{st.session_state.search_query}"에
                    정확히 일치하거나 관련된 음악을 찾지 못했습니다.

                    <br><br>

                    가수 이름이나 곡 제목을
                    조금 더 정확하게 입력해보세요.

                </div>
                """,
                unsafe_allow_html=True
            )


    # =====================================================
    # 추천받기
    # =====================================================

    elif st.session_state.choice_mode == "recommend":

        st.markdown(
            """
            <div class="coming-wrap">

                <div class="coming-title">
                    COMING SOON
                </div>

                <div class="coming-text">
                    YOUR NEXT SONG IS WAITING
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# 기타 페이지
# =========================================================

else:

    st.markdown(
        """
        <div class="coming-wrap">

            <div class="coming-title">
                —
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )
