import streamlit as st

# MBTI별 추천 작업/직업 데이터
mbti_jobs = {
    "INTJ": ["전략 기획", "데이터 분석", "연구원"],
    "ENTP": ["기업가", "마케팅", "컨설턴트"],
    "INFJ": ["상담사", "작가", "교육자"],
    "ESFP": ["연예인", "이벤트 플래너", "세일즈"],
    "ISTJ": ["회계사", "공무원", "프로젝트 매니저"],
    "ENFP": ["디자이너", "광고 기획자", "강연가"],
    # ... 나머지 MBTI도 추가 가능
}

st.title("MBTI 기반 진로 추천 웹앱")
st.write("당신의 MBTI를 선택하면 적절한 진로/작업을 추천해드립니다!")

# MBTI 선택
mbti = st.selectbox("당신의 MBTI를 선택하세요", list(mbti_jobs.keys()))

# 결과 출력
if mbti:
    st.subheader(f"🔎 {mbti} 유형을 위한 추천 작업/직업")
    for job in mbti_jobs[mbti]:
        st.write(f"- {job}")
