import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# 한글 폰트 설정 및 마이너스 기호 깨짐 방지 (스트림릿 클라우드 대응)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

st.title("☀️ 서울 연도별 특정 날짜 기온 분석")
st.markdown("1907년부터 2018년까지의 서울 기온 데이터를 분석합니다.")

# 1. 데이터 불러오기 및 정제
@st.cache_data
def load_data():
    # 한국 공공기관 CSV 인코딩 방식인 'cp949' 적용
    df = pd.read_csv("seoul.csv", encoding='cp949')
    
    # 열 이름의 앞뒤 공백 제거
    df.columns = df.columns.str.strip()
    
    # 날짜 열의 '\t' 문자 등 모든 공백 제거 후 datetime 변환
    df['날짜'] = df['날짜'].astype(str).str.replace(r'\s+', '', regex=True)
    df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
    
    # 날짜 파싱 실패 데이터 및 기온 결측치 제거
    df = df.dropna(subset=['날짜', '최고기온(℃)', '최저기온(℃)'])
    
    # 분석에 필요한 연, 월, 일 컬럼 추가
    df['연도'] = df['날짜'].dt.year
    df['월'] = df['날짜'].dt.month
    df['일'] = df['날짜'].dt.day
    
    return df

try:
    df = load_data()

    # 2. 사용자 입력 인터페이스 (사이드바)
    st.sidebar.header("📅 날짜 선택")
    selected_month = st.sidebar.selectbox("월을 선택하세요", sorted(df['월'].unique()), index=7) # 기본값 8월
    
    # 선택한 월에 존재하는 일만 선택 가능하도록 제한
    available_days = sorted(df[df['월'] == selected_month]['일'].unique())
    selected_day = st.sidebar.selectbox("일을 선택하세요", available_days, index=0) # 기본값 1일

    # 3. 데이터 필터링
    filtered_df = df[(df['월'] == selected_month) & (df['일'] == selected_day)].sort_values('연도')

    if filtered_df.empty:
        st.warning("선택한 날짜에 해당하는 데이터가 없습니다.")
    else:
        st.subheader(f"📊 {selected_month}월 {selected_day}일의 연도별 기온 변화")
        
        # 4. 그래프 그리기
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # 데이터 개수(연도 수) 파악
        num_years = len(filtered_df)
        
        # 최고기온: 무지개색 (Jet 컬러맵 정방향)
        high_colors = cm.jet(range(num_years))
        
        # 최저기온: 무지개 반전색 (Jet 컬러맵 역방향)
        low_colors = cm.jet(range(num_years))[::-1]
        
        # 꺾은선 그래프 플롯 (전체 추세를 은은하게 보여주기 위한 기본 선 선언)
        ax.plot(filtered_df['연도'], filtered_df['최고기온(℃)'], color='#ff9999', alpha=0.4, label='최고기온 추세')
        ax.plot(filtered_df['연도'], filtered_df['최저기온(℃)'], color='#9999ff', alpha=0.4, label='최저기온 추세')
        
        # 각 연도별 점(Scatter)에 무지개색 및 반전색을 각각 적용 (zorder로 선 위로 배치)
        ax.scatter(filtered_df['연도'], filtered_df['최고기온(℃)'], c=high_colors, edgecolor='none', s=45, zorder=3)
        ax.scatter(filtered_df['연도'], filtered_df['최저기온(℃)'], c=low_colors, edgecolor='none', s=45, zorder=3)
        
        # 축 및 레이블 설정
        ax.set_xlabel("Year (연도)", fontsize=12)
        ax.set_ylabel("Temperature (기온 ℃)", fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.5)
        
        # 범례 표시 (상단 좌측)
        ax.legend(loc='upper left')
        
        # 스트림릿 웹페이지에 그래프 출력
        st.pyplot(fig)
        
        # 5. 상세 데이터 테이블 
        with st.expander("🔍 선택한 날짜의 전체 데이터 목록 보기"):
            st.dataframe(filtered_df[['연도', '평균기온(℃)', '최저기온(℃)', '최고기온(℃)']].reset_index(drop=True))

except FileNotFoundError:
    st.error("📂 `seoul.csv` 파일을 찾을 수 없습니다. 이 스크립트 파일과 같은 폴더(혹은 루트 폴더)에 업로드되어 있는지 확인해 주세요.")
except Exception as e:
    st.error(f"알 수 없는 오류가 발생했습니다: {e}")
