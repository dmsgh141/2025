# filename: test.py
import streamlit as st
import pandas as pd
from io import StringIO

# ------------------------------------------------------------
# 내장 데이터셋
# ------------------------------------------------------------
RAW_CSV = """title,genre,mood,tempo,media,desc,link
나 혼자만 레벨업,Action,긴장감 넘치는,빠른 전개,Webtoon,헌터 세계에서 각성한 주인공의 성장기,https://comic.naver.com
신의 탑,Fantasy,미스터리,중간 속도,Webtoon,탑을 오르며 펼쳐지는 모험과 갈등,https://comic.naver.com
유미의 세포들,Romance,밝고 유쾌,중간 속도,Webtoon,세포 시점으로 보는 사랑과 일상,https://comic.naver.com
"""  # (중략) — 실제 데이터는 그대로 유지하세요!

# ------------------------------------------------------------
# 데이터 로드
# ------------------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv(StringIO(RAW_CSV))

st.set_page_config(page_title="만화 · 웹툰 추천기", page_icon="📚", layout="wide")
df = load_data()

for col in ["genre", "mood", "tempo", "media"]:
    df[col] = df[col].astype(str).str.strip()

# ------------------------------------------------------------
# 스타일 (CSS)
# ------------------------------------------------------------
st.markdown("""
<style>
    .stApp {background-color: #f9f9fb;}
    .block-container {padding-top: 2rem; padding-bottom: 2rem;}
    .result-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
    }
    h1 {color: #3b5998;}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# 헤더
# ------------------------------------------------------------
st.title("📚 나에게 딱 맞는 만화 · 웹툰 추천기")
st.caption("👉 질문 몇 개로 바로 추천받기 · 데이터 내장형 · CSV 파일 불필요")

st.divider()

# ------------------------------------------------------------
# 선택 영역
# ------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)
with col1:
    sel_genre = st.selectbox("🎭 장르", sorted(df["genre"].unique()))
with col2:
    sel_mood = st.selectbox("🎨 분위기", sorted(df["mood"].unique()))
with col3:
    sel_tempo = st.selectbox("⏱ 전개 속도", sorted(df["tempo"].unique()))
with col4:
    sel_media = st.selectbox("📺 매체", sorted(df["media"].unique()))

left, right = st.columns([1,1])
with left:
    go = st.button("🎯 추천 받기", use_container_width=True)
with right:
    random_go = st.button("🎲 랜덤 추천", use_container_width=True)

# ------------------------------------------------------------
# 추천 로직
# ------------------------------------------------------------
def pick_one(frame: pd.DataFrame):
    if frame.empty:
        return None
    return frame.sample(1).iloc[0]

def recommend(genre, mood, tempo, media):
    for cond in [
        (df["genre"]==genre) & (df["mood"]==mood) & (df["tempo"]==tempo) & (df["media"]==media),
        (df["genre"]==genre) & (df["mood"]==mood) & (df["tempo"]==tempo),
        (df["genre"]==genre) & (df["mood"]==mood),
        (df["genre"]==genre)
    ]:
        r = pick_one(df[cond])
        if r is not None:
            return r
    return pick_one(df)

# ------------------------------------------------------------
# 결과 영역
# ------------------------------------------------------------
if go:
    rec = recommend(sel_genre, sel_mood, sel_tempo, sel_media)
    if rec is not None:
        st.success("추천 결과를 가져왔어요!")
        with st.container():
            st.markdown(f"""
            <div class="result-card">
                <h3>🎬 {rec['title']}</h3>
                <p><b>장르</b>: {rec['genre']}  |  
                <b>분위기</b>: {rec['mood']}  |  
                <b>전개</b>: {rec['tempo']}  |  
                <b>매체</b>: {rec['media']}</p>
                <p>📖 {rec['desc']}</p>
                <a href="{rec['link']}" target="_blank">🔗 보러 가기</a>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.error("추천 데이터를 찾지 못했어요. 선택값을 바꿔보세요.")

if random_go:
    rec = df.sample(1).iloc[0]
    st.info("랜덤으로 하나 뽑았어요!")
    st.markdown(f"""
    <div class="result-card">
        <h3>🎬 {rec['title']}</h3>
        <p><b>장르</b>: {rec['genre']}  |  
        <b>분위기</b>: {rec['mood']}  |  
        <b>전개</b>: {rec['tempo']}  |  
        <b>매체</b>: {rec['media']}</p>
        <p>📖 {rec['desc']}</p>
        <a href="{rec['link']}" target="_blank">🔗 보러 가기</a>
    </div>
    """, unsafe_allow_html=True)

st.divider()
with st.expander("📖 전체 목록 보기"):
    st.dataframe(df, use_container_width=True)
