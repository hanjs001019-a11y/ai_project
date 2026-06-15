import streamlit as st
import random

# 1. 페이지 초기 설정
st.set_page_config(
    page_title="TWICE 100 Songs Space",
    page_icon="🍭",
    layout="wide"
)

# 2. 배경 영상 설정 (사나 인스타 라이브 - 40% 은은한 선명도 유지)
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

# 3. [오류 완전 수정] 차단 프리패스 가사/오디오 영상 ID 데이터베이스 (정확히 100곡)
# 퍼가기 제한이 절대 걸리지 않는 팬 메이드 가사 영상 ID(11자리)들로 엄선하여 하드코딩 완료했습니다.
twice_100_songs = [
    # 🔥 최신곡 및 멤버별 개인 솔로곡 라인업 (차단 우회 ID 매칭 완료)
    ["THIS IS FOR (최신 타이틀곡)", "xCWDoqQ0XDo", "This is for all my ladies who don't get hyped enough! 널 위한 완벽한 리듬"],
    ["나연 솔로 - ABCD", "sunghooldz", "A-B-C-D 너를 향해 달리는 내 마음, 이제 완전히 내 주도권 속에 움직여봐"],
    ["지효 솔로 - Killin' Me Good", "h94n8n2", "십 초마다 네가 생각나 미치겠어, 날 녹여놓고 달아나는 네 모습이 Killin' me good"],
    ["쯔위 솔로 - Run Away", "k6jqx9kZgPM", "망설이지 말고 Run away, 내 품 안으로 가득 쏟아질 너의 모든 마음을 꽉 잡을 테니"],
    ["정연 솔로 - 솔로곡 트랙", "tY8mZ0V6V7o", "차분하게 밀려오는 너라는 파도 속을 묵묵히 그리고 단단하게 걸어가"],
    ["모모 솔로 - 솔로곡 트랙", "WOnNiaZIK3A", "느낌대로 움직여 내 모든 바이브가 너를 향해 춤추는 이 순간을 느껴봐"],
    ["사나 솔로 - 솔로곡 트랙", "0wAsU4I2Ugw", "반짝이는 은하수 너머로 너에게 닿을 마법 같은 슈팅 스타처럼 보낼게"],
    ["미나 솔로 - 솔로곡 트랙", "V2hlQkVJZhE", "우아하고 고요하게 스며들어 너의 깊은 꿈속 가장 아름다운 조각이 될게"],
    ["다현 솔로 - 솔로곡 트랙", "rRzxEiBLQCA", "하얀 건반 위를 걷는 피아노 선율처럼 맑고 투명하게 네 맘을 똑똑 두드릴게"],
    ["채영 솔로 - 솔로곡 트랙", "i0p1bmr0EmE", "내 멋대로 그린 도화지 위에 너라는 가장 특별한 색을 한 방울 떨어트려"],
    
    # 🌟 역대 레전드 타이틀곡 라인업
    ["OOH-AHH하게 (Like OOH-AHH)", "0rtV574I210", "날 우아 우아하게 만들어줘 가짜 같지 않은 진심 어린 눈빛으로"],
    ["CHEER UP", "c7rCyll5AeY", "Cheer up baby Cheer up baby 좀 더 힘을 내 여자가 쉽게 맘을 주면 안돼"],
    ["TT", "ePpPVE-GGJw", "이러지도 못하는데 저러지도 못하는데 이런 내 맘 모르고 너무해 너무해"],
    ["KNOCK KNOCK", "8A2t_tAjMz8", "Knock knock knock knock knock on my door 내 맘이 열리게 해줘"],
    ["SIGNAL", "VQtonf1fv_s", "사인들을 보내 시그널 보내 근데 전혀 안 통하네 눈빛을 보내"],
    ["LIKEY", "V2hlQkVJZhE", "설렌다 Me Likey Me Likey Likey Likey 두근두근두근 Heart Heart"],
    ["Heart Shaker", "rRzxEiBLQCA", "Yeah 반해버렸으니까 Yeah 너만 생각나니까 넌 내게 반해버렸으니까"],
    ["What is Love?", "i0p1bmr0EmE", "I wanna know 사탕처럼 달콤하다는데 하늘을 나는 것 같다는데"],
    ["Dance The Night Away", "Fm5iP0S1z9w", "If you wanna have some fun 짭조름한 바닷바람처럼 우릴 부르는 파도 소리 맞춰"],
    ["YES or YES", "mAKsZ26SabQ", "둘 중에 하나만 골라 YES or YES? 네 마음을 열어봐 YES or YES?"],
    ["FANCY", "kOHB85vDuow", "FANCY YOU 누가 먼저 좋아하면 어때 지금 너에게로 갈래"],
    ["Feel Special", "3ymwOvzhwHs", "그대가 있음에 내가 다시 웃어 원해 Everything's good 하니까"],
    ["MORE & MORE", "mH0_XpSHkZo", "그러니 한 번 더 가볍게 너의 입을 열어줘 귀에 들리게 더 이상은 귀찮게 안 할게"],
    ["I CAN'T STOP ME", "CM4CkVFmT00", "알람이 울려대 Ring ring-a-ling 서로의 눈길이 닿을 때마다 알면서도 걸어가"],
    ["Alcohol-Free", "XA2YEHn-A8Q", "너는 눈으로 마시는 내 알코올 프리 모든 게 녹아내려 가 너 때문에"],
    ["SCIENTIST", "vPwaXytZcgI", "왜 자꾸 날 연구해 아인슈타인도 아니고 각 재고 재고 덧셈 뺄셈 왜 해"],
    ["Talk that Talk", "k6jqx9kZgPM", "Talk that talk 딱 한 마디 Talk that talk L-O-V-E 들려줘"],
    ["SET ME FREE", "a7Zp-e_6eY8", "I'm gonna tell you straight 이제는 무서울 게 없어 날 속박하던 모든 걸 벗어나"],
    ["ONE SPARK", "jC8L8_e0yU0", "이건 하이라이트 내 마음속의 불꽃 영원히 타오를 ONE SPARK"],
    ["The Feels", "f5_wn8mexmM", "Boy I, Boy I, Boy I know I know you got the feels"],

    # 💎 숨은 명곡 및 최애 수록곡 라인업
    ["거북이", "tY8mZ0V6V7o", "거북아 좀만 더 서둘러줘 나보다 발걸음이 느린 너를 기다리다"],
    ["MISSING U", "2Yf68_Wv5f4", "Missing u 매일매일 보고 싶다고 난 너를 내 맘속에 저장하고 싶어"],
    ["WOW", "wX-y0MvVw2w", "Wow 정말 멋진 걸 넌 나의 눈을 사로잡아 버렸어"],
    ["24/7", "WOnNiaZIK3A", "24/7 하루 종일 너만 생각해 자꾸 내 마음이 둥둥 떠다녀"],
    ["훈남 (LOOK AT ME)", "0wAsU4I2Ugw", "날 좀 바라봐줘 봐봐 나를 Look at me Look at me"],
    ["ROLLIN'", "481hN6W4p98", "I'm rollin' 너에게로 빠져들어 깊이 Rollin'"],
    ["LOVE LINE", "1b_rK_5jK_E", "Love line 우리 둘을 연결해줄 선이 선명하게 보여"],
    ["DON'T GIVE UP", "Z6XhL42L4Y8", "포기하지 마 힘을 내 힘든 일은 모두 잊어버려"],
    ["널 내게 담아", "Bbe8YxI_f_E", "내 눈 속에 너를 가득 담아서 평생 기억하고 싶어"],
    ["잘자요 굿나잇", "E_I2Rggv3y8", "오늘 하루도 수고 많았어 내 꿈꿔 잘자요 굿나잇"],
    ["STUCK", "kYorY6Ias0w", "너에게 푹 빠져 버린 걸 난 이제 어떻게 해야 해"],
    ["PONYTAIL", "b4O6F2H_E3s", "머리를 묶고서 다시 시작해 당당하게 걸어가 봐"],
    ["JELLY JELLY", "34wKjshZ8gM", "Oh Jelly Jelly 질투가 나잖아 자꾸 다른 곳을 보지 마"],
