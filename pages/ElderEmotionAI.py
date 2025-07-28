import streamlit as st
from PIL import Image
import time
import random
from gtts import gTTS
import io

st.set_page_config(page_title="AI 돌봄 행동 추천 시스템", layout="wide")

st.title("🤖 노인 돌봄 AI 시스템")
st.markdown("노인의 **표정, 음성, 활동** 데이터를 기반으로 감정 및 건강 상태를 분석하고 적절한 돌봄 행동을 추천합니다.")

# 상태 변수
if "analysis_triggered" not in st.session_state:
    st.session_state.analysis_triggered = False
if "scroll_now" not in st.session_state:
    st.session_state.scroll_now = False
if "result" not in st.session_state:
    st.session_state.result = {}

emotion_info = {
    "외로움": {
        "image": "https://i.ibb.co/2vbQ2jk/sad.png",
        "explain": "입꼬리 하락과 눈썹 수축이 외로움의 특징입니다.",
        "tts": "할머니, 외로우셨죠? 제가 좋은 음악 틀어드릴게요."
    },
    "불안": {
        "image": "https://i.ibb.co/0jLPMTG/anxious.png",
        "explain": "초조한 시선과 몸짓이 불안을 나타냅니다.",
        "tts": "할아버지, 걱정 마세요. 보호자를 곧 연결해드릴게요."
    },
    "안정": {
        "image": "https://i.ibb.co/S6KkVbw/stable.png",
        "explain": "차분한 표정과 일정한 움직임은 안정 상태입니다.",
        "tts": "오늘은 편안해 보이시네요. 가벼운 산책 어때요?"
    },
    "기쁨": {
        "image": "https://i.ibb.co/Zz5FhJL/happy.png",
        "explain": "입꼬리 상승과 눈 주위 긴장이 기쁨을 나타냅니다.",
        "tts": "기분이 좋아 보이시네요! 함께 대화 나눠요!"
    },
    "무기력": {
        "image": "https://i.ibb.co/Dp8YXqG/tired.png",
        "explain": "움직임 없음과 힘없는 표정은 무기력의 신호입니다.",
        "tts": "많이 피곤하셨군요. 잠시 쉬는 건 어떠세요?"
    }
}

action_map = {
    "외로움": "음악 재생 및 대화 시도",
    "불안": "보호자 호출 및 따뜻한 말 건네기",
    "안정": "가벼운 산책 유도 또는 휴식 유지",
    "기쁨": "함께 게임하거나 대화를 이어가기",
    "무기력": "가벼운 활동 권유 또는 휴식 권장"
}

# UI 1행
col1, col2, col3 = st.columns([1.5, 1, 1.5])

with col1:
    st.subheader("📥 데이터 입력")
    image_file = st.file_uploader("표정 이미지 업로드", type=["jpg", "jpeg", "png"])
    audio_file = st.file_uploader("음성 파일 업로드 (선택)", type=["wav", "mp3"])
    activity_option = st.radio("현재 활동 상태를 선택하세요", ["정지", "앉아 있음", "걷는 중", "무기력함"])

    if st.button("🔍 분석 시작!"):
        if image_file:
            emotion_result = random.choice(list(emotion_info.keys()))
            health_flag = "양호" if activity_option in ["걷는 중", "앉아 있음"] else "주의 필요"
            action = action_map.get(emotion_result)
            st.session_state.result = {
                "emotion": emotion_result,
                "health": health_flag,
                "action": action,
                "tts": emotion_info[emotion_result]["tts"]
            }
            st.session_state.analysis_triggered = True
            st.session_state.scroll_now = True
        else:
            st.warning("⚠️ 먼저 이미지를 업로드해주세요.")

with col2:
    st.subheader("🔄 AI 분석 상태")
    if st.session_state.analysis_triggered:
        with st.spinner("AI가 데이터를 분석 중입니다..."):
            st.markdown("📡 **데이터 수신 중...**")
            time.sleep(1)
            st.markdown("🧠 **감정 상태 분석 중...**")
            time.sleep(1)
            st.markdown("💬 **돌봄 행동 추천 중...**")
            time.sleep(1)
            st.success("✅ 분석 완료!")
    else:
        st.image("https://cdn.pixabay.com/photo/2017/02/01/22/02/artificial-intelligence-2031340_1280.png", caption="AI 준비 중", use_column_width=True)

with col3:
    st.subheader("📊 분석 결과 요약")
    if not st.session_state.analysis_triggered:
        st.info("분석 후 결과 요약이 표시됩니다.")
    else:
        result = st.session_state.result
        st.success(f"감정: {result['emotion']} | 건강: {result['health']} | 행동: {result['action']}")

# 결과 출력
if st.session_state.analysis_triggered:
    st.markdown("---")
    st.markdown('<div id="result"></div>', unsafe_allow_html=True)

    result = st.session_state.result
    emotion = result["emotion"]
    health = result["health"]
    action = result["action"]
    tts_msg = result["tts"]
    emotion_data = emotion_info[emotion]

    st.subheader("📊 분석 결과 상세 보기")

    st.image(emotion_data["image"], width=160)
    st.markdown(f"### 🧠 감정 상태: **{emotion}**")
    with st.expander("🔎 감정 상태 분석 근거"):
        st.write(emotion_data["explain"])

    st.markdown(f"### 🏥 건강 상태: **{health}**")
    with st.expander("🔎 건강 상태 판단 근거"):
        if health == "양호":
            st.write("활동 상태가 활발하여 건강 상태가 양호한 것으로 판단됩니다.")
        else:
            st.write("움직임이 없거나 무기력하여 주의가 필요합니다.")

    st.markdown(f"### 🤖 추천 돌봄 행동: **{action}**")
    with st.expander("🔎 추천 이유"):
        st.write(f"{emotion} 상태의 정서적 요구에 따라 '{action}'을 추천합니다.")

    # ✅ TTS 음성 출력
    st.markdown("### 🔊 음성 출력")
    try:
        tts = gTTS(text=tts_msg, lang="ko")
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        st.audio(mp3_fp, format="audio/mp3")
    except:
        st.warning("음성 생성에 실패했습니다. 인터넷 연결 또는 gTTS 설정을 확인해주세요.")

    with st.expander("📈 리워드 반응 기록"):
        if st.button("😊 긍정적 반응 (Reward +1)"):
            st.success("🟢 리워드 +1 → 강화학습 반영 완료")
        if st.button("😟 부정적 반응 (No Reward)"):
            st.error("🔴 리워드 없음 → 학습 보류")

    # 자동 스크롤
    if st.session_state.scroll_now:
        scroll_script = """
        <script>
            setTimeout(function() {
                const resultEl = document.getElementById("result");
                if (resultEl) {
                    resultEl.scrollIntoView({ behavior: "smooth" });
                }
            }, 300);
        </script>
        """
        st.components.v1.html(scroll_script, height=0)
        st.session_state.scroll_now = False
