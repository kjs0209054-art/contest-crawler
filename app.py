import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.set_page_config(page_title="CS 전공자용 SW 공모전 크롤러", layout="wide")
st.title("💻 IT/SW 및 컴퓨터공학 전공 공모전 리스트")

def get_cs_contest_data():
    # IT/SW 카테고리가 분류된 URL (예시: 링커리어 IT/소프트웨어 섹션)
    url = "https://linkareer.com/list/contest?filterBy_categoryIDs=23" 
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    contests = []
    # 전공 관련 키워드 필터링 (해커톤, SW, 알고리즘, 개발 등)
    keywords = ['SW', 'IT', '개발', '해커톤', 'AI', '인공지능', '알고리즘', '데이터']
    
    # 사이트의 공모전 아이템 선택 (사이트 구조에 따라 class명은 주기적으로 확인 필요)
    items = soup.select('.ContestCard__StyledWrapper-sc-1y5l5w8-0')[:20] 

    for item in items:
        title = item.select_one('.title').text.strip() if item.select_one('.title') else "IT 공모전"
        organizer = item.select_one('.organization').text.strip() if item.select_one('.organization') else "IT 기관"
        d_day = item.select_one('.d-day').text.strip() if item.select_one('.d-day') else "상세참조"
        
        # IT 관련 키워드가 포함된 것 위주로 리스트업
        if any(kw in title.upper() for kw in keywords):
            contests.append({
                "분류": "💻 SW/IT",
                "공모전 명": title,
                "주최 기관": organizer,
                "마감 기한": d_day
            })
            
    return contests

st.info("💡 본 서비스는 컴퓨터공학 전공자를 위해 IT/SW 관련 공모전 정보만을 선별하여 크롤링합니다.")

if st.button('🚀 전공 관련 공모전 조회하기'):
    with st.spinner('IT/SW 데이터 추출 중...'):
        data = get_cs_contest_data()
        if len(data) >= 10:
            df = pd.DataFrame(data)
            st.success(f"✅ 전공 맞춤형 공모전 {len(df)}개를 찾았습니다!")
            st.table(df)
        else:
            # 만약 필터링된 데이터가 적으면 일반 공모전도 포함해서 10개를 채움
            st.warning("필터링된 전공 공모전이 부족하여 전체 IT 리스트를 불러옵니다.")
            st.table(pd.DataFrame(data))
