# app.py
import re
from io import StringIO
import pandas as pd
import streamlit as st

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
나빌레라,Drama,따뜻한,느긋한 전개,Webtoon,노년과 청년의 발레 도전기,https://comic.naver.com
D.P.,Drama,현실적,중간 속도,Webtoon,군대 탈영병을 쫓는 병사의 이야기,https://comic.naver.com
신도림,Sci-Fi,긴장감 넘치는,빠른 전개,Webtoon,가상현실과 현실을 넘나드는 전투,https://comic.naver.com
덴마,Sci-Fi,신비로운,느긋한 전개,Webtoon,우주를 배경으로 한 서사시,https://comic.naver.com
미생,Drama,현실적,중간 속도,Webtoon,직장인들의 애환과 성장,https://comic.naver.com
킬링 스토킹,Horror,충격적,느린 전개,Webtoon,집착과 광기의 심리 스릴러,https://comic.naver.com
호랑이형님,Fantasy,코믹,빠른 전개,Webtoon,호랑이와 인간들의 판타지 모험,https://comic.naver.com
무빙,Superhero,감동적,중간 속도,Webtoon,초능력을 가진 가족들의 이야기,https://comic.naver.com
싸움독학,Action,열혈,빠른 전개,Webtoon,평범한 소년의 싸움 성장기,https://comic.naver.com
테러맨,Thriller,불안한,빠른 전개,Webtoon,불운한 소년이 테러와 맞서는 이야기,https://comic.naver.com
연의 편지,Romance,감동적,느긋한 전개,Webtoon,편지를 통해 이어지는 청춘의 사랑,https://comic.naver.com
나이트런,Sci-Fi,장대한,빠른 전개,Webtoon,우주 전쟁을 그린 장편 서사,https://comic.naver.com
패션왕,Comedy,병맛,빠른 전개,Webtoon,평범한 소년의 패션 도전기,https://comic.naver.com
외모지상주의,Drama,청춘,빠른 전개,Webtoon,외모가 바뀐 소년의 학교 생활,https://comic.naver.com
갓 오브 하이스쿨,Action,격투,빠른 전개,Webtoon,전국 고등학생들의 무투대회,https://comic.naver.com
신과 함께,Fantasy,감동적,중간 속도,Webtoon,사후 세계를 그린 대서사시,https://comic.naver.com
블랙클로버,Fantasy,열정적,빠른 전개,Manga,마법 없는 소년의 마법제 도전,https://www.shonenjump.com
약속의 네버랜드,Thriller,불안한,빠른 전개,Manga,고아원의 비밀을 파헤치는 아이들,https://www.shonenjump.com
은혼,Comedy,패러디,중간 속도,Manga,사무라이와 외계인이 공존하는 시대극,https://www.shonenjump.com
죠죠의 기묘한 모험,Adventure,독특한,빠른 전개,Manga,세대를 거듭하는 기묘한 전투,https://www.shonenjump.com
도쿄구울,Horror,어두운,중간 속도,Manga,반인간·반구울 소년의 고뇌,https://www.shonenjump.com
강철의 연금술사,Fantasy,철학적,빠른 전개,Manga,연금술사 형제의 여정,https://www.shonenjump.com
"""

# === (아래 robust_parse, load_df, UI 코드는 아까 준 거랑 동일) ===
# ... (생략, 이전 코드 그대로 사용) ...
