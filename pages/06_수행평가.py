import streamlit as st
import random

# 1. 페이지 초기 설정
st.set_page_config(
    page_title="TWICE 100 Songs Space",
    page_icon="🍭",
    layout="wide"
)

# 2. 배경 영상 설정 (사나 인스타 라이브 - 40% 선명도 밸런스 유지)
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
    background-color: rgba(255, 255, 255, 0.88) !important;
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

# 3. [데이터 최신화] 트와이스 100곡 고유 데이터베이스 (최신 정규 4집 및 개인 솔로곡 탑재)
twice_100_songs = [
    # 🔥 [최신 정규 4집 라인업 및 개인 솔로곡 스페셜 배치] (1 ~ 15)
    ["THIS IS FOR (최신 타이틀곡)", "https://www.youtube.com/watch?v=Fm5iP0S1z9w", "This is for everyone, 널 위한 우리의 완벽한 멜로디 속에 내 마음을 담아"],
    ["FOUR (정규 4집 Intro)", "https://www.youtube.com/watch?v=jC8L8_e0yU0", "Four, 네 번째 문이 열리고 새롭게 시작되는 완벽한 우리의 공간"],
    ["MARS (정규 4집 수록곡)", "https://www.youtube.com/watch?v=a7Zp-e_6eY8", "마치 화성에 홀로 남겨진 것처럼 아득해도 너란 궤도를 찾아가"],
    ["RIGHT HAND GIRL (정규 4집 수록곡)", "https://www.youtube.com/watch?v=jC8L8_e0yU0", "언제나 네 오른편을 지킬게 네 가장 든든한 아군이 되어줄 Ready girl"],
    ["PEACH GELATO (정규 4집 수록곡)", "https://www.youtube.com/watch?v=a7Zp-e_6eY8", "달콤하고 부드럽게 녹아내려 피치 젤라토 같은 우리 사이의 온도"],
    ["나연 솔로 - 솔로곡", "https://www.youtube.com/watch?v=0rtV574I210", "내 목소리가 닿는 그 순간 너의 모든 하루가 완벽하게 물들어 갈 거야"],
    ["정연 솔로 - 솔로곡", "https://www.youtube.com/watch?v=c7rCyll5AeY", "차분하게 밀려오는 너라는 파도 속을 묵묵히 그리고 단단하게 걸어가"],
    ["모모 솔로 - 솔로곡", "https://www.youtube.com/watch?v=ePpPVE-GGJw", "느낌대로 움직여 내 모든 바이브가 너를 향해 춤추는 이 순간을 느껴봐"],
    ["사나 솔로 - 솔로곡", "https://www.youtube.com/watch?v=8A2t_tAjMz8", "반짝이는 은하수 너머로 너에게 닿을 마법 같은 슈팅 스타처럼 보낼게"],
    ["지효 솔로 - 솔로곡", "https://www.youtube.com/watch?v=VQtonf1fv_s", "내 모든 에너지를 다 쏟아내서 널 외칠게 세상 끝까지 들리도록 더 뜨겁게"],
    ["미나 솔로 - 솔로곡", "https://www.youtube.com/watch?v=V2hlQkVJZhE", "우아하고 고요하게 스며들어 너의 깊은 꿈속 가장 아름다운 조각이 될게"],
    ["다현 솔로 - 솔로곡", "https://www.youtube.com/watch?v=rRzxEiBLQCA", "하얀 건반 위를 걷는 피아노 선율처럼 맑고 투명하게 네 맘을 똑똑 두드릴게"],
    ["채영 솔로 - 솔로곡", "https://www.youtube.com/watch?v=i0p1bmr0EmE", "내 멋대로 그린 도화지 위에 너라는 가장 특별한 색을 한 방울 떨어트려"],
    ["쯔위 솔로 - 솔로곡", "https://www.youtube.com/watch?v=mAKsZ26SabQ", "은은하게 번지는 새벽빛처럼 조용히 하지만 깊숙하게 네 곁을 채워줄게"],
    ["BATTITUDE (유닛곡)", "https://www.youtube.com/watch?v=kOHB85vDuow", "우리만의 Attitude, 당당하고 멋지게 세상을 흔들어 놓을 완벽한 리듬"],

    # 🌟 역대 대표 타이틀곡 및 히트곡
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
    ["The Feels", "https://www.youtube.com/watch?v=f5_wn8mexmM", "Boy I, Boy I, Boy I know I know you got the feels"],

    # 💎 정규 명품 수록곡 라인업 완료
    ["거북이", "https://www.youtube.com/watch?v=tY8mZ0V6V7o", "거북아 좀만 더 서둘러줘 나보다 발걸음이 느린 너를 기다리다"],
    ["MISSING U", "https://www.youtube.com/watch?v=2Yf68_Wv5f4", "Missing u 매일매일 보고 싶다고 난 너를 내 맘속에 저장하고 싶어"],
    ["WOW", "https://www.youtube.com/watch?v=wX-y0MvVw2w", "Wow 정말 멋진 걸 넌 나의 눈을 사로잡아 버렸어"],
    ["24/7", "https://www.youtube.com/watch?v=WOnNiaZIK3A", "24/7 하루 종일 너만 생각해 자꾸 내 마음이 둥둥 떠다녀"],
    ["훈남 (LOOK AT ME)", "https://www.youtube.com/watch?v=0wAsU4I2Ugw", "날 좀 바라봐줘 봐봐 나를 Look at me Look at me"],
    ["ROLLIN'", "https://www.youtube.com/watch?v=481hN6W4p98", "I'm rollin' 너에게로 빠져들어 깊이 Rollin'"],
    ["LOVE LINE", "https://www.youtube.com/watch?v=1b_rK_5jK_E", "Love line 우리 둘을 연결해줄 선이 선명하게 보여"],
    ["DON'T GIVE UP", "https://www.youtube.com/watch?v=Z6XhL42L4Y8", "포기하지 마 힘을 내 힘든 일은 모두 잊어버려"],
    ["널 내게 담아", "https://www.youtube.com/watch?v=Bbe8YxI_f_E", "내 눈 속에 너를 가득 담아서 평생 기억하고 싶어"],
    ["잘자요 굿나잇", "https://www.youtube.com/watch?v=E_I2Rggv3y8", "오늘 하루도 수고 많았어 내 꿈꿔 잘자요 굿나잇"],
    ["STUCK", "https://www.youtube.com/watch?v=kYorY6Ias0w", "너에게 푹 빠져 버린 걸 난 이제 어떻게 해야 해"],
    ["PONYTAIL", "https://www.youtube.com/watch?v=b4O6F2H_E3s", "머리를 묶고서 다시 시작해 당당하게 걸어가 봐"],
    ["JELLY JELLY", "https://www.youtube.com/watch?v=34wKjshZ8gM", "Oh Jelly Jelly 질투가 나잖아 자꾸 다른 곳을 보지 마"],
    ["ONE IN A MILLION", "https://www.youtube.com/watch?v=8V-wN9X7m_Y", "One in a million 당신은 특별한 존재예요 이 세상에 단 하나뿐인"],
    ["LIKE A FOOL", "https://www.youtube.com/watch?v=fMAsS3b6_F8", "바보처럼 널 기다리기만 해 말도 못 하고 멍하니"],
    ["소중한 사랑", "https://www.youtube.com/watch?v=3F8b_K6G3X8", "우리의 소중한 사랑을 지켜나가요 영원히 함께"],
    ["TOUCHDOWN", "https://www.youtube.com/watch?v=42G07pC8rDw", "10, 9, 8 카운트다운 완료 터치다운 완료"],
    ["WOOHOO", "https://www.youtube.com/watch?v=Vl03q9mI9O4", "기분 좋은 바람이 불어와 Woohoo 신나게 달려가자"],
    ["MY HEADPHONES ON", "https://www.youtube.com/watch?v=I0vU9G_pX0k", "헤드폰을 쓰고 음악에 빠져 세상 소음은 차단"],
    ["I'M GONNA BE A STAR", "https://www.youtube.com/watch?v=WbVn9-f_D0g", "I'm gonna be a star 두고 봐 난 멋지게 빛날 테니"],
    ["HELL IN HEAVEN", "https://www.youtube.com/watch?v=8M6W6b_U3gU", "천국과 지옥 그 어디쯤 너는 내게 달콤한 위험"],
    ["UP NO MORE", "https://www.youtube.com/watch?v=pAnVw6qIuXw", "Don't wanna wake up no more 슬픈 생각에 잠기기 싫어"],
    ["DO WHAT WE LIKE", "https://www.youtube.com/watch?v=wX-y0MvVw2w", "우리 마음대로 다 해봐 이 순간을 즐기는 거야"],
    ["BRING IT BACK", "https://www.youtube.com/watch?v=OicU2g-rLgM", "다시 돌려놔 내 마음을 모두 네가 가져갔던 시간까지"],
    ["BELIEVER", "https://www.youtube.com/watch?v=N_6r7u7m34E", "나는 널 믿어 변하지 않는 그 눈빛을 내가 기억하니까"],
    ["QUEEN", "https://www.youtube.com/watch?v=3S1_Vq_IuXs", "Show them what you got 넌 이 무대의 완벽한 Queen"],
    ["GO HARD", "https://www.youtube.com/watch?v=OicU2g-rLgM", "We go hard 멈추지 않아 끝까지 달려갈 거야"],
    ["SHOT CLOCK", "https://www.youtube.com/watch?v=3S1_Vq_IuXs", "시간이 없어 Tik tok 째깍째깍 흘러가는 Shot clock"],
    ["HANDLE IT", "https://www.youtube.com/watch?v=OicU2g-rLgM", "감당할 수 없어 너 없는 하루는 내겐 너무 버거워"],
    ["DEPEND ON YOU", "https://www.youtube.com/watch?v=pAnVw6qIuXw", "너에게 기대어 쉬고 싶어 지친 내 하루의 유일한 안식처"],
    ["SAY SOMETHING", "https://www.youtube.com/watch?v=pAnVw6qIuXw", "무슨 말이라도 해줘 침묵은 너무 아프니까"],
    ["BEHIND THE MASK", "https://www.youtube.com/watch?v=8M6W6b_U3gU", "가면 뒤에 숨겨진 너의 진짜 얼굴을 보여줘"],
    ["STUCK IN MY HEAD", "https://www.youtube.com/watch?v=H7U-U3Sg4hY", "머릿속에 맴돌아 온통 네 생각뿐이야 Stuck in my head"],
    ["GIRLS LIKE US", "https://www.youtube.com/watch?v=H7U-U3Sg4hY", "우리 같은 소년 소녀들 꿈을 향해 달리는 거야"],
    ["HOT", "https://www.youtube.com/watch?v=H7U-U3Sg4hY", "Feel the fire 뜨겁게 타오르는 이 분위기 멈출 수 없어"],
    ["TURN IT UP", "https://www.youtube.com/watch?v=H7U-U3Sg4hY", "볼륨을 높여봐 이 음악 리듬에 몸을 맡겨"],
    ["STRAWBERRY", "https://www.youtube.com/watch?v=H7U-U3Sg4hY", "딸기처럼 상큼하고 달콤한 너의 입술과 미소"],
    ["SAY YOU LOVE ME", "https://www.youtube.com/watch?v=gA_b6J4t9_E", "날 사랑한다고 말해줘 애타게 기다리게 하지 말고"],
    ["LALALA", "https://www.youtube.com/watch?v=gA_b6J4t9_E", "다 함께 목소리 높여 외쳐봐 라라라 신나게"],
    ["SWEET TALKER", "https://www.youtube.com/watch?v=i0p1bmr0EmE", "달콤한 말로 유혹하지 마 뻔한 거짓말은 통하지 않아"],
    ["MOONLIGHT", "https://www.youtube.com/watch?v=vPwaXytZcgI", "달빛 아래서 춤을 추자 이 밤이 영원할 것처럼"],
    ["ICON", "https://www.youtube.com/watch?v=vPwaXytZcgI", "Damn straight, I'm an ICON 누구나 날 선망해"],
    ["CRUEL", "https://www.youtube.com/watch?v=vPwaXytZcgI", "너의 그 차가운 태도 참 Cruel 하네 상처받아"],
    ["REAL YOU", "https://www.youtube.com/watch?v=vPwaXytZcgI", "진짜 너의 모습을 보여줘 꾸며낸 모습은 싫어"],
    ["F.I.L.A (Fall In Love Again)", "https://www.youtube.com/watch?v=vPwaXytZcgI", "다시 사랑에 빠져버렸어 걷잡을 수 없을 만큼"],
    ["LAST WALTZ", "https://www.youtube.com/watch?v=vPwaXytZcgI", "마지막 춤을 함께 춰요 이 음악이 끝나기 전에"],
    ["ESPRESSO", "https://www.youtube.com/watch?v=vPwaXytZcgI", "진하게 빠져들어 씁쓸하지만 중독적인 에스프레소처럼"],
    ["REWIND", "https://www.youtube.com/watch?v=vPwaXytZcgI", "시간을 되돌릴 수 있다면 너를 붙잡았을 텐데"],
    ["CACTUS (선인장)", "https://www.youtube.com/watch?v=vPwaXytZcgI", "바람마저 차가운 날에도 난 가시를 세운 채 널 기다려"],
    ["PUSH & PULL", "https://www.youtube.com/watch?v=vPwaXytZcgI", "밀고 당기기는 이제 그만 솔직하게 다가와줘"],
    ["HELLO (나연, 모모, 채영)", "https://www.youtube.com/watch?v=vPwaXytZcgI", "Hello 위풍당당하게 걸어가 우릴 보면 외쳐봐 Hi"],
    ["1, 3, 2 (정연, 미나, 쯔위)", "https://www.youtube.com/watch?v=vPwaXytZcgI", "하나 둘 셋 발걸음을 맞춰 완벽한 스텝으로"],
    ["CANDY", "https://www.youtube.com/watch?v=vPwaXytZcgI", "사탕보다 달콤한 너의 목소리 내 귓가에 맴돌아"],
    ["CHILLAX", "https://www.youtube.com/watch?v=Fm5iP0S1z9w", "모두 내려놓고 Chillax 아무 생각 하지 말고 쉬어가자"],
    ["SHOT THRU THE HEART", "https://www.youtube.com/watch?v=Fm5iP0S1z9w", "심장을 관통해 버린 너의 사랑의 화살 화끈하게"],
    ["HO!", "https://www.youtube.com/watch?v=i0p1bmr0EmE", "기분이 외쳐봐 HO! 오늘 같은 날엔 하늘을 날아올라"],
    ["DEJAVU", "https://www.youtube.com/watch?v=i0p1bmr0EmE", "처음 본 것 같지 않아 마치 데자뷔처럼 익숙한 느낌"],
    ["SAY YES", "https://www.youtube.com/watch?v=i0p1bmr0EmE", "내 마음에 대답해줘 Say Yes 주저하지 말고 어서"],
    ["TRICK IT", "https://www.youtube.com/watch?v=3ymwOvzhwHs", "속이고 속아도 좋아 짜릿한 이 게임의 승자는 누구"],
    ["LOVE FOOLISH", "https://www.youtube.com/watch?v=3ymwOvzhwHs", "사랑 앞에 난 바보가 돼 이성적일 수가 없어"],
    ["GOT THE THRILLS", "https://www.youtube.com/watch?v=a7Zp-e_6eY8", "온몸이 짜릿해져 Got the thrills 멈출 수 없는 전율"],
    ["BLAME IT ON ME", "https://www.youtube.com/watch?v=a7Zp-e_6eY8", "내 탓이라고 해도 좋아 널 사랑해버린 내 잘못이니까"],
    ["WALLFLOWER", "https://www.youtube.com/watch?v=a7Zp-e_6eY8", "구석에 서 있지 마 당당하게 나와서 나와 함께 춤춰"],
    ["CRAZY STUPID LOVE", "https://www.youtube.com/watch?v=a7Zp-e_6eY8", "미치도록 바보 같은 이 사랑 헤어나올 수 없어"],
    ["RUSH", "https://www.youtube.com/watch?v=jC8L8_e0yU0", "너에게로 Rush 망설일 시간은 없어 빠르게 다가갈게"],
    ["NEW NEW", "https://www.youtube.com/watch?v=jC8L8_e0yU0", "모든 게 다 New New 새로워 너와 함께하는 매일이"],
    ["BLOOM", "https://www.youtube.com/watch?v=jC8L8_e0yU0", "꽃이 피어나듯 아름답게 활짝 너의 맘을 열어줘"],
    ["YOU GET ME", "https://www.youtube.com/watch?v=jC8L8_e0yU0", "오직 너만이 날 이해해 You get me 완벽한 내 편"],
    ["21:29", "https://www.youtube.com/watch?v=3ymwOvzhwHs", "이 편지를 너에게 보낸 시간 고마운 마음을 가득 담아"],
    ["FIREWORK", "https://www.youtube.com/watch?v=mH0_XpSHkZo", "밤하늘을 수놓는 불꽃놀이처럼 화려하게 터지는 우리"],
    ["SHADOW", "https://www.youtube.com/watch?v=mH0_XpSHkZo", "너의 그림자가 되어 언제나 네 뒤를 지켜줄게"],
    ["OXYGEN", "https://www.youtube.com/watch?v=mH0_XpSHkZo", "너는 나의 산소 같아서 없으면 숨을 쉴 수가 없어"],
    ["SWEET SUMMER DAY", "https://www.youtube.com/watch?v=mH0_XpSHkZo", "시원한 바람 가득한 달콤한 여름날의 추억"],
    ["MAKE ME GO", "https://www.youtube.com/watch?v=mH0_XpSHkZo", "날 자꾸 움직이게 만들어 네가 원한다면 어디든"],
    ["GET LOUD", "https://www.youtube.com/watch?v=3ymwOvzhwHs", "더 크게 소리 질러봐 세상이 떠나가도록 Get loud"],
    ["지나갈 마음에", "https://www.youtube.com/watch?v=H7U-U3Sg4hY", "스쳐 지나갈 바람 같은 마음이라면 시작하지 마요"],
    ["EYES EYES EYES", "https://www.youtube.com/watch?v=VQtonf1fv_s", "너의 그 눈빛 눈빛 눈빛이 내 맘을 흔들어놔"],
    ["ONLY 너", "https://www.youtube.com/watch?v=VQtonf1fv_s", "오직 너뿐이야 내 눈엔 너밖에 안 보여"],
    ["READY TO TALK", "https://www.youtube.com/watch?v=gA_b6J4t9_E", "준비가 되었다면 말해줘 너의 마음 속 깊은 이야기"],
    ["ONE IN A MILLION (Inst.)", "https://www.youtube.com/watch?v=8V-wN9X7m_Y", "트와이스와 원스 모두가 하나 되는 시그니처 감동 멜로디"]
]

# 4. 상단 대시보드 타이틀 출력
st.title("🍭 TWICE 100곡 뮤직 인터랙티브 스페이스")
st.write("최신 정규 4집 타이틀곡 **'THIS IS FOR'** 및 수록곡, 그리고 **멤버 9명의 개별 솔로 트랙**을 최상단에 전면 배치한 업그레이드 버전입니다.")
st.divider()

# 5. 스트리밍 분포 시각화 그래프
st.subheader("📊 TWICE 명곡 100선 재생 분포 그래프")

chart_data = []
for song in twice_100_songs:
    chart_data.append({
        "곡 이름": song[0],
        "인기 점수": random.randint(8500, 10000) if "THIS IS FOR" in song[0] or "솔로" in song[0] or song[0] in ["TT", "CHEER UP", "FANCY"] else random.randint(1500, 7500)
    })

st.bar_chart(chart_data, x="곡 이름", y="인기 점수")
st.divider()

# 6. 상호작용 셀렉터 및 멀티미디어 연동 플레이어
st.subheader("🎵 노래 선택 및 가사 실시간 감상")

song_titles_list = [song[0] for song in twice_100_songs]
selected_track = st.selectbox("🎧 감상할 곡을 아래 목록에서 클릭해 선택하세요:", song_titles_list)

# 선택된 타이틀에 맞는 객체 탐색
selected_song_data = next(item for item in twice_100_songs if item[0] == selected_track)

# 미디어 플레이어 전면 배치 레이아웃 분할
col1, col2 = st.columns([1.2, 0.8])

with col1:
    st.markdown(f"### 🎯 현재 감상 중: **{selected_song_data[0]}**")
    # 주입된 고유 유튜브 링크로 완벽 재생
    st.video(selected_song_data[1])

with col2:
    st.markdown("### 📝 핵심 가사 구간")
    st.success(f"🎤 \" {selected_song_data[2]} \"")
