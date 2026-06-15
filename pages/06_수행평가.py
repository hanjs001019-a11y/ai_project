import streamlit as st
import random

# 1. 페이지 및 레이아웃 설정
st.set_page_config(
    page_title="TWICE Premium Home",
    page_icon="🍭",
    layout="wide"
)

# 2. 배경 영상 설정 (사나 인스타 라이브 배경)
background_video_html = """
<style>
.stApp {
    background: transparent !important;
}
#yt-bg-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: -9999;
    pointer-events: none;
    overflow: hidden;
}
#yt-bg-iframe {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 100vw;
    height: 56.25vw;
    min-height: 100vh;
    min-width: 177.77vh;
    transform: translate(-50%, -50%);
    opacity: 0.35;
}
.main .block-container {
    background-color: rgba(255, 255, 255, 0.93) !important;
    padding: 3rem !important;
    border-radius: 24px !important;
    box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.15) !important;
    margin-top: 3rem;
    margin-bottom: 3rem;
}
</style>
<div id="yt-bg-container">
    <iframe id="yt-bg-iframe"
        src="https://www.youtube.com/embed/XPl101FON7A?autoplay=1&mute=1&loop=1&playlist=XPl101FON7A&controls=0&showinfo=0&rel=0&enablejsapi=1&playsinline=1"
        frameborder="0"
        allow="autoplay; encrypted-media"
        allowfullscreen>
    </iframe>
</div>
"""
st.markdown(background_video_html, unsafe_allow_html=True)

# 3. 뮤비가 아니어도 대중에게 가장 사랑받은 5곡의 명품 수록곡 DB
twice_essential_5 = [
    ["🎵 ONE IN A MILLION", "OA41_pkBL50", "원스(ONCE)와 트와이스 모두에게 눈물 버튼이자 감동인 최고의 팬송! '넌 단 한 사람뿐이야'"],
    ["🎵 Like a Fool", "4V11N2A_W7Y", "데뷔 앨범 수록곡 중 단연 원탑으로 꼽히는, 트와이스의 명품 보컬과 감성을 보여주는 발라드 곡"],
    ["🎵 거북이 (TURTLE)", "tVv_C2fYStU", "정규 1집의 최고 인기 수록곡! 거북이처럼 느려도 한 걸음씩 다가와 달라는 청량하고 귀여운 감성"],
    ["🎵 선인장 (CACTUS)", "OTHG8RqPSKE", "리더 지효의 애절하고 폭발적인 가창력과 작사/작곡 능력이 돋보이는 웰메이드 락 발라드 트랙"],
    ["🎵 SAY YOU LOVE ME", "x2cUrOnaCDg", "망설이는 상대방에게 당당하고 시원하게 마음을 요구하는 트와이스 특유의 에너제틱한 팝 사운드"]
]

# 4. 앱 헤더 화면 출력
st.title("🍭 TWICE 엄선 명품 수록곡 베스트 5 전용 룸")
st.write("재생 에러가 발생하는 대용량 요소를 전부 걷어내고, 뮤직비디오가 없어도 대중과 팬들에게 우호적인 사랑을 가장 많이 받은 트랙 5가지로 재조정했습니다.")
st.divider()

# 5. 스트리밍 분포 시각화 그래프
st.subheader("📊 선호도 트랙 실시간 시뮬레이션")
chart_data = []
for song in twice_essential_5:
    chart_data.append({
        "곡 이름": song[0],
        "팬덤 지지율": random.randint(8500, 9999)
    })
st.bar_chart(chart_data, x="곡 이름", y="팬덤 지지율")
st.divider()

# 6. 상호작용 셀렉터 및 내부 빌트인 비디오 플레이어
st.subheader("🎧 곡을 골라 즉시 감상해보세요")

song_titles_list = [song[0] for song in twice_essential_5]
selected_track = st.selectbox("리스트를 열어 곡을 선택하세요:", song_titles_list)

selected_song_data = next(item for item in twice_essential_5 if item[0] == selected_track)

# 화면 분할 배치
col1, col2 = st.columns([1.3, 0.7])

with col1:
    st.markdown(f"### 📺 사이트 내부 온스크린 오디오 재생: **{selected_track}**")
    
    # 퍼가기 차단을 피하는 최적화된 내부 인라인 아이프레임
    inline_player_html = f"""
    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.15);">
        <iframe 
            src="https://www.youtube.com/embed/{selected_song_data[1]}?autoplay=0&rel=0&showinfo=0&controls=1&enablejsapi=1" 
            style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
            allowfullscreen>
        </iframe>
    </div>
    """
    st.components.v1.html(inline_player_html, height=480)

with col2:
    st.markdown("### 📝 추천 감상 포인트")
    st.info(f"🎤 {selected_song_data[2]}")
