import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import urllib.request
import os

# --- 1. 스트림릿 클라우드 한글 폰트 설정 ---
@st.cache_data
def load_korean_font():
    font_url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf"
    font_path = "NanumGothic-Regular.ttf"
    
    # 폰트 파일이 없으면 다운로드
    if not os.path.exists(font_path):
        urllib.request.urlretrieve(font_url, font_path)
    
    # Matplotlib에 폰트 등록
    fe = fm.FontEntry(fname=font_path, name='NanumGothic')
    fm.font_manager.ttflist.insert(0, fe)
    plt.rcParams['font.family'] = 'NanumGothic'
    plt.rcParams['axes.unicode_minus'] = False # 마이너스 기호 깨짐 방지

# 폰트 로드 실행
load_korean_font()

# --- 2. 데이터 로드 및 전처리 ---
@st.cache_data
def load_data():
    # 업로드된 population.csv 파일을 읽어옵니다.
    df = pd.read_csv("population.csv", encoding="utf-8")
    return df

try:
    df = load_data()
except Exception as e:
    st.error("`population.csv` 파일을 찾을 수 없거나 불러오는데 실패했습니다. 파일이 코드와 같은 위치에 있는지 확인해주세요.")
    st.stop()

# --- 3. UI 구성 ---
st.title("🗺️ 행정구역별 연령별 인구수 분석")
st.write("선택한 행정구역의 연령별 인구 분포를 무지개색 꺾은선 그래프로 확인하세요.")

# 행정구역 선택창 (첫 번째 컬럼 기준)
region_list = df['행정구역'].unique()
selected_region = st.selectbox("분석할 행정구역을 선택하세요:", region_list)

# 선택된 행정구역 데이터 필터링
region_data = df[df['행정구역'] == selected_region]

# '0세'부터 시작하는 연령 컬럼들만 추출
age_columns = [col for col in df.columns if '거주자_' in col and '총인구수' not in col and '연령구간인구수' not in col]

# 나이 숫자만 추출 (예: '2026년04월_거주자_0세' -> 0)
# '100세 이상'과 같은 예외 처리를 위해 숫자가 아닌 것은 처리
age_labels = []
age_values = []

for col in age_columns:
    age_str = col.split('_')[-1].replace('세', '')
    if '이상' in age_str:
        age_labels.append(100) # 100세 이상은 100으로 간주
    else:
        age_labels.append(int(age_str))
    
    # 데이터 값 추출 (콤마 제거 후 숫자로 변환)
    val = str(region_data[col].values[0]).replace(',', '')
    age_values = [int(val) if val.isdigit() else 0] + age_values # 순서대로 쌓기 위해 리스트 정렬 필요할 수 있음

# 데이터프레임으로 재구성 후 나이 순으로 정렬
plot_df = pd.DataFrame({'나이': age_labels, '인구수': [int(str(region_data[col].values[0]).replace(',', '')) for col in age_columns]})
plot_df = plot_df.sort_values('나이').reset_index(drop=True)

# --- 4. 무지개색 꺾은선 그래프 그리기 ---
fig, ax = plt.subplots(figsize=(12, 6))

# 1살 단위로 무지개 색상을 적용하기 위해 각 선분(segment)을 따로 그려줍니다.
num_points = len(plot_df)
cmap = plt.get_cmap('jet') # 무지개색을 표현하는 컬러맵 (jet 또는 rainbow)

for i in range(num_points - 1):
    # 각 구간마다 무지개 색상 비율 계산
    color = cmap(i / num_points)
    ax.plot(plot_df['나이'].iloc[i:i+2], plot_df['인구수'].iloc[i:i+2], color=color, linewidth=2.5)

# 그래프 서식 설정
ax.set_title(f"[{selected_region}] 연령별 인구수 추이", fontsize=16, fontweight='bold', pad=15)
ax.set_xlabel("나이 (세)", fontsize=12, labelpad=10)
ax.set_ylabel("인구수 (명)", fontsize=12, labelpad=10)

# 가로축 10살 단위 설정 및 주 격자선(Grid) 설정
ax.set_xticks(range(0, plot_df['나이'].max() + 1, 10))
ax.grid(True, which='both', axis='x', linestyle='--', linewidth=1, color='gray', alpha=0.7)
ax.grid(False, axis='y') # 세로축 그리드는 제외 (가로축 구분선 강조)

# 스트림릿에 그래프 출력
st.pyplot(fig)
