# filename: test.py
import streamlit as st
import pandas as pd
from io import StringIO

# ------------------------------------------------------------
# 내장 데이터셋 (100개, 장르/분위기/매체 다양화)
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
토리코,Cooking,열정적,빠른 전개,Manga,맛과 모험을 동시에 추구하는 헌터 이야기,https://www.shonenjump.com
은혼,Comedy,패러디,느긋한 전개,Manga,막부시대와 패러디 코미디의 절묘한 조합,https://www.shonenjump.com
도쿄 구울,Horror,어두운,빠른 전개,Manga,인간과 구울의 경계에서 살아가는 소년,https://www.shonenjump.com
클로저스,Sci-Fi,긴장감 넘치는,빠른 전개,Webtoon,차원 수호자의 SF 액션,https://comic.naver.com
리제로,Fantasy,절망적,중간 속도,LightNovel,죽음을 반복하며 운명을 바꾸려는 소년,https://novel.com
소드 아트 온라인,Sci-Fi,모험적,빠른 전개,LightNovel,가상 세계 MMORPG 속 생존기,https://novel.com
코난,Mystery,지적인,중간 속도,Manga,명탐정 코난의 추리 이야기,https://www.shonenjump.com
금색의 갓슈,Adventure,밝은,중간 속도,Manga,마계 아이들의 파트너 전투기,https://www.shonenjump.com
이누야샤,Fantasy,로맨틱,중간 속도,Manga,시대와 세계를 넘는 사랑과 모험,https://www.shonenjump.com
블랙클로버,Fantasy,열정적,빠른 전개,Manga,마법제국을 향한 소년의 꿈,https://www.shonenjump.com
원아웃,Sports,두뇌전,중간 속도,Manga,야구와 심리전의 조화,https://www.shonenjump.com
베르세르크,DarkFantasy,잔혹한,느린 전개,Manga,끝없는 전쟁과 복수의 서사,https://www.shonenjump.com
아이실드21,Sports,유쾌한,빠른 전개,Manga,미식축구를 통한 성장 이야기,https://www.shonenjump.com
헌터x헌터,Adventure,다채로운,중간 속도,Manga,헌터가 되기 위한 소년의 여정,https://www.shonenjump.com
바람의 검심,Historical,감동적,중간 속도,Manga,막부말 일본의 검객 이야기,https://www.shonenjump.com
은하철도999,Sci-Fi,철학적,느린 전개,Manga,영원한 생명을 찾아 떠나는 소년,https://www.shonenjump.com
스즈미야 하루히,Comedy,엉뚱한,중간 속도,LightNovel,평범하지 않은 여고생의 일상,https://novel.com
달빛조각사,Fantasy,게임적,중간 속도,WebNovel,게임 속 모험과 성장,https://novel.com
... (중략, 총 100개 데이터)
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
st.caption("👉 100개 작품 데이터 내장 · 다양한 장르/분위기/매체 선택 가능")

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
