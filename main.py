import streamlit as st
import urllib.parse
import urllib.request
import urllib.error
import json
import re
from html import escape


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

if "search_error" not in st.session_state:
    st.session_state.search_error = ""


# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

/* =====================================================
   전체 배경
===================================================== */

html,
body,
[data-testid="stAppViewContainer"] {
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
    padding-bottom: 50px !important;
    max-width: 1400px !important;
}


/* =====================================================
   SIDEBAR
===================================================== */

[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #170d09 0%,
            #120906 55%,
            #0d0705 100%
        ) !important;

    border-right:
        1px solid rgba(190,145,92,0.22);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 35px;
}

.sidebar-title {
    color: #d9a96f;
    font-family: Georgia, "Times New Roman", serif;
    font-size: 23px;
    letter-spacing: 5px;
    text-align: center;
    margin-top: 5px;
}

.sidebar-subtitle {
    color: #805c3d;
    font-family: Georgia, "Times New Roman", serif;
    font-size: 8px;
    letter-spacing: 4px;
    text-align: center;
    margin-top: 9px;
    margin-bottom: 62px;
}

.sidebar-divider {
    width: 67px;
    height: 1px;
    background: rgba(168,115,69,0.18);
    margin: 2px 0 22px 20px;
}

[data-testid="stSidebar"] .stButton {
    width: 100%;
}

[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
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
        15px 12px !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    color: #e1b67c !important;

    background:
        linear-gradient(
            90deg,
            rgba(190,137,82,0.10),
            transparent
        ) !important;
}


/* =====================================================
   MAIN 첫 화면
===================================================== */

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

    font-family:
        Georgia,
        "Times New Roman",
        serif;

    font-size: 13px;
    letter-spacing: 5px;

    margin-bottom: 20px;
}

.welcome-title {
    color: #dcae73;

    font-family:
        Georgia,
        "Times New Roman",
        serif;

    font-size:
        clamp(58px, 7vw, 100px);

    font-weight: 400;

    letter-spacing: 8px;

    line-height: 1.05;

    text-shadow:
        0 2px 18px rgba(0,0,0,0.45);
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

    margin: 27px auto;
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

.enter-holder {
    display: flex;
    justify-content: center;

    margin-top: -120px;

    position: relative;
    z-index: 10;
}

.enter-holder .stButton > button {
    min-width: 190px !important;
    height: 52px !important;

    background: transparent !important;

    border:
        1px solid #936b45 !important;

    color:
        #d6aa75 !important;

    border-radius: 0 !important;

    font-family:
        Georgia,
        "Times New Roman",
        serif !important;

    letter-spacing: 4px !important;
}

.enter-holder .stButton > button:hover {
    background:
        rgba(197,145,88,0.10) !important;

    border-color:
        #d5a66c !important;

    color:
        #efd0a0 !important;
}


/* =====================================================
   LETTER
===================================================== */

.letter-area {
    min-height: 92vh;

    display: flex;
    justify-content: center;
    align-items: center;

    padding: 35px 20px;
}

.letter-paper {
    width: min(1080px, 90vw);
    min-height: 650px;

    box-sizing: border-box;

    padding:
        72px 90px;

    background:
        radial-gradient(
            ellipse at center,
            #f7eedb 0%,
            #eee0c4 62%,
            #e2cfac 100%
        );

    border:
        1px solid rgba(115,76,39,0.45);

    box-shadow:
        0 30px 70px rgba(0,0,0,0.45),
        inset 0 0 45px rgba(99,62,27,0.08);

    position: relative;
}

.letter-paper::before {
    content: "";

    position: absolute;
    inset: 15px;

    border:
        1px solid rgba(117,80,42,0.18);

    pointer-events: none;
}

.letter-date {
    color: #856344;

    text-align: right;

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

.letter-sign {
    color: #604531;

    font-family:
        Georgia,
        "Times New Roman",
        serif;

    text-align: right;

    font-size: 16px;

    line-height: 1.9;

    margin-top: 55px;
}


/* =====================================================
   CHOICE
===================================================== */

.choice-area {
    min-height: 90vh;

    display: flex;
    flex-direction: column;

    justify-content: center;
    align-items: center;

    text-align: center;
}

.choice-title {
    color: #d5a56d;

    font-family:
        Georgia,
        "Times New Roman",
        serif;

    font-size: 44px;

    letter-spacing: 6px;

    margin-bottom: 14px;
}

.choice-subtitle {
    color: #96765d;

    font-family:
        Georgia,
        "Times New Roman",
        serif;

    font-size: 14px;

    letter-spacing: 2px;

    margin-bottom: 45px;
}

.choice-buttons .stButton > button {
    min-height: 95px !important;

    background:
        radial-gradient(
            ellipse at center,
            #fbf3e3 0%,
            #ead9b9 100%
        ) !important;

    color: #4c3424 !important;

    border:
        1px solid rgba(111,75,42,0.45)
        !important;

    border-radius: 2px !important;

    font-family:
        Georgia,
        "Times New Roman",
        serif !important;

    font-size: 20px !important;

    letter-spacing: 3px !important;

    box-shadow:
        0 15px 35px rgba(0,0,0,0.25),
        inset 0 0 20px rgba(104,67,32,0.08)
        !important;
}

.choice-buttons .stButton > button:hover {
    transform: translateY(-4px);

    border-color:
        #a77a4e !important;
}


/* =====================================================
   LISTEN
===================================================== */

.listen-container {
    width: min(1100px, 90vw);

    margin:
        65px auto 30px auto;
}

.listen-title {
    color: #d5a56d;

    font-family:
        Georgia,
        "Times New Roman",
        serif;

    font-size: 42px;

    letter-spacing: 5px;

    text-align: center;
}

.listen-subtitle {
    color: #9d8069;

    font-family:
        Georgia,
        "Times New Roman",
        serif;

    font-size: 14px;

    letter-spacing: 1px;

    text-align: center;

    margin-top: 12px;

    margin-bottom: 38px;
}


/* =====================================================
   SEARCH
===================================================== */

div[data-testid="stTextInput"] input {
    background:
        #f7eedb !important;

    color:
        #493528 !important;

    border:
        1px solid #8d6746 !important;

    border-radius:
        2px !important;

    height:
        52px !important;

    font-family:
        "Malgun Gothic",
        Arial,
        sans-serif !important;

    font-size:
        15px !important;
}

.search-button .stButton > button {
    height: 52px !important;
    width: 100% !important;

    background:
        #25160f !important;

    color:
        #d8aa73 !important;

    border:
        1px solid #946b45 !important;

    border-radius:
        2px !important;

    font-family:
        Georgia,
        "Times New Roman",
        serif !important;

    letter-spacing:
        3px !important;
}


/* =====================================================
   SEARCH RESULT
===================================================== */

.result-title {
    color: #cda072;

    font-family:
        Georgia,
        "Times New Roman",
        serif;

    font-size: 19px;

    letter-spacing: 2px;

    border-bottom:
        1px solid rgba(180,130,79,0.20);

    padding-bottom: 14px;

    margin-top: 50px;
    margin-bottom: 22px;
}

.song-info {
    background:
        linear-gradient(
            135deg,
            #f8efdd,
            #e5d2b2
        );

    border:
        1px solid rgba(116,79,44,0.40);

    padding:
        20px;

    min-height:
        130px;

    box-shadow:
        0 12px 30px rgba(0,0,0,0.20);
}

.song-title {
    color: #392519;

    font-family:
        "Malgun Gothic",
        Arial,
        sans-serif;

    font-size: 20px;

    font-weight: 600;

    margin-bottom: 8px;
}

.song-artist {
    color: #705039;

    font-size: 14px;

    margin-bottom: 5px;
}

.song-album {
    color: #876b53;

    font-size: 13px;
}

.song-release {
    color: #987b60;

    font-size: 11px;

    margin-top: 9px;
}

.song-link {
    color: #765238 !important;

    font-size: 12px;

    text-decoration: none !important;

    display: inline-block;

    margin-top: 12px;
}

.no-result {
    color: #b89b80;

    text-align: center;

    border:
        1px solid rgba(157,112,72,0.35);

    padding: 30px;

    margin-top: 35px;

    line-height: 1.9;
}


/* =====================================================
   COMING
===================================================== */

.coming-area {
    min-height: 80vh;

    display: flex;

    flex-direction: column;

    justify-content: center;

    align-items: center;
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

.coming-subtitle {
    color: #8d715d;

    margin-top: 18px;

    letter-spacing: 2px;
}


/* =====================================================
   MOBILE
===================================================== */

@media (max-width: 800px) {

    .letter-paper {
        padding: 50px 35px;
    }

    .letter-body {
        font-size: 15px;
    }

    .choice-title {
        font-size: 36px;
    }

}

</style>
""")


# =========================================================
# APPLE API
# =========================================================

SEARCH_URL = "https://itunes.apple.com/search"


def apple_request(params):
    """
    Apple iTunes Search API 호출
    """

    url = SEARCH_URL + "?" + urllib.parse.urlencode(params)

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent":
                "Mozilla/5.0"
        }
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=15
        ) as response:

            data = response.read().decode(
                "utf-8"
            )

            return json.loads(data)

    except urllib.error.HTTPError as e:

        raise Exception(
            f"Apple API 오류: HTTP {e.code}"
        )

    except urllib.error.URLError:

        raise Exception(
            "Apple 음악 검색 서버에 연결하지 못했습니다."
        )

    except json.JSONDecodeError:

        raise Exception(
            "Apple에서 올바른 검색 데이터를 받지 못했습니다."
        )


# =========================================================
# 문자열 정리
# =========================================================

def normalize(text):

    if not text:
        return ""

    text = str(text).lower()

    text = text.replace(
        " ",
        ""
    )

    text = re.sub(
        r"[^0-9a-z가-힣]",
        "",
        text
    )

    return text


# =========================================================
# 가수 검색
# =========================================================

@st.cache_data(
    ttl=600,
    show_spinner=False
)
def search_artist(query):

    data = apple_request(
        {
            "term": query,
            "country": "KR",
            "media": "music",
            "entity": "song",
            "attribute": "artistTerm",
            "limit": 50
        }
    )

    results = data.get(
        "results",
        []
    )

    query_normalized = normalize(
        query
    )

    # ---------------------------------------------
    # 1. 아티스트 이름 완전 일치
    # ---------------------------------------------

    exact = []

    for item in results:

        artist = item.get(
            "artistName",
            ""
        )

        if normalize(
            artist
        ) == query_normalized:

            exact.append(item)

    if exact:
        return exact


    # ---------------------------------------------
    # 2. Apple이 반환한 가장 가까운 artist
    # ---------------------------------------------

    artists = []

    seen_artists = set()

    for item in results:

        artist = item.get(
            "artistName",
            ""
        )

        artist_key = normalize(
            artist
        )

        if not artist_key:
            continue

        if artist_key in seen_artists:
            continue

        seen_artists.add(
            artist_key
        )

        # 검색어가 artist 이름 안에 포함되는 경우
        if query_normalized in artist_key:

            artists.append(
                artist
            )

    if len(artists) == 1:

        target = artists[0]

        return [
            item
            for item in results
            if item.get(
                "artistName",
                ""
            ) == target
        ]

    return []


# =========================================================
# 곡 제목 검색
# =========================================================

@st.cache_data(
    ttl=600,
    show_spinner=False
)
def search_song(query):

    data = apple_request(
        {
            "term": query,
            "country": "KR",
            "media": "music",
            "entity": "song",
            "attribute": "songTerm",
            "limit": 50
        }
    )

    results = data.get(
        "results",
        []
    )

    query_normalized = normalize(
        query
    )

    exact = []
    partial = []

    for item in results:

        if item.get(
            "kind"
        ) != "song":

            continue

        track_name = item.get(
            "trackName",
            ""
        )

        track_normalized = normalize(
            track_name
        )

        if not track_normalized:
            continue

        if track_normalized == query_normalized:

            exact.append(item)

        elif query_normalized in track_normalized:

            partial.append(item)

    if exact:
        return exact[:30]

    return partial[:30]


# =========================================================
# 전체 음악 검색
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
            "results": []
        }


    # ---------------------------------------------
    # 먼저 가수 검색
    # ---------------------------------------------

    artist_results = search_artist(
        query
    )

    if artist_results:

        return {
            "type": "artist",
            "results": artist_results
        }


    # ---------------------------------------------
    # 가수가 아니면 곡 제목 검색
    # ---------------------------------------------

    song_results = search_song(
        query
    )

    return {
        "type": "song",
        "results": song_results
    }


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    # HTML을 전혀 중첩하지 않고 한 줄로 출력
    st.markdown(
        '<div class="sidebar-title">RECORD ROOM</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">A ROOM FOR MUSIC</div>',
        unsafe_allow_html=True
    )


    if st.button(
        "MAIN",
        key="side_main"
    ):

        st.session_state.page = "main"

        st.session_state.main_entered = False

        st.session_state.choice_mode = "select"

        st.rerun()


    st.markdown(
        '<div class="sidebar-divider"></div>',
        unsafe_allow_html=True
    )


    if st.button(
        "CHOICE",
        key="side_choice"
    ):

        st.session_state.page = "choice"

        st.session_state.choice_mode = "select"

        st.rerun()


    st.markdown(
        '<div class="sidebar-divider"></div>',
        unsafe_allow_html=True
    )


    if st.button(
        "—",
        key="side_empty"
    ):

        st.session_state.page = "unknown"

        st.rerun()


    st.markdown(
        '<div class="sidebar-divider"></div>',
        unsafe_allow_html=True
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
            '<div class="welcome-area">'
            '<div class="welcome-small">WELCOME TO</div>'
            '<div class="welcome-title">record room</div>'
            '<div class="welcome-line"></div>'
            '<div class="welcome-description">'
            '음악을 듣고, 발견하고,<br>'
            '잠시 머무는 작은 방'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="enter-holder">',
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
    # LETTER
    # -----------------------------------------------------

    else:

        st.markdown(
            '<div class="letter-area">'
            '<div class="letter-paper">'
            '<div class="letter-date">RECORD ROOM</div>'
            '<div class="letter-title">Dear visitor,</div>'
            '<div class="letter-body">'
            '<p>이곳에 들어온 것을 환영합니다.</p>'
            '<p>'
            '이 방에는 수많은 음악이 있습니다. '
            '누군가에게는 오래된 기억이고, '
            '누군가에게는 아직 만나지 못한 새로운 장면일지도 모릅니다.'
            '</p>'
            '<p>'
            '오늘 어떤 음악을 듣게 될지는 '
            '아직 아무도 알 수 없습니다.'
            '</p>'
            '<p>'
            '천천히 둘러보세요. '
            '듣고 싶은 음악을 찾아도 좋고, '
            '우연히 새로운 음악을 발견해도 좋습니다.'
            '</p>'
            '<p>'
            '이곳에서 잠시, '
            '당신만의 음악을 찾아가길 바랍니다.'
            '</p>'
            '</div>'
            '<div class="letter-sign">'
            'from,<br>'
            'record room'
            '</div>'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )


# =========================================================
# CHOICE
# =========================================================

elif st.session_state.page == "choice":

    # -----------------------------------------------------
    # CHOICE MENU
    # -----------------------------------------------------

    if st.session_state.choice_mode == "select":

        st.markdown(
            '<div class="choice-area">'
            '<div class="choice-title">CHOICE</div>'
            '<div class="choice-subtitle">'
            'WHAT WOULD YOU LIKE TO DO?'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="choice-buttons">',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(
            2,
            gap="large"
        )

        with col1:

            if st.button(
                "노래 듣기",
                key="listen_button",
                use_container_width=True
            ):

                st.session_state.choice_mode = "listen"

                st.rerun()

        with col2:

            if st.button(
                "추천받기",
                key="recommend_button",
                use_container_width=True
            ):

                st.session_state.choice_mode = "recommend"

                st.rerun()

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


    # =====================================================
    # LISTEN
    # =====================================================

    elif st.session_state.choice_mode == "listen":

        st.markdown(
            '<div class="listen-container">'
            '<div class="listen-title">LISTEN</div>'
            '<div class="listen-subtitle">'
            '가수 이름 또는 곡 제목을 검색해보세요.'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )


        # ---------------------------------------------
        # 검색창
        # ---------------------------------------------

        col1, col2 = st.columns(
            [5, 1],
            gap="medium"
        )


        with col1:

            query = st.text_input(
                "music search",
                placeholder=
                    "가수 이름 또는 곡 제목을 입력하세요",
                label_visibility="collapsed",
                key="music_input"
            )


        with col2:

            st.markdown(
                '<div class="search-button">',
                unsafe_allow_html=True
            )

            search_clicked = st.button(
                "SEARCH",
                key="search_button",
                use_container_width=True
            )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )


        # ---------------------------------------------
        # 검색 실행
        # ---------------------------------------------

        if search_clicked:

            query = query.strip()

            if not query:

                st.session_state.search_results = []

                st.session_state.search_query = ""

                st.session_state.search_type = ""

                st.session_state.search_error = (
                    "검색어를 입력해주세요."
                )

            else:

                try:

                    with st.spinner(
                        "음악을 찾는 중..."
                    ):

                        result = search_music(
                            query
                        )

                    st.session_state.search_results = (
                        result["results"]
                    )

                    st.session_state.search_type = (
                        result["type"]
                    )

                    st.session_state.search_query = (
                        query
                    )

                    st.session_state.search_error = ""

                except Exception as e:

                    st.session_state.search_results = []

                    st.session_state.search_query = query

                    st.session_state.search_type = ""

                    st.session_state.search_error = str(e)


        # ---------------------------------------------
        # 오류
        # ---------------------------------------------

        if st.session_state.search_error:

            st.markdown(
                '<div class="no-result">'
                + escape(
                    st.session_state.search_error
                )
                + '</div>',
                unsafe_allow_html=True
            )


        # ---------------------------------------------
        # 결과
        # ---------------------------------------------

        results = st.session_state.search_results

        if results:

            searched = (
                st.session_state.search_query
            )

            search_type = (
                st.session_state.search_type
            )


            if search_type == "artist":

                # 첫 번째 결과의 artistName을
                # 실제 표시 제목으로 사용
                artist_name = results[0].get(
                    "artistName",
                    searched
                )

                title_text = (
                    escape(artist_name)
                    + " — SONGS"
                )

            else:

                title_text = (
                    'SEARCH RESULTS FOR "'
                    + escape(searched)
                    + '"'
                )


            st.markdown(
                '<div class="result-title">'
                + title_text
                + '</div>',
                unsafe_allow_html=True
            )


            # -----------------------------------------
            # 곡 표시
            # -----------------------------------------

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


                artwork = song.get(
                    "artworkUrl100",
                    ""
                )

                track_url = song.get(
                    "trackViewUrl",
                    ""
                )

                preview_url = song.get(
                    "previewUrl",
                    ""
                )


                image_col, info_col = st.columns(
                    [1, 6],
                    gap="medium"
                )


                with image_col:

                    if artwork:

                        st.image(
                            artwork,
                            width=110
                        )


                with info_col:

                    link_html = ""

                    if track_url:

                        safe_url = escape(
                            track_url,
                            quote=True
                        )

                        link_html = (
                            '<a '
                            'class="song-link" '
                            'href="'
                            + safe_url
                            + '" '
                            'target="_blank">'
                            'OPEN IN APPLE MUSIC / ITUNES ↗'
                            '</a>'
                        )


                    st.markdown(
                        '<div class="song-info">'
                        '<div class="song-title">'
                        + track_name
                        + '</div>'
                        '<div class="song-artist">'
                        + artist_name
                        + '</div>'
                        '<div class="song-album">'
                        + album_name
                        + '</div>'
                        '<div class="song-release">'
                        'RELEASE · '
                        + release_date
                        + '</div>'
                        + link_html
                        + '</div>',
                        unsafe_allow_html=True
                    )


                    if preview_url:

                        st.audio(
                            preview_url
                        )


                st.markdown(
                    '<div style="height:18px;"></div>',
                    unsafe_allow_html=True
                )


        # ---------------------------------------------
        # 결과 없음
        # ---------------------------------------------

        elif (
            st.session_state.search_query
            and not st.session_state.search_error
        ):

            st.markdown(
                '<div class="no-result">'
                '"'
                + escape(
                    st.session_state.search_query
                )
                + '"'
                '<br>'
                '에 해당하는 음악을 Apple에서 찾지 못했습니다.'
                '<br><br>'
                '가수 이름이나 곡 제목을 정확하게 입력해보세요.'
                '</div>',
                unsafe_allow_html=True
            )


    # =====================================================
    # RECOMMEND
    # =====================================================

    elif st.session_state.choice_mode == "recommend":

        st.markdown(
            '<div class="coming-area">'
            '<div class="coming-title">'
            'COMING SOON'
            '</div>'
            '<div class="coming-subtitle">'
            'YOUR NEXT SONG IS WAITING'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )


# =========================================================
# EMPTY PAGE
# =========================================================

else:

    st.markdown(
        '<div class="coming-area">'
        '<div class="coming-title">—</div>'
        '</div>',
        unsafe_allow_html=True
    )
