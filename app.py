# filename: test.py
import streamlit as st
import pandas as pd
from io import StringIO

# ------------------------------------------------------------
# 내장 데이터셋 (100개 작품 풀버전)
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
도박묵시록 카이지,Thriller,긴장감 넘치는,중간 속도,Manga,생존을 건 심리 게임,https://www.shonenjump.com
은혼,Comedy,패러디적,빠른 전개,Manga,패러디와 개그로 가득한 사무라이 이야기,https://www.shonenjump.com
리제로,Fantasy,어두운,중간 속도,Light Novel,죽음을 반복하는 소년의 운명,https://www.kadokawa.co.jp
소드 아트 온라인,Fantasy,가상현실,빠른 전개,Light Novel,VRMMORPG 속 모험,https://www.kadokawa.co.jp
엔젤전설,Comedy,착각 코미디,중간 속도,Manga,착한 주인공이 무서운 외모로 오해받는 이야기,https://www.shonenjump.com
약속의 네버랜드,Thriller,미스터리,빠른 전개,Manga,고아원의 숨겨진 진실을 파헤치는 아이들,https://www.shonenjump.com
테라포마스,Sci-Fi,하드코어,빠른 전개,Manga,진화한 바퀴벌레와 인류의 전투,https://www.shonenjump.com
베르세르크,Fantasy,다크,느린 전개,Manga,어둠 속에서 싸우는 검사의 이야기,https://www.younganimal.com
헬싱,Horror,고딕적,중간 속도,Manga,뱀파이어와 비밀 조직의 대결,https://www.younganimal.com
강철의 연금술사,Fantasy,감동적인,중간 속도,Manga,연금술사 형제의 여정,https://www.shonenjump.com
블랙 클로버,Fantasy,열정적인,빠른 전개,Manga,마법과 우정의 소년 만화,https://www.shonenjump.com
주술회전,Fantasy,스릴 넘치는,빠른 전개,Manga,저주와 마술사의 전투,https://www.shonenjump.com
페어리 테일,Fantasy,따뜻한,중간 속도,Manga,마법 길드의 우정과 모험,https://www.shonenjump.com
던만추,Fantasy,모험적인,중간 속도,Light Novel,던전 속 신과 인간의 이야기,https://www.kadokawa.co.jp
이세계 콰르텟,Comedy,패러디적,빠른 전개,Anime,이세계 캐릭터들의 코미디,https://www.kadokawa.co.jp
클레이모어,Fantasy,다크,빠른 전개,Manga,요괴와 싸우는 여전사들,https://www.shonenjump.com
플루토,Sci-Fi,지적인,느린 전개,Manga,인공지능과 인간의 갈등,https://www.shonenjump.com
20세기 소년,Mystery,스릴 넘치는,중간 속도,Manga,어린 시절 비밀과 세계 멸망 음모,https://www.shonenjump.com
몽키 피크,Horror,긴장감 넘치는,빠른 전개,Manga,생존을 건 산악 호러,https://www.shonenjump.com
골든 카무이,Adventure,역사적,중간 속도,Manga,금괴를 둘러싼 사투와 문화 이야기,https://www.shonenjump.com
식극의 소마,Comedy,열정적인,빠른 전개,Manga,요리 배틀과 성장 이야기,https://www.shonenjump.com
히카루의 바둑,Sports,차분한,중간 속도,Manga,바둑을 통해 성장하는 소년 이야기,https://www.shonenjump.com
데이트 어 라이브,Fantasy,로맨틱,중간 속도,Light Novel,정령과의 데이트로 세상을 구한다,https://www.kadokawa.co.jp
강식장갑 가이버,Sci-Fi,하드코어,빠른 전개,Manga,바이오 슈트와 괴수의 전투,https://www.shonenjump.com
블러드 레인,Horror,스릴 넘치는,빠른 전개,Webtoon,뱀파이어와 인간의 대립,https://comic.naver.com
D.Gray-man,Fantasy,어두운,중간 속도,Manga,엑소시스트들의 전투,https://www.shonenjump.com
아인,Horror,긴장감 넘치는,빠른 전개,Manga,불사의 존재와 인간의 갈등,https://www.shonenjump.com
강철신 지그,Action,레트로,빠른 전개,Anime,고전 슈퍼 로봇의 부활,https://www.toei.co.jp
헌터x헌터,Adventure,지적인,중간 속도,Manga,헌터 시험과 미지의 모험,https://www.shonenjump.com
카우보이 비밥,Sci-Fi,재즈 감성,느긋한 전개,Anime,현상금 사냥꾼들의 쓸쓸한 모험,https://www.sunrise-inc.co.jp
사무라이 참프루,Action,힙합 감성,빠른 전개,Anime,사무라이와 힙합의 결합,https://www.manglobe.net
은하철도 999,Sci-Fi,철학적,느린 전개,Anime,우주를 여행하는 철도 이야기,https://www.toei.co.jp
바람의 검심,Action,역사적,중간 속도,Manga,겉은 방랑자 속은 검사인 남자의 이야기,https://www.shonenjump.com
스즈미야 하루히의 우울,Comedy,초현실적,중간 속도,Light Novel,괴짜 소녀와 SOS단의 모험,https://www.kadokawa.co.jp
클라나드,Romance,감동적,느린 전개,Visual Novel,가슴 아픈 가족 이야기,https://key.visualarts.gr.jp
에반게리온,Sci-Fi,심리적,중간 속도,Anime,거대한 로봇과 인류의 구원,https://www.gainax.co.jp
토리코,Adventure,유쾌한,빠른 전개,Manga,음식을 향한 모험과 전투,https://www.shonenjump.com
레벨E,Comedy,SF 패러디,중간 속도,Manga,외계인의 황당한 지구생활,https://www.shonenjump.com
바쿠만,Slice of Life,현실적,중간 속도,Manga,만화가를 꿈꾸는 소년들의 이야기,https://www.shonenjump.com
블루 록,Sports,치열한,빠른 전개,Manga,축구와 생존 경쟁,https://www.shonenjump.com
데빌맨,Horror,비극적,빠른 전개,Manga,악마와 인간의 충돌,https://www.shonenjump.com
카이지 2,Thriller,지독한,중간 속도,Manga,또 다른 심리 도박의 세계,https://www.shonenjump.com
죠죠의 기묘한 모험,Adventure,스타일리시,빠른 전개,Manga,세대를 이어가는 기묘한 전투,https://www.shonenjump.com
스펙트럼맨,Sci-Fi,고전적,빠른 전개,Anime,히어로 특촬물 애니메이션,https://www.toei.co.jp
마루코는 아홉살,Slice of Life,유쾌한,중간 속도,Anime,초등학생의 일상과 가족 이야기,https://www.nippon-animation.co.jp
짱구는 못말려,Comedy,엉뚱한,빠른 전개,Anime,엉뚱 발랄한 꼬마의 일상,https://www.tv-asahi.co.jp
도라에몽,Comedy,따뜻한,중간 속도,Manga,고양이형 로봇과 아이들의 모험,https://www.shogakukan.co.jp
명탐정 코난,Mystery,지적인,빠른 전개,Manga,소년 탐정의 추리 모험,https://www.shogakukan.co.jp
원아웃,Thriller,치밀한,중간 속도,Manga,도박 같은 야구 심리전,https://www.shonenjump.com
캡틴 츠바사,Sports,열정적인,빠른 전개,Manga,축구로 꿈을 향해 달리는 소년,https://www.shonenjump.com
가면라이더 스피리츠,Action,레트로,빠른 전개,Manga,고전 특촬물의 만화판,https://www.shonenjump.com
베이블레이드,Sports,유쾌한,빠른 전개,Anime,배틀 팽이의 대결,https://www.takaratomy.co.jp
유희왕,Fantasy,전략적,중간 속도,Manga,카드 배틀과 모험,https://www.shonenjump.com
소드 브레이커,Fantasy,액션,빠른 전개,Light Novel,검과 마법의 대결,https://www.kadokawa.co.jp
하이스쿨 DxD,Fantasy,코믹 섹시,중간 속도,Light Novel,악마와의 학교 생활,https://www.kadokawa.co.jp
갓 오브 하이스쿨,Action,격투 중심,빠른 전개,Webtoon,전국 고등학생 격투 대회,https://comic.naver.com
외모지상주의,Slice of Life,풍자적,중간 속도,Webtoon,외모와 계급 사회 풍자,https://comic.naver.com
싸움독학,Action,스릴 넘치는,빠른 전개,Webtoon,격투 기술을 배우는 소년,https://comic.naver.com
인생존망,Thriller,긴장감 넘치는,빠른 전개,Webtoon,죽음의 게임에서 살아남기,https://comic.naver.com
독립일기,Slice of Life,밝고 유쾌,중간 속도,Webtoon,자취생 일상의 소소한 이야기,https://comic.naver.com
지옥,Horror,철학적,느린 전개,Webtoon,예고된 죽음과 인간의 반응,https://comic.naver.com
연애혁명,Romance,코믹,중간 속도,Webtoon,고등학생들의 풋풋한 연애,https://comic.naver.com
뷰티풀 군바리,Comedy,엉뚱한,빠른 전개,Webtoon,군대 속 다양한 에피소드,https://comic.naver.com
삼국지,History,전략적,중간 속도,Manga,중국 고전 삼국지의 만화판,https://www.shonenjump.com
봉신연의,Fantasy,고전적,중간 속도,Manga,중국 신화를 바탕으로 한 전투,https://www.shonenjump.com
킹덤,History,치열한,빠른 전개,Manga,중국 전국시대 전쟁 이야기,https://www.shonenjump.com
아라카와 언더 더 브리지,Comedy,초현실적,중간 속도,Manga,강 밑 마을의 기묘한 사람들,https://www.shonenjump.com
아키라,Sci-Fi,사이버펑크,중간 속도,Manga,도쿄 붕괴 이후 초능력 소년 이야기,https://www.shonenjump.com
블루 자이언트,Slice of Life,재즈 감성,중간 속도,Manga,재즈 색소폰을 꿈꾸는 소년,https://www.shonenjump.com
노다메 칸타빌레,Romance,음악적,중간 속도,Manga,피아니스트와 지휘자의 성장,https://www.shonenjump.com
베케몬,Comedy,엉뚱한,빠른 전개,Webtoon,귀여운 캐릭터들의 일상,https://comic.naver.com
좀비고,Action,스릴 넘치는,빠른 전개,Webtoon,좀비 아포칼립스 속 생존,https://comic.naver.com
슈퍼 우리집,Comedy,따뜻한,중간 속도,Webtoon,가족과의 유쾌한 일상,https://comic.naver.com
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
