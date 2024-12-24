import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import textwrap
from route import file_path_video

# 데이터 로드 및 영상 선택 
videos_data = pd.read_csv(file_path_video)
video_mju = 6526
video_compare = 7

# ------------------------------------------------------------------------------------------------------

# 선택된 영상 데이터 추출
video_mju_data = videos_data[videos_data['id'] == video_mju].iloc[0]
video_compare_data = videos_data[videos_data['id'] == video_compare].iloc[0]




# 시각화 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 카드 생성
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
fig.suptitle('영상 요약본 비교', fontsize=16, y=0.95)

# 텍스트 래핑 함수 정의
def wrap_text(text, width=40):
    return '\n'.join(textwrap.wrap(text, width=width))

# 테두리 스타일 설정
border_props = dict(boxstyle='round,pad=0.5', facecolor='white', 
                   edgecolor='gray', linewidth=2)

# 명지대 영상 요약본 카드
ax1.add_patch(patches.Rectangle((0.1, 0.1), 0.8, 0.8, fill=False, 
              edgecolor='blue', linewidth=2))
ax1.text(0.5, 0.9, '명지대학교 영상 요약', ha='center', va='center', fontsize=12)
wrapped_text_mju = wrap_text(video_mju_data['summary'])
ax1.text(0.5, 0.45, wrapped_text_mju, 
         ha='center', va='center', fontsize=10,
         bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8),
         wrap=True,
         transform=ax1.transAxes,
         linespacing=1.5)
ax1.axis('off')

# 비교 영상 요약본 카드
ax2.add_patch(patches.Rectangle((0.1, 0.1), 0.8, 0.8, fill=False, 
              edgecolor='orange', linewidth=2))
ax2.text(0.5, 0.9, '비교 영상 요약', ha='center', va='center', fontsize=12)
wrapped_text_compare = wrap_text(video_compare_data['summary'])
ax2.text(0.5, 0.45, wrapped_text_compare,
         ha='center', va='center', fontsize=10,
         bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8),
         wrap=True,
         transform=ax2.transAxes,
         linespacing=1.5)
ax2.axis('off')

plt.tight_layout()
plt.show()





# 텍스트로도 출력
print("\n명지대학교 영상 요약:")
print("-" * 50)
print(video_mju_data['summary'])
print("\n비교 영상 요약:")
print("-" * 50)
print(video_compare_data['summary'])