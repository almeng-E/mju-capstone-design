import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from route import file_path_video

# ------------------------------------------------------------------------------------------------------
# 1. 데이터 로드
# ------------------------------------------------------------------------------------------------------

# 데이터 로드
videos_data = pd.read_csv(file_path_video)
view_counts = videos_data['view_count'].dropna()

# 선택된 영상 ID
video_mju = 6526  # 명지대 선택 영상
video_compare = 7  # 비교 영상

# ------------------------------------------------------------------------------------------------------
# 2. 데이터 정리
# ------------------------------------------------------------------------------------------------------

# 선택된 영상들의 백분위수 계산
video_mju_view = videos_data[videos_data['id'] == video_mju]['view_count'].values[0]
video_compare_view = videos_data[videos_data['id'] == video_compare]['view_count'].values[0]

mju_percentile = np.clip(stats.percentileofscore(view_counts, video_mju_view), 0.1, 99.9)
compare_percentile = np.clip(stats.percentileofscore(view_counts, video_compare_view), 0.1, 99.9)

# ------------------------------------------------------------------------------------------------------
# 3. 시각화
# ------------------------------------------------------------------------------------------------------

# 그래프 기본 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
plt.figure(figsize=(12, 4))

# 표준정규분포 곡선
x = np.linspace(-3, 3, 1000)
y = stats.norm.pdf(x, 0, 1)

# 선택된 영상들의 위치 계산
mju_x = stats.norm.ppf(mju_percentile/100)
compare_x = stats.norm.ppf(compare_percentile/100)

# 정규분포 곡선 그리기
plt.plot(x, y, 'k-', lw=2, label='조회수 분포')

# 영상 위치의 구간 채우기
plt.fill_between(x, y, where=(x <= mju_x), color='blue', alpha=0.3, 
                label=f'명지대 영상 (상위 {100-mju_percentile:.1f}%)')
plt.fill_between(x, y, where=(x <= compare_x), color='orange', alpha=0.3, 
                label=f'비교 영상 (상위 {100-compare_percentile:.1f}%)')

# 백분위수 표시
plt.text(mju_x, y.max()/4, f'상위\n{100-mju_percentile:.1f}%', 
         color='blue', ha='center', va='center')
plt.text(compare_x, y.max()/4, f'상위\n{100-compare_percentile:.1f}%', 
         color='orange', ha='center', va='center')

# 범례 및 축 설정
plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1))
percentiles = range(0, 101, 10)
x_ticks = [stats.norm.ppf(p/100) if 0 < p < 100 else (-3 if p == 0 else 3) for p in percentiles]
x_labels = [f'{p}%' if p == 50 else '' for p in percentiles]
plt.xticks(x_ticks, x_labels)
plt.gca().set_yticks([])
plt.grid(True, axis='x', alpha=0.2)

# 그래프 마무리
plt.title('전체 영상 중 선택된 영상들의 조회수 위치')
plt.tight_layout()
plt.show()

# 상세 정보 출력
print(f"\n명지대 영상 (ID: {video_mju})")
print(f"조회수: {video_mju_view:,}")
print(f"상위: {100-mju_percentile:.1f}%")

print(f"\n비교 영상 (ID: {video_compare})")
print(f"조회수: {video_compare_view:,}")
print(f"상위: {100-compare_percentile:.1f}%")