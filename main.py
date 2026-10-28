                st.rerun()

    else:
        user_email = ""
        if st.session_state.current_user is not None:
            user_email = getattr(st.session_state.current_user, "email", "") or ""

        view = st.session_state.my_room_view

        if view == "room":
            render_room_lobby()
            st.markdown('<div style="height:18px"></div>', unsafe_allow_html=True)
            if st.button("← BACK TO ROOM SERVICE", key="my_room_back_room", use_container_width=True):
                go_room_service()

        elif view == "fireplace":
            render_fireplace()
            st.markdown('<div style="height:18px"></div>', unsafe_allow_html=True)
            nav_left, nav_center, nav_right = st.columns([1,2,1])
            with nav_center:
                if st.button("← BACK TO MY ROOM", key="back_room_from_fire", use_container_width=True):
                    st.session_state.my_room_view = "room"
                    st.rerun()
            if st.button("← BACK TO ROOM SERVICE", key="my_room_back_fire", use_container_width=True):
                go_room_service()

        elif view == "lp":
            st.markdown('<div class="room-tabs">PLAY YOUR RECORD</div>', unsafe_allow_html=True)
            render_lp_player(st.session_state.current_record)
            nav_left, nav_center, nav_right = st.columns([1,2,1])
            with nav_center:
                if st.button("← BACK TO MY ROOM", key="back_room_from_lp", use_container_width=True):
                    st.session_state.my_room_view = "room"
                    st.rerun()
            if st.button("← BACK TO ROOM SERVICE", key="my_room_back_lp", use_container_width=True):
                go_room_service()

        elif view == "bookshelf":
            st.markdown(
                '<div class="room-service-container"><div class="room-service-title">BOOKSHELF</div>'
                '<div class="room-service-subtitle">책장에 두고 싶은 책을 모아두세요.</div></div>',
                unsafe_allow_html=True
            )
            with st.form("add_room_book_form", clear_on_submit=True):
                book_title = st.text_input("책 제목", placeholder="예: 책 제목을 입력하세요")
                book_author = st.text_input("작가", placeholder="작가 이름")
                book_note = st.text_input("짧은 메모 (선택)", placeholder="이 책을 고른 이유")
                submitted_book = st.form_submit_button("책장에 추가")
                if submitted_book:
                    if book_title.strip():
                        st.session_state.room_books.append({"title": book_title.strip(), "author": book_author.strip(), "note": book_note.strip()})
                        st.rerun()
                    else:
                        st.warning("책 제목을 입력해 주세요.")

            if not st.session_state.room_books:
                st.markdown(
                    '<div class="room-record-empty">아직 책장에 등록한 책이 없습니다.<br>위에서 실제 책 제목과 작가를 추가해 주세요.</div>',
                    unsafe_allow_html=True
                )
            else:
                for book_index, book in enumerate(st.session_state.room_books):
                    book_col, detail_col, remove_col = st.columns([1, 5, 1.2], vertical_alignment="center")
                    with book_col:
                        st.markdown('<div style="font-size:32px;text-align:center;">📖</div>', unsafe_allow_html=True)
                    with detail_col:
                        st.markdown(
                            '<div class="room-record-title">' + escape(book.get("title", "책")) + '</div>'
                            '<div class="room-record-meta">' + escape(book.get("author", "")) + '</div>'
                            + ('<div class="room-record-meta">' + escape(book.get("note", "")) + '</div>' if book.get("note") else ''),
                            unsafe_allow_html=True
                        )
                    with remove_col:
                        if st.button("꺼내기", key=f"remove_room_book_{book_index}", use_container_width=True):
                            st.session_state.room_books.pop(book_index)
                            st.rerun()
                    st.markdown('<div style="height:1px;background:rgba(199,157,109,0.10);margin:8px 0 16px 0;"></div>', unsafe_allow_html=True)

            st.caption("참고: 현재 책 목록은 이 앱 세션에 저장됩니다. 계정별로 영구 저장하는 기능은 별도 DB 연동 단계에서 추가할 수 있어요.")

            # Keep the existing saved-record collection available separately from physical books.
            st.markdown('<div class="room-tabs" style="margin-top:34px;">MY RECORDS · 객실에 가져온 음반</div>', unsafe_allow_html=True)
            if not st.session_state.room_records:
                st.caption("아직 객실로 가져온 음반이 없습니다. ROOM SERVICE에서 음악을 선택해 주세요.")
            else:
                for record_index, record in enumerate(st.session_state.room_records):
                    record_art_col, record_info_col, record_action_col = st.columns([1, 4, 1.5], vertical_alignment="center")
                    with record_art_col:
                        if record.get("artwork"):
                            st.image(record["artwork"], width=72)
                    with record_info_col:
                        st.markdown(
                            '<div class="room-record-title">' + escape(record.get("track", "RECORD")) + '</div>'
                            '<div class="room-record-meta">' + escape(record.get("artist", "")) + '<br>' + escape(record.get("album", "")) + '</div>',
                            unsafe_allow_html=True
                        )
                    with record_action_col:
                        if st.button("PLAY ON LP", key=f"cabinet_play_{record_index}_{record.get('track_id')}", use_container_width=True):
                            st.session_state.current_record = record
                            st.session_state.my_room_view = "lp"
                            st.rerun()
                        if st.button("RETURN", key=f"cabinet_return_{record_index}_{record.get('track_id')}", use_container_width=True):
                            remove_from_room(record.get("track_id"))
                            st.rerun()

            nav_left, nav_center, nav_right = st.columns([1,2,1])
            with nav_center:
                if st.button("← BACK TO MY ROOM", key="back_room_from_shelf", use_container_width=True):
                    st.session_state.my_room_view = "room"
                    st.rerun()
            if st.button("← BACK TO ROOM SERVICE", key="my_room_back_shelf", use_container_width=True):
                go_room_service()

