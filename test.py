# streamlit_app.py
# ------------------------------------------------------
# 📚 만화/웹툰 추천기 — 올인원(데이터+로직+디자인) 완성본
# - 외부 CSV 없이 바로 실행 가능
# - 조건 불일치 시 유사 조건(장르→분위기)로 단계적 대체 추천
# - 깔끔하고 세련된 미니멀 UI
# ------------------------------------------------------

import streamlit as st
import pandas as pd
import random
from io import StringIO

# ========== 데이터 (내장 CSV) ==========
RAW_CSV = """title,genre,mood,tempo,media,desc,image,link
Solo Leveling,Action/Fantasy,긴장감 넘치는,빠른 전개,Webtoon,약한 헌터가 레벨업 시스템으로 성장하는 이야기,https://upload.wikimedia.org/wikipedia/en/3/38/Solo_Leveling_Webtoon.png,https://comic.naver.com/webtoon/list?titleId=675554
Omniscient Reader's Viewpoint,Fantasy/Thriller,긴장감 넘치는,서서히 몰입,Webtoon,소설 속 세계에 들어가 시나리오를 바꾸는 이야기,https://upload.wikimedia.org/wikipedia/commons/3/3a/Omniscient_Reader%27s_Viewpoint_logo.png,https://series.naver.com/comic/detail.series?productNo=4975346
Tower of God,Action/Dark Fantasy,모험·미스터리,서서히 몰입,Webtoon,탑을 오르며 진실을 파헤치는 장기 연재,https://upload.wikimedia.org/wikipedia/en/4/4e/Tower_of_God_Volume_1.png,https://comic.naver.com/webtoon/list?titleId=183559
Noblesse,Dark Fantasy/Action,드라마틱,중간 속도,Webtoon,잠에서 깨어난 귀족의 현대 적응기와 전투,https://upload.wikimedia.org/wikipedia/en/2/21/Noblesse_Volume_1.jpg,https://comic.naver.com/webtoon/list?titleId=25455
The Gamer,Fantasy/Action,게임 느낌,빠른 전개,Webtoon,현실이 RPG처럼 변한 세계의 일상 액션,https://m.media-amazon.com/images/I/81p57xOQZtL._AC_UF1000,1000_QL80_.jpg,https://comic.naver.com/webtoon/list?titleId=402949
True Beauty,Romantic Comedy/Coming-of-age,밝고 감성적,서서히 몰입,Webtoon,외모와 자존감을 다루는 성장 로맨스,https://upload.wikimedia.org/wikipedia/en/f/fd/True_Beauty_TV_series.jpg,https://comic.naver.com/webtoon/list?titleId=703846
Love Revolution,Romantic Comedy,달달하고 유쾌,서서히 몰입,Webtoon,고등학생 커플의 사랑스러운 일상 로코,https://upload.wikimedia.org/wikipedia/en/3/31/Love_Revolution_%28webtoon%29.png,https://comic.naver.com/webtoon/list?titleId=570503
Misaeng,Drama/Reality,현실적·공감,느리지만 깊이,Webtoon,직장인의 삶을 현실적으로 그린 드라마,https://upload.wikimedia.org/wikipedia/en/8/8a/Misaeng_Volume_1.jpg,https://comic.naver.com/webtoon/list?titleId=552960
Lookism,Comedy/Social Drama,풍자적·웃픈,빠른 전개,Webtoon,두 개의 몸을 통해 외모 편견을 풍자하는 드라마,https://upload.wikimedia.org/wikipedia/en/3/33/Lookism%2C_Volume_1.jpg,https://comic.naver.com/webtoon/list?titleId=718021
Sweet Home,Horror/Thriller,어둡고 진지,빠른 전개,Webtoon,아파트에 고립된 사람들의 괴물 생존 스릴러,https://upload.wikimedia.org/wikipedia/en/4/48/Sweet_Home_Vol_1.jpg,https://comic.naver.com/webtoon/list?titleId=7038469
Bastard,Thriller,어둡고 진지,서서히 몰입,Webtoon,살인마 아버지와 아들의 숨막히는 비밀,https://upload.wikimedia.org/wikipedia/en/4/4a/Bastard_webtoon.jpg,https://comic.naver.com/webtoon/list?titleId=669723
Yumi's Cells,Slice of Life/Romance,힐링,중간 속도,Webtoon,유미의 머릿속 세포들이 전하는 일과 사랑,https://upload.wikimedia.org/wikipedia/en/0/0a/Yumi%27s_Cells.jpg,https://comic.naver.com/webtoon/list?titleId=651673
Itaewon Class,Drama,현실적·공감,긴 호흡,Webtoon,불합리한 사회에 맞서는 청춘 창업기,https://upload.wikimedia.org/wikipedia/en/0/0f/Itaewon_Class_poster.jpg,https://comic.naver.com/webtoon/list?titleId=703311
A Business Proposal,Romantic Comedy,달달하고 유쾌,빠른 전개,Webtoon,회사에서 시작된 계약 연애 로맨틱 코미디,https://upload.wikimedia.org/wikipedia/en/5/5e/A_Business_Proposal_poster.jpg,https://comic.naver.com/webtoon/list?titleId=6755541
Slam Dunk,Sports,열정적·도전적,빠른 전개,Manga,농구에 빠져드는 고등학생들의 성장기,https://upload.wikimedia.org/wikipedia/en/3/3f/Slam_Dunk_vol01_Cover.jpg,https://en.wikipedia.org/wiki/Slam_Dunk_(manga)
Haikyu!!,Sports,열정적·도전적,중간 속도,Manga,배구를 통해 성장하는 청춘 스포츠물,https://upload.wikimedia.org/wikipedia/en/6/6f/Haikyu%21%21_vol01.jpg,https://en.wikipedia.org/wiki/Haikyu!!
Blue Lock,Sports/Thriller,긴장감 넘치는,빠른 전개,Manga,스트라이커 육성 프로젝트의 서바이벌 축구,https://upload.wikimedia.org/wikipedia/en/e/e5/Blue_Lock_volume_1_cover.jpg,https://en.wikipedia.org/wiki/Blue_Lock
One Piece,Adventure/Action,밝고 유쾌,긴 호흡,Manga,바다를 무대로 펼쳐지는 모험과 우정,https://upload.wikimedia.org/wikipedia/en/6/65/OnePieceVol61Cover.jpg,https://en.wikipedia.org/wiki/One_Piece
My Hero Academia,Action/Superhero,밝고 유쾌,중간 속도,Manga,히어로 사회에서 성장하는 소년의 이야기,https://upload.wikimedia.org/wikipedia/en/3/3f/My_Hero_Academia_Volume_1.png,https://en.wikipedia.org/wiki/My_Hero_Academia
Chainsaw Man,Dark Fantasy/Action,어둡고 진지,빠른 전개,Manga,악마와 계약한 소년의 폭주 액션 드라마,https://upload.wikimedia.org/wikipedia/en/7/79/Chainsaw_Man_volume_1_cover.jpg,https://en.wikipedia.org/wiki/Chainsaw_Man
Spy x Family,Comedy/Action,밝고 유쾌,중간 속도,Manga,가짜 가족이 만들어가는 따뜻하고 유쾌한 첩보 일상,https://upload.wikimedia.org/wikipedia/en/0/0f/Spy_x_Family_volume_1_cover.jpg,https://en.wikipedia.org/wiki/Spy_%C3%97_Family
Vinland Saga,Historical/Action,어둡고 진지,서서히 몰입,Manga,바이킹 시대의 복수와 성장 서사,https://upload.wikimedia.org/wikipedia/en/d/db/Vinland_Saga_volume_1_cover.jpg,https://en.wikipedia.org/wiki/Vinland_Saga
Death Note,Mystery/Thriller,긴장감 넘치는,서서히 몰입,Manga,죽음의 노트를 둘러싼 두 천재의 심리전,https://upload.wikimedia.org/wikipedia/en/6/6f/Death_Note_Vol_1.jpg,https://en.wikipedia.org/wiki/Death_Note
Monster,Mystery/Thriller,어둡고 진지,긴 호흡,Manga,의사가 쫓는 연쇄살인범과 도덕의 문제,https://upload.wikimedia.org/wikipedia/en/3/3b/Monster_v01_cover.jpg,https://en.wikipedia.org/wiki/Monster_(manga)
Orange,Romance/Drama,감성적,서서히 몰입,Manga,미래의 편지를 통해 후회를 바꾸려는 청춘,https://upload.wikimedia.org/wikipedia/en/7/72/Orange_manga_volume_1.jpg,https://en.wikipedia.org/wiki/Orange_(manga)
"""

# ========== 유틸 ==========
@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(StringIO(RAW_CSV))
    # 문자열 트림
    for col in ["title","genre","mood","tempo","media","desc","image","link"]:
        df[col] = df[col].astype(str).str.strip()
    return df

def stepwise_recommend(df, answers):
    """정확 일치 → (tempo 제외) → (genre+media) → (genre) → (mood) 순으로 완화하며 추천."""
    g, m, t, md = answers["genre"], answers["mood"], answers["tempo"], answers["media"]

    # 0) 정확 일치
    q = (df["genre"] == g) & (df["mood"] == m) & (df["tempo"] == t) & (df["media"] == md)
    exact = df[q]
    if not exact.empty:
        return exact.sample(1).iloc[0], "✅ 조건 완벽 일치"

    # 1) tempo 제외
    q = (df["genre"] == g) & (df["mood"] == m) & (df["media"] == md)
    near = df[q]
    if not near.empty:
        return near.sample(1).iloc[0], "👍 tempo 제외 유사 매칭"

    # 2) genre + media
    q = (df["genre"] == g) & (df["media"] == md)
    gm = df[q]
    if not gm.empty:
        return gm.sample(1).iloc[0], "👍 장르+매체 유사 매칭"

    # 3) genre만
    gonly = df[df["genre"] == g]
    if not gonly.empty:
        return gonly.sample(1).iloc[0], "👉 장르 기반 대체 추천"

    # 4) mood만
    monly = df[df["mood"] == m]
    if not monly.empty:
        return monly.sample(1).iloc[0], "👉 분위기 기반 대체 추천"

    # 5) 최후: 랜덤
    return df.sample(1).iloc[0], "🤝 취향에 가까운 전체 랜덤"

# ========== 기본 설정 & 스타일 ==========
st.set_page_config(page_title="만화/웹툰 추천기", page_icon="📚", layout="wide")

MINIMAL_CSS = """
<style>
/* 전체 폰트 사이즈/행간 살짝 업 */
html, body, [class*="css"]  { font-size: 16px; line-height: 1.55; }

/* 타이틀 */
.main-title { text-align:center; font-weight:800; font-size:2.1rem; margin-top:0.2rem; }

/* 카드 */
.card {
  background: #ffffff;
  border: 1px solid rgba(0,0,0,0.06);
  border-radius: 16px;
  padding: 22px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.06);
}
.badge {
  display:inline-block; padding:6px 10px; border-radius:999px;
  border:1px solid rgba(0,0,0,0.08); margin-right:6px; font-size:0.85rem;
}
.cta {
  display:inline-block; padding:10px 16px; border-radius:12px; font-weight:700;
  text-decoration:none; border:1px solid rgba(0,0,0,0.1);
}
.cta:hover { background:#f6f6f9; }
.center { text-align:center; }
.dim { color:#666; }
</style>
"""
st.markdown(MINIMAL_CSS, unsafe_allow_html=True)
st.markdown("<h1 class='main-title'>📚 나만의 만화/웹툰 추천기</h1>", unsafe_allow_html=True)
st.caption("질문에 답하면 취향에 맞는 작품을 찾아드려요. (미니멀 & 세련된 UI)")

# ========== 데이터 로드 ==========
df = load_data()

# 사이드바: 필터 안내
with st.sidebar:
    st.header("ℹ️ 도움말")
    st.write("- 장르/분위기/전개/매체를 고르면 작품을 추천해요.")
    st.write("- 너무 좁은 조건이면 자동으로 비슷한 조건에서 찾아드려요.")
    st.write("- **데이터 내장형**이라 배포도 간편합니다.")

# ========== 질문 영역 ==========
st.subheader("🎛️ 취향 선택")
with st.container():
    c1, c2 = st.columns(2)
    with c1:
        genre = st.selectbox("장르", sorted(df["genre"].unique()))
        tempo = st.radio("전개 속도", sorted(df["tempo"].unique()))
    with c2:
        mood = st.selectbox("분위기", sorted(df["mood"].unique()))
        media = st.radio("매체", sorted(df["media"].unique()))

st.markdown("")
center = st.columns([1,1,1])[1]
with center:
    go = st.button("✨ 추천받기")

# ========== 추천 로직 ==========
if go:
    random.seed()  # 매번 신선하게
    answers = {"genre": genre, "mood": mood, "tempo": tempo, "media": media}
    choice, note = stepwise_recommend(df, answers)

    st.markdown("---")
    container = st.container()
    with container:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"**{note}**")
        cc1, cc2 = st.columns([1,1.4], vertical_alignment="center")
        with cc1:
            st.image(choice["image"], use_column_width=True, caption=choice["title"])
        with cc2:
            st.markdown(f"### {choice['title']}")
            st.write(choice["desc"])
            st.write(
                f"<span class='badge'>{choice['genre']}</span>"
                f"<span class='badge'>{choice['mood']}</span>"
                f"<span class='badge'>{choice['tempo']}</span>"
                f"<span class='badge'>{choice['media']}</span>",
                unsafe_allow_html=True
            )
            st.markdown(f"[👉 작품 보러가기]({choice['link']})", help="새 탭에서 열립니다.")
        st.markdown("</div>", unsafe_allow_html=True)
else:
    with st.expander("🔎 현재 데이터셋 미리보기"):
        st.dataframe(df[["title","genre","mood","tempo","media"]].sample(min(8, len(df))), use_container_width=True)

# 풋터
st.markdown("")
st.caption("© 만화/웹툰 추천기 • Streamlit")

