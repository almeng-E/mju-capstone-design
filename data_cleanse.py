import pandas as pd 
# 리스트 정의
VALID = [
    "대학 역사", "대학 사업", "캠퍼스 투어","전공 탐구 및 소개", "커리큘럼 설명", "대학원 소개","입학 전형 안내", "입시 관련 팁", "신입생 정보","학생 생활 전반", "기숙사 소개", "학식 소개", "동아리/학회", "학생 복지 서비스", "선배 멘토링","수강 신청", "학습 노하우", "연구 프로젝트", "학술 대회", "연구 성과 및 논문 발표","교환학생 프로그램", "국제 교류 프로그램","취업 설명회 및 박람회", "진로 지원", "기업 연계 프로그램","장학금 안내","축제", "체전", "이벤트", "입학식", "졸업식","학생 인터뷰", "동문 인터뷰", "교수 인터뷰", "교수 강연","기타 자체 콘텐츠", "브이로그", "학교 홍보대사"
]

# CSV 파일 읽어오기
file_path = 'tagged_videos4_test.csv'  # CSV 파일 경로를 지정해 주세요
df = pd.read_csv(file_path)

# 'tags' 열의 빈 값을 "No Transcript"로 채우기
df['tags'].fillna("No Transcript", inplace=True)

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
# 수정된 데이터를 새로운 CSV 파일로 저장 (선택사항)
df.to_csv('updated_file.csv', index=False)