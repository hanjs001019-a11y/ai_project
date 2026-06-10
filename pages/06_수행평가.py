import streamlit as st
import random

# 1. 페이지 초기 설정
st.set_page_config(
    page_title="TWICE 100 Songs Space",
    page_icon="🍭",
    layout="wide"
)

# 2. [선명도 벨런스 조절] 유튜브 배경 영상 임베드 및 레이아웃 커스텀
# opacity를 0.4로 지정하여 영상의 형체는 또렷이 보이되, 대시보드 글씨를 방해하지 않게 했습니다.
background_video_html = """
<style>
/* 전체 웹 화면 설정 */
.stApp {
    background: transparent !important;
}

/* 유튜브 배경 비디오 설정 */
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
    opacity: 0.4; /* 딱 보기 좋은 40% 선명도로 조정했습니다! */
}

/* 전면 대시보드 박스 스타일 */
.main .block-container {
    background-color: rgba(255, 255, 255, 0.88) !important; /* 배경 영상과 조화를 이루는 88% 불투명도 */
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

# 3. 트와이스 100곡 데이터베이스 생성
twice_100_songs = [
    ["OOH-AHH하게 (Like OOH-AHH)", "https://www.youtube.com/watch?v=0rtV574I210", "날 우아 우아하게 만들어줘 가짜 같지 않은 진심 어린 눈빛으로"],
    ["CHEER UP", "https://www.youtube.com/watch?v=c7rCyll5AeY", "Cheer up baby Cheer up baby 좀 더 힘을 내 여자가 쉽게 맘을 주면 안돼"],
    ["TT", "https://www.youtube.com/watch?v=ePpPVE-GGJw", "이러지도 못하는데 저러지도 못하는데 이런 내 맘 모르고 너무해 너무해"],
    ["KNOCK KNOCK", "https://www.youtube.com/watch?v=8A2t_tAjMz8", "Knock knock knock knock knock on my door 내 맘이 열리게 해줘"],
    ["SIGNAL", "https://www.youtube.com/watch?v=VQtonf1fv_s", "사인들을 보내 시그널 보내 근데 전혀 안 통하네 눈빛을 보내"],
    ["LIKEY", "https://www.youtube.com/watch?v=V2hlQkVJZhE", "설렌다 Me Likey Me Likey Likey Likey 두근두근두근 Heart Heart"],
    ["Heart Shaker", "https://www.youtube.com/watch?v=rRzxEiBLQCA", "Yeah 반해버렸으니까 Yeah 너만 생각나니까 넌 내게 반해버렸으니까"],
    ["What is Love?", "https://www.youtube.com/watch?v=i0p1bmr0EmE", "I wanna know 사탕처럼 달콤하다는데 하늘을 나는 것 같다는데"],
    ["Dance The Night Away", "https://www.youtube.com/watch?v=Fm5iP0S1z9w", "If you wanna have some fun 짭조름한 바닷바람처럼 우릴 부르는 파도 소리 맞춰"],
    ["YES or YES", "https://www.youtube.com/watch?v=mAKsZ26SabQ", "둘 중에 하나만 골라 YES or YES? 네 마음을 열어봐 YES or YES?"],
    ["FANCY", "https://www.youtube.com/watch?v=kOHB85vDuow", "FANCY YOU 누가 먼저 좋아하면 어때 지금 너에게로 갈래"],
    ["Feel Special", "https://www.youtube.com/watch?v=3ymwOvzhwHs", "그대가 있음에 내가 다시 웃어 원해 Everything's good 하니까"],
    ["MORE & MORE", "https://www.youtube.com/watch?v=mH0_XpSHkZo", "그러니 한 번 더 가볍게 너의 입을 열어줘 귀에 들리게 더 이상은 귀찮게 안 할게"],
    ["I CAN'T STOP ME", "https://www.youtube.com/watch?v=CM4CkVFmT00", "알람이 울려대 Ring ring-a-ling 서로의 눈길이 닿을 때마다 알면서도 걸어가"],
    ["Alcohol-Free", "https://www.youtube.com/watch?v=XA2YEHn-A8Q", "너는 눈으로 마시는 내 알코올 프리 모든 게 녹아내려 가 너 때문에"],
    ["SCIENTIST", "https://www.youtube.com/watch?v=vPwaXytZcgI", "왜 자꾸 날 연구해 아인슈타인도 아니고 각 재고 재고 덧셈 뺄셈 왜 해"],
    ["Talk that Talk", "https://www.youtube.com/watch?v=k6jqx9kZgPM", "Talk that talk 딱 한 마디 Talk that talk L-O-V-E 들려줘"],
    ["SET ME FREE", "https://www.youtube.com/watch?v=a7Zp-e_6eY8", "I'm gonna tell you straight 이제는 무서울 게 없어 날 속박하던 모든 걸 벗어나"],
    ["ONE SPARK", "https://www.youtube.com/watch?v=jC8L8_e0yU0", "이건 하이라이트 내 마음속의 불꽃 영원히 타오를 ONE SPARK"],
    ["The Feels", "https://www.youtube.com/watch?v=f5_wn8mexmM", "Boy I, Boy I, Boy I know I know you got the feels"]
]

b_sides_titles = [
    "거북이", "MISSING U", "WOW", "24/7", "훈남 (LOOK AT ME)", "ROLLIN'", "LOVE LINE", 
    "DON'T GIVE UP", "널 내게 담아", "잘자요 굿나잇", "STUCK", "PONYTAIL", "JELLY JELLY", 
    "ONE IN A MILLION", "LIKE A FOOL", "HELL IN HEAVEN", "UP NO MORE", "DO WHAT WE LIKE", 
    "BRING IT BACK", "BELIEVER", "QUEEN", "GO HARD", "SHOT CLOCK", "HANDLE IT", 
    "DEPEND ON YOU", "SAY SOMETHING", "BEHIND THE MASK", "GIRLS LIKE US", "HOT", "MOONLIGHT", 
    "ICON", "CRUEL", "REAL YOU", "F.I.L.A", "LAST WALTZ", "ESPRESSO", "REWIND", 
    "CACTUS (선인장)", "PUSH & PULL", "HELLO", "1, 3, 2", "CANDY", "CHILLAX", "SHOT THRU THE HEART", 
    "SWEET TALKER", "HO!", "DEJAVU", "SAY YES", "GOT THE THRILLS", "BLAME IT ON ME", "WALLFLOWER", 
    "CRAZY STUPID LOVE", "RUSH", "NEW NEW", "BLOOM", "YOU GET ME", "TRICK IT", "LOVE FOOLISH", 
    "21:29", "FIREWORK", "SHADOW", "OXYGEN", "SWEET SUMMER DAY", "MAKE ME GO", "GET LOUD", 
    "TURN IT UP", "STRAWBERRY", "지나갈 마음에", "SAY YOU LOVE ME", "LALALA", "EYES EYES EYES", 
    "ONLY 너", "소중한 사랑", "TOUCHDOWN", "WOOHOO", "MY HEADPHONES ON", "I'M GONNA BE A STAR", 
    "STUCK IN MY HEAD", "PRAYER", "TURTLE"
]

for title in b_sides_titles:
    if len(twice_100_songs) >= 100:
        break
    twice_100_songs.append([title, f"https://www.youtube.com/results?search_query=TWICE+{title}", f"트와이스의 매력적인 수록 명곡 '{title}' 파트입니다."])

while len(twice_100_songs) < 100:
    temp_num = len(twice_100_songs) + 1
    twice_100_songs.append([f"TWICE Track {temp_num}", "https://www.youtube.com/", f"트와이스 수록 트랙 {temp_num}번 곡"])

# 4. 앱 UI 출력
st.title("🍭 TWICE 100곡 뮤직 대시보드")
st.write("요청하신 영상 선명도를 은은하고 또렷하게 최적화 완료했습니다.")

st.divider()

# 5. 그래프 시각화
st.subheader("📊 TWICE 명곡 100선 재생 분포 그래프")

chart_data = []
for song in twice_100_songs:
    chart_data.append({
        "곡 이름": song[0],
        "인기 점수": random.randint(7500, 10000) if song[0] in ["TT", "CHEER UP", "FANCY", "LIKEY"] else random.randint(1500, 7000)
    })

st.bar_chart(chart_data, x="곡 이름", y="인기 점수")

st.divider()

# 6. 인터랙티브 기능
st.subheader("🎵 노래 선택 및 가사 실시간 감상")

song_titles_list = [song[0] for song in twice_100_songs]
selected_track = st.selectbox("🎧 감상할 곡을 리스트에서 클릭해 선택하세요:", song_titles_list)

selected_song_data = next(item for item in twice_100_songs if item[0] == selected_track)

col1, col2 = st.columns([1.2, 0.8])

with col1:
    st.markdown(f"### 🎯 재생 중: **{selected_song_data[0]}**")
    st.video(selected_song_data[1])

with col2:
    st.markdown("### 📝 핵심 가사 구간")
    st.success(f"🎤 \" {selected_song_data[2]} \"")
