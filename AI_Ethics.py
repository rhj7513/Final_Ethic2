import streamlit as st
import re
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# ---------- 기본 설정 ----------
video_urls = [
    'https://www.youtube.com/watch?v=h9nQNPXPWig',
    'https://www.youtube.com/watch?v=eir-zqegNV8',
    'https://www.youtube.com/watch?v=iZhI5oD8zwM',
    'https://www.youtube.com/watch?v=oiz6hyvTbXY',
]
video_titles = [
    "돌봄 로봇 개요",
    "Paro (치유 인형)",
    "Pepper (감정인식 로봇)",
    "효돌이 (한국형 AI 돌봄로봇)"
]

st.set_page_config(layout="wide", page_title="EthicApp")
st.title("Ethic is good for us")

# ---------- 세션 상태 ----------
if 'video_index' not in st.session_state:
    st.session_state.video_index = 0
if 'section' not in st.session_state:
    st.session_state.section = "video"

# ---------- 사이드바 ----------
st.sidebar.subheader("Menu...")
if st.sidebar.button("📺 AI 돌봄 로봇이란?"):
    st.session_state.section = "video"
if st.sidebar.button("🧠 윤리적 문제는?"):
    st.session_state.section = "ethics"
if st.sidebar.button("✍️ 나의 생각은?"):
    st.session_state.section = "opinion"
if st.sidebar.button("📂 학생 의견 보기"):
    st.session_state.section = "student_data"

# ---------- 화면 구성 ----------
col1, col2 = st.columns((4, 1))

with col1:
    section = st.session_state.section

    # 🎥 영상 탭
    if section == "video":
        idx = st.session_state.video_index
        st.subheader(f"👀 영상으로 보는 'AI 돌봄 로봇' – {video_titles[idx]}")
        st.video(video_urls[idx])

        prev_col, next_col = st.columns([1, 1])
        with prev_col:
            if st.button("⬅️ 이전 영상", use_container_width=True, key="prev"):
                st.session_state.video_index = (idx - 1) % len(video_urls)
                st.rerun()

        with next_col:
            if st.button("다음 영상 ➡️", use_container_width=True, key="next"):
                st.session_state.video_index = (idx + 1) % len(video_urls)
                st.rerun()

        st.caption(f"📼 현재 영상: {idx + 1} / {len(video_urls)}")

    # 🤖 윤리 탭
    elif section == "ethics":
        st.subheader("🤖 돌봄 로봇의 윤리")
        st.markdown("""
        - Pepper, Paro, 효돌이와 같은 AI 로봇이 인간을 어떻게 돌보는지 살펴보세요.  
        - 돌봄은 따뜻함인가, 효율성인가?  
        - 감정 인식, 인간 대체, 책임성 등의 윤리적 쟁점을 함께 고민해보세요.
        """)

    # ✍️ 의견 작성
    elif section == "opinion":
        st.subheader("✍️ 나의 생각을 적어보세요")

        st.markdown("<p style='font-size:20px; font-weight:bold; margin-bottom:5px;'>이름을 입력하세요</p>", unsafe_allow_html=True)
        user_name = st.text_input(label="", key="name", label_visibility="collapsed")

        st.markdown("<p style='font-size:20px; font-weight:bold; margin-bottom:5px;'>돌봄 로봇이 왜 필요할까? 영상을 시청 후 자유롭게 작성해주세요.</p>", unsafe_allow_html=True)
        user_opinion = st.text_area(label="", key="opinion", label_visibility="collapsed")

        if st.button("제출하기", key="submit"):
            if user_name.strip() == "" or user_opinion.strip() == "":
                st.warning("이름과 의견을 모두 입력해주세요.")
            else:
                with open("./data/data.txt", "a", encoding="utf-8") as f:
                    f.write(f"[이름] {user_name}\n[의견] {user_opinion}\n{'-'*40}\n")
                st.success("의견이 성공적으로 제출되었습니다. 감사합니다!")

    # 📂 학생 의견 보기
    elif section == "student_data":
        st.subheader("📋 제출된 학생 의견")

        try:
            with open("./data/data.txt", "r", encoding="utf-8") as f:
                data = f.read()

            if data.strip() == "":
                st.info("아직 제출된 의견이 없습니다.")
            else:
                st.text_area("전체 의견 보기", data, height=300, disabled=True)

                # 단어 빈도 분석
                opinions = re.findall(r"\[의견\](.*?)\-{10,}", data, re.DOTALL)
                all_text = " ".join(opinions).lower()
                tokens = re.findall(r"\b[가-힣a-zA-Z]{2,}\b", all_text)
                word_counts = Counter(tokens)
                df_freq = pd.DataFrame(word_counts.most_common(10), columns=["단어", "출현 빈도수"])

                # st.markdown("### ☁️ 단어 워드클라우드")

                # try:
                #     wordcloud = WordCloud(
                #         font_path=None,  # 🔥 중요: 폰트 경로 없이 명시적으로 설정
                #         width=800,
                #         height=400,
                #         background_color='white',
                #         colormap='tab10'
                #     ).generate(" ".join(tokens))

                #     fig_wc, ax_wc = plt.subplots(figsize=(10, 5))
                #     ax_wc.imshow(wordcloud, interpolation='bilinear')
                #     ax_wc.axis("off")
                #     st.pyplot(fig_wc)

                # except Exception as e:
                #     st.warning(f"⚠️ 워드클라우드 생성 중 오류 발생: {e}")

        except FileNotFoundError:
            st.error("data.txt 파일이 존재하지 않습니다.")

# ---------- Tips 영역 ----------
with col2:
    st.subheader("💡 Tips...")
    st.info("""
    ▸ 돌봄 로봇은 인간을 대신할 수 있을까요?  
    ▸ 감정을 인식하고 반응하는 AI는 인간과 같을까요?  
    ▸ 우리는 이 기술을 어떻게 바라보아야 할까요?
    """)
    st.markdown("---")
    st.write("👉 아래 영상은 수업 도입용으로 사용 가능합니다.")
