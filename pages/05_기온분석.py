# 💡 반드시 파일의 "가장 첫 줄"에 이 임포트문들이 있어야 합니다!
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# 데이터 불러오기 및 정제 (2번째 줄부터 시작)
@st.cache_data
def load_data():
    # 이전 단계에서 수정했던 encoding='cp949'도 같이 확인해 주세요.
    df = pd.read_csv("seoul.csv", encoding='cp949') 
    
    # 열 이름의 공백 제거
    df.columns = df.columns.str.strip()
    
    # 날짜 열의 '\t' 문자 제거 및 datetime 변환
    df['날짜'] = df['날짜'].astype(str).str.replace(r'\s+', '', regex=True)
    df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
    
    # 결측치 제거 및 연/월/일 컬럼 추가
    df = df.dropna(subset=['날짜', '최고기온(℃)', '최저기온(℃)'])
    df['연도'] = df['날짜'].dt.year
    df['월'] = df['날짜'].dt.month
    df['일'] = df['날짜'].dt.day
    
    return df

# ... 이후 하단 코드 생략 ...
