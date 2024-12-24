import pandas as pd
import matplotlib.pyplot as plt
from route import file_path_channel, selected_channels

# ------------------------------------------------------------------------------------------------------
# 1. 데이터 로드
# ------------------------------------------------------------------------------------------------------

# 채널 데이터 로드
channel_data = pd.read_csv(file_path_channel)

# ------------------------------------------------------------------------------------------------------
# 2. 데이터 정리
# ------------------------------------------------------------------------------------------------------

# 구독자 수 기준 정렬 및 순위 부여
ranked_channels = channel_data.sort_values(
    by='subscriber_count', 
    ascending=False
).reset_index(drop=True)
ranked_channels['rank'] = range(1, len(ranked_channels) + 1)

# 채널별 색상 및 범례 정보 초기화
bar_colors = ['gray'] * len(ranked_channels)
legend_items = []

# 명지대학교 채널 정보 처리
mju_channel = ranked_channels[ranked_channels['id'] == 21].iloc[0]
mju_index = ranked_channels[ranked_channels['id'] == 21].index[0]
bar_colors[mju_index] = 'blue'
legend_items.append({
    'color': 'blue',
    'label': f"{mju_channel['title']} ({mju_channel['rank']}위)"
})

# 선택된 채널들 정보 처리
for channel_id in selected_channels:
    if channel_id != 21:  # 명지대 제외
        channel_info = ranked_channels[ranked_channels['id'] == channel_id].iloc[0]
        channel_index = ranked_channels[ranked_channels['id'] == channel_id].index[0]
        bar_colors[channel_index] = 'pink'
        legend_items.append({
            'color': 'pink',
            'label': f"{channel_info['title']} ({channel_info['rank']}위)"
        })

# ------------------------------------------------------------------------------------------------------
# 3. 시각화
# ------------------------------------------------------------------------------------------------------

# 그래프 기본 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
plt.figure(figsize=(12, 8))

# 막대 그래프 생성
bars = plt.bar(ranked_channels['rank'], 
               ranked_channels['subscriber_count'], 
               color=bar_colors, 
               edgecolor='black')

# 범례 설정
legend_handles = [plt.Rectangle((0,0),1,1, color=item['color']) for item in legend_items]
legend_labels = [item['label'] for item in legend_items]
plt.legend(legend_handles, legend_labels,
          title='주요 채널 순위',
          loc='upper right',
          bbox_to_anchor=(1.15, 1))

# 그래프 스타일링
plt.title('채널별 구독자 수 순위')
plt.xlabel('순위')
plt.ylabel('구독자 수')
plt.xticks(ranked_channels['rank'], rotation=30, ha='right')

plt.tight_layout()
plt.show()
