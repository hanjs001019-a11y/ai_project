import streamlit as st
import folium
from streamlit_folium import st_folium

# 1. 페이지 설정
st.set_page_config(
    page_title="Seoul Top 10 Tourist Attractions",
    page_icon="📌",
    layout="wide"
)

st.title("🇰🇷 외국인이 사랑하는 서울 주요 관광지 Top 10")
st.markdown("스트림릿과 폴리움(Folium)을 활용해 서울의 랜드마크를 지도에 표시합니다.")

# 2. 데이터셋 정의 (외국인 선호 서울 관광지 Top 10)
locations = [
    {"name": "경복궁 (Gyeongbokgung Palace)", "lat": 37.5796, "lon": 126.9770, "desc": "조선 왕조의 주궁, 한복 체험의 성지"},
    {"name": "N서울타워 (N Seoul Tower)", "lat": 37.5512, "lon": 126.9882, "desc": "남산 정상에서 바라보는 최고의 서울 야경 및 사랑의 자물쇠"},
    {"name": "명동 쇼핑거리 (Myeong-dong)", "lat": 37.5629, "lon": 126.9850, "desc": "K-뷰티, 길거리 음식, 쇼핑의 중심지"},
    {"name": "북촌한옥마을 (Bukchon Hanok Village)", "lat": 37.5829, "lon": 126.9835, "desc": "도심 속 실제 주민들이 거주하는 고즈넉한 전통 한옥 주거지"},
    {"name": "인사동 (Insadong)", "lat": 37.5744, "lon": 126.9875, "desc": "한국 전통 골동품, 화랑, 전통 찻집이 모여있는 문화의 거리"},
    {"name": "홍대거리 (Hongdae)", "lat": 37.5567, "lon": 126.9235, "desc": "젊은 에너지가 가득한 버스킹, 클럽, 트렌디한 패션의 메카"},
    {"name": "동대문디자인플라자 (DDP)", "lat": 37.5365, "lon": 127.0093, "desc": "자하 하디드가 설계한 우주선 모양의 세계 최대 규모 3차원 비정형 건축물"},
    {"name": "스타필드 코엑스몰 (COEX - Starfield Library)", "lat": 37.5119, "lon": 127.0589, "desc": "인스타그램 핫플레이스인 거대한 별마당 도서관이 있는 복합몰"},
    {"name": "롯데월드타워 & 서울스카이 (Lotte World Tower)", "lat": 37.5126, "lon": 127.1025, "desc": "세계 6위 높이(555m)에서 서울을 내려다보는 전망대"},
    {"name": "반포 한강공원 (Banpo Hangang Park)", "lat": 37.5114, "lon": 126.9962, "desc": "달빛무지개분수와 한강 라면, 치맥 문화 체험의 필수 코스"}
]

# 3. 레이아웃 분할 (사이드바 및 메인 화면)
st.sidebar.header("🗺️ 지도 설정")
map_type = st.sidebar.selectbox(
    "지도 스타일 선택",
    ["OpenStreetMap", "CartoDB positron", "CartoDB dark_matter"]
)

# 사이드바로 빠른 위치 확인 기능 제공
st.sidebar.markdown("---")
st.sidebar.subheader("📍 관광지 바로가기")
selected_attraction = st.sidebar.selectbox("정보를 볼 관광지를 선택하세요:", [loc["name"] for loc in locations])

# 4. 지도 생성 및 마커 추가
# 서울 중심부 좌표로 초기화
m = folium.Map(location=[37.550, 126.990], zoom_start=12, tiles=map_type)

for loc in locations:
    # 팝업에 들어갈 HTML 서식 지정
    popup_html = f"""
    <div style="font-family: 'Malgun Gothic', sans-serif; width:220px;">
        <h4 style="margin-bottom:5px; color:#1E3A8A;">{loc['name']}</h4>
        <p style="font-size:12px; color:#555; line-height:1.4;">{loc['desc']}</p>
    </div>
    """
    
    # 특정 관광지가 선택되었을 때 마커 색상을 다르게 표시하는 포인트 부여
    marker_color = "red" if loc["name"] == selected_attraction else "blue"
    
    folium.Marker(
        location=[loc["lat"], loc["lon"]],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=loc["name"],
        icon=folium.Icon(color=marker_color, icon="info-sign")
    ).add_to(m)

# 5. 스트림릿 화면에 지도 렌더링
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("서울 관광 지도")
    # 지도 출력 및 변경 이력 수집
    st_folium(m, width=800, height=550, returned_objects=[])

with col2:
    st.subheader("상세 정보")
    # 사이드바에서 선택한 명소 정보를 우측에 표시
    for loc in locations:
        if loc["name"] == selected_attraction:
            st.info(f"**{loc['name']}**")
            st.write(loc["desc"])
            st.caption(f"위도: {loc['lat']} / 경도: {loc['lon']}")

st.markdown("---")
st.caption("Data Source: 한국관광공사 및 서울관광재단 선호도 기준 재구성 (2026)")
