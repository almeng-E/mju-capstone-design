import pandas as pd

# 데이터프레임을 로드합니다.
file_path = 'title_to_tags.csv'
df = pd.read_csv(file_path)


# 데이터프레임의 전체 행과 열의 개수를 출력합니다.
print(f"DataFrame shape: {df.shape}")

# 모든 열의 결측치를 확인하고 출력합니다.
missing_values = df.isnull().sum()
print("Missing values in each column:")
print(missing_values)


# 체크할 열 목록과 기대하는 데이터 타입
columns_to_check = {
    'id': int,
    'like_count': int,
    'view_count': int,
    'comment_count': int,
    'has_caption': int,
    'channel_id': int,
    'url': str
}

# 각 열의 데이터 타입을 체크하고, 다른 값이 있는 경우 요약을 출력합니다.
type_issues = {}

for column, expected_type in columns_to_check.items():
    incorrect_types = df[~df[column].apply(lambda x: isinstance(x, expected_type))]
    if not incorrect_types.empty:
        type_issues[column] = incorrect_types

if type_issues:
    print("Type issues found:")
    for column, issues in type_issues.items():
        print(f"\nColumn '{column}' has incorrect types:")
        print(issues)
else:
    print("All columns have correct types.")



# 소분류 태그와 대분류 태그 매핑
tag_mapping = {
    "대학 정보": "대학 정보",
    "학과 및 전공 정보": "학과 및 전공 정보",
    "입학 및 입시": "입학 및 입시",
    "학생 생활": "학생 생활",
    "수업 및 학습 지원": "수업 및 학습 지원",
    "국제 교류": "국제 교류",
    "진로 및 취업 지원": "진로 및 취업 지원",
    "장학금 및 재정 지원": "장학금 및 재정 지원",
    "학교 행사": "학교 행사",
    "인터뷰 및 강연": "인터뷰 및 강연",
    "기타": "기타"
}

# 태그를 대분류로 변환하는 함수
def is_valid_tag(tag):
    return tag in tag_mapping

# NaN 값을 빈 문자열로 대체
df['tags'] = df['tags'].fillna('')

# 빈 문자열을 제외하고 tags 열을 확인하고, 대분류 값과 다른 값이 있는 경우 요약
invalid_tags = df[(df['tags'] != '') & (~df['tags'].apply(lambda x: all(is_valid_tag(tag.strip()) for tag in x.split('+'))))]

if not invalid_tags.empty:
    print("\nInvalid tags found in the following rows:")
    print(invalid_tags)
else:
    print("\nAll tags are valid.")