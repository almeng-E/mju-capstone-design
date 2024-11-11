import pandas as pd 
# 리스트 정의
VALID = [
    "대학 정보", "학과 및 전공 정보", "입학 및 입시", "학생 생활", "수업 및 학습 지원", "국제 교류", "진로 및 취업 지원", "장학금 및 재정 지원", "학교 행사", "인터뷰 및 강연", "기타"
]

# CSV 파일 읽어오기
file_path = 'title_to_tags.csv'  # CSV 파일 경로를 지정해 주세요
df = pd.read_csv(file_path)

# # 'tags' 열의 빈 값을 "No Transcript"로 채우기
# df['tags'].fillna("No Transcript", inplace=True)

# 유효한 tags 값만 남기고, 다시 +로 연결
for index, row in df.iterrows():
    tag_str = row['tags']
    print(f"{index+1}번째 row 수정 중: {tag_str}")

    # "No Transcript"인 경우 빈 문자열로 설정
    if tag_str == "No Transcript" or tag_str == "N/A" or pd.isna(tag_str):
        df.at[index, 'tags'] = ""
    else:
        # 태그를 "+" 기준으로 분리하고 VALID_TAGS와 비교하여 유효한 태그만 유지
        tags = tag_str.split('+')
        valid_tags = [tag.strip() for tag in tags if tag.strip() in VALID]
        
        # 유효한 태그가 없는 경우 빈 문자열, 있으면 +로 재연결
        new_tag_str = '+'.join(valid_tags) if valid_tags else ""
        
        # 변경된 태그 값을 DataFrame에 반영
        df.at[index, 'tags'] = new_tag_str
        print(f"수정된 tags 값: {new_tag_str}")

# 수정 결과 확인
print("\n수정 완료 후 데이터:")
print(df.head())
# 수정된 데이터를 새로운 CSV 파일로 저장
df.to_csv('title_to_tags_final.csv', index=False, encoding='utf-8')