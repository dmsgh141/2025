# filename: test.py
import streamlit as st
import pandas as pd
from io import StringIO

# ------------------------------------------------------------
# 내장 데이터셋 (다양한 장르/분위기/매체 30여개 작품)
# ------------------------------------------------------------
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
미생,Slice of Life,현실적,느긋한 전개,Manhwa,직장인의 현실을 그린 드라마,https://comic.naver.com
치즈인더트랩,Romance,긴장감 있는,중간 속도,Webtoon,대학생들의 관계와 심리 묘사,https://comic.naver.com
칼의 노래,Historical,엄숙한,느긋한 전개,Manhwa,역사 속 인물의 삶과 결단,https://comic.naver.com
헌터x헌터,Adventure,치밀한,중간 속도,Manga,헌터가 되기 위한 소년의 여정,https://www.shonenjump.com
토리코,Adventure,유머러스한,빠른 전개,Manga,미식 헌터들의 모험과 전투,https://www.shonenjump.com
은혼,Comedy,풍자적,빠른 전개,Manga,에도시대 패러디 액션 코미디,https://www.shonenjump.com
플루토,Sci-Fi,진지한,중간 속도,Manga,인공지능과 인간의 철학적 대립,https://www.shonenjump.com
몬스터,Thriller,긴장감 넘치는,느긋한 전개,Manga,천재 의사와 연쇄 살인마의 대결,https://www.shonenjump.com
리얼,Sports,감동적인,느긋한 전개,Manga,장애인 농구를 다룬 휴먼 드라마,https://www.shonenjump.com
블랙클로버,Fantasy,열정적인,빠른 전개,Manga,마법이 전부인 세계의 소년 이야기,https://www.shonenjump.com
소드 아트 온라인,Sci-Fi,모험적,빠른 전개,Light Novel,가상 현실 MMORPG에서의 생존,https://www.kadokawa.co.jp
아노하나,Slice of Life,감성적,중간 속도,Anime,어린 시절 친구의 죽음을 극복하는 이야기,https://www.aniplex.co.jp
"""

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
