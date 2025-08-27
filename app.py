# app.py  — 그대로 복붙해서 `streamlit run app.py` 실행
import re
from io import StringIO
import pandas as pd
import streamlit as st

# 👉 여기에 네 CSV 원문을 그대로 붙여넣어도 됨 (줄바꿈 없어도, desc에 콤마 있어도 OK)
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

# --------------------------- 파서 (CSV가 망가져 있어도 전부 복구) ---------------------------

HEADER = ['title','genre','mood','tempo','media','desc','link']

def try_pandas(text: str) -> pd.DataFrame | None:
    try:
        df = pd.read_csv(StringIO(text))
        if set(HEADER).issubset(df.columns):
            return df[HEADER]
    except Exception:
        return None
    return None

def robust_parse(text: str) -> pd.DataFrame:
    s = text.strip()
    # 헤더 제거
    low = s.lower().lstrip()
    if low.startswith(','.join(HEADER)):
        s = s[s.lower().find(','.join(HEADER)) + len(','.join(HEADER)) :].strip()

    # 레코드 경계를 "URL 끝"으로 잡아 자르기
    recs = []
    prev = 0
    for m in re.finditer(r'https?://\S+', s):
        seg = s[prev:m.end()].strip().strip(',')  # 레코드 한 덩어리
        if seg:
            recs.append(seg)
        prev = m.end()
    # 혹시 마지막에 URL 없는 찌꺼기 있으면 버림

    rows = []
    for r in recs:
        # 마지막 콤마 뒤 = 링크
        last = r.rfind(',')
        if last == -1:
            continue
        link = r[last+1:].strip()
        left = r[:last]
        # 앞의 5개 콤마로 잘라서 나머지 전부를 desc로
        parts = left.split(',', 5)
        if len(parts) != 6:
            # 혹시 정상 줄바꿈 레코드였다면 안전하게 패스
            continue
        title, genre, mood, tempo, media, desc = [p.strip() for p in parts]
        rows.append([title, genre, mood, tempo, media, desc, link])

    df = pd.DataFrame(rows, columns=HEADER)
    return df

def load_df(raw: str) -> pd.DataFrame:
    # 1) 정상 CSV 시도
    df = try_pandas(raw)
    if df is None:
        # 2) 비정상 CSV 복구 파싱
        df = robust_parse(raw)
    # 정리
    for c in HEADER:
        df[c] = df[c].astype(str).str.strip()
    # 중복 제거
    df = df.drop_duplicates(subset=['title']).reset_index(drop=True)
    return df

# --------------------------- UI ---------------------------

st.set_page_config(page_title="만화·웹툰 추천기 (강제-풀옵션)", page_icon="📚", layout="wide")
st.title("📚 만화·웹툰 추천기")

df = load_df(RAW_CSV)

# 선택지: 데이터에 있는 걸 전부 수집
def unique_sorted(col):
    return sorted([x for x in df[col].dropna().astype(str).str.strip().unique() if x])

# 장르는 합성값 대응(Romance/Drama 같은 것)
def split_tokens(s):
    return [t.strip() for t in re.split(r'[/,&|]', str(s)) if t.strip()]

ALL = "— 전체 —"

# 모든 장르 토큰 펼치기
genre_tokens = sorted({tok for cell in df["genre"] for tok in split_tokens(cell)})
mood_tokens  = unique_sorted("mood")
tempo_tokens = unique_sorted("tempo")
media_tokens = unique_sorted("media")

col1, col2, col3, col4 = st.columns(4)
with col1:
    sel_genre = st.selectbox("🎭 장르", [ALL] + genre_tokens, index=0)
with col2:
    sel_mood = st.selectbox("🎨 분위기", [ALL] + mood_tokens, index=0)
with col3:
    sel_tempo = st.selectbox("⏱ 전개 속도", [ALL] + tempo_tokens, index=0)
with col4:
    sel_media = st.selectbox("📺 매체", [ALL] + media_tokens, index=0)

# 필터링
def match_genre(cell, token):
    if token == ALL:
        return True
    return token in split_tokens(cell)

def match_exact(cell, token):
    return token == ALL or str(cell).strip() == token

mask = df["genre"].apply(lambda v: match_genre(v, sel_genre)) \
       & df["mood"].apply(lambda v: match_exact(v, sel_mood)) \
       & df["tempo"].apply(lambda v: match_exact(v, sel_tempo)) \
       & df["media"].apply(lambda v: match_exact(v, sel_media))

result = df[mask].reset_index(drop=True)

st.caption(f"🔎 조건에 맞는 작품: **{len(result)}개** / 전체 {len(df)}개")

c1, c2 = st.columns([1,1])
with c1:
    if st.button("🎯 랜덤 1개 추천"):
        if len(result) == 0:
            st.error("조건에 맞는 작품이 없어요. 필터를 넓혀보세요.")
        else:
            rec = result.sample(1).iloc[0]
            st.success(f"추천: {rec['title']}")
            st.write(f"장르: {rec['genre']} | 분위기: {rec['mood']} | 전개: {rec['tempo']} | 매체: {rec['media']}")
            st.write(f"📖 {rec['desc']}")
            st.markdown(f"[🔗 보러가기]({rec['link']})")
with c2:
    if st.button("📜 전체 보기"):
        if len(result) == 0:
            st.error("조건에 맞는 작품이 없어요. 필터를 넓혀보세요.")
        else:
            for i, rec in result.iterrows():
                st.markdown(f"### {i+1}. {rec['title']}")
                st.write(f"장르: {rec['genre']} | 분위기: {rec['mood']} | 전개: {rec['tempo']} | 매체: {rec['media']}")
                st.write(f"📖 {rec['desc']}")
                st.markdown(f"[🔗 보러가기]({rec['link']})")
                st.divider()
