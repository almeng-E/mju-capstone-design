import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from route import file_path_video, file_path_channel

# ------------------------------------------------------------------------------------------------------
# 1. 데이터 로드
# ------------------------------------------------------------------------------------------------------

# 데이터 로드
videos_data = pd.read_csv(file_path_video)
channels_data = pd.read_csv(file_path_channel)

# 채널 ID-이름 매핑 생성
channel_names = dict(zip(channels_data['id'], channels_data['title']))

# ------------------------------------------------------------------------------------------------------
# 2. 데이터 정리
# ------------------------------------------------------------------------------------------------------

# 사용자 선택
channel_mju = 21      # 명지대 채널
channel_compare = 1   # 비교할 채널
selected_channels = [channel_mju, channel_compare]

# 선택된 영상 ID
video_mju = 6526     # 명지대 선택 영상
video_compare = 7     # 비교할 선택 영상

# 채널별 데이터 필터링
filtered_videos = videos_data[videos_data['channel_id'].isin(selected_channels)]
mju_videos = filtered_videos[filtered_videos['channel_id'] == channel_mju]['view_count'].dropna()
compare_videos = filtered_videos[filtered_videos['channel_id'] == channel_compare]['view_count'].dropna()

# 각 채널의 98퍼센타일 계산
mju_percentile_98 = np.percentile(mju_videos, 98)
compare_percentile_98 = np.percentile(compare_videos, 98)

# 98퍼센타일 이하 데이터만 필터링
mju_videos_filtered = mju_videos[mju_videos <= mju_percentile_98]
compare_videos_filtered = compare_videos[compare_videos <= compare_percentile_98]

# 선택된 영상들의 조회수 추출

video_mju_view = videos_data[videos_data['id'] == video_mju]['view_count'].values[0] if video_mju in videos_data['id'].values else None

video_compare_view = videos_data[videos_data['id'] == video_compare]['view_count'].values[0] if video_compare in videos_data['id'].values else None

# 시각화 : 히스토그램 + 하이라이트
plt.figure(figsize=(12, 6))

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 히스토그램 생성 (필터링된 데이터)
plt.hist(mju_videos_filtered, bins=30, 
         alpha=0.3,                    # 투명도
         color='blue',                 # 채우기 색상
         edgecolor='blue',            # 테두리 색상
         linewidth=1,                 # 테두리 두께
         label=f'명지대학교 동영상')

plt.hist(compare_videos_filtered, bins=30, 
         alpha=0.4,                    # 투명도
         color='orange',               # 채우기 색상
         edgecolor='orange',          # 테두리 색상
         linewidth=1,                 # 테두리 두께
         label=f'선택된 채널 동영상')

# 선택된 영상들 하이라이트 (상위 2% 제외)

if video_mju_view and video_mju_view <= mju_percentile_98:
    plt.axvline(
        video_mju_view, 
        color='blue', 
        linestyle='--', 
        linewidth=2, 
        label=f'MJU 동영상: {video_mju_view:,} views'
        )

if video_compare_view and video_compare_view <= compare_percentile_98:
    plt.axvline(
        video_compare_view, 
        color='orange', 
        linestyle='--', 
        linewidth=2, 
        label=f'선택된 동영상: {video_compare_view:,} views'
        )

plt.title('채널 별 조회수 분포와 선택된 동영상 위치')
plt.xlabel('조회수')
plt.ylabel('동영상 개수')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# 필터링된 데이터 정보 출력

print(f"\nMJU Channel Statistics (excluding top 2%):")
print(f"Videos included: {len(mju_videos_filtered)} out of {len(mju_videos)}")
print(f"98 % : {mju_percentile_98:,.0f} views")
print(f"\nCompare Channel Statistics (excluding top 2%):")
print(f"Videos included: {len(compare_videos_filtered)} out of {len(compare_videos)}")
print(f"98 % : {compare_percentile_98:,.0f} views")