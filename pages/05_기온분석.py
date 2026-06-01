import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# 한글 폰트 설정 (스트림릿 클라우드 리눅스 환경 대응)
# 나눔고딕 등 폰트가 없을 때를 대비해 기본 맑은고딕 및 시스템 폰트 설정
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

st.title("☀️ 서울 연도별 특정 날짜 기온 분석")
st.markdown("1907년부터 2018년까지의 서울 기온 데이터를 분석합니다.")

# 1. 데이터 불러오기 및 정제
@st.cache_data
def load_data():
    # CSV 파일을 읽어옵니다.
    df = pd.read_csv("seoul.csv")
    
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
        
        # 데이터 개수에 맞춰 무지개색(Jet colormap) 색상 추출
        num_years = len(filtered_df)
        
        # 최고기온: 무지개색 (보라 -> 청 -> 녹 -> 황 -> 적)
        high_colors = cm.jet(range(num_years))
        
        # 최저기온: 무지개 반전색 (적 -> 황 -> 녹 -> 청 -> 보라)
        low_colors = cm.jet(range(num_years))[::-1]
        
        # 꺾은선 그래프 플롯 (기본 선은 회색조로 은은하게 깔고, 각 점에 무지개색 지정)
        ax.plot(filtered_df['연도'], filtered_df['최고기온(℃)'], color='#ff9999', alpha=0.5, label='최고기온 추세')
        ax.plot(filtered_df['연도'], filtered_df['최저기온(℃)'], color='#9999ff', alpha=0.5, label='최저기온 추세')
        
        # 연도별 점(Scatter)에 무지개 및 반전색 적용하여 시각 효과 극대화
        ax.scatter(filtered_df['연度'], filtered_df['최고기온(℃)'], c=high_colors, edgecolor='none', s=40, zorder=3)
        ax.scatter(filtered_df['연도'], filtered_df['최저기온(℃)'], c=low_colors, edgecolor='none', s=40, zorder=3)
        
        # 그래프 꾸미기
        ax.set_xlabel("Year (연도)", fontsize=12)
        ax.set_ylabel("Temperature (기온 ℃)", fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.6)
        
        # 범례 표시
        ax.legend(loc='upper left')
        
        # 스트림릿에 그래프 출력
        st.pyplot(fig)
        
        # 5. 데이터 테이블 보여주기 (선택사항)
        with st.expander("🔍 선택한 날짜의 상세 데이터 보기"):
            st.dataframe(filtered_df[['연도', '평균기온(℃)', '최저기온(℃)', '최고기온(℃)']].reset_index(drop=True))

except FileNotFoundError:
    st.error("📂 `seoul.csv` 파일을 찾을 수 없습니다. 앱과 같은 폴더에 업로드해주세요.")
