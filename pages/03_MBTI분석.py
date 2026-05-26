import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. 페이지 레이아웃 설정
st.set_page_config(
    page_title="국가별 MBTI 데이터 분석",
    page_icon="📊",
    layout="centered"
)

st.title("📊 국가별 MBTI 분포 시각화 대시보드")
st.markdown("전 세계 국가별 MBTI 16가지 성격 유형 비율 데이터를 시각화합니다.")

# 2. 데이터 파일 로드 (캐싱 처리)
@st.cache_data
def load_data():
    try:
        # 업로드하신 데이터셋 파일 이름과 일치시킵니다.
        df = pd.read_csv("countriesMBTI_16types.csv")
        return df
    except FileNotFoundError:
        st.error("⚠️ 'countriesMBTI_16types.csv' 파일을 찾을 수 없습니다. GitHub 저장소에 데이터 파일을 함께 업로드해 주세요.")
        return None

df = load_data()

if df is not None:
    # 3. 사이드바 - 국가 선택 인터페이스
    st.sidebar.header("🗺️ 필터 설정")
    countries = sorted(df['Country'].unique())
    selected_country = st.sidebar.selectbox("분석할 국가를 선택하세요:", countries)

    # 4. 선택된 국가 데이터 추출 및 비율 기준 정렬
    country_data = df[df['Country'] == selected_country].iloc[0]
    
    mbti_types = df.columns[1:]
    percentages = [country_data[mbti] * 100 for mbti in mbti_types] # 백분율(%) 변환
    
    # 데이터프레임 빌드 후 내림차순(높은 순) 정렬
    mbti_df = pd.DataFrame({
        'MBTI': mbti_types,
        'Percentage': percentages
    }).sort_values(by='Percentage', ascending=False).reset_index(drop=True)

    # 5. 요청 맞춤형 디자인: 1등은 흰색, 나머지는 검은색에서 점점 흐려지는(밝아지는) 색상 계산
    colors = []
    num_items = len(mbti_df)
    
    for i in range(num_items):
        if i == 0:
            colors.append("rgb(255, 255, 255)") # 1등은 완전히 하얀색
        else:
            # 2등부터 마지막 16등까지 검은색(0,0,0) -> 흐린 회색(180,180,180)으로 단계적 그라데이션
            ratio = (i - 1) / (num_items - 2) if num_items > 2 else 0
            val = int(0 + (180 * ratio)) # 가독성을 고려해 최대 밝기를 180으로 제한
            colors.append(f"rgb({val}, {val}, {val})")

    # 6. Plotly 막대그래프 생성
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=mbti_df['MBTI'],
        y=mbti_df['Percentage'],
        marker_color=colors,
        marker_line=dict(color='#888888', width=1), # 하얀색 막대가 배경과 구별되도록 테두리 적용
        text=[f"{val:.2f}%" for val in mbti_df['Percentage']],
        textposition='auto',
        hoverinfo='x+y'
    ))

    # 차트의 가독성을 극대화하기 위해 다크 테마 배경 적용
    fig.update_layout(
        title=dict(
            text=f"✨ {selected_country}의 MBTI 순위 (1위: {mbti_df.loc[0, 'MBTI']})",
            font=dict(size=18, color="white")
        ),
        xaxis=dict(title="MBTI 유형", tickfont=dict(color="white")),
        yaxis=dict(title="비율 (%)", tickfont=dict(color="white"), gridcolor="#444444"),
        plot_bgcolor="#222222",  # 차트 안쪽 어두운 배경색
        paper_bgcolor="#111111", # 차트 바깥쪽 어두운 배경색
        margin=dict(l=40, r=40, t=60, b=40),
        height=500
    )

    # 7. 스트림릿 화면에 차트 렌더링
    st.plotly_chart(fig, use_container_width=True)

    # 8. 핵심 지표 요약 카드 제공
    st.subheader(f"📌 {selected_country} 주요 지표 요약")
    col1, col2, col3 = st.columns(3)
    col1.metric(label="가장 많은 유형 (1위)", value=mbti_df.loc[0, 'MBTI'], delta=f"{mbti_df.loc[0, 'Percentage']:.2f}%")
    col2.metric(label="2위 유형", value=mbti_df.loc[1, 'MBTI'], delta=f"{mbti_df.loc[1, 'Percentage']:.2f}%")
    col3.metric(label="가장 적은 유형 (16위)", value=mbti_df.loc[num_items-1, 'MBTI'], delta=f"{mbti_df.loc[num_items-1, 'Percentage']:.2f}%", delta_color="inverse")

    # 원본 데이터 테이블 보기 열기
    with st.expander("📊 정렬된 데이터 시트 확인하기"):
        st.dataframe(mbti_df.rename(columns={'MBTI': '성격 유형', 'Percentage': '비율 (%)'}), use_container_width=True)
