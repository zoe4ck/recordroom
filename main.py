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
   LISTEN
   ========================================================= */

.listen-container {
    width: min(1100px, 90vw);
    margin: 60px auto 0 auto;
}

.listen-title {
    color: #d5a56d;
    font-family: "Cormorant Garamond", Georgia, serif;
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
    margin-bottom: 35px;
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
</style>
"""

# CSS 렌더링
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
# APPLE iTUNES API
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
# ARTIST SEARCH
# =========================================================
# ★ 검색 오류 수정된 부분
# =========================================================

@st.cache_data(ttl=600, show_spinner=False)
def find_artist_tracks(query):

    query = query.strip()

    if not query:
        return []

    nq = normalize(query)

    # Apple에서 검색된 아티스트 후보를 모두 모음
    candidates = []

    # 한국 + 미국 스토어 모두 확인
    for country in ["KR", "US"]:

        data = apple_search({
            "term": query,
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

            # 중복 아티스트 제거
            if not any(
                x.get("artistId") == artist_id
                for x in candidates
            ):
                candidates.append(artist)

    if not candidates:
        return []

    # =====================================================
    # 1순위
    # 이름 완전 일치
    # 예: zico → ZICO
    #     아이유 → 아이유
    # =====================================================

    exact = [
        artist
        for artist in candidates
        if normalize(
            artist.get("artistName", "")
        ) == nq
    ]

    if exact:

        selected = exact[0]

    else:

        # =================================================
        # 2순위
        # 이름에 검색어 포함
        # =================================================

        contains = [
            artist
            for artist in candidates
            if nq in normalize(
                artist.get("artistName", "")
            )
        ]

        if contains:

            selected = contains[0]

        else:

            # =================================================
            # 3순위
            # 곡 검색에서 artistId를 다시 찾음
            #
            # 한글 이름 검색에서 아티스트 검색이
            # 제대로 잡히지 않는 경우를 위한 fallback
            # =================================================

            song_candidates = []

            for country in ["KR", "US"]:

                data = apple_search({
                    "term": query,
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
                        for x in song_candidates
                    ):

                        song_candidates.append({
                            "artistId": artist_id,
                            "artistName": artist_name
                        })

            if not song_candidates:
                return []

            # 곡 검색 결과에서도 이름 완전 일치 우선
            song_exact = [
                artist
                for artist in song_candidates
                if normalize(
                    artist.get("artistName", "")
                ) == nq
            ]

            if song_exact:

                selected = song_exact[0]

            else:

                # 부분 일치
                song_contains = [
                    artist
                    for artist in song_candidates
                    if nq in normalize(
                        artist.get("artistName", "")
                    )
                ]

                if not song_contains:
                    return []

                selected = song_contains[0]

    # =====================================================
    # 선택된 아티스트의 Apple artistId
    # =====================================================

    artist_id = selected.get(
        "artistId"
    )

    if not artist_id:
        return []

    # =====================================================
    # artistId를 이용해서 정확한 곡 목록 가져오기
    # =====================================================

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
# ★ 검색 오류 수정된 부분
# =========================================================

@st.cache_data(ttl=600, show_spinner=False)
def find_song(query):

    query = query.strip()

    if not query:
        return []

    nq = normalize(query)

    all_results = []

    # 한국 + 미국 스토어 모두 검색
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

            # 중복 제거
            if track_id and any(
                x.get("trackId") == track_id
                for x in all_results
            ):
                continue

            all_results.append(result)

    if not all_results:
        return []

    # =====================================================
    # 1순위: 제목 완전 일치
    # =====================================================

    exact = [
        result
        for result in all_results
        if normalize(
            result.get("trackName", "")
        ) == nq
    ]

    if exact:
        return exact

    # =====================================================
    # 2순위: 제목 부분 일치
    # =====================================================

    partial = [
        result
        for result in all_results
        if nq in normalize(
            result.get("trackName", "")
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

    # 사용자가 '가수' 선택
    if mode == "artist":

        return find_artist_tracks(
            query
        )

    # 사용자가 '곡' 선택
    if mode == "song":

        return find_song(
            query
        )

    # 자동 검색
    # 먼저 가수로 검색
    artist_results = find_artist_tracks(
        query
    )

    if artist_results:

        return artist_results

    # 가수가 아니면 곡 검색
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
# MAIN PAGE
# =========================================================

if st.session_state.page == "main":

    # -----------------------------------------------------
    # 처음 MAIN
    # -----------------------------------------------------

    if not st.session_state.main_entered:

        st.markdown(
            '<div class="welcome-area"><div class="welcome-small">WELCOME TO</div><div class="welcome-title">record room</div><div class="welcome-line"></div><div class="welcome-description">음악을 듣고, 발견하고, 잠시 머무는 작은 방</div></div>',
            unsafe_allow_html=True
        )

        left, center, right = st.columns(
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

    # -----------------------------------------------------
    # 편지
    # -----------------------------------------------------

    else:

        # HTML을 한 줄 문자열로 만들어
        # 코드 블록으로 인식되는 문제 방지
        letter_html = (
            '<div class="letter-wrap">'
            '<div class="letter-paper">'
            '<div class="letter-date">SEPTEMBER 28, 2026</div>'
            '<div class="letter-title">DEAR, VISITOR</div>'
            '<div class="letter-body">'
            '이곳에는 조금 오래 머물러도 괜찮습니다.'
            '<br><br>'
            '누군가에게는 스쳐 지나갈 한 곡이, '
            '누군가에게는 오래 기억될 밤이 되기도 하니까요.'
            '<br><br>'
            '이 방에서는 이름을 알고 찾아온 음악도, '
            '우연히 발견한 음악도 천천히 들여다볼 수 있습니다.'
            '<br><br>'
            '문을 열었으니, '
            '이제 당신이 들을 차례입니다.'
            '</div>'
            '<div class="letter-sign">— record room</div>'
            '</div>'
            '</div>'
        )

        st.markdown(
            letter_html,
            unsafe_allow_html=True
        )


# =========================================================
# CHOICE PAGE
# =========================================================

elif st.session_state.page == "choice":

    # -----------------------------------------------------
    # CHOICE 선택 화면
    # -----------------------------------------------------

    if st.session_state.choice_mode is None:

        st.markdown(
            '<div class="section-area"><div class="section-title">CHOICE</div><div class="section-subtitle">오늘은 어떤 방식으로 음악을 만날까요?</div></div>',
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

    # -----------------------------------------------------
    # LISTEN
    # -----------------------------------------------------

    elif st.session_state.choice_mode == "listen":

        st.markdown(
            '<div class="listen-container"><div class="listen-title">LISTEN</div><div class="listen-subtitle">가수 이름 또는 곡 제목을 검색하세요.</div></div>',
            unsafe_allow_html=True
        )

        search_col, button_col = st.columns(
            [5, 1]
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

    # -----------------------------------------------------
    # RECOMMEND
    # -----------------------------------------------------

    else:

        st.markdown(
            '<div class="section-area"><div class="section-title">RECOMMEND</div><div class="section-subtitle">당신에게 맞는 음악을 찾는 공간입니다.</div><div style="color:#8f7059;font-family:Georgia,serif;margin-top:20px;">COMING SOON</div></div>',
            unsafe_allow_html=True
        )


# =========================================================
# OTHER PAGE
# =========================================================

else:

    st.markdown(
        '<div class="section-area"><div class="section-title">—</div></div>',
        unsafe_allow_html=True
    )
