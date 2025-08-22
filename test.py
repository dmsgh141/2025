import streamlit as st
import pandas as pd

# ------------------------
# 데이터 불러오기
# ------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("comics_sample_clean.csv", encoding="utf-8")
    return df

df = load_data()

# ------------------------
# 앱 기본 설정
# ------------------------
st.set_page_config(page_title="만화·웹툰 추천기 🎉", layout="wide")

st.title("📚 나만의 만화·웹툰 추천기")
st.write("당신의 취향에 맞는 작품을 찾아드릴게요! ✨")

# ------------------------
# 질문 단계
# ------------------------
genre = st.selectbox("🎭 어떤 장르가 좋아요?", df["genre"].unique())
mood = st.selectbox("🌈 분위기를 골라주세요!", df["mood"].unique())
tempo = st.selectbox("⏱️ 전개 속도는 어떤 게 좋아요?", df["tempo"].unique())
media = st.selectbox("💻 매체는?", df["media"].unique())

# ------------------------
# 추천 로직
# ------------------------
if st.button("📖 작품 추천받기"):
    results = df[
        (df["genre"] == genre) &
        (df["mood"] == mood) &
        (df["tempo"] == tempo) &
        (df["media"] == media)
    ]

    if results.empty:
        st.warning("정확히 맞는 작품이 없네요! 대신 비슷한 작품을 추천해드릴게요 😅")
        results = df[
            (df["genre"] == genre) &
            (df["media"] == media)
        ]

    if not results.empty:
        choice = results.sample(1).iloc[0]

        st.subheader(f"🎉 당신을 위한 추천 작품: **{choice['title']}**")
        st.image(choice["image"], width=300)
        st.write(choice["desc"])
        st.markdown(f"[👉 작품 보러 가기]({choice['link']})")
