import pandas as pd
import time
from youtube_transcript_api import YouTubeTranscriptApi as YTA

# 1. CSV 파일 읽어오기
csv_file_path = 'for_translation.csv'
df = pd.read_csv(csv_file_path)

# Video ID 추출 함수 (문자열 슬라이싱을 이용)
def extract_video_id(url):
    return url.split('v=')[1] if 'v=' in url else None

# 자막 데이터를 문자열로 변환하는 함수
def format_transcript(transcript):
    return " ".join([entry['text'] for entry in transcript])

# 자막 처리 함수
def process_transcript(video_id):
    try:
        transcript_list = YTA.list_transcripts(video_id)

        # 자막 우선순위에 따라 처리
        return (
            get_transcript(transcript_list, 'ko', manual=True) or
            get_transcript(transcript_list, 'en', manual=True, translate_to='ko') or
            get_transcript(transcript_list, 'ko', manual=False) or
            get_transcript(transcript_list, 'en', manual=False, translate_to='ko')
        )
    except Exception as e:
        print(f"Error processing video {video_id}: {e}")
        return None

# 자막을 가져오는 함수 (언어 및 번역 여부 처리)
def get_transcript(transcript_list, language_code, manual=True, translate_to=None):
    try:
        if manual:
            transcript = transcript_list.find_manually_created_transcript([language_code])
        else:
            transcript = transcript_list.find_generated_transcript([language_code])

        # 자막을 번역해야 하는 경우
        if translate_to:
            transcript = transcript.translate(translate_to)

        return format_transcript(transcript.fetch())
    except Exception:
        return None

# CSV 파일의 각 행에 대해 처리
for index, row in df.iterrows():
    video_url = row['url']
    video_id = extract_video_id(video_url)
    
    if video_id:
        print(f"Processing video ID: {video_id}")
        # 자막 처리 후 CSV에 업데이트
        transcript_text = process_transcript(video_id)
        df.at[index, 'transcript'] = transcript_text
    
        # API 요청 간 딜레이 추가 (1초)
        time.sleep(1)  # YouTube API의 과도한 요청을 방지하기 위해 지연 시간 추가

# 결과를 CSV 파일에 저장
df.to_csv('transcript_processed.csv', index=False)
print("처리가 완료되었습니다. 결과가 'transcript_test_processed.csv'에 저장되었습니다.")
