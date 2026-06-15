import streamlit as st
import random

# 1. 페이지 초기 설정
st.set_page_config(
    page_title="TWICE Premium Home",
    page_icon="🍭",
    layout="wide"
)

# 2. 배경 영상 설정 (사나 인스타 라이브 - 40% 투명도 인라인 배경)
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
    opacity: 0.4;
}
.main .block-container {
    background-color: rgba(255, 255, 255, 0.90) !important;
    padding: 3rem !important;
    border-radius: 24px !important;
    box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.15) !important;
    margin-top: 2rem;
    margin-bottom: 2rem;
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

# 3. [오류 트랙 제외] 신곡 THIS IS FOR + 에러 프리 대표곡 최종 라인업
# 요청하신 대로 재생 에러를 일으키던 3곡을 완벽히 제거했습니다.
twice_reliable_songs = [
    ["🔥 THIS IS FOR (최신 히트곡)", "xCWDoqQ0XDo", "This is for all my ladies who don't get hyped enough! 완벽한 조화"],
    ["🍭 CHEER UP", "c7rCyll5AeY", "Cheer up baby Cheer up baby 좀 더 힘을 내 여자가 쉽게 맘을 주면 안돼"],
    ["🍭 TT", "ePpPVE-GGJw", "이러지도 못하는데 저러지도 못하는데 이런 내 맘 모르고 너무해 너무해"],
    ["🍭 KNOCK KNOCK", "8A2t_tAjMz8", "Knock knock knock knock knock on my door 내 맘이 열리게 해줘"],
    ["🍭 SIGNAL", "VQtonf1fv_s", "사인들을 보내 시그널 보내 근데 전혀 안 통하네 눈빛을 보내"],
    ["🍭 LIKEY", "V2hlQkVJZhE", "설렌다 Me Likey Me Likey Likey Likey 두근두근두근 Heart Heart"],
    ["🍭 Heart Shaker", "rRzxEiBLQCA", "Yeah 반해버렸으니까 Yeah 너만 생각나니까 넌 내게 반해버렸으니까"],
    ["🍭 What is Love?", "i0p1bmr0EmE", "I wanna know 사탕처럼 달콤하다는데 하늘을 나는 것 같다는데"],
    ["🍭 Dance The Night Away", "Fm5iP0S1z9w", "If you wanna have some fun 짭조름한 바닷바람처럼 우릴 부르는 파도 소리 맞춰"],
    ["🍭 YES or YES", "mAKsZ26SabQ", "둘 중에 하나만 골라 YES or YES? 네 마음을 열어봐 YES or YES?"],
    ["🍭 FANCY", "kOHB85vDuow", "FANCY YOU 누가 먼저 좋아하면 어때 지금 너에게로 갈래"],
    ["🍭 Feel Special", "3ymwOvzhwHs", "그대가 있음에 내가 다시 웃어 원해 Everything's good 하니까"],
    ["🍭 Alcohol-Free", "XA2YEHn-A8Q", "너는 눈으로 마시는 내 알코올 프리 모든 게 녹아내려 가 너 때문에"],
    ["🍭 Talk that Talk", "k6jqx9kZgPM", "Talk that talk 딱 한 마디 Talk that talk L-O-V-E 들려줘"]
]

# 4. 상단 대시보드 타이틀 출력
st.title("🍭 TWICE 프리미엄 인라인 뮤직 룸")
st.write("요청에 따라 일부 에러 발생 트랙을 완전히 제외한 최종 화면 내장 재생 버전입니다.")
st.divider()

# 5. 스트리밍 분포 시각화 그래프
st.subheader("📊 선호도 트랙 실시간 시뮬레이션")

chart_data = []
for song in twice_reliable_songs:
    chart_data.append({
        "곡 이름": song[0],
        "인기 지수": random.randint(9000, 10000) if "THIS IS FOR" in song[0] or song[0] in ["🍭 TT", "🍭 CHEER UP", "🍭 FANCY"] else random.randint(4000, 8000)
    })

st.bar_chart(chart_data, x="곡 이름", y="인기 지수")
st.divider()

# 6. 상호작용 셀렉터 및 내부 빌트인 비디오 플레이어
st.subheader("🎵 노래 선택 및 대시보드 내 즉시 감상")

song_titles_list = [song[0] for song in twice_reliable_songs]
selected_track = st.selectbox("🎧 감상할 곡을 아래 목록에서 클릭해 선택하세요:", song_titles_list)

selected_song_data = next(item for item in twice_reliable_songs if item[0] == selected_track)

# 화면 분할 배치 (플레이어 최적화 레이아웃)
col1, col2 = st.columns([1.3, 0.7])

with col1:
    st.markdown(f"### 📺 사이트 내부 인라인 비디오: **{selected_song_data[0]}**")
    
    # 임베드 표준 컨테이너 구조 적용
    inline_player_html = f"""
    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.2);">
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
    st.markdown("### 📝 핵심 가사 구간")
    st.success(f"🎤 \" {selected_song_data[2]} \"")
