
            if supabase is None and SUPABASE_CONFIG_ERROR:
                st.error(SUPABASE_CONFIG_ERROR)
            email = st.text_input("EMAIL", placeholder="guest@example.com", key="auth_email")
            password = st.text_input("ROOM KEY", type="password", placeholder="비밀번호", key="auth_password")
            password_confirm = ""
            if st.session_state.auth_mode == "signup":
                password_confirm = st.text_input("ROOM KEY AGAIN", type="password", placeholder="비밀번호를 다시 입력하세요", key="auth_password_confirm")

            if st.session_state.auth_mode == "login":
                if st.button("ENTER MY ROOM", key="login_submit", use_container_width=True):
                    if not email.strip() or not password:
                        st.warning("이메일과 비밀번호를 입력해 주세요.")
                    else:
                        ok, message = login_user(email.strip(), password)
                        if ok:
                            st.session_state.my_room_view = "fireplace"
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
            else:
                if st.button("CREATE ROOM KEY", key="signup_submit", use_container_width=True):
                    if not email.strip() or not password:
                        st.warning("이메일과 비밀번호를 입력해 주세요.")
                    elif password != password_confirm:
                        st.warning("두 비밀번호가 일치하지 않습니다.")
                    elif len(password) < 6:
                        st.warning("비밀번호는 6자 이상으로 입력해 주세요.")
                    else:
                        ok, message = signup_user(email.strip(), password)
                        if ok:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)

            if st.button("← BACK", key="my_room_back_auth", use_container_width=True):
                st.session_state.my_room_checkin_open = False
                st.rerun()

    else:
        user_email = ""
        if st.session_state.current_user is not None:
            user_email = getattr(st.session_state.current_user, "email", "") or ""

        st.markdown(
            '<div class="room-service-container">'
            '<div class="room-service-title">MY ROOM</div>'
            '<div class="room-service-subtitle">GUEST PRIVATE ROOM</div>'
            '</div>', unsafe_allow_html=True
        )

        top_left, top_mid, top_right = st.columns([2,3,2])
        with top_left:
            st.caption("CHECKED IN")
        with top_mid:
            if user_email:
                st.markdown(
                    '<div style="text-align:center;color:#a98a70;font-family:Georgia,serif;letter-spacing:1px;">'
                    + escape(user_email) + '</div>', unsafe_allow_html=True
                )
        with top_right:
            if st.button("CHECK-OUT", key="logout_button", use_container_width=True):
                logout_user()

        view = st.session_state.my_room_view

        if view == "fireplace":
            render_fireplace()
            st.markdown('<div style="height:25px;"></div>', unsafe_allow_html=True)
            nav_left, nav_center, nav_right = st.columns([1,2,1])
            with nav_center:
                if st.button("GO TO LP PLAYER →", key="go_lp_from_fire", use_container_width=True):
                    st.session_state.my_room_view = "lp"
                    st.rerun()
            if st.button("← BACK TO ROOM SERVICE", key="my_room_back_fire", use_container_width=True):
                go_room_service()

        else:
            st.markdown('<div class="room-tabs">PLAY YOUR RECORD</div>', unsafe_allow_html=True)
            render_lp_player(st.session_state.current_record)

            st.markdown('<div class="room-tabs">RECORD CABINET</div>', unsafe_allow_html=True)
            if not st.session_state.room_records:
                st.markdown(
                    '<div class="room-record-empty">아직 객실로 가져온 음악이 없습니다.<br>ROOM SERVICE에서 음악을 선택해 주세요.</div>',
                    unsafe_allow_html=True
                )
                if st.button("GO TO ROOM SERVICE", key="go_room_service_empty", use_container_width=True):
                    go_room_service()
            else:
                for index, record in enumerate(st.session_state.room_records):
                    img_col, info_col, action_col = st.columns([1,4,1.5], vertical_alignment="center")
                    with img_col:
                        if record.get("artwork"):
                            st.image(record["artwork"], width=86)
                    with info_col:
                        st.markdown(
                            '<div class="room-record-title">' + escape(record.get("track", "RECORD")) + '</div>'
                            '<div class="room-record-meta">' + escape(record.get("artist", "")) + '<br>' + escape(record.get("album", "")) + '</div>',
                            unsafe_allow_html=True
                        )
                    with action_col:
                        if st.button("PLAY ON LP", key=f"cabinet_play_{index}_{record.get('track_id')}", use_container_width=True):
                            st.session_state.current_record = record
                            st.rerun()
                        if st.button("RETURN", key=f"cabinet_return_{index}_{record.get('track_id')}", use_container_width=True):
                            remove_from_room(record.get("track_id"))
                            st.rerun()
                    st.markdown('<div style="height:1px;background:rgba(199,157,109,0.10);margin:8px 0 16px 0;"></div>', unsafe_allow_html=True)

            st.markdown('<div style="height:25px;"></div>', unsafe_allow_html=True)
            nav_left, nav_center, nav_right = st.columns([1,2,1])
            with nav_center:
                if st.button("← BACK TO FIREPLACE", key="back_to_fireplace", use_container_width=True):
                    st.session_state.my_room_view = "fireplace"
                    st.rerun()
            if st.button("← BACK TO ROOM SERVICE", key="my_room_back_lp", use_container_width=True):
                go_room_service()

