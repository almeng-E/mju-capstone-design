import pandas as pd
import matplotlib.pyplot as plt
from route import file_path_video

# ------------------------------------------------------------------------------------------------------
# 1. 데이터 로드
# ------------------------------------------------------------------------------------------------------

# 데이터 로드
videos_data = pd.read_csv(file_path_video)

# 선택된 영상 ID
video_mju = 6526  # 명지대 선택 영상
video_compare = 7  # 비교 영상

# ------------------------------------------------------------------------------------------------------
# 2. 데이터 정리
# ------------------------------------------------------------------------------------------------------

# 선택된 영상들의 데이터 추출
video_mju_data = videos_data[videos_data['id'] == video_mju].iloc[0]
video_compare_data = videos_data[videos_data['id'] == video_compare].iloc[0]

# ------------------------------------------------------------------------------------------------------
# 3. 시각화
# ------------------------------------------------------------------------------------------------------

# 그래프 기본 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 서브플롯 생성
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 6))
fig.suptitle('선택된 영상 지표 비교', fontsize=16, y=0.95)
plt.subplots_adjust(top=0.85)

# 시각화 스타일 설정
bar_colors = ['blue', 'orange']
bar_labels = ['명지대 영상', '비교 영상']
alpha_value = 0.3
edge_width = 1

# 1. 조회수 비교
ax1.bar(bar_labels, 
        [video_mju_data['view_count'], video_compare_data['view_count']], 
        color=bar_colors,
        alpha=alpha_value,
        edgecolor=bar_colors,
        linewidth=edge_width)
ax1.set_title('조회수 비교')
ax1.set_ylabel('조회수')

# 2. 좋아요 수 비교
ax2.bar(bar_labels, 
        [video_mju_data['like_count'], video_compare_data['like_count']], 
        color=bar_colors,
        alpha=alpha_value,
        edgecolor=bar_colors,
        linewidth=edge_width)
ax2.set_title('좋아요 수 비교')
ax2.set_ylabel('좋아요 수')

# 3. 댓글 수 비교
ax3.bar(bar_labels, 
        [video_mju_data['comment_count'], video_compare_data['comment_count']], 
        color=bar_colors,
        alpha=alpha_value,
        edgecolor=bar_colors,
        linewidth=edge_width)
ax3.set_title('댓글 수 비교')
ax3.set_ylabel('댓글 수')

plt.tight_layout()
plt.show()