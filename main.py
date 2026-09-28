import streamlit as st


# =========================================================
# RECORD ROOM
# Main Page / Onboarding
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

if "entered" not in st.session_state:
    st.session_state.entered = False


# =========================================================
# STYLE
# =========================================================

st.markdown(
    """
    <style>

    /* ------------------------------
       전체 화면
    ------------------------------ */

    .stApp {
        background:
            radial-gradient(
                circle at 50% 35%,
                rgba(91, 63, 42, 0.18) 0%,
                rgba(20, 15, 12, 0.0) 45%
            ),
            linear-gradient(
                135deg,
                #17110d 0%,
                #241810 25%,
                #342318 50%,
                #21160f 75%,
                #120d09 100%
            );

        color: #e9dcc9;
    }


    /* ------------------------------
       사이드바
    ------------------------------ */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #17100c 0%,
                #21150e 50%,
                #130d09 100%
            );

        border-right: 1px solid rgba(191, 151, 102, 0.18);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
    }

    .sidebar-logo {
        font-family: Georgia, "Times New Roman", serif;
        color: #d4b28a;
        font-size: 22px;
        letter-spacing: 4px;
        margin-bottom: 45px;
        text-align: center;
    }

    .sidebar-subtitle {
        color: #75604d;
        font-size: 9px;
        letter-spacing: 3px;
        text-align: center;
        margin-top: -35px;
        margin-bottom: 35px;
    }

    /* 사이드바 버튼 */

    section[data-testid="stSidebar"] .stButton > button {
        width: 100%;
        background: transparent;
        border: none;
        border-bottom: 1px solid rgba(180, 140, 94, 0.10);
        border-radius: 0;

        color: #897360;

        font-family: Georgia, "Times New Roman", serif;
        font-size: 13px;
        letter-spacing: 2px;

        text-align: left;
        padding: 14px 12px;

        transition:
            color 0.25s ease,
            padding-left 0.25s ease,
            background 0.25s ease;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        color: #dfc39e;
        background: rgba(157, 111, 68, 0.08);
        padding-left: 18px;
    }


    /* ------------------------------
       메인 영역
    ------------------------------ */

    .main-container {
        min-height: 82vh;

        display: flex;
        flex-direction: column;

        align-items: center;
        justify-content: center;

        text-align: center;
    }

    .small-label {
        color: #94785c;
        font-family: Georgia, "Times New Roman", serif;
        font-size: 10px;
        letter-spacing: 6px;
        margin-bottom: 22px;
    }

    .main-title {
        color: #dfc29b;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size: clamp(58px, 8vw, 104px);

        font-weight: normal;

        letter-spacing: 8px;

        line-height: 1;

        margin: 0;

        text-shadow:
            0 2px 20px rgba(0,0,0,0.45);
    }

    .main-line {
        width: 70px;
        height: 1px;

        background: #967553;

        margin: 28px auto 22px;

        opacity: 0.65;
    }

    .main-description {
        color: #9d8975;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size: 14px;

        letter-spacing: 1.8px;

        line-height: 1.9;

        margin-bottom: 38px;
    }


    /* ------------------------------
       ENTER ROOM 버튼
    ------------------------------ */

    .enter-wrapper {
        display: flex;
        justify-content: center;
    }

    div[data-testid="stButton"] > button {
        background:
            linear-gradient(
                145deg,
                #8a6545,
                #60452f
            );

        border: 1px solid rgba(210, 174, 132, 0.35);

        color: #f1e3d1;

        border-radius: 1px;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size: 11px;

        letter-spacing: 4px;

        padding: 12px 30px;

        transition:
            all 0.3s ease;

        box-shadow:
            0 5px 20px rgba(0,0,0,0.25);
    }

    div[data-testid="stButton"] > button:hover {
        background:
            linear-gradient(
                145deg,
                #a27b55,
                #765538
            );

        color: #fff5e7;

        border-color: rgba(225, 194, 157, 0.55);

        transform: translateY(-2px);

        box-shadow:
            0 8px 25px rgba(0,0,0,0.35);
    }


    /* ------------------------------
       미스터리 INTRO CARD
    ------------------------------ */

    .intro-paper {
        width: min(720px, 90%);

        margin: 35px auto 0;

        padding: 58px 65px;

        background:
            radial-gradient(
                ellipse at center,
                rgba(255, 252, 235, 0.96),
                rgba(228, 218, 194, 0.96)
            );

        color: #33281f;

        border: 1px solid rgba(105, 81, 59, 0.45);

        box-shadow:
            0 20px 55px rgba(0,0,0,0.45),
            inset 0 0 45px rgba(88, 61, 36, 0.08);

        position: relative;

        transform: rotate(-0.3deg);
    }

    .intro-paper::before {
        content: "";

        position: absolute;

        inset: 12px;

        border: 1px solid rgba(99, 76, 53, 0.20);

        pointer-events: none;
    }

    .paper-label {
        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size: 9px;

        letter-spacing: 4px;

        color: #7c6854;

        margin-bottom: 25px;
    }

    .paper-title {
        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size: 27px;

        font-weight: normal;

        letter-spacing: 3px;

        color: #30251d;

        margin-bottom: 25px;
    }

    .paper-text {
        font-family:
            "Palatino Linotype",
            "Book Antiqua",
            Georgia,
            serif;

        font-size: 15px;

        line-height: 2.15;

        letter-spacing: 0.5px;

        color: #4a3b2e;

        text-align: left;
    }

    .paper-signature {
        margin-top: 35px;

        font-family:
            "Brush Script MT",
            "Segoe Script",
            cursive;

        font-size: 22px;

        color: #49382b;

        text-align: right;
    }


    /* ------------------------------
       CHOICE / OTHER PAGE
    ------------------------------ */

    .page-title {
        font-family: Georgia, "Times New Roman", serif;

        font-size: 48px;

        font-weight: normal;

        color: #d5b58d;

        letter-spacing: 5px;

        margin-top: 40px;
    }

    .page-description {
        color: #897564;

        font-family: Georgia, "Times New Roman", serif;

        font-size: 13px;

        letter-spacing: 1.5px;

        margin-top: 10px;
    }

    .coming-soon {
        margin-top: 100px;

        text-align: center;

        color: #6f5b49;

        font-family: Georgia, "Times New Roman", serif;

        font-size: 12px;

        letter-spacing: 4px;
    }


    /* ------------------------------
       Streamlit 기본 요소 숨기기
    ------------------------------ */

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
# SIDEBAR NAVIGATION
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

    st.write("")

    if st.button("MAIN", key="nav_main"):
        st.session_state.page = "main"
        st.session_state.entered = False
        st.rerun()

    if st.button("CHOICE", key="nav_choice"):
        st.session_state.page = "choice"
        st.rerun()

    if st.button("—", key="nav_unknown"):
        st.session_state.page = "unknown"
        st.rerun()


# =========================================================
# MAIN PAGE
# =========================================================

if st.session_state.page == "main":

    st.markdown(
        '<div class="main-container">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="small-label">WELCOME TO</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<h1 class="main-title">record room</h1>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-line"></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="main-description">
            음악을 고르고, 발견하고, 잠시 머무는 작은 방
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("ENTER ROOM", key="enter_room"):

        st.session_state.entered = True

        st.rerun()

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # ENTER ROOM 이후
    # -----------------------------------------------------

    if st.session_state.entered:

        st.markdown(
            """
            <div class="intro-paper">

                <div class="paper-label">
                    RECORD ROOM · PRIVATE NOTE
                </div>

                <div class="paper-title">
                    당신의 음악을 위한 방
                </div>

                <div class="paper-text">
                    이곳은 음악을 조금 더 천천히 만나는 공간입니다.
                    <br><br>
                    오늘 듣고 싶은 음악을 직접 찾아도 좋고,
                    지금의 기분과 취향을 이야기하며
                    새로운 음악을 발견해도 좋습니다.
                    <br><br>
                    수많은 곡들 사이에서 우연히 한 곡을 발견하는 순간,
                    오래된 레코드 한 장을 꺼내어 바늘을 올리는 순간처럼
                    이 방에서의 시간이 조금 특별해지기를 바랍니다.
                    <br><br>
                    조용히 음악을 듣고 싶은 날에도,
                    무엇을 들어야 할지 모르겠는 날에도,
                    이곳의 문은 열려 있습니다.
                </div>

                <div class="paper-signature">
                    — record room
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# CHOICE PAGE
# =========================================================

elif st.session_state.page == "choice":

    st.markdown(
        '<div class="page-title">choice</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="page-description">
            choose how you want to spend your time
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="coming-soon">
            LISTEN · RECOMMEND
            <br><br>
            COMING SOON
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# UNKNOWN PAGE
# =========================================================

elif st.session_state.page == "unknown":

    st.markdown(
        '<div class="page-title">—</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="page-description">
            another room is waiting to be opened
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="coming-soon">
            THIS ROOM HAS NOT BEEN NAMED YET
        </div>
        """,
        unsafe_allow_html=True
    )
