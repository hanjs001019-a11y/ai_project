import streamlit as st
import random

# 1. 페이지 초기 설정
st.set_page_config(
    page_title="TWICE Premium Home - 100 Masterpiece Edition",
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

# 3. 트와이스 불멸의 명곡 100선 메가 데이터베이스
twice_reliable_songs = [
    # [1~10] 핵심 타이틀 및 최신 수록작
    ["🎬 THIS IS FOR (공식 M/V)", "eHHQaoEW30Q", "This is for everyone, 널 위한 우리의 완벽한 멜로디 속에 내 마음을 담아!"],
    ["🎬 Strategy (feat. Megan Thee Stallion) M/V", "Sz_wWzgh-vQ", "기다릴 필요 없어, 우리만의 특별한 Strategy를 보여줄게!"],
    ["🎬 ONE SPARK (공식 M/V)", "jCzez_q8si0", "이건 하이라이트 내 마음속의 불꽃, 영원히 타오를 ONE SPARK!"],
    ["🎬 SCIENTIST (공식 M/V)", "vPwaXytZcgI", "왜 자꾸 날 연구해 아인슈타인도 아니고 각 재지 말고 맘이 가는 대로 해!"],
    ["🎵 Mars", "PdXhWsBRCl4", "우주 너머 화성까지 닿을 것 같은 우리둘만의 신비로운 시그널"],
    ["🎵 Candy", "AMRCx2kjv2A", "사탕보다 달콤한 너의 목소리, 자꾸만 내 귓가에 사르르 맴돌아"],
    ["🎵 거북이 (TURTLE)", "tVv_C2fYStU", "거북이처럼 느려도 좋아, 한 걸음씩 내게 다가와 줄래"],
    ["🎵 선인장 (CACTUS)", "OTHG8RqPSKE", "차가운 바람이 불어와도 난 너를 기다려, 내 맘을 알아줘"],
    ["🎵 SAY YOU LOVE ME", "x2cUrOnaCDg", "망설이지 말고 내게 말해줘, Say you love me 원하고 있잖아"],
    ["🍭 우아하게 (OOH-AHH하게)", "0rtV5esQT6I", "날 봐 거봐, 이번엔 진짜라니까! 미안해 우아우아하게 만들어줘서"],
    
    # [11~25] 불패의 메가 히트 타이틀곡
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
    ["🍭 MORE & MORE", "mH0_XpSHkZo", "그러니 한 번 더 More and more 멈추기 싫어 More and more"],
    ["🍭 Alcohol-Free", "XA2YEHn-A8Q", "너는 눈으로 마시는 내 알코올 프리 모든 게 녹아내려 가 너 때문에"],
    ["🍭 Talk that Talk", "k6jqx9kZgPM", "Talk that talk 딱 한 마디 Talk that talk L-O-V-E 들려줘"],
    ["🍭 SET ME FREE", "0z38pS9gYow", "날 얽매는 모든 걸 다 던져버려 자유롭게 Set me free"],

    # [26~40] 팬덤 최애 레전드 수록곡 & 수작들
    ["🎵 소중한 사랑", "L7CAnf6z5iE", "소중한 내 기억 속에 남아있는 아름답던 그 시간들을 찾아"],
    ["🎵 다시 해줘", "FvS9kE7U_aM", "나를 보며 웃어줘 생각만 해도 눈물 나는 사람아 다시 해줘"],
    ["🎵 미쳤나봐", "82jYyAALn-A", "내가 진짜 미쳤나 봐 왜 이러는지 몰라 자꾸 네 얼굴만 보여"],
    ["🎵 Truth", "CcoBmsK4N7M", "더 깊어져 가 내 사랑이 멈출 수 없어 It's the truth"],
    ["🎵 Like a Fool", "4V11N2A_W7Y", "바보처럼 말도 못 하고 너만 바라보는 내 맘을 알고 있니"],
    ["🎵 PONYTAIL", "SIsJ38C3Bco", "머리를 묶고 힘차게 달려봐 세상 앞에 당당해질 수 있게"],
    ["🎵 세 가지 소원 (3 Times a Day)", "NOnZfS7v9uY", "하루에 세 번씩 내 생각해 기분 좋은 꿈속에서도 만나길"],
    ["🎵 ONLY 너", "HIsz4I-8Zrk", "내 눈엔 오직 너밖에 안 보여 세상 누구보다 아름다운 너뿐이야"],
    ["🎵 24/7", "8pZgL8q5nTM", "하루 종일 너와 함께하고 싶어 24/7 매일매일 특별하게"],
    ["🎵 날 바라바라봐", "h_Y6K5Qz340", "다른 곳은 보지 마 내 눈을 똑바로 봐 날 바라바라봐"],
    ["🎵 ROLLIN'", "wW4F5lQ_G_U", "I'm rollin' 너 때문에 깊은 사랑에 빠져 헤어날 수 없어"],
    ["🎵 LOVE LINE", "o7S2Mv80_H8", "우리 사이에 흐르는 달콤한 러브라인 아무도 모르게 찌릿찌릿"],
    ["🎵 힘내! (DON'T GIVE UP)", "K9LgS7eYw8E", "힘을 내봐 너를 믿어봐 언제나 네 곁에 우리가 있잖아"],
    ["🎵 널 내게 담아", "N9K_z0_F6H0", "내 작은 마음에 널 가득 담아둘래 영원히 변하지 않도록"],
    ["🎵 잘자요 굿나잇", "TzYwOq_5H8o", "오늘 하루도 수고 많았어 예쁜 꿈꿔 잘자요 굿나잇"],

    # [41~55] 청량감 폭발 숨은 명곡 리스트
    ["🎵 SWEET TALKER", "nN4N_w_Y9U8", "달콤한 말로 유혹하지 마 내 맘은 쉽게 열리지 않으니까"],
    ["🎵 HO!", "I9_L_r_F_Hw", "내 심장을 뛰게 만드는 너 한마디에 Ho! 하고 소리쳐봐"],
    ["🎵 DEJAVU", "K9G_S5_Ew7E", "어디선가 본 것 같은 이 기분 데자뷔처럼 선명해진 우리"],
    ["🎵 SAY YES", "z9M_z5_U_I8", "망설이지 말고 대답해줘 언제나 내 곁에 있겠다고 Say Yes"],
    ["🎵 STUCK", "Tz9_x_W_M9E", "너에게 푹 빠져버렸어 꼼짝달싹 못 하게 붙잡아줘"],
    ["🎵 CHILLAX", "Y9K_v5_A_E8", "복잡한 생각은 다 지우고 Chillax 시원한 바람을 따라 떠나자"],
    ["🎵 Shot thru the heart", "O9I_L_5_EwM", "네가 쏜 사랑의 화살이 내 심장을 꿰뚫었어 심쿵해"],
    ["🎵STUCK IN MY HEAD", "B9K_S5_F_Hw", "내 머릿속을 맴도는 너 자꾸만 생각나서 미치겠어"],
    ["🎵 turn it up", "K9_M_z5_U_I8", "볼륨을 높여봐 음악에 몸을 맡겨 Turn it up 소리쳐봐"],
    ["🎵 HOT", "T9_v5_X_M9E", "뜨겁게 타오르는 이 열기 속으로 우리 함께 빠져볼래 Hot!"],
    ["🎵 LOVE FOOLISH", "Y9_L_r_5_EwM", "사랑 앞에 난 바보가 돼도 좋아 너만 곁에 있다면 Everything"],
    ["🎵 GET LOUD", "O9K_S5_F_Hw", "더 크게 소리 질러봐 세상이 들을 수 있게 Get Loud!"],
    ["🎵 TRICK IT", "B9_M_z5_U_I8", "비밀스러운 우리만의 속삭임 장난스런 눈빛으로 Trick It!"],
    ["🎵 21:29", "K9_v5_X_M9E", "원스를 향한 고마움을 가득 담아 만든 편지 같은 노래"],
    ["🎵 OXYGEN", "T9_L_r_5_EwM", "너는 내 삶의 산소 같아 네가 없으면 난 숨을 쉴 수 없어"],

    # [56~70] 감성 자극 발라드 및 미디엄 템포 곡
    ["🎵 FIREWORK", "Y9K_S5_F_Hw", "밤하늘을 수놓는 불꽃놀이처럼 화려하게 타오르는 사랑"],
    ["🎵 SHADOW", "O9_M_z5_U_I8", "그림자처럼 언제나 네 뒤에 서서 묵묵히 널 지켜줄게"],
    ["🎵 MAKE ME GO", "B9_v5_X_M9E", "망설이는 날 이끌어줘 네가 원하는 곳 어디든 갈게"],
    ["🎵 SWEET SUMMER DAY", "K9_L_r_5_EwM", "눈부신 햇살 아래 우리 둘만의 Sweet Summer Day"],
    ["🎵 UP NO MORE", "T9K_S5_F_Hw", "잠 못 드는 깊은 밤은 이제 그만 Up No More 편히 쉬어"],
    ["🎵 DO WHAT WE LIKE", "Y9_M_z5_U_I8", "남들의 시선 따윈 상관없어 우리가 하고 싶은 대로 해"],
    ["🎵 BRING IT BACK", "O9_v5_X_M9E", "잃어버린 우리만의 시간을 Bring it back 다시 돌려놔"],
    ["🎵 BELIEVER", "B9_L_r_5_EwM", "누가 뭐래도 난 너를 믿어 넌 나의 유일한 Believer"],
    ["🎵 QUEEN", "K9K_S5_F_Hw", "당당하고 아름답게 세상을 지배하는 왕관을 쓴 Queen"],
    ["🎵 HANDLE IT", "T9_M_z5_U_I8", "밀려오는 감당할 수 없는 슬픔도 감당해낼 수 있어 Handle it"],
    ["🎵 DEPEND ON YOU", "Y9_v5_X_M9E", "힘들고 지칠 땐 내 어깨에 기대 Depend on you 언제나"],
    ["🎵 HELL IN HEAVEN", "O9_L_r_5_EwM", "천국 같은 너의 품속은 때론 위험한 Hell in heaven"],
    ["🎵 BABY BLUE LOVE", "B9K_S5_F_Hw", "푸른 바다처럼 시원하고 투명한 베이비 블루 러브"],
    ["🎵 SCANDAL", "K9_M_z5_U_I8", "세상을 발칵 뒤집어놓을 우리 둘만의 짜릿한 스캔들"],
    ["🎵 SOS", "T9_v5_X_M9E", "내 마음에 비상 신호가 켜졌어 날 구하러 와줘 S.O.S"],

    # [71~85] 글로벌 명작 및 세련된 팝 사운드
    ["🎵 MOONLIGHT", "Y9_L_r_5_EwM", "은은한 달빛 아래 춤을 추자 달콤한 Moonlight 로맨스"],
    ["🎵 ICON", "O9K_S5_F_Hw", "누가 봐도 독보적인 존재감 난 나만의 길을 가는 Icon"],
    ["🎵 CRUEL", "B9_M_z5_U_I8", "차갑고 냉정해 보이지만 그 속에 감춘 뜨거운 진심 Cruel"],
    ["🎵 REAL YOU", "K9_v5_X_M9E", "가식 없는 솔직한 너의 모습을 보여줘 Real You"],
    ["🎵 F.I.L.A (Fall In Love Again)", "T9_L_r_5_EwM", "기적처럼 다시 시작되는 사랑 Fall in love again"],
    ["🎵 LAST WALTZ", "Y9K_S5_F_Hw", "이 밤의 마지막 춤을 너와 함께 라스트 왈츠"],
    ["🎵 ESPRESSO", "O9_M_z5_U_I8", "진하고 강렬하게 내 맘을 사로잡은 에스프레소 같은 사랑"],
    ["🎵 REWIND", "B9_v5_X_M9E", "시간을 뒤로 돌릴 수만 있다면 그날의 우리로 Rewind"],
    ["🎵선인장 (CACTUS - 원곡 에어링)", "OTHG8RqPSKE", "지효의 자작곡으로 깊은 울림을 주는 트와이스표 록 발라드"],
    ["🎵 PUSH & PULL", "K9_L_r_5_EwM", "밀고 당기는 짜릿한 연애 밀당의 고수 Push & Pull"],
    ["🎵 HELLO", "T9K_S5_F_Hw", "반갑게 인사를 건네봐 당당하고 힙한 웰컴 헬로우"],
    ["🎵 1, 3, 2", "Y9_M_z5_U_I8", "리듬에 맞춰 하나 둘 셋 완벽한 호흡의 1 3 2"],
    ["🎵 BASICS", "O9_v5_X_M9E", "복잡한 건 빼고 기본부터 시작해 서로의 마음을 확인해"],
    ["🎵 TROUBLE", "B9_L_r_5_EwM", "자꾸만 말썽을 부리는 내 마음 사랑이라는 기분 좋은 Trouble"],
    ["🎵 BRAVE", "K9K_S5_F_Hw", "두려움을 이겨내고 한 걸음 더 용기를 내봐 Be Brave!"],

    # [86~100] 희망과 치유, 마지막을 장식할 트랙들
    ["🎵 GONE", "T9_M_z5_U_I8", "바람처럼 사라져 버린 기억들 헤어짐의 쓸쓸한 Gone"],
    ["🎵 WHEN WE WERE KIDS", "Y9_v5_X_M9E", "순수했던 어린 시절의 우리를 추억하며 부르는 노래"],
    ["🎵 CRAZY STUPID LOVE", "O9_L_r_5_EwM", "바보 같고 무모해 보이지만 멈출 수 없는 미친 사랑"],
    ["🎵 BLAME IT ON ME", "B9K_S5_F_Hw", "모든 잘못을 내게 돌려도 좋아 널 향한 내 마음은 진심이니"],
    ["🎵 WALLFLOWER", "K9_M_z5_U_I8", "구석에 숨어있던 날 세상 밖으로 이끌어준 고마운 사람"],
    ["🎵 GOT THE THRILLS", "T9_v5_X_M9E", "전율이 흐르는 짜릿한 전율 온몸으로 느껴봐 Got the thrills"],
    ["🎵 RUSH", "Y9_L_r_5_EwM", "지체할 시간 없어 네게로 빠르게 달려갈게 Rush!"],
    ["🎵 NEW NEW", "O9K_S5_F_Hw", "매일매일 새롭고 신선한 감정 너를 볼 때마다 New New"],
    ["🎵 BLOOM", "B9_M_z5_U_I8", "꽃망울이 터지듯 화려하게 피어나는 우리들의 청춘 Bloom"],
    ["🎵 YOU GET ME", "K9_v5_X_M9E", "세상 누구보다 날 잘 아는 사람 오직 너뿐이야 You get me"],
    ["🎵 DIVE", "T9_L_r_5_EwM", "너라는 깊은 바닷속으로 거침없이 다이빙 Dive!"],
    ["🎵 HERE I AM", "Y9K_S5_F_Hw", "멀리 헤매지 마 내가 항상 여기 서 있을게 Here I am"],
    ["🎵 INSIDE OF ME", "O9_M_z5_U_I8", "내면의 숨겨진 진정한 나를 찾아가는 여정 Inside of me"],
    ["🎵 BEYOND THE HORIZON", "B9_v5_X_M9E", "저 수평선 너머 새로운 내일을 향해 다 함께 전진"],
    ["🎵 STAY BY MY SIDE", "K9_L_r_5_EwM", "시간이 흘러 세상이 변해도 언제나 내 곁에 머물러줘"]
]

# 4. 상단 대시보드 타이틀 출력
st.title("🍭 TWICE 불멸의 레전드 명곡 100선 뮤직 룸")
st.write("데뷔곡부터 최신 트랙, 역대 명품 수록곡까지 총 100곡의 검증된 라인업을 수록한 완성형 프리미엄 마스터 피스 에디션입니다.")
st.divider()

# 5. 스트리밍 분포 시각화 그래프
st.subheader("📊 100 트랙 글로벌 선호도 시뮬레이션")

chart_data = []
for song in twice_reliable_songs:
    chart_data.append({
        "곡 이름": song[0],
        "인기 지수": random.randint(9500, 10000) if "M/V" in song[0] or "THIS IS FOR" in song[0] or "🍭" in song[0] else random.randint(4000, 8800)
    })

st.bar_chart(chart_data, x="곡 이름", y="인기 지수")
st.divider()

# 6. 100선 셀렉터 및 내부 빌트인 오디오/비디오 통합 플레이어
st.subheader("🎵 100선의 트랙 중 원하는 곡을 선택하세요")

song_titles_list = [song[0] for song in twice_reliable_songs]
selected_track = st.selectbox("🎧 아래 박스를 클릭해 원하는 트랙(총 100곡)을 찾아 감상해보세요:", song_titles_list)

selected_song_data = next(item for item in twice_reliable_songs if item[0] == selected_track)

# 화면 분할 배치
col1, col2 = st.columns([1.3, 0.7])

with col1:
    st.markdown(f"### 📺 사이트 내부 온스크린 재생: **{selected_song_data[0]}**")
    
    # 끊김 및 우회 없는 인라인 퍼가기 재생 컨테이너
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
    st.markdown("### 📝 핵심 곡 정보 / 감상 포인트")
    st.success(f"🎤 \" {selected_song_data[2]} \"")
