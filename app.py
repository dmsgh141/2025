# filename: test.py
import streamlit as st
import pandas as pd
from io import StringIO

RAW_CSV = """title,genre,mood,tempo,media,desc,link
나 혼자만 레벨업,Action,긴장감 넘치는,빠른 전개,Webtoon,헌터 세계에서 각성한 주인공의 성장기,https://comic.naver.com
신의 탑,Fantasy,미스터리,중간 속도,Webtoon,탑을 오르며 펼쳐지는 모험과 갈등,https://comic.naver.com
유미의 세포들,Romance,밝고 유쾌,중간 속도,Webtoon,세포 시점으로 보는 사랑과 일상,https://comic.naver.com
귀멸의 칼날,Action,감정적,빠른 전개,Manga,가족의 복수를 위한 소년의 여정,https://www.shonenjump.com
원피스,Adventure,유쾌하고 활기찬,느긋한 전개,Manga,해적들의 꿈과 우정 이야기,https://www.shonenjump.com
나루토,Adventure,감동적인,빠른 전개,Manga,닌자의 세계에서 인정받기 위한 소년의 성장기,https://www.shonenjump.com
드래곤볼,Action,에너지 넘치는,빠른 전개,Manga,손오공과 동료들의 전설적인 모험,https://www.shonenjump.com
진격의 거인,Thriller,어두운,빠른 전개,Manga,거인과 인류의 생존 전투,https://www.shonenjump.com
슬램덩크,Sports,열정적인,중간 속도,Manga,농구로 성장하는 소년들의 이야기,https://www.shonenjump.com
하이큐,Sports,밝고 활기찬,빠른 전개,Manga,배구 소년들의 도전기,https://www.shonenjump.com
블리치,Action,미스터리,빠른 전개,Manga,사신의 세계에서 펼쳐지는 모험,https://www.shonenjump.com
데스노트,Thriller,지적인,중간 속도,Manga,죽음의 노트를 둘러싼 심리전,https://www.shonenjump.com
쿠베라,Fantasy,철학적,중간 속도,Webtoon,신과 인간, 마법이 얽힌 거대한 서사,https://comic.naver.com
헬퍼,Action,하드코어,빠른 전개,Webtoon,범죄와 복수를 그린 하드보일드 액션,https://comic.naver.com
노블레스,Fantasy,차분한,중간 속도,Webtoon,오랜 잠에서 깬 귀족의 이야기,https://comic.naver.com
호오즈키의 냉철,Comedy,풍자적,느긋한 전개,Manga,지옥을 배경으로 한 코믹 판타지,https://www.shonenjump.com
가정교사 히트맨 리본,Action,유쾌한,중간 속도,Manga,마피아 후계자의 성장기,https://www.shonenjump.com
스파이 패밀리,Comedy,따뜻한,중간 속도,Manga,가짜 가족의 스파이 코미디,https://www.shonenjump.com
체인소맨,Horror,충격적,빠른 전개,Manga,체인소 악마와 소년의 사투,https://www.shonenjump.com
원펀맨,Comedy,패러디적,빠른 전개,Webtoon,최강 히어로의 일상과 유머,https://comic.naver.com
"""

@st.cache_data
def load_data():
    return pd.read_csv(StringIO(RAW_CSV))

st.set_page_config(page_title="만화 · 웹툰 추천기", page_icon="📚", layout="wide")
df = load_data()

# 문자열 앞뒤 공백 제거
for col in ["genre", "mood", "tempo", "media"]:
    df[col] = df[col].astype(str).str.strip()

# ✅ 무조건 다양한 옵션 뽑기 (중복 제거 + 정렬)
genres = sorted(df["genre"].unique().tolist())
moods = sorted(df["mood"].unique().tolist())
tempos = sorted(df["tempo"].unique().tolist())
medias = sorted(df["media"].unique().tolist())

# UI
st.title("📚 만화 · 웹툰 추천기")

col1, col2, col3, col4 = st.columns(4)
with col1:
    sel_genre = st.selectbox("🎭 장르", genres)
with col2:
    sel_mood = st.selectbox("🎨 분위기", moods)
with col3:
    sel_tempo = st.selectbox("⏱ 전개 속도", tempos)
with col4:
    sel_media = st.selectbox("📺 매체", medias)

if st.button("🎯 추천 받기"):
    cond = (
        (df["genre"] == sel_genre) &
        (df["mood"] == sel_mood) &
        (df["tempo"] == sel_tempo) &
        (df["media"] == sel_media)
    )
    result = df[cond]
    if not result.empty:
        rec = result.sample(1).iloc[0]
        st.success("추천 결과 🎉")
        st.write(f"**{rec['title']}**")
        st.write(f"장르: {rec['genre']} | 분위기: {rec['mood']} | 전개: {rec['tempo']} | 매체: {rec['media']}")
        st.write(f"📖 {rec['desc']}")
        st.markdown(f"[🔗 보러가기]({rec['link']})")
    else:
        st.error("조건에 맞는 작품이 없어요 😢")

if st.button("🎲 랜덤 추천"):
    rec = df.sample(1).iloc[0]
    st.info("랜덤 결과 🎲")
    st.write(f"**{rec['title']}**")
    st.write(f"장르: {rec['genre']} | 분위기: {rec['mood']} | 전개: {rec['tempo']} | 매체: {rec['media']}")
    st.write(f"📖 {rec['desc']}")
    st.markdown(f"[🔗 보러가기]({rec['link']})")
