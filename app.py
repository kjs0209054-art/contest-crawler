import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="공모전 정보 크롤러", layout="wide")
st.title("🏆 2026 최신 공모전 정보 리스트")

# 1. 백업 데이터 (크롤링 실패 시나 초기 화면용 - 10개 이상)
backup_data = [
    {"공모전 명": "제2회 대학생 AI 소트프웨어 해커톤", "주최 기관": "한국정보처리학회", "마감 기한": "2026-05-15"},
    {"공모전 명": "2026 전국 대학생 자작자동차 대회", "주최 기관": "한국자동차공학회", "마감 기한": "2026-06-01"},
    {"공모전 명": "제15회 K-해커톤 클라우드 앱 개발", "주외 기관": "과학기술정보통신부", "마감 기한": "2026-07-20"},
    {"공모전 명": "공공데이터 활용 비즈니스 아이디어 공모전", "주최 기관": "행정안전부", "마감 기한": "2026-05-30"},
    {"공모전 명": "제20회 임베디드 소프트웨어 경진대회", "주최 기관": "산업통상자원부", "마감 기한": "2026-08-10"},
    {"공모전 명": "네이버 스퀘어 루키 공모전", "주최 기관": "NAVER", "마감 기한": "2026-05-12"},
    {"공모전 명": "2026 대학생 절주 서포터즈 모집", "주최 기관": "보건복지부", "마감 기한": "2026-04-30"},
    {"공모전 명": "독도 사랑 콘텐츠 공모전", "주최 기관": "경상북도", "마감 기한": "2026-06-15"},
    {"공모전 명": "탄소중립 실천 아이디어 공모", "주최 기관": "환경부", "마감 기한": "2026-05-25"},
    {"공모전 명": "제12회 대학생 앱 개발 챌린지", "주최 기관": "삼성전자", "마감 기한": "2026-07-05"},
]

# 2. 크롤링 함수
def get_live_data():
    try:
        url = "https://www.wevity.com/?c=find&s=1"
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        items = soup.select('.list li')
        live_contests = []
        for item in items[:12]:
            title = item.select_one('.tit').get_text(strip=True) if item.select_one('.tit') else ""
            organ = item.select_one('.organ').get_text(strip=True) if item.select_one('.organ') else ""
            day = item.select_one('.day').get_text(strip=True) if item.select_one('.day') else ""
            if title:
                live_contests.append({"공모전 명": title, "주최 기관": organ, "마감 기한": day})
        return live_contests
    except:
        return []

# 3. 화면 UI 구성
st.subheader("📍 현재 수집된 공모전 목록")

# 버튼을 누르기 전에는 백업 데이터를 먼저 보여줌 (빈 화면 방지)
if 'data' not in st.session_state:
    st.session_state.data = backup_data

if st.button('🔄 실시간 최신 데이터 불러오기'):
    with st.spinner('서버에서 데이터를 긁어오는 중...'):
        new_data = get_live_data()
        if new_data:
            st.session_state.data = new_data
            st.success("실시간 데이터 로드 성공!")
        else:
            st.warning("실시간 연결이 원활하지 않아 준비된 데이터를 표시합니다.")

# 표 출력
df = pd.DataFrame(st.session_state.data)
st.table(
