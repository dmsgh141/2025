# filename: test.py
import streamlit as st
import pandas as pd
from io import StringIO
import random

# ------------------------------------------------------------
# 내장 데이터셋 (100+ 작품)
# ------------------------------------------------------------
RAW_CSV = """title,genre,mood,tempo,media,desc,link 나 혼자만 레벨업,Action,긴장감 넘치는,빠른 전개,Webtoon,헌터 세계에서 각성한 주인공의 성장기,https://comic.naver.com 신의 탑,Fantasy,미스터리,중간 속도,Webtoon,탑을 오르며 펼쳐지는 모험과 갈등,https://comic.naver.com 유미의 세포들,Romance,밝고 유쾌,중간 속도,Webtoon,세포 시점으로 보는 사랑과 일상,https://comic.naver.com 스위트홈,Horror,어두운,빠른 전개,Webtoon,괴물로 변한 세상에서의 아파트 생존기,https://comic.naver.com 테러맨,Thriller,드라마틱,빠른 전개,Webtoon,불운한 소년의 의도치 않은 영웅담,https://comic.naver.com 약한영웅,Action,긴장감 넘치는,빠른 전개,Webtoon,두뇌로 싸우는 리얼 학교 액션,https://comic.naver.com 외모지상주의,Drama,현실적,중간 속도,Webtoon,외모와 사회를 다루는 청춘 서사,https://comic.naver.com 참교육,Action,사회적,빠른 전개,Webtoon,악질 교사와 학폭을 응징하는 이야기,https://comic.naver.com 비질란테,Thriller,어두운,빠른 전개,Webtoon,법이 놓친 범죄자를 응징하는 자경단,https://comic.naver.com 독립일기,Slice of Life,힐링,중간 속도,Webtoon,자취 일상을 담은 공감 에세이,https://comic.naver.com 마음의 소리,Comedy,밝고 유쾌,빠른 전개,Webtoon,일상 개그의 정수,https://comic.naver.com 소녀의 세계,Romance/Drama,감성적,중간 속도,Webtoon,여고생 우정과 사랑의 성장기,https://comic.naver.com 연의 편지,Romance,잔잔한,서서히 몰입,Webtoon,편지로 이어지는 청춘의 기록,https://comic.naver.com 윈드브레이커,Sports/Drama,청춘감성,빠른 전개,Webtoon,자전거 크루들의 우정과 레이스,https://comic.naver.com 노블레스,Fantasy/Action,드라마틱,중간 속도,Webtoon,깨어난 귀족과 동료들의 현대 판타지,https://comic.naver.com 쿠베라,Fantasy,미스터리,서서히 몰입,Webtoon,신과 인간의 거대한 서사,https://comic.naver.com 덴마,SF,미스터리,중간 속도,Webtoon,우주를 무대로 한 장편 드라마,https://comic.naver.com 가담항설,Historical/Drama,감성적,서서히 몰입,Webtoon,조선 시대 이야기를 해학적으로 풀어냄,https://comic.naver.com 나이트런,SF/Action,긴장감 넘치는,빠른 전개,Webtoon,우주괴와 싸우는 인간들의 기록,https://comic.naver.com 신도림,Action/Fantasy,어두운,빠른 전개,Webtoon,멸망 이후 세계의 생존과 권력,https://comic.naver.com 테니스의 왕자,Sports,밝고 유쾌,빠른 전개,Manga,중학생 테니스 천재들의 대결,https://example.com 하이큐,Sports,감성적,빠른 전개,Manga,배구 소년단의 성장과 도전,https://haikyu.jp 슬램덩크,Sports,감성적,중간 속도,Manga,농구를 통해 변해가는 청춘,https://slam-dunk.jp 블루록,Sports/Drama,긴장감 넘치는,빠른 전개,Manga,최강 스트라이커 육성 프로젝트,https://example.com 원피스,Adventure,밝고 유쾌,서서히 몰입,Manga,해적단의 모험과 우정,https://one-piece.com 나루토,Action/Fantasy,드라마틱,중간 속도,Manga,인정을 꿈꾸는 닌자의 성장,https://naruto-official.com 블리치,Action/Fantasy,드라마틱,빠른 전개,Manga,사신과 호로의 전투,https://example.com 진격의 거인,Action/Drama,어두운,빠른 전개,Manga,거인과 인류의 생존 전쟁,https://attackontitan.com 귀멸의 칼날,Action,감성적,빠른 전개,Manga,가족을 구하기 위한 소년 검사,https://kimetsu.com 체인소맨,Horror,어두운,빠른 전개,Manga,악마와 계약한 청년의 생존기,https://chainsawman.dog 헌터헌터,Adventure/Action,미스터리,중간 속도,Manga,헌터가 되기 위한 시험과 모험,https://example.com 드래곤볼,Action/Adventure,밝고 유쾌,빠른 전개,Manga,손오공과 동료들의 대서사,https://dragon-ball-official.com 블랙클로버,Fantasy/Action,밝고 유쾌,빠른 전개,Manga,마력 없는 소년의 마법황 도전,https://example.com 원펀맨,Action/Comedy,밝고 유쾌,빠른 전개,Manga,한 방으로 끝내는 히어로의 일상,https://onepunchman.org 모브사이코100,Fantasy/Comedy,감성적,중간 속도,Manga,초능력 소년의 성장과 고민,https://example.com 데스노트,Thriller,스릴러틱,중간 속도,Manga,죽음의 노트로 벌이는 두뇌전,https://example.com 강철의 연금술사,Fantasy/Drama,드라마틱,중간 속도,Manga,형제를 되찾기 위한 연금술 여정,https://example.com 플루토,SF/Thriller,미스터리,중간 속도,Manga,아톰 세계관의 서늘한 추리극,https://example.com 원아웃,Thriller/Sports,긴장감 넘치는,빠른 전개,Manga,두뇌 승부가 핵심인 야구 심리전,https://example.com 베르세르크,Dark Fantasy,어두운,서서히 몰입,Manga,복수와 광기의 기사 이야기,https://example.com 바가본드,Historical/Drama,드라마틱,중간 속도,Manga,무사 미야모토 무사시의 일대기,https://example.com 20세기 소년,Thriller/Drama,미스터리,서서히 몰입,Manga,어릴 적 놀이가 현실이 된 음모극,https://example.com 몬스터,Thriller,어두운,서서히 몰입,Manga,살인마를 쫓는 의사의 추격,https://example.com 핑퐁,Sports/Drama,감성적,중간 속도,Manga,탁구를 통해 그리는 청춘의 결,https://example.com 츠루네,Sports,잔잔한,서서히 몰입,Manga,궁도부 소년들의 성장,https://example.com 체육교사 도지마,Comedy,밝고 유쾌,빠른 전개,Manga,체육교사의 기상천외한 일상,https://example.com 카이지,Thriller,긴장감 넘치는,빠른 전개,Manga,목숨 건 도박 심리전,https://example.com 블루자이언트,Music/Drama,감성적,서서히 몰입,Manga,색소폰 소년의 재즈 성장기,https://example.com 유루캠△,Slice of Life,힐링,서서히 몰입,Manga,캠핑으로 채우는 소소한 행복,https://example.com 카구야님은 고백받고 싶어,Romantic Comedy,밝고 유쾌,중간 속도,Manga,두 천재의 사랑 두뇌 싸움,https://example.com 월요일의 친구,Slice of Life,잔잔한,서서히 몰입,Manga,주말을 기다리는 마음을 그린 단정한 이야기,https://example.com 골든 카무이,Adventure/Drama,긴장감 넘치는,중간 속도,Manga,황금과 생존 기술의 북방 모험,https://example.com 킹덤,Historical/Action,드라마틱,빠른 전개,Manga,춘추전국을 무대로 한 대서사,https://example.com 불멸의 그대에게,Fantasy/Drama,감성적,서서히 몰입,Manga,형태를 바꾸는 존재의 긴 여정,https://example.com 스파이 패밀리,Comedy/Spy,밝고 유쾌,중간 속도,Manga,가짜 가족의 진짜 정이 피어나는 이야기,https://example.com 마시마로 탐정단,Kids/Comedy,밝고 유쾌,빠른 전개,Comic,아이들과 함께 보는 추리 코미디,https://example.com 배트맨,Superhero,어두운,중간 속도,Comic,고담을 지키는 어둠의 기사,https://example.com 스파이더맨,Superhero,밝고 유쾌,빠른 전개,Comic,평범한 소년의 거미 능력 히어로물,https://example.com 아이언맨,Superhero,드라마틱,빠른 전개,Comic,천재 억만장자 히어로의 선택,https://example.com 닥터 스트레인지,Superhero/Fantasy,미스터리,중간 속도,Comic,마법과 다차원의 수호자,https://example.com 샌드맨,Dark Fantasy,어두운,서서히 몰입,Comic,꿈의 군주가 그리는 신화적 서사,https://example.com 사가,Sci-Fi/Fantasy,드라마틱,중간 속도,Comic,전쟁 속 가족의 우주 활극,https://example.com 워킹데드,Horror/Drama,어두운,중간 속도,Comic,좀비 아포칼립스 생존기,https://example.com 위치스,Supernatural,스릴러틱,중간 속도,Comic,숲과 마녀 전설을 뒤틀어낸 공포,https://example.com 페이퍼 걸스,Sci-Fi,미스터리,중간 속도,Comic,신문 배달 소녀들의 시간 여행,https://example.com 질리언 플린 더 컬렉션,Thriller,스릴러틱,중간 속도,Comic,어두운 심리의 단편 모음,https://example.com 연애혁명,Romance/Comedy,밝고 유쾌,중간 속도,Webtoon,엉뚱한 커플의 스쿨 로맨스,https://comic.naver.com 여신강림,Romance/Comedy,밝고 유쾌,중간 속도,Webtoon,메이크업으로 바뀌는 자존감 이야기,https://comic.naver.com 뽀짜툰,Slice of Life,힐링,서서히 몰입,Webtoon,반려묘와 일상의 소소한 행복,https://comic.naver.com 오늘도 사랑스럽개,Romantic Comedy,밝고 유쾌,중간 속도,Webtoon,저주로 개가 되는 그녀의 로맨스,https://comic.naver.com 놓지마 정신줄,Comedy,밝고 유쾌,빠른 전개,Webtoon,폭발적 텐션의 일상 개그,https://comic.naver.com SWEET HOME,Thriller/Horror,어두운,빠른 전개,Webtoon,아파트에서 벌어지는 괴물 생존기,https://comic.naver.com 호랑이형님,Fantasy/Action,드라마틱,중간 속도,Webtoon,호랑이와 인간이 뒤섞인 세계의 모험,https://comic.naver.com 갓 오브 하이스쿨,Action/Sports,에너제틱,빠른 전개,Webtoon,무술 대회를 둘러싼 초격투,https://comic.naver.com 신과 함께,Fantasy/Drama,감성적,중간 속도,Webtoon,사후 세계 재판과 인간의 삶,https://comic.naver.com 어게인 마이 라이프,Thriller/Action,긴장감 넘치는,빠른 전개,Webtoon,회귀로 정의를 완성하는 검사,https://comic.naver.com 내일,Fantasy/Drama,감성적,중간 속도,Webtoon,저승사자들의 자살방지팀 이야기,https://comic.naver.com 취사병 전설이 되다,Military/Comedy,밝고 유쾌,중간 속도,Webtoon,군대 급식의 전설이 되는 요리 액션,https://comic.naver.com 무장학원,Action,드라마틱,빠른 전개,Webtoon,학원 배경의 장르 혼합 액션,https://example.com 로렐라이의 소녀,Romance/Fantasy,감성적,서서히 몰입,Webtoon,전설과 사랑이 교차하는 청춘,https://example.com 미생,Drama,현실적,서서히 몰입,Webtoon,회사원의 현실 밀착 드라마,https://comic.naver.com 나빌레라,Drama,감성적,서서히 몰입,Webtoon,은퇴 후 발레를 향한 도전,https://comic.naver.com DICE,Fantasy,미스터리,빠른 전개,Webtoon,주사위로 능력을 얻는 청소년들,https://comic.naver.com 에레이나의 여행기,Fantasy/Adventure,잔잔한,중간 속도,Manga,마녀의 여행에서 만나는 인연,https://example.com 라노벨 덕후의 이세계,Fantasy/Comedy,밝고 유쾌,중간 속도,Manga,이세계에서 펼치는 오타쿠 활극,https://example.com 골프왕Z,Sports/Comedy,밝고 유쾌,중간 속도,Webtoon,상상초월 골프 예능감,https://example.com 삼국지 리로디드,Historical/Action,드라마틱,중간 속도,Webtoon,삼국지를 재해석한 전략 활극,https://example.com 치즈인더트랩,Romance/Drama,감성적,서서히 몰입,Webtoon,대학 로맨스의 섬세한 심리,https://comic.naver.com 유일무이 로맨스,Romance,밝고 유쾌,중간 속도,Webtoon,연예계 배경의 가짜 연애 리얼 로맨스,https://example.com 바른연애 길잡이,Romance/Comedy,밝고 유쾌,중간 속도,Webtoon,연애 초보들의 성장기,https://example.com 오렌지 마말레이드,Romance/Fantasy,감성적,중간 속도,Webtoon,뱀파이어와 인간의 청춘 로맨스,https://comic.naver.com 바벨,Thriller,스릴러틱,빠른 전개,Webtoon,검은 비밀을 쫓는 기자의 추격,https://example.com 블라인드,Thriller/Drama,어두운,서서히 몰입,Webtoon,사라진 진실을 향한 심리 미스터리,https://example.com 소년심판,Drama,사회적,중간 속도,Webtoon,소년범죄와 사법의 딜레마,https://example.com 경이로운 소문,Supernatural/Action,긴장감 넘치는,빠른 전개,Webtoon,지상의 악귀 사냥꾼들,https://comic.naver.com 어나더 레벨,Action/Fantasy,에너제틱,빠른 전개,Webtoon,이세계식 성장 치트물,https://example.com 전지적 독자 시점,Fantasy/Action,긴장감 넘치는,빠른 전개,Webtoon,읽던 소설이 현실이 된 생존기,https://comic.naver.com 윈터우즈,Fantasy/Romance,잔잔한,서서히 몰입,Webtoon,고전적 분위기의 따뜻한 로맨스,https://example.com 그림자 미녀,Thriller/Drama,미스터리,중간 속도,Webtoon,겉과 속이 다른 청춘의 초상,https://example.com ELECEED,Fantasy/Action,밝고 유쾌,빠른 전개,Webtoon,고양이 사부와 번개 능력 소년,https://comic.naver.com 더 박서,Drama/Sports,강렬한,빠른 전개,Webtoon,재능의 무게를 견디는 복서 이야기,https://example.com 사이렌,Thriller,스릴러틱,중간 속도,Webtoon,도시의 연쇄 사건을 파고드는 형사,https://example.com 복학왕,Comedy,밝고 유쾌,빠른 전개,Webtoon,세대를 아우르는 캠퍼스 개그,https://comic.naver.com 개를 낳았다,Slice of Life,힐링,서서히 몰입,Webtoon,연애와 반려의 성장담,https://comic.naver.com 지금 우리 학교는,Horror,어두운,빠른 전개,Webtoon,좀비 발생 고등학교의 생존,https://comic.naver.com 오딩가드,Fantasy/Adventure,드라마틱,중간 속도,Webtoon,북구 신화를 차용한 모험,https://example.com 어느날 공주가 되어버렸다,Romantasy,감성적,중간 속도,Webtoon,빌런 공주의 생존 로맨스,https://example.com 그 오빠들을 조심해,Romantasy,감성적,중간 속도,Webtoon,예언과 운명의 궁정 로맨스,https://example.com 재혼 황후,Romantasy,감성적,서서히 몰입,Webtoon,새로운 선택으로 펼쳐지는 궁정 서사,https://example.com 유어 스로운,Fantasy/Drama,음모적,중간 속도,Webtoon,권력과 복수의 심리전,https://example.com 퍼플 하이신스,Romance/Thriller,스릴러틱,중간 속도,Webtoon,암살단과 수사관의 위험한 공조,https://example.com 렘마리드 엠프레스,Romantasy,감성적,서서히 몰입,Webtoon,궁정 정치와 사랑의 선택,https://example.com 미드나잇 파피 랜드,Romantic Thriller,스릴러틱,서서히 몰입,Webtoon,어두운 세계에 빠져드는 로맨스,https://example.com 언오디너리,Action,긴장감 넘치는,빠른 전개,Webtoon,능력이 일상이 된 학교의 권력 싸움,https://example.com 위크 히어로,Action/Drama,어두운,빠른 전개,Webtoon,약자의 복수와 연대,https://example.com 정글 주스,Action/Fantasy,이색적,빠른 전개,Webtoon,곤충 변이 청춘들의 생존기,https://example.com 겟 스쿨드,Action/Drama,사회적,빠른 전개,Webtoon,학폭 응징 전문가의 통쾌한 해결,https://example.com 바운드리스,Fantasy/Comedy,밝고 유쾌,중간 속도,Webtoon,차원 여행 속 소소한 해프닝,https://example.com 금요일의 서스펜스,Thriller,스릴러틱,중간 속도,Webtoon,일상에 숨어든 의심과 반전,https://example.com 서브제로,Fantasy/Romance,드라마틱,서서히 몰입,Webtoon,왕국의 운명을 건 얼음 로맨스,https://example.com 아이 러브 유,Romantic Comedy,감성적,중간 속도,Webtoon,유쾌한 삼각 구도의 성장 로코,https://example.com 씨 유 인 마이 19th 라이프,Romantic Fantasy,애틋한,서서히 몰입,Webtoon,환생을 거듭한 사랑의 재회,https://example.com 오라시언트 리더,Fantasy/Action,몰입감 있는,빠른 전개,Webtoon,독자만 아는 플래그로 살아남기,https://example.com 타워 오브 갓,Fantasy/Adventure,스펙터클,서서히 몰입,Webtoon,탑의 규칙과 시험을 뛰어넘는 모험,https://example.com 갓 오브 하이스쿨,Action/Sports,에너제틱,빠른 전개,Webtoon,초격투와 우정의 폭발,https://example.com 솔로 레벨링,Fantasy/Action,긴박한,빠른 전개,Webtoon,약자에서 최강자로 성장하는 판타지,https://example.com 나이트메어 파크,Horror,어두운,중간 속도,Webtoon,폐쇄 놀이공원의 괴이담,https://example.com 트레이스,Supernatural,어두운,빠른 전개,Webtoon,초능력자와 괴수의 공존 세계,https://example.com D.P.,Military/Drama,현실적,중간 속도,Webtoon,군무이탈 체포조의 기록,https://example.com 로그 호라이즌,Fantasy,잔잔한,서서히 몰입,Manga,게임 세계에 갇힌 유저들의 사회,https://example.com 소드 아트 온라인,Fantasy/Action,드라마틱,빠른 전개,Manga,가상 세계 데스게임에서의 생존,https://example.com Re:제로,Fantasy/Drama,미스터리,서서히 몰입,Manga,죽음 회귀로 운명을 바꾸는 소년,https://example.com 원더우먼,Superhero,드라마틱,중간 속도,Comic,진실의 올가미를 든 여전사,https://example.com 데어데블,Superhero,어두운,중간 속도,Comic,시각을 잃은 변호사의 야간 경계,https://example.com 헬보이,Dark Fantasy,어두운,중간 속도,Comic,악마 혈통 탐정의 초자연 수사,https://example.com 헬싱,Horror/Action,어두운,빠른 전개,Manga,흡혈귀와 종교 조직의 전투,https://example.com 나나,Romance/Drama,감성적,서서히 몰입,Manga,두 나나의 우정과 사랑,https://example.com 시그널100,Horror/Thriller,긴장감 넘치는,빠른 전개,Manga,최면 명령이 걸린 데스게임,https://example.com 진격의 거인 외전,Action/Drama,어두운,중간 속도,Manga,벽 밖으로 확장되는 세계관,https://example.com 스캇 필그림,Romantic Comedy,밝고 유쾌,빠른 전개,Comic,게임 같은 현실의 러브 배틀,https://example.com 왓치맨,Superhero/Thriller,미스터리,서서히 몰입,Comic,히어로와 권력의 윤리,https://example.com 코난,Detective,미스터리,중간 속도,Manga,사건을 해결하는 명탐정 소년,https://example.com 금색의 갓슈,Fantasy/Comedy,밝고 유쾌,중간 속도,Manga,마물과 파트너의 성장 대결,https://example.com 토가시 단편선,Anthology,다양함,중간 속도,Manga,개성 강한 실험적 이야기 모음,https://example.com """

# ------------------------------------------------------------
# 데이터 로드
# ------------------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv(StringIO(RAW_CSV))

st.set_page_config(page_title="만화 · 웹툰 추천기", page_icon="📚", layout="wide")
df = load_data()

# 값 정리
for col in ["genre", "mood", "tempo", "media"]:
    df[col] = df[col].astype(str).str.strip()

# ------------------------------------------------------------
# 페이지 꾸미기
# ------------------------------------------------------------
st.markdown(
    """
    <style>
    /* 전체 배경 */
    .stApp {
        background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
    }

    /* 버튼 꾸미기 */
    .stButton>button {
        border-radius: 12px;
        padding: 0.6em 1.2em;
        font-weight: bold;
        font-size: 1em;
        background: linear-gradient(90deg, #ff758c, #ff7eb3);
        color: white;
        border: none;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #6a11cb, #2575fc);
        color: white;
    }

    /* 추천 결과 카드 */
    .result-card {
        padding: 1.2em;
        border-radius: 15px;
        background: white;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
        margin-top: 1em;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------------
# 헤더
# ------------------------------------------------------------
st.title("📚 나에게 딱 맞는 만화 · 웹툰 추천기")
st.caption("질문 몇 개만 고르면 바로 추천! 데이터 내장 · CSV 파일 불필요")

# ------------------------------------------------------------
# 선택 영역
# ------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)
with col1:
    sel_genre = st.selectbox("장르", sorted(df["genre"].unique()))
with col2:
    sel_mood = st.selectbox("분위기", sorted(df["mood"].unique()))
with col3:
    sel_tempo = st.selectbox("전개 속도", sorted(df["tempo"].unique()))
with col4:
    sel_media = st.selectbox("매체", sorted(df["media"].unique()))

left, right = st.columns([1,1])
with left:
    go = st.button("🎯 추천 받기")
with right:
    random_go = st.button("🎲 아무거나 추천")

# ------------------------------------------------------------
# 추천 로직
# ------------------------------------------------------------
def pick_one(frame: pd.DataFrame):
    if frame.empty:
        return None
    return frame.sample(1).iloc[0]

def recommend(genre, mood, tempo, media):
    # 1) 완전 일치
    f1 = df[(df["genre"]==genre) & (df["mood"]==mood) & (df["tempo"]==tempo) & (df["media"]==media)]
    r = pick_one(f1)
    if r is not None: return r

    # 2) 장르 + 분위기 + 전개
    f2 = df[(df["genre"]==genre) & (df["mood"]==mood) & (df["tempo"]==tempo)]
    r = pick_one(f2)
    if r is not None: return r

    # 3) 장르 + 분위기
    f3 = df[(df["genre"]==genre) & (df["mood"]==mood)]
    r = pick_one(f3)
    if r is not None: return r

    # 4) 장르만
    f4 = df[df["genre"]==genre]
    r = pick_one(f4)
    if r is not None: return r

    # 5) 아무거나
    return pick_one(df)

# ------------------------------------------------------------
# 결과 영역
# ------------------------------------------------------------
if go:
    rec = recommend(sel_genre, sel_mood, sel_tempo, sel_media)
    if rec is not None:
        st.markdown(
            f"""
            <div class="result-card">
            <h3>🎬 {rec['title']}</h3>
            <p><b>장르</b>: {rec['genre']} | <b>분위기</b>: {rec['mood']} | <b>전개</b>: {rec['tempo']} | <b>매체</b>: {rec['media']}</p>
            <p>📖 {rec['desc']}</p>
            <a href="{rec['link']}" target="_blank">🔗 보러 가기</a>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.error("추천 데이터를 찾지 못했어요. 선택값을 바꿔보세요.")

if random_go:
    rec = df.sample(1).iloc[0]
    st.markdown(
        f"""
        <div class="result-card">
        <h3>🎬 {rec['title']}</h3>
        <p><b>장르</b>: {rec['genre']} | <b>분위기</b>: {rec['mood']} | <b>전개</b>: {rec['tempo']} | <b>매체</b>: {rec['media']}</p>
        <p>📖 {rec['desc']}</p>
        <a href="{rec['link']}" target="_blank">🔗 보러 가기</a>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")
with st.expander("📖 전체 목록 보기"):
    st.dataframe(df, use_container_width=True)
