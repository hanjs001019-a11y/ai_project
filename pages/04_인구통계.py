import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import urllib.request
import os

# --- 1. 스트림릿 클라우드 한글 폰트 설정 ---
@st.cache_data
def load_korean_font():
    # 현재 스크립트 파일이 있는 폴더 경로를 기준으로 설정
    current_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(current_dir, "NanumGothic-Regular.ttf")
    
    font_url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf"
    
    # 폰트 파일이 없으면 해당 폴더에 다운로드
    if not os.path.exists(font_path):
        urllib.request.urlretrieve(font_url, font_path)
    
    # 최신 Matplotlib 공식 메서드로 폰트 등록
    fm.fontManager.addfont(font_path)
    prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = prop.get_name()
    plt.rcParams['axes.unicode_minus'] = False # 마이너스 기호 깨짐 방지

# 폰트 로드 실행
load_korean_font()

# --- 2. 데이터 로드 및 경로 보안 ---
@st.cache_data
def load_data():
    # [핵심 수정] 현재 파이썬 파일이 실행되는 절대 경로를 구한 뒤, 그 옆에 있는 파일을 찾습니다.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "population.csv")
    
    # 혹시 상위 폴더(루트)에 있을 경우를 대비한 2차 탐색
    if not os.path.exists(file_path):
        parent_dir = os.path.dirname(current_dir)
        file_path = os.path.join(parent_dir, "population.csv")
        
    df = pd.read_csv(file_path, encoding="utf-8")
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"⚠️ 파일 로드 실패! 에러 메시지: {e}")
    st.info("💡 깃허브 저장소에 'population.csv' 파일이 이 파이썬 파일과 같은 폴더에 있는지 다시 한번 확인해 주세요.")
    st.stop()

# --- 3. UI 구성 및 데이터 필터링 ---
st.title("🗺️ 행정구역별 연령별 인구수 분석")
st.write("선택한 행정구역의 연령별 인구 분포를 무지개색 꺾은선 그래프로 확인하세요.")

# 행정구역 선택창
region_list = df['행정구역'].unique()
selected_region = st.selectbox("분석할 행정구역을 선택하세요:", region_list)

# 선택된 행정구역 데이터 필터링
region_data = df[df['행정구역'] == selected_region].iloc[0]

# '0세'부터 단일 연령 컬럼만 추출 (총인구수, 연령구간인구수 제외)
age_columns = [col for col in df.columns if '거주자_' in col and '총인구수' not in col and '연령구간인구수' not in col]

age_labels = []
age_values = []

for col in age_columns:
    # 컬럼명에서 나이 숫자 추출 (예: '2026년04월_거주자_0세' -> '0')
    age_str = col.split('_')[-1].replace('세', '')
    
    if '이상' in age_str:
        age_num = 100  # 100세 이상은 100으로 통일
    else:
        age_num = int(age_str)
        
    # 데이터 값 추출 및 콤마(,) 제거 후 정수 변환
    val_raw = str(region_data[col]).replace(',', '').strip()
    age_num_val = int(val_raw) if val_raw.isdigit() else 0
    
    age_labels.append(age_num)
    age_values.append(age_num_val)

# 시각화를 위한 데이터프레임 빌드 및 나이순 정렬
plot_df = pd.DataFrame({'나이': age_labels, '인구수': age_values})
plot_df = plot_df.sort_values('나이').reset_index(drop=True)

# --- 4. 무지개색 꺾은선 그래프 시각화 ---
fig, ax = plt.subplots(figsize=(12, 6))

num_points = len(plot_df)
cmap = plt.get_cmap('jet') # 화려한 무지개 패턴을 표현하는 컬러맵

# 1살 구간마다 색상을 다르게 주어 연결 (무지개 효과)
for i in range(num_points - 1):
    color = cmap(i / num_points)
    ax.plot(plot_df['나이'].iloc[i:i+2], plot_df['인구수'].iloc[i:i+2], color=color, linewidth=3)

# 그래프 레이아웃 설정
ax.set_title(f"[{selected_region}] 연령별 인구수 추이", fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel("나이 (세)", fontsize=12, labelpad=10)
ax.set_ylabel("인구수 (명)", fontsize=12, labelpad=10)

# 가로축 10살 단위로 구분선(Grid) 및 눈금 설정
max_age = plot_df['나이'].max()
ax.set_xticks(range(0, max_age + 1, 10))
ax.grid(True, which='both', axis='x', linestyle='--', linewidth=1, color='gray', alpha=0.5)
ax.grid(False, axis='y') # 깔끔한 뷰를 위해 가로 구분선만 강조

# 스트림릿 웹페이지에 렌더링
st.pyplot(fig)
