import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="EthicApp 메인화면",
    page_icon="🌐",
    layout="wide"
)

# 타이틀
st.title("👋 Welcome to EthicApp")

# 폰트 스타일 추가
st.markdown("""
<style>
h2 { font-size: 28px !important; }       /* ## 제목 */
h3 { font-size: 24px !important; }       /* ### 소제목 */
ul, ol, p, li, div {
    font-size: 18px !important;
}
</style>
""", unsafe_allow_html=True)

# 소개 메시지
st.markdown("""
---
## 🌟 이 웹앱은 무엇인가요?

> **AI 돌봄 로봇, 효도일까 방임일까?**  
> 를 주제로 한 **AI 윤리 융합 수업 웹앱**입니다.

---

### 📂 좌측 탭에서 페이지를 선택하세요:

- **AI 윤리 수업** 👉 AI 윤리 수업 활동이 담긴 메인 페이지 (Main page for AI Ethics activities)
- **노인 감정분석** 👉 노인 감정 분석 AI 도구 (AI tool for Elderly Emotion Analysis)

---

### 💡 사용법

1. 왼쪽 상단 ≡ 메뉴를 클릭하여 페이지 목록을 확인합니다.  
2. 원하는 페이지를 선택하여 수업 자료 또는 학생 의견을 살펴보세요.  
3. run.py에서 학생 의견을 직접 작성할 수도 있어요 ✍️  

---

🎓 **학생 참여형 AI 윤리 수업을 위한 플랫폼**,  
지금 바로 시작해볼까요?
""")
