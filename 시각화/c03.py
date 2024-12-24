import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from route import file_path_video, file_path_channel

# ------------------------------------------------------------------------------------------------------
# 1. 데이터 로드
# ------------------------------------------------------------------------------------------------------

# 데이터 로드
videos_data = pd.read_csv(file_path_video)
channels_data = pd.read_csv(file_path_channel)

# ------------------------------------------------------------------------------------------------------
# 2. 데이터 정리
# ------------------------------------------------------------------------------------------------------

# 채널별 지표 집계
channel_metrics = videos_data.groupby('channel_id').agg({
    'view_count': 'sum',
    'comment_count': 'sum'
}).reset_index()

# 순위 계산
channel_metrics['view_rank'] = channel_metrics['view_count'].rank(ascending=False)
channel_metrics['comment_rank'] = channel_metrics['comment_count'].rank(ascending=False)

# 명지대학교 채널 정보 추출
mju_metrics = channel_metrics[channel_metrics['channel_id'] == 21].iloc[0]
total_channels = len(channel_metrics)

# ------------------------------------------------------------------------------------------------------
# 3. 시각화
# ------------------------------------------------------------------------------------------------------

# 그래프 기본 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 2x2 서브플롯 생성
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle('명지대학교 채널 현황', fontsize=16, y=1.05)

# 테두리 스타일 설정
border_props = dict(boxstyle='round,pad=0.5', 
                   facecolor='white', 
                   edgecolor='gray', 
                   linewidth=2)

# 조회수 순위 카드
ax1.add_patch(patches.Rectangle((0.1, 0.1), 0.8, 0.8, fill=False, 
              edgecolor='gray', linewidth=2))
ax1.text(0.5, 0.5, f"{mju_metrics['view_rank']:.0f}위", 
         ha='center', va='center', fontsize=40, bbox=border_props)
ax1.text(0.5, 0.8, '조회수 순위', ha='center', va='center', fontsize=12)
ax1.text(0.5, 0.2, f'전체 {total_channels}개 채널 중', ha='center', va='center', fontsize=10)
ax1.axis('off')

# 댓글수 순위 카드
ax2.add_patch(patches.Rectangle((0.1, 0.1), 0.8, 0.8, fill=False, 
              edgecolor='gray', linewidth=2))
ax2.text(0.5, 0.5, f"{mju_metrics['comment_rank']:.0f}위", 
         ha='center', va='center', fontsize=40, bbox=border_props)
ax2.text(0.5, 0.8, '댓글수 순위', ha='center', va='center', fontsize=12)
ax2.text(0.5, 0.2, f'전체 {total_channels}개 채널 중', ha='center', va='center', fontsize=10)
ax2.axis('off')

# 총 조회수 카드
ax3.add_patch(patches.Rectangle((0.1, 0.1), 0.8, 0.8, fill=False, 
              edgecolor='gray', linewidth=2))
ax3.text(0.5, 0.5, f"{mju_metrics['view_count']:,.0f}", 
         ha='center', va='center', fontsize=20, bbox=border_props)
ax3.text(0.5, 0.8, '총 조회수', ha='center', va='center', fontsize=12)
ax3.axis('off')

# 총 댓글수 카드
ax4.add_patch(patches.Rectangle((0.1, 0.1), 0.8, 0.8, fill=False, 
              edgecolor='gray', linewidth=2))
ax4.text(0.5, 0.5, f"{mju_metrics['comment_count']:,.0f}", 
         ha='center', va='center', fontsize=20, bbox=border_props)
ax4.text(0.5, 0.8, '총 댓글수', ha='center', va='center', fontsize=12)
ax4.axis('off')

plt.tight_layout()
plt.show()

# 상세 정보 출력
print("\n명지대학교 채널 상세 현황:")
print(f"조회수 순위: {mju_metrics['view_rank']:.0f}위 / {total_channels}개 채널")
print(f"댓글수 순위: {mju_metrics['comment_rank']:.0f}위 / {total_channels}개 채널")
print(f"총 조회수: {mju_metrics['view_count']:,.0f}")
print(f"총 댓글수: {mju_metrics['comment_count']:,.0f}")