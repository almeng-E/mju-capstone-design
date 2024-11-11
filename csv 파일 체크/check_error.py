import csv
import pandas as pd

def check_id_column_for_errors(csv_file_path):
    error_rows = []
    empty_transcript_rows = []  # transcript가 비어있는 행을 기록

    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # 헤더 건너뛰기
        
        # 헤더의 'transcript' 열의 인덱스 확인
        transcript_idx = header.index('transcript')
        
        for row_num, row in enumerate(reader, start=2):  # 헤더가 1행이므로 실제 데이터는 2행부터 시작
            id_value = row[0]  # 첫 번째 열인 id 열
            
            # ID 컬럼 체크 (숫자로만 이루어져 있지 않은 경우)
            if not id_value.isdigit():
                error_rows.append(row_num)
            
            # transcript 열이 비어있는지 체크
            transcript_value = row[transcript_idx]
            if not transcript_value.strip():  # 공백이거나 빈 문자열일 경우
                empty_transcript_rows.append(row_num)

    # 결과 출력
    if error_rows:
        print(f"ID 컬럼에 오류가 있는 행 번호: {error_rows}")
        print(f"총 {len(error_rows)}개의 행에 오류가 있습니다.")
    else:
        print("ID 컬럼에 오류가 없습니다.")
    
    if empty_transcript_rows:
        # print(f"Transcript가 비어있는 행 번호: {empty_transcript_rows}")
        print(f"총 {len(empty_transcript_rows)}개의 행이 비어있습니다.")
    else:
        print("Transcript가 비어있는 행이 없습니다.")

# 사용 예시
csv_file_path = 'transcript_test_processed19.csv'
check_id_column_for_errors(csv_file_path)


def print_dataframe_shape(csv_file_path):
  df = pd.read_csv(csv_file_path)
  print(f"DataFrame shape: {df.shape}")

# 사용 예시
print_dataframe_shape(csv_file_path)
