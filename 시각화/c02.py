import pandas as pd
import matplotlib.pyplot as plt
from math import pi
from route import file_path_video, file_path_channel, selected_channels

# ------------------------------------------------------------------------------------------------------
# 1. 데이터 로드
# ------------------------------------------------------------------------------------------------------

# 데이터 로드
videos_data = pd.read_csv(file_path_video)
channels_data = pd.read_csv(file_path_channel)

# 채널 ID-이름 매핑 생성
channel_names = dict(zip(channels_data['id'], channels_data['title']))

# 선택된 채널 데이터 필터링
filtered_data = videos_data[videos_data['channel_id'].isin(selected_channels)]

# ------------------------------------------------------------------------------------------------------
# 2. 데이터 정리
# ------------------------------------------------------------------------------------------------------

# 채널별 지표 집계
metrics = ['like_count', 'comment_count', 'view_count']
metrics_korean = ['좋아요 수', '댓글 수', '조회 수']

channel_metrics = filtered_data.groupby('channel_id').agg({
    'like_count': 'sum',
    'comment_count': 'sum',
    'view_count': 'sum'
}).reset_index()

# 명지대학교(채널 21) 기준 정규화
mju_metrics = channel_metrics[channel_metrics['channel_id'] == 21][metrics].iloc[0]
normalized_metrics = channel_metrics[metrics].div(mju_metrics)

# ------------------------------------------------------------------------------------------------------
# 3. 시각화
# ------------------------------------------------------------------------------------------------------

# 그래프 기본 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
plt.figure(figsize=(8, 6))

# 레이더 차트 각도 계산
N = len(metrics)
angles = [n / float(N) * 2 * pi for n in range(N)] + [0]

# 채널별 레이더 차트 그리기
for i, row in normalized_metrics.iterrows():
    values = row.tolist() + [row[0]]  # Close the loop
    channel_id = channel_metrics.loc[i, 'channel_id']
    color = 'blue' if channel_id == 21 else 'orange'
    plt.polar(angles, values, label=channel_names[channel_id], color=color)

# 그래프 스타일링
plt.xticks(angles[:-1], metrics_korean)
plt.title('채널별 상호작용 비교 (명지대학교 기준)')
plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

plt.tight_layout()
plt.show()
