
\import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import urllib.request
import os

# --- 1. 스트림릿 클라우드 한글 폰트 설정 ---
@st.cache_data
def load_korean_font():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(current_dir, "NanumGothic-Regular.ttf")
    font_url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf"
    
    if not os.path.exists(font_path):
        urllib.request.urlretrieve(font_url, font_path)
    
    fm.fontManager.addfont(font_path)
    prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = prop.get_name()
    plt.rcParams['axes.unicode_minus'] = False

# 폰트 로드 실행
load_korean_font()

# --- 2. [강력화된] 전체 프로젝트 내 파일 자동 탐색 로직 ---
@st.cache_data
def find_and_load_data(target_filename="population.csv"):
    # 1단계: 현재 파일 위치 기준 탐색
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2단계: 최상위 프로젝트 폴더(작업 디렉토리) 기준으로 확장 탐색
    # 스트림릿 클라우드의 기본 배포 루트인 /mount/src/ 안의 모든 곳을 뒤집니다.
    search_root = "/mount/src" if os.path.exists("/mount/src") else current_dir
    
    for root, dirs, files in os.walk(search_root):
        if target_filename in files:
            full_path = os.path.join(root, target_filename)
            # 파일을 찾으면 즉시 데이터프레임으로 로드 후 반환
            df = pd.read_csv(full_path, encoding="utf-8")
            return df, full_path

    # 만약 위의 자동 탐색으로도 못 찾았다면 3단계 기본 로드 시도
    df = pd.read_csv(target_filename, encoding="utf-8")
    return df, target_filename

try:
    df, absolute_path = find_and_load_data()
    # 파일이 어디서 발견되었는지 관리자 메시지 형태로 출력 (성공 확인용)
    st.success(f"✅ 파일을 성공적으로 찾았습니다! (위치: {absolute_path})")
except Exception as e:
    st.error(f"⚠️ 시스템 전체에서 'population.csv' 파일을 검색했으나 찾지 못했습니다.")
    st.info("💡 깃허브(GitHub) 저장소에 올리신 파일명이 정확히 소문자 `population.csv` 인지 다시 한 번 확인해 주세요. 대소문자가 다르면 리눅스 서버에서 인식하지 못할 수 있습니다.")
    st.stop()

# --- 3. UI 구성 및 데이터 필터링 ---
st.title("🗺️ 행정구역별 연령별 인구수 분석")
st.write("선택한 행정구역의 연령별 인구 분포를 무지개색 꺾은선 그래프로 확인하세요.")

# 행정구역 선택창
region_list = df['행정구역'].unique()
selected_region = st.selectbox("분석할 행정구역을 선택하세요:", region_list)

# 선택된 행정구역 데이터 필터링
region_data = df[df['행정구역'] == selected_region].iloc[0]

# '0세'부터 단일 연령 컬럼만 추출
age_columns = [col for col in df.columns if '거주자_' in col and '총인구수' not in col and '연령구간인구수' not in col]

age_labels = []
age_values = []

for col in age_columns:
    age_str = col.split('_')[-1].replace('세', '')
    
    if '이상' in age_str:
        age_num = 100
    else:
        age_num = int(age_str)
        
    val_raw = str(region_data[col]).replace(',', '').strip()
    age_num_val = int(val_raw) if val_raw.isdigit() else 0
    
    age_labels.append(age_num)
    age_values.append(age_num_val)

# 데이터프레임 빌드 및 정렬
plot_df = pd.DataFrame({'나이': age_labels, '인구수': age_values})
plot_df = plot_df.sort_values('나이').reset_index(drop=True)

# --- 4. 무지개색 꺾은선 그래프 시각화 ---
fig, ax = plt.subplots(figsize=(12, 6))
num_points = len(plot_df)
cmap = plt.get_cmap('jet')

for i in range(num_points - 1):
    color = cmap(i / num_points)
    ax.plot(plot_df['나이'].iloc[i:i+2], plot_df['인구수'].iloc[i:i+2], color=color, linewidth=3)

ax.set_title(f"[{selected_region}] 연령별 인구수 추이", fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel("나이 (세)", fontsize=12, labelpad=10)
ax.set_ylabel("인구수 (명)", fontsize=12, labelpad=10)

max_age = plot_df['나이'].max()
ax.set_xticks(range(0, max_age + 1, 10))
ax.grid(True, which='both', axis='x', linestyle='--', linewidth=1, color='gray', alpha=0.5)
ax.grid(False, axis='y')

st.pyplot(fig)
