import streamlit as st


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

if "entered_room" not in st.session_state:
    st.session_state.entered_room = False


# =========================================================
# GLOBAL STYLE
# =========================================================

st.markdown(
    """
    <style>

    /* =========================================
       전체 웹
    ========================================= */

    .stApp {
        background:
            radial-gradient(
                circle at 55% 40%,
                #3b271b 0%,
                #2b1c13 35%,
                #1a100b 75%,
                #100a07 100%
            );

        color: #e5d0b1;
    }

    .main .block-container {
        max-width: 1400px;
        padding-top: 0rem;
        padding-bottom: 3rem;
    }


    /* =========================================
       사이드바
    ========================================= */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #160d09 0%,
                #1b100b 50%,
                #100906 100%
            );

        border-right: 1px solid rgba(188, 142, 91, 0.22);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 3.5rem;
    }

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

    .sidebar-subtitle {
        text-align: center;

        color: #765b43;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size: 8px;

        letter-spacing: 3px;

        margin-bottom: 60px;
    }


    /* 사이드바 버튼 */

    section[data-testid="stSidebar"] .stButton {
        margin-bottom: 4px;
    }

    section[data-testid="stSidebar"] .stButton > button {
        width: 100%;

        background: transparent;

        border: none;
        border-bottom: 1px solid rgba(176, 128, 78, 0.12);

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

        transition: all 0.25s ease;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        color: #d8b17f;

        background: rgba(150, 105, 61, 0.08);

        padding-left: 20px;

        border-bottom-color: rgba(202, 158, 105, 0.3);
    }


    /* =========================================
       MAIN ONBOARDING
    ========================================= */

    .welcome-area {
        min-height: 88vh;

        display: flex;

        flex-direction: column;

        justify-content: center;

        align-items: center;

        text-align: center;

        padding-top: 30px;
    }

    .welcome-small {
        color: #9d7955;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size: 10px;

        letter-spacing: 7px;

        margin-bottom: 22px;
    }

    .welcome-title {
        color: #e0bd8d;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size: clamp(55px, 7vw, 100px);

        font-weight: normal;

        letter-spacing: 8px;

        line-height: 1;

        margin: 0;

        text-shadow:
            0 4px 25px rgba(0, 0, 0, 0.5);
    }

    .welcome-line {
        width: 65px;

        height: 1px;

        background: #9b7652;

        margin: 30px auto 24px;

        opacity: 0.7;
    }

    .welcome-description {
        color: #a68d75;

        font-family:
            "Noto Serif KR",
            "Malgun Gothic",
            serif;

        font-size: 14px;

        letter-spacing: 1px;

        line-height: 2;

        margin-bottom: 38px;
    }


    /* =========================================
       ENTER ROOM BUTTON
    ========================================= */

    .enter-button-area {
        display: flex;

        justify-content: center;

        width: 100%;
    }

    .enter-button-area .stButton {
        display: flex;

        justify-content: center;

        width: 100%;
    }

    .enter-button-area .stButton > button {
        width: auto;

        min-width: 170px;

        height: 48px;

        background:
            linear-gradient(
                135deg,
                #8a6343,
                #65462e
            );

        border: 1px solid rgba(220, 179, 129, 0.45);

        border-radius: 1px;

        color: #f3e3ce;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size: 11px;

        letter-spacing: 4px;

        box-shadow:
            0 8px 25px rgba(0, 0, 0, 0.35);

        transition: all 0.3s ease;
    }

    .enter-button-area .stButton > button:hover {
        background:
            linear-gradient(
                135deg,
                #a27851,
                #795638
            );

        color: #fff6e9;

        border-color: rgba(230, 198, 160, 0.7);

        transform: translateY(-2px);

        box-shadow:
            0 12px 30px rgba(0, 0, 0, 0.45);
    }


    /* =========================================
       INTRODUCTION PAPER
    ========================================= */

    .paper-area {
        min-height: 88vh;

        display: flex;

        align-items: center;

        justify-content: center;

        padding: 60px 30px;
    }

    .mystery-paper {
        position: relative;

        width: min(720px, 90%);

        padding: 65px 75px;

        background:
            radial-gradient(
                ellipse at center,
                #f4edda 0%,
                #e7dcc0 65%,
                #d9cbaa 100%
            );

        color: #35281d;

        border: 1px solid rgba(82, 60, 41, 0.45);

        box-shadow:
            0 25px 60px rgba(0, 0, 0, 0.55),
            inset 0 0 45px rgba(91, 66, 40, 0.12);

        transform: rotate(-0.4deg);
    }

    .mystery-paper::before {
        content: "";

        position: absolute;

        top: 13px;
        left: 13px;
        right: 13px;
        bottom: 13px;

        border: 1px solid rgba(88, 64, 42, 0.22);

        pointer-events: none;
    }

    .paper-top {
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

    .paper-title {
        text-align: center;

        color: #38291e;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size: 28px;

        font-weight: normal;

        letter-spacing: 3px;

        margin-bottom: 35px;
    }

    .paper-text {
        color: #4b3a2b;

        font-family:
            "Palatino Linotype",
            "Book Antiqua",
            Georgia,
            serif;

        font-size: 15px;

        line-height: 2.15;

        letter-spacing: 0.4px;

        text-align: left;
    }

    .paper-text em {
        color: #634b36;

        font-style: italic;
    }

    .paper-divider {
        width: 45px;

        height: 1px;

        background: #80654b;

        margin: 32px auto;
    }

    .paper-signature {
        text-align: right;

        color: #513c2b;

        font-family:
            "Brush Script MT",
            "Segoe Script",
            cursive;

        font-size: 22px;

        margin-top: 32px;
    }


    /* =========================================
       OTHER PAGES
    ========================================= */

    .other-page {
        min-height: 88vh;

        padding-top: 80px;

        text-align: left;
    }

    .other-title {
        color: #d7b486;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size: 52px;

        font-weight: normal;

        letter-spacing: 6px;
    }

    .other-subtitle {
        color: #80664e;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size: 12px;

        letter-spacing: 3px;

        margin-top: 12px;
    }

    .coming-soon {
        margin-top: 120px;

        text-align: center;

        color: #67503d;

        font-family:
            Georgia,
            "Times New Roman",
            serif;

        font-size: 11px;

        letter-spacing: 5px;
    }


    /* =========================================
       STREAMLIT UI 정리
    ========================================= */

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

    if st.button("MAIN", key="main_navigation"):
        st.session_state.page = "main"
        st.session_state.entered_room = False
        st.rerun()

    if st.button("CHOICE", key="choice_navigation"):
        st.session_state.page = "choice"
        st.rerun()

    if st.button("—", key="unknown_navigation"):
        st.session_state.page = "unknown"
        st.rerun()


# =========================================================
# MAIN PAGE
# =========================================================

if st.session_state.page == "main":

    # ---------------------------------------------
    # ENTER ROOM 전
    # ---------------------------------------------

    if not st.session_state.entered_room:

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
                    음악을 듣고, 발견하고,<br>
                    잠시 머무는 작은 방
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="enter-button-area">',
            unsafe_allow_html=True
        )

        if st.button("ENTER ROOM", key="enter_room_button"):
            st.session_state.entered_room = True
            st.rerun()

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


    # ---------------------------------------------
    # ENTER ROOM 후
    # ---------------------------------------------

    else:

        st.markdown(
            """
            <div class="paper-area">

                <div class="mystery-paper">

                    <div class="paper-top">
                        RECORD ROOM · PRIVATE NOTE
                    </div>

                    <div class="paper-title">
                        이 방에 들어온 당신에게
                    </div>

                    <div class="paper-text">

                        음악을 찾는 일은
                        어쩌면 기억을 찾는 일과 비슷합니다.
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

                    <div class="paper-divider"></div>

                    <div class="paper-text">

                        그러니 잠시만 머물러 주세요.
                        <br>
                        바늘이 레코드에 닿는 순간처럼,
                        이 방의 이야기도 천천히 시작될 테니까요.

                    </div>

                    <div class="paper-signature">
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

    st.markdown(
        """
        <div class="other-page">

            <div class="other-title">
                choice
            </div>

            <div class="other-subtitle">
                CHOOSE YOUR WAY INTO MUSIC
            </div>

            <div class="coming-soon">
                LISTEN · RECOMMEND
                <br><br>
                THIS ROOM IS WAITING
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# UNKNOWN PAGE
# =========================================================

elif st.session_state.page == "unknown":

    st.markdown(
        """
        <div class="other-page">

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
