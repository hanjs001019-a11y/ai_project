# 기존 코드 (수정 전)
@st.cache_data
def load_data():
    df = pd.read_csv("seoul.csv")
    ...

# 변경할 코드 (수정 후)
@st.cache_data
def load_data():
    # encoding='cp949'를 추가하여 한국어 인코딩을 올바르게 읽어옵니다.
    df = pd.read_csv("seoul.csv", encoding='cp949')
    
    # 열 이름의 공백 제거
    df.columns = df.columns.str.strip()
    
    # 날짜 열의 '\t' 문자 제거 및 datetime 변환
    df['날짜'] = df['날짜'].astype(str).str.replace(r'\s+', '', regex=True)
    df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
    
    # 날짜 파싱 실패 데이터 및 기온 결측치 제거
    df = df.dropna(subset=['날짜', '최고기온(℃)', '최저기온(℃)'])
    
    # 분석에 필요한 연, 월, 일 컬럼 추가
    df['연도'] = df['날짜'].dt.year
    df['월'] = df['날짜'].dt.month
    df['일'] = df['날짜'].dt.day
    
    return df
