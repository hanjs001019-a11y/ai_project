import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# 1. 페이지 레이아웃 설정
st.set_page_config(
    page_title="전 세계 MBTI 데이터 분석기",
    page_icon="🌍",
    layout="centered"
)

st.title("📊 전 세계 MBTI 데이터 분석 대시보드")
st.markdown("전 세계 국가별 MBTI 16가지 성격 유형 데이터를 다각도로 분석하고 시각화합니다.")

# 2. 데이터 파일 로드 (캐싱 처리)
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("countriesMBTI_16types.csv")
        return df
    except FileNotFoundError:
        st.error("⚠️ 'countriesMBTI_16types.csv' 파일을 찾을 수 없습니다. GitHub 저장소에 데이터 파일이 있는지 확인해 주세요.")
        return None

df = load_data()

if df is not None:
    # 3. 사이드바 - 분석 모드 선택
    st.sidebar.header("⚙️ 분석 모드 선택")
    analysis_mode = st.sidebar.radio(
        "원하는 분석 방식을 선택하세요:",
        ["🗺️ 국가별 MBTI 비율 보기", "✨ MBTI별 상위 10개국 보기"]
    )

    # ----------------------------------------------------
    # 모드 1: 국가별 MBTI 비율 보기 (기존 기능 + 무지개 색상 변경)
    # ----------------------------------------------------
    if "국가별 MBTI 비율 보기" in analysis_mode:
        st.sidebar.subheader("🗺️ 국가 선택")
        countries = sorted(df['Country'].unique())
        selected_country = st.sidebar.selectbox("분석할 국가를 선택하세요:", countries)

        # 국가 데이터 추출 및 비율 기준 정렬
        country_data = df[df['Country'] == selected_country].iloc[0]
        mbti_types = df.columns[1:]
        percentages = [country_data[mbti] * 100 for mbti in mbti_types]
        
        mbti_df = pd.DataFrame({
            'MBTI': mbti_types,
            'Percentage': percentages
        }).sort_values(by='Percentage', ascending=False).reset_index(drop=True)

        num_items = len(mbti_df)
        # 1등부터 순서대로 무지개 색상 분배 (Plotly 무지개 스케일 샘플링)
        rainbow_colors = px.colors.sample_colorscale("Rainbow", [i/(num_items-1) for i in range(num_items)])

        # Plotly 막대그래프 생성
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=mbti_df['MBTI'],
            y=mbti_df['Percentage'],
            marker_color=rainbow_colors,
            marker_line=dict(color='#ffffff', width=0.5),
            text=[f"{val:.2f}%" for val in mbti_df['Percentage']],
            textposition='auto',
            hoverinfo='x+y'
        ))

        fig.update_layout(
            title=dict(
                text=f"🌈 {selected_country}의 MBTI 성격 유형 순위 (1위: {mbti_df.loc[0, 'MBTI']})",
                font=dict(size=18, color="white")
            ),
            xaxis=dict(title="MBTI 유형", tickfont=dict(color="white")),
            yaxis=dict(title="비율 (%)", tickfont=dict(color="white"), gridcolor="#444444"),
            plot_bgcolor="#1e1e1e",
            paper_bgcolor="#111111",
            margin=dict(l=40, r=40, t=60, b=40),
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)

        # 주요 지표 요약 카드
        st.subheader(f"📌 {selected_country} 주요 지표 요약")
        col1, col2, col3 = st.columns(3)
        col1.metric(label="가장 많은 유형 (1위)", value=mbti_df.loc[0, 'MBTI'], delta=f"{mbti_df.loc[0, 'Percentage']:.2f}%")
        col2.metric(label="2위 유형", value=mbti_df.loc[1, 'MBTI'], delta=f"{mbti_df.loc[1, 'Percentage']:.2f}%")
        col3.metric(label="가장 적은 유형 (16위)", value=mbti_df.loc[num_items-1, 'MBTI'], delta=f"{mbti_df.loc[num_items-1, 'Percentage']:.2f}%", delta_color="inverse")

        with st.expander("📊 정렬된 데이터 시트 확인하기"):
            st.dataframe(mbti_df.rename(columns={'MBTI': '성격 유형', 'Percentage': '비율 (%)'}), use_container_width=True)

    # ----------------------------------------------------
    # 모드 2: MBTI별 상위 10개국 보기 (신규 추가 기능)
    # ----------------------------------------------------
    elif "MBTI별 상위 10개국 보기" in analysis_mode:
        st.sidebar.subheader("✨ MBTI 유형 선택")
        mbti_list = sorted(df.columns[1:])
        selected_mbti = st.sidebar.selectbox("조회할 MBTI 유형을 선택하세요:", mbti_list)

        # 선택한 MBTI 비율을 기준으로 내림차순 정렬 후 상위 10개국 추출
        top10_df = df[['Country', selected_mbti]].copy()
        top10_df[selected_mbti] = top10_df[selected_mbti] * 100  # 백분율 변환
        top10_df = top10_df.sort_values(by=selected_mbti, ascending=False).head(10).reset_index(drop=True)
        top10_df.index = top10_df.index + 1  # 순위를 1부터 시작하도록 변경

        # 1등부터 10등까지 무지개 색상 배치
        rainbow_colors_top10 = px.colors.sample_colorscale("Rainbow", [i/9 for i in range(10)])

        # Plotly 막대그래프 생성
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=top10_df['Country'],
            y=top10_df[selected_mbti],
            marker_color=rainbow_colors_top10,
            marker_line=dict(color='#ffffff', width=0.5),
            text=[f"{val:.2f}%" for val in top10_df[selected_mbti]],
            textposition='auto',
            hoverinfo='x+y'
        ))

        fig.update_layout(
            title=dict(
                text=f"🌈 {selected_mbti} 비율이 가장 높은 상위 10개국 (1위: {top10_df.loc[1, 'Country']})",
                font=dict(size=18, color="white")
            ),
            xaxis=dict(title="국가 (Country)", tickfont=dict(color="white"), categoryorder='array', categoryarray=top10_df['Country']),
            yaxis=dict(title="비율 (%)", tickfont=dict(color="white"), gridcolor="#444444"),
            plot_bgcolor="#1e1e1e",
            paper_bgcolor="#111111",
            margin=dict(l=40, r=40, t=60, b=40),
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)

        # 순위 리스트 출력
        st.subheader(f"🏆 {selected_mbti} 보유 비율 순위 TOP 10")
        
        # 가독성을 높이기 위한 테이블 포맷팅
        display_df = top10_df.copy()
        display_df.columns = ['국가명', f'{selected_mbti} 비율 (%)']
        st.dataframe(display_df, use_container_width=True)
