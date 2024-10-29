import pandas as pd

# CSV 파일 읽기
df = pd.read_csv('langchain/video_with_transcript.csv')  # 파일명을 적절히 변경해 주세요.


# 행별 결측치 확인 및 출력
print("행별 결측치 확인:")
missing_info = []
for idx, row in df.iterrows():
    missing_columns = row[row.isnull()].index.tolist()
    if missing_columns:
        for column in missing_columns:
            print(f"{idx + 1}번째 행의 '{column}' 컬럼 데이터가 비어있습니다.")
            missing_info.append((column, idx + 1))

# 컬럼별 결측치 요약 정보
print("\n컬럼별 결측치 요약:")
summary = {}
for column in df.columns:
    missing_rows = df[df[column].isnull()].index + 1
    missing_count = missing_rows.size
    if missing_count > 0:
        summary[column] = {"count": missing_count, "rows": missing_rows.tolist()}
        print(f"'{column}' 컬럼: {missing_count}개의 결측치가 있으며, 위치는 {missing_rows.tolist()}입니다.")
    else:
        print(f"'{column}' 컬럼: 결측치가 없습니다.")

# 추가적으로 컬럼별 요약 정보가 필요할 때 summary 사전을 사용하면 됩니다.