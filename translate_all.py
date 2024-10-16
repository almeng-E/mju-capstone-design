import pandas as pd
import re
from youtube_transcript_api import YouTubeTranscriptApi as YTA
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv

# 1. CSV 파일 읽어오기
csv_file_path = 'transcript_test_processed18.csv'
df = pd.read_csv(csv_file_path)

# 'transcript' 열을 문자열 타입으로 변환 (혹은 새로 생성)
df['transcript'] = df['transcript'].astype('object')

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
        return ""

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
        return ""

# 비디오 ID에 대해 자막 처리하는 함수 (병렬 처리에서 호출)
def process_row(index, row):
    # 이미 자막이 있으면 처리하지 않고 넘김
    if pd.notna(row['transcript']) and row['transcript'] != '':
        print(f"Skipping row {index} (ID: {row['id']}), transcript already exists.")
        return index, row['transcript']  # 기존 자막을 그대로 반환

    video_url = row['url']
    video_id = extract_video_id(video_url)
    
    if video_id:
        print(f"Processing row {index} (ID: {row['id']}) - Video ID: {video_id}")
        transcript_text = process_transcript(video_id)
        return index, transcript_text
    return index, ""

# 최대 50번 반복하는 설정 추가
max_attempts = 10
attempt = 0
total_updated_rows = 0  # 전체 업데이트된 행 개수를 추적

while attempt < max_attempts:
    attempt += 1
    updated_rows = 0  # 이번 반복에서 업데이트된 행 개수 추적
    print(f"\n========== Attempt {attempt} ==========")
    
    with ThreadPoolExecutor(max_workers=37) as executor:
        # 각 행에 대해 비디오 ID를 처리하고 결과를 병렬로 가져오기
        futures = [executor.submit(process_row, index, row) for index, row in df.iterrows()]

        # 완료된 작업들에 대해 CSV 파일 업데이트
        for future in as_completed(futures):
            index, transcript_text = future.result()
            # 자막 데이터를 문자열로 변환하여 저장
            if transcript_text != "":  # 빈 문자열이 아닌 경우에만 저장
                df.at[index, 'transcript'] = str(transcript_text)
                updated_rows += 1  # 이번 시도에서 업데이트된 행 개수 카운팅

    print(f"Attempt {attempt} completed. {updated_rows} rows updated.")

    # 이번 시도에서 업데이트된 자막이 없으면 종료
    if updated_rows == 0:
        print(f"No updates found in Attempt {attempt}. Stopping early.")
        break

    total_updated_rows += updated_rows

# CSV 파일을 저장할 때 quotechar와 quoting 옵션을 추가하여 자막을 큰 따옴표로 감싸서 저장
df.to_csv('transcript_test_processed19.csv', index=False, quoting=csv.QUOTE_ALL, quotechar='"')

print(f"처리가 완료되었습니다. 총 {total_updated_rows}개의 행이 업데이트되었습니다.")
