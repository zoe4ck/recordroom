            '<div class="cocktail-header">'
            '<div class="cocktail-kicker">ROOM SERVICE · NIGHT CONCIERGE</div>'
            '<div class="cocktail-title">COCKTAIL BAR</div>'
            '<div class="cocktail-subtitle">오늘의 기분을 한 잔 골라주세요. 음악은 그 다음에 고를게요.</div>'
            '</div>',
            unsafe_allow_html=True
        )

        if st.session_state.cocktail_mood is None:
            mood_cols = st.columns(4, gap="medium")
            for col, (key, config) in zip(mood_cols, MOOD_CONFIG.items()):
                with col:
                    mini_visual = cocktail_visual_html(config["color"], mini=True)
                    st.markdown(
                        f'<div class="order-slip {config["color"]}">'
                        f'<div class="slip-no">ORDER NO. {list(MOOD_CONFIG).index(key)+1:02d}</div>'
                        f'<div class="slip-label">{config["label"]}</div>'
                        + mini_visual
                        + f'<div class="slip-drink">{config["drink"]}</div>'
                        + f'<div class="slip-desc">{config["description"]}</div>'
                        + '</div>',
                        unsafe_allow_html=True
                    )
                    if st.button("ORDER THIS", key=f"order_mood_{key}", use_container_width=True):
                        st.session_state.cocktail_mood = key
                        st.session_state.cocktail_sips = 0
                        st.session_state.cocktail_recommendations = []
                        st.rerun()

        else:
            if st.button("← BACK TO COCKTAIL BAR", key="cocktail_back_top", use_container_width=True):
                st.session_state.cocktail_mood = None
                st.session_state.cocktail_sips = 0
                st.session_state.cocktail_recommendations = []
                st.rerun()

            mood_key = st.session_state.cocktail_mood
            config = MOOD_CONFIG[mood_key]
            sips = st.session_state.cocktail_sips
            fill = max(0, 100 - sips * 17)

            st.markdown(
                f'<div class="selected-order">'
                f'<div class="selected-order-small">ROOM SERVICE ORDER</div>'
                f'<div class="selected-order-title">{config["label"]}</div>'
                f'<div class="selected-order-sub">{config["description"]}</div>'
                '</div>',
                unsafe_allow_html=True
            )

            # 추천은 음료를 고르는 즉시 불러오고, 화면 오른쪽에 고정해서 보여줍니다.
            if not st.session_state.cocktail_recommendations:
                with st.spinner("CONCIERGE IS CHOOSING RECORDS..."):
                    recs, used_ai = get_ai_recommendations(mood_key)
                st.session_state.cocktail_recommendations = recs
                st.session_state.cocktail_ai_used = used_ai

            recs = st.session_state.cocktail_recommendations

            drink_col, info_col = st.columns([1.02, 1.28], gap="large", vertical_alignment="top")

            with drink_col:
                st.markdown(
                    cocktail_visual_html(config["color"], fill=fill),
                    unsafe_allow_html=True
                )

                st.markdown(
                    f'<div class="drink-name">{config["drink"]}</div>'
                    f'<div class="drink-state">{("FULL" if sips == 0 else f"{fill}% REMAINING")}</div>',
                    unsafe_allow_html=True
                )

                st.write("")
                sip_col, refill_col = st.columns(2, gap="small")
                with sip_col:
                    if st.button("TAKE A SIP", key="take_sip", use_container_width=True):
                        if sips < 6:
                            st.session_state.cocktail_sips += 1
                        st.rerun()
                with refill_col:
                    if st.button("다시 먹기", key="refill_drink", use_container_width=True):
                        st.session_state.cocktail_sips = 0
                        st.rerun()

            with info_col:
                st.markdown(
                    '<div class="concierge-card">'
                    '<div class="concierge-label">NIGHT CONCIERGE</div>'
                    '<div class="concierge-title">오늘의 한 잔 옆에<br>어울리는 레코드를 골랐어요.</div>'
                    '<div class="concierge-copy">현재 대한민국에서 인기 있는 음악을 우선으로, 선택한 기분과 장르에 맞는 실제 Apple 음악 카탈로그의 곡을 골라옵니다.</div>'
                    '</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    '<div class="recommendation-title">TONIGHT\'S RECORDS</div>',
                    unsafe_allow_html=True
                )
                if st.session_state.get("cocktail_ai_used", False):
                    st.markdown('<div class="ai-note">AI CONCIERGE · MOOD MATCHED · KOREA POPULAR FIRST</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="ai-note">CONCIERGE · FALLBACK MENU · KOREA POPULAR FIRST</div>', unsafe_allow_html=True)

                if recs:
                    for index, result in enumerate(recs[:5]):
                        artwork = result.get("artworkUrl100", "")
                        track = escape(result.get("trackName", "제목 없음"))
                        artist = escape(result.get("artistName", "아티스트 없음"))
                        album = escape(result.get("collectionName", "앨범 정보 없음"))

                        with st.container(border=True):
                            image_col, text_col = st.columns([0.8, 3.4], gap="small", vertical_alignment="center")
                            with image_col:
                                if artwork:
                                    st.image(artwork, width=68)
                            with text_col:
                                st.markdown(
                                    f'<div class="compact-rec-title">{track}</div>'
                                    f'<div class="compact-rec-meta">{artist}<br>{album}</div>',
                                    unsafe_allow_html=True
                                )

                            if result.get("previewUrl"):
                                st.audio(result["previewUrl"])

                            if st.button(
                                "TAKE TO MY ROOM",
                                key=f"cocktail_take_{index}_{result.get('trackId')}",
                                use_container_width=True
                            ):
                                add_to_room(result)
                                st.session_state.my_room_view = "lp"
                                st.session_state.page = "my_room"
                                st.rerun()
                else:
                    st.markdown(
                        '<div class="no-result" style="margin-top:20px;">'
                        '오늘 밤에 맞는 레코드를 찾지 못했어요.<br>'
                        '다시 주문하면 다른 메뉴를 찾아볼게요.'
                        '</div>',
                        unsafe_allow_html=True
                    )

            st.write("")
            if st.button("← BACK TO ROOM SERVICE", key="recommend_back", use_container_width=True):
                go_room_service()

# =========================================================
# MY ROOM
# =========================================================

elif st.session_state.page == "my_room":

    if not st.session_state.logged_in:
        st.markdown(
            '<div class="section-area" style="margin-bottom:30px;">'
            '<div class="section-title">MY ROOM</div></div>',
            unsafe_allow_html=True
        )

        if not st.session_state.my_room_checkin_open:
            st.markdown(
                '<div class="auth-box" style="margin-top:0;">'
                '<div class="auth-subtitle">객실에 들어가려면 먼저 CHECK-IN이 필요합니다.</div>'
                '</div>', unsafe_allow_html=True
            )
            gate_left, gate_center, gate_right = st.columns([2,1,2])
            with gate_center:
                if st.button("CHECK-IN", key="open_checkin", use_container_width=True):
                    st.session_state.my_room_checkin_open = True
                    st.session_state.auth_mode = "login"
                    st.rerun()
            if st.button("← BACK TO LOBBY", key="my_room_back_gate", use_container_width=True):
                st.session_state.page = "main"
                st.session_state.my_room_checkin_open = False
                st.rerun()
        else:
            st.markdown(
                '<div class="auth-box"><div class="auth-title">CHECK-IN</div>'
                '<div class="auth-subtitle">ROOM KEY를 입력하거나 새로운 GUEST로 등록하세요.</div></div>',
                unsafe_allow_html=True
            )
            auth_left, auth_right = st.columns(2)
            with auth_left:
                if st.button("CHECK-IN", key="auth_login_tab", use_container_width=True):
                    st.session_state.auth_mode = "login"
                    st.rerun()
            with auth_right:
                if st.button("NEW GUEST", key="auth_signup_tab", use_container_width=True):
                    st.session_state.auth_mode = "signup"
                    st.rerun()
