import streamlit as st
import urllib.parse
import urllib.request
import json


# =========================================================
# RECORD ROOM
# =========================================================

st.set_page_config(
    page_title="record room",
    page_icon="♢",
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


# =========================================================
# APPLE iTUNES SEARCH
# =========================================================

@st.cache_data(ttl=600)
def apple_search_songs(query):
    """
    Apple iTunes Search API를 이용해
    노래 제목 / 가수명 검색
    """

    query = query.strip()

    if not query:
        return []

    # -----------------------------------------------------
    # 1. 먼저 가수 검색
    # -----------------------------------------------------

    artist_params = {
        "term": query,
        "country": "KR",
        "media": "music",
        "entity": "musicArtist",
        "limit": 5,
        "lang": "ko_kr"
    }

    artist_url = (
        "https://itunes.apple.com/search?"
        + urllib.parse.urlencode(artist_params)
    )

    artists = []

    try:
        with urllib.request.urlopen(
            artist_url,
            timeout=10
        ) as response:

            artist_data = json.loads(
                response.read().decode("utf-8")
            )

            artists = artist_data.get("results", [])

    except Exception:
        artists = []


    # -----------------------------------------------------
    # 2. 가수 결과가 있으면 해당 가수들의 곡 검색
    # -----------------------------------------------------

    artist_results = []

    for artist in artists[:3]:

        artist_id = artist.get("artistId")

        if not artist_id:
            continue

        lookup_params = {
            "id": artist_id,
            "entity": "song",
            "country": "KR",
            "limit": 20,
            "sort": "recent"
        }

        lookup_url = (
            "https://itunes.apple.com/lookup?"
            + urllib.parse.urlencode(lookup_params)
        )

        try:

            with urllib.request.urlopen(
                lookup_url,
                timeout=10
            ) as response:

                lookup_data = json.loads(
                    response.read().decode("utf-8")
                )

                lookup_results = lookup_data.get(
                    "results",
                    []
                )

                for item in lookup_results:

                    if item.get("kind") == "song":
                        artist_results.append(item)

        except Exception:
            continue


    # -----------------------------------------------------
    # 3. 일반 노래 검색
    # -----------------------------------------------------

    song_params = {
        "term": query,
        "country": "KR",
        "media": "music",
        "entity": "song",
        "limit": 30,
        "lang": "ko_kr"
    }

    song_url = (
        "https://itunes.apple.com/search?"
        + urllib.parse.urlencode(song_params)
    )

    song_results = []

    try:

        with urllib.request.urlopen(
            song_url,
            timeout=10
        ) as response:

            song_data = json.loads(
                response.read().decode("utf-8")
            )

            song_results = song_data.get(
                "results",
                []
            )

    except Exception:
        song_results = []


    # -----------------------------------------------------
    # 4. 결과 합치기 + 중복 제거
    # -----------------------------------------------------

    combined = []

    seen = set()

    for item in artist_results + song_results:

        track_id = item.get("trackId")

        if not track_id:
            continue

        if track_id in seen:
            continue

        seen.add(track_id)

        combined.append(item)


    return combined[:40]


# =========================================================
# GLOBAL CSS
# =========================================================

st.markdown(
    """
<style>

/* ========================================================
   전체 화면
======================================================== */

.stApp {

    background:
        radial-gradient(
            circle at 52% 35%,
            #3d291d 0%,
            #2d1d14 35%,
            #1c110c 72%,
            #100906 100%
        );

    color: #e5d0b1;
}

.main .block-container {

    max-width: 1450px;

    padding-top: 0 !important;
    padding-bottom: 0 !important;
}


/* ========================================================
   SIDEBAR
======================================================== */

section[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            #160d09 0%,
            #1b100b 50%,
            #100906 100%
        );

    border-right:
        1px solid rgba(188, 142, 91, 0.22);
}

section[data-testid="stSidebar"] > div {

    padding-top: 3.2rem;
}


/* 로고 */

.sidebar-logo {

    text-align: center;

    color: #d8b17f;

    font-family:
        Georgia,
        "Times New Roman",
        serif;

    font-size: 21px;

    letter-spacing: 4px;

    margin-bottom: 8px;
}


/* 작은 설명 */

.sidebar-subtitle {

    text-align: center;

    color: #765b43;

    font-family:
        Georgia,
        "Times New Roman",
        serif;

    font-size: 8px;

    letter-spacing: 3px;

    margin-bottom: 55px;
}


/* 메뉴 */

section[data-testid="stSidebar"] .stButton {

    margin-bottom: 5px;
}

section[data-testid="stSidebar"] .stButton > button {

    width: 100%;

    background: transparent;

    border: none;

    border-bottom:
        1px solid rgba(176, 128, 78, 0.12);

    border-radius: 0;

    color: #82664b;

    font-family:
        Georgia,
        "Times New Roman",
        serif;

    font-size: 12px;

    letter-spacing: 3px;

    text-align: left;

    padding: 15px 12px;

    transition:
        all 0.25s ease;
}

section[data-testid="stSidebar"] .stButton > button:hover {

    color: #d8b17f;

    background:
        rgba(150, 105, 61, 0.08);

    padding-left: 20px;

    border-bottom-color:
        rgba(202, 158, 105, 0.3);
}


/* ========================================================
   공통 상단 제목
======================================================== */

.page-header {

    width: 100%;

    padding-top: 48px;

    padding-left: 3vw;

    padding-right: 3vw;
}

.page-header-title {

    color: #d9b584;

    font-family:
        Georgia,
        "Times New Roman",
        serif;

    font-size: 14px;

    letter-spacing: 5px;

    text-transform: lowercase;
}

.page-header-line {

    width: 45px;

    height: 1px;

    background: #94704d;

    margin-top: 12px;

    opacity: 0.55;
}


/* ========================================================
   MAIN 첫 화면
======================================================== */

.main-welcome {

    min-height: 78vh;

    display: flex;

    flex-direction: column;

    justify-content: center;

    align-items: center;

    text-align: center;

    margin-top: -25px;
}


.welcome-small {

    color: #9d7955;

    font-family:
        Georgia,
        "Times New Roman",
        serif;

    font-size: 10px;

    letter-spacing: 7px;

    margin-bottom: 23px;
}


.welcome-title {

    color: #e0bd8d;

    font-family:
        Georgia,
        "Times New Roman",
        serif;

    font-size:
        clamp(55px, 7vw, 100px);

    font-weight: normal;

    letter-spacing: 8px;

    line-height: 1;

    text-shadow:
        0 4px 25px rgba(0,0,0,0.5);
}


.welcome-line {

    width: 65px;

    height: 1px;

    background: #9b7652;

    margin: 30px auto 23px;

    opacity: 0.7;
}


.welcome-description {

    color: #ad9277;

    font-family:
        "Malgun Gothic",
        "Noto Serif KR",
        serif;

    font-size: 14px;

    letter-spacing: 1px;

    line-height: 2;

    margin-bottom: 30px;
}


/* ========================================================
   공통 양장피 버튼
======================================================== */

/*
   버튼 자체가 종이 역할을 하도록 구성.
   따라서 별도의 HTML 박스와 Streamlit 버튼이
   어긋나는 문제를 피함.
*/

.paper-button-area {

    width: 100%;

    display: flex;

    justify-content: center;
}

.paper-button-area .stButton {

    display: flex;

    justify-content: center;

    width: 100%;
}


.paper-button-area .stButton > button {

    min-width: 220px;

    min-height: 82px;

    padding: 20px 45px;

    background:
        radial-gradient(
            ellipse at center,
            #f4edda 0%,
            #e8ddc2 70%,
            #d7c8a7 100%
        );

    border:
        1px solid rgba(104, 79, 52, 0.45);

    border-radius: 0;

    color: #493727;

    font-family:
        Georgia,
        "Times New Roman",
        serif;

    font-size: 15px;

    letter-spacing: 3px;

    box-shadow:
        0 12px 30px rgba(0,0,0,0.35),
        inset 0 0 25px rgba(88,62,36,0.08);

    transition:
        all 0.3s ease;
}


.paper-button-area .stButton > button:hover {

    background:
        radial-gradient(
            ellipse at center,
            #faf3df 0%,
            #eee2c7 70%,
            #ddceb0 100%
        );

    color: #2f2117;

    transform:
        translateY(-3px)
        rotate(-0.3deg);

    box-shadow:
        0 16px 35px rgba(0,0,0,0.45),
        inset 0 0 25px rgba(88,62,36,0.10);
}


/* ========================================================
   MAIN 편지
======================================================== */

.letter-page {

    min-height: 78vh;

    display: flex;

    align-items: center;

    justify-content: center;

    padding:
        25px 3vw 55px;
}


.mystery-letter {

    position: relative;

    width: min(1080px, 90vw);

    min-height: 650px;

    padding:
        75px 90px 70px;

    background:
        radial-gradient(
            ellipse at center,
            #f5eedb 0%,
            #e9dfc6 65%,
            #d8c9aa 100%
        );

    color: #3d2e21;

    border:
        1px solid rgba(82,60,41,0.5);

    box-shadow:
        0 25px 70px rgba(0,0,0,0.55),
        inset 0 0 55px rgba(91,66,40,0.12);

    transform: rotate(-0.25deg);
}


/* 편지 안쪽 테두리 */

.mystery-letter::before {

    content: "";

    position: absolute;

    top: 17px;
    left: 17px;
    right: 17px;
    bottom: 17px;

    border:
        1px solid rgba(88,64,42,0.22);

    pointer-events: none;
}


/* 편지 상단 */

.letter-meta {

    text-align: center;

    color: #806b53;

    font-family:
        Georgia,
        "Times New Roman",
        serif;

    font-size: 9px;

    letter-spacing: 5px;

    margin-bottom: 25px;
}


/* 편지 제목 */

.letter-title {

    text-align: center;

    color: #38291e;

    font-family:
        Georgia,
        "Times New Roman",
        serif;

    font-size: 31px;

    font-weight: normal;

    letter-spacing: 4px;

    margin-bottom: 40px;
}


/* 편지 본문 */

.letter-body {

    color: #51402f;

    font-family:
        "Palatino Linotype",
        "Book Antiqua",
        "Malgun Gothic",
        serif;

    font-size: 16px;

    line-height: 2.15;

    letter-spacing: 0.3px;

    text-align: left;
}

.letter-body em {

    color: #654a32;

    font-style: italic;
}


/* 구분선 */

.letter-divider {

    width: 55px;

    height: 1px;

    background: #80654b;

    margin: 38px auto;
}


/* 서명 */

.letter-signature {

    text-align: right;

    color: #513c2b;

    font-family:
        "Brush Script MT",
        "Segoe Script",
        cursive;

    font-size: 24px;

    margin-top: 35px;
}


/* ========================================================
   CHOICE
======================================================== */

.choice-page {

    min-height: 78vh;

    padding:
        0 4vw 50px;
}


/* Choice 제목 */

.choice-title {

    color: #dfbd8e;

    font-family:
        Georgia,
        "Times New Roman",
        serif;

    font-size:
        clamp(38px, 5vw, 62px);

    font-weight: normal;

    letter-spacing: 6px;

    margin-top: 35px;
}


.choice-subtitle {

    color: #82664d;

    font-family:
        Georgia,
        "Times New Roman",
        serif;

    font-size: 11px;

    letter-spacing: 4px;

    margin-top: 12px;

    margin-bottom: 55px;
}


/* Choice 버튼 배치 */

.choice-buttons {

    display: flex;

    justify-content: center;

    align-items: center;

    gap: 45px;

    flex-wrap: wrap;

    margin-top: 20px;
}


/* ========================================================
   CHOICE 안의 LISTEN 화면
======================================================== */

.listen-page {

    min-height: 78vh;

    padding:
        20px 4vw 50px;
}


.listen-title {

    color: #dfbd8e;

    font-family:
        Georgia,
        "Times New Roman",
        serif;

    font-size:
        clamp(34px, 4vw, 52px);

    font-weight: normal;

    letter-spacing: 5px;

    margin-bottom: 10px;
}


.listen-subtitle {

    color: #82664d;

    font-family:
        Georgia,
        "Times New Roman",
        serif;

    font-size: 10px;

    letter-spacing: 3px;

    margin-bottom: 35px;
}


/* 검색창 */

.search-box {

    max-width: 850px;

    margin: 0 auto 45px;
}

.search-box input {

    background:
        rgba(238, 224, 198, 0.96) !important;

    color: #3d2d20 !important;

    border:
        1px solid rgba(105, 78, 50, 0.55) !important;

    border-radius: 0 !important;

    font-family:
        Georgia,
        "Malgun Gothic",
        serif !important;

    font-size: 15px !important;

    letter-spacing: 1px !important;

    padding: 15px !important;
}


/* 검색 결과 */

.results-title {

    color: #b69670;

    font-family:
        Georgia,
        "Times New Roman",
        serif;

    font-size: 11px;

    letter-spacing: 4px;

    margin-bottom: 22px;
}


.song-card {

    position: relative;

    display: flex;

    align-items: center;

    gap: 24px;

    width: 100%;

    padding: 20px 25px;

    margin-bottom: 16px;

    background:
        linear-gradient(
            135deg,
            rgba(226, 211, 182, 0.96),
            rgba(205, 188, 155, 0.96)
        );

    border:
        1px solid rgba(105, 78, 50, 0.42);

    box-shadow:
        0 8px 22px rgba(0,0,0,0.28);

    color: #3c2c20;
}


.song-image {

    width: 90px;

    height: 90px;

    object-fit: cover;

    box-shadow:
        0 5px 15px rgba(0,0,0,0.3);
}


.song-info {

    flex: 1;

    min-width: 0;
}


.song-name {

    color: #302216;

    font-family:
        Georgia,
        "Malgun Gothic",
        serif;

    font-size: 18px;

    letter-spacing: 1px;

    margin-bottom: 7px;
}


.song-artist {

    color: #5d4733;

    font-family:
        "Malgun Gothic",
        Georgia,
        serif;

    font-size: 13px;

    margin-bottom: 5px;
}


.song-album {

    color: #7a6149;

    font-family:
        "Malgun Gothic",
        Georgia,
        serif;

    font-size: 11px;
}


.song-date {

    color: #80684f;

    font-family:
        Georgia,
        "Malgun Gothic",
        serif;

    font-size: 10px;

    margin-top: 8px;
}


/* Apple Music 링크 */

.song-link {

    display: inline-block;

    margin-top: 10px;

    color: #654a32;

    font-family:
        Georgia,
        "Times New Roman",
        serif;

    font-size: 10px;

    letter-spacing: 2px;

    text-decoration: none;
}

.song-link:hover {

    color: #2d2117;

    text-decoration: underline;
}


/* ========================================================
   OTHER PAGE
======================================================== */

.other-page {

    min-height: 78vh;

    padding:
        0 4vw 50px;
}

.other-title {

    color: #dfbd8e;

    font-family:
        Georgia,
        "Times New Roman",
        serif;

    font-size:
        clamp(38px, 5vw, 62px);

    font-weight: normal;

    letter-spacing: 6px;

    margin-top: 35px;
}

.other-subtitle {

    color: #80664e;

    font-family:
        Georgia,
        "Times New Roman",
        serif;

    font-size: 11px;

    letter-spacing: 4px;

    margin-top: 12px;
}

.coming-soon {

    margin-top: 130px;

    text-align: center;

    color: #67503d;

    font-family:
        Georgia,
        "Times New Roman",
        serif;

    font-size: 11px;

    letter-spacing: 5px;

    line-height: 2;
}


/* ========================================================
   STREAMLIT 기본 요소
======================================================== */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-logo">RECORD ROOM</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">A ROOM FOR MUSIC</div>',
        unsafe_allow_html=True
    )

    if st.button("MAIN", key="navigation_main"):

        st.session_state.page = "main"

        st.session_state.main_entered = False

        st.session_state.choice_mode = "select"

        st.rerun()


    if st.button("CHOICE", key="navigation_choice"):

        st.session_state.page = "choice"

        st.session_state.choice_mode = "select"

        st.rerun()


    if st.button("—", key="navigation_unknown"):

        st.session_state.page = "unknown"

        st.rerun()


# =========================================================
# MAIN PAGE
# =========================================================

if st.session_state.page == "main":


    # -----------------------------------------------------
    # MAIN 첫 화면
    # -----------------------------------------------------

    if not st.session_state.main_entered:

        st.markdown(
            """
            <div class="main-welcome">

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
            '<div class="paper-button-area">',
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
    # ENTER ROOM 이후
    # -----------------------------------------------------

    else:

        st.markdown(
            """
            <div class="page-header">

                <div class="page-header-title">
                    main
                </div>

                <div class="page-header-line"></div>

            </div>
            """,
            unsafe_allow_html=True
        )


        st.markdown(
            """
            <div class="letter-page">

                <div class="mystery-letter">

                    <div class="letter-meta">
                        RECORD ROOM · PRIVATE LETTER
                    </div>

                    <div class="letter-title">
                        이 방에 들어온 당신에게
                    </div>

                    <div class="letter-body">

                        음악을 찾는 일은 어쩌면
                        기억을 찾는 일과 비슷합니다.

                        <br><br>

                        어떤 날에는 오래전부터 알고 있던 한 곡이
                        이상하리만큼 선명하게 들리고,
                        또 어떤 날에는 이름조차 들어본 적 없는 노래가
                        당신의 하루에 흔적을 남기기도 합니다.

                        <br><br>

                        <em>
                        record room은 그런 우연을 위한 작은 방입니다.
                        </em>

                        <br><br>

                        듣고 싶은 음악이 있다면 천천히 골라도 좋고,
                        무엇을 들어야 할지 모르겠다면
                        지금의 당신에게 어울리는 음악을 찾아도 좋습니다.

                        <br><br>

                        이곳에서 재생되는 것은 단순한 노래가 아니라,
                        어쩌면 오늘의 당신만이 알아볼 수 있는
                        하나의 장면일지도 모릅니다.

                    </div>

                    <div class="letter-divider"></div>

                    <div class="letter-body">

                        그러니 잠시만 머물러 주세요.

                        <br>

                        바늘이 레코드에 닿는 순간처럼,
                        이 방의 이야기도 천천히 시작될 테니까요.

                    </div>

                    <div class="letter-signature">
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


    # =====================================================
    # CHOICE 선택 화면
    # =====================================================

    if st.session_state.choice_mode == "select":

        st.markdown(
            """
            <div class="choice-page">

                <div class="page-header">

                    <div class="page-header-title">
                        choice
                    </div>

                    <div class="page-header-line"></div>

                </div>

                <div class="choice-title">
                    choice
                </div>

                <div class="choice-subtitle">
                    WHAT WOULD YOU LIKE TO DO?
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        # 두 버튼
        col1, col2 = st.columns(2, gap="large")


        with col1:

            st.markdown(
                '<div class="paper-button-area">',
                unsafe_allow_html=True
            )

            if st.button(
                "노래 듣기",
                key="listen_button"
            ):

                st.session_state.choice_mode = "listen"

                st.rerun()

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )


        with col2:

            st.markdown(
                '<div class="paper-button-area">',
                unsafe_allow_html=True
            )

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
    # CHOICE → 노래 듣기
    # =====================================================

    elif st.session_state.choice_mode == "listen":

        st.markdown(
            """
            <div class="listen-page">

                <div class="page-header">

                    <div class="page-header-title">
                        choice
                    </div>

                    <div class="page-header-line"></div>

                </div>

                <div class="listen-title">
                    listen
                </div>

                <div class="listen-subtitle">
                    SEARCH FOR A SONG OR AN ARTIST
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        # -------------------------------------------------
        # 검색창
        # -------------------------------------------------

        st.markdown(
            '<div class="search-box">',
            unsafe_allow_html=True
        )

        search_query = st.text_input(
            "음악 검색",
            placeholder="가수 이름이나 노래 제목을 입력해보세요",
            label_visibility="collapsed",
            key="music_search"
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


        # -------------------------------------------------
        # 검색 실행
        # -------------------------------------------------

        if search_query.strip():

            with st.spinner("record room에서 음악을 찾는 중..."):

                results = apple_search_songs(
                    search_query
                )


            if not results:

                st.markdown(
                    """
                    <div class="coming-soon">
                        NO RECORD FOUND
                        <br><br>
                        다른 가수 이름이나 노래 제목을 검색해보세요.
                    </div>
                    """,
                    unsafe_allow_html=True
                )


            else:

                st.markdown(
                    f"""
                    <div class="results-title">
                        SEARCH RESULTS · {len(results)} TRACKS
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                # -------------------------------------------------
                # 결과 카드
                # -------------------------------------------------

                for song in results:

                    track_name = song.get(
                        "trackName",
                        "Unknown Track"
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

                        release_date = release_date[:10]

                    preview_url = song.get(
                        "previewUrl",
                        ""
                    )

                    track_view_url = song.get(
                        "trackViewUrl",
                        ""
                    )


                    # -------------------------------------------------
                    # 카드
                    # -------------------------------------------------

                    st.markdown(
                        '<div class="song-card">',
                        unsafe_allow_html=True
                    )


                    if artwork:

                        st.image(
                            artwork,
                            width=90
                        )


                    st.markdown(
                        f"""
                        <div class="song-info">

                            <div class="song-name">
                                {track_name}
                            </div>

                            <div class="song-artist">
                                {artist_name}
                            </div>

                            <div class="song-album">
                                {album_name}
                            </div>

                            <div class="song-date">
                                {release_date}
                            </div>

                            {
                                f'<a class="song-link" href="{track_view_url}" target="_blank">OPEN IN APPLE MUSIC / ITUNES</a>'
                                if track_view_url
                                else ""
                            }

                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                    st.markdown(
                        '</div>',
                        unsafe_allow_html=True
                    )


                    # 30초 미리듣기
                    if preview_url:

                        st.audio(
                            preview_url,
                            format="audio/mp4"
                        )


        else:

            st.markdown(
                """
                <div class="coming-soon">

                    SEARCH FOR SOMETHING

                    <br><br>

                    artist · song · album

                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# 추천받기
# =========================================================

elif (
    st.session_state.page == "choice"
    and st.session_state.choice_mode == "recommend"
):

    st.markdown(
        """
        <div class="other-page">

            <div class="page-header">

                <div class="page-header-title">
                    choice
                </div>

                <div class="page-header-line"></div>

            </div>

            <div class="other-title">
                recommend
            </div>

            <div class="other-subtitle">
                A SONG WAITING TO BE FOUND
            </div>

            <div class="coming-soon">
                AI RECOMMENDATION
                <br><br>
                COMING SOON
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# 미정 페이지
# =========================================================

elif st.session_state.page == "unknown":

    st.markdown(
        """
        <div class="other-page">

            <div class="page-header">

                <div class="page-header-title">
                    —
                </div>

                <div class="page-header-line"></div>

            </div>

            <div class="other-title">
                —
            </div>

            <div class="other-subtitle">
                ANOTHER ROOM
            </div>

            <div class="coming-soon">
                THIS ROOM HAS NOT BEEN NAMED YET
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )
