# TODO : 스키마 구성 , 태깅체인 아규먼트 확인 및 구성

import os
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain.chains import create_tagging_chain
from langchain_core.prompts import PromptTemplate

from pydantic import BaseModel, Field


from api_key import OPENAI_API_KEY

# Setup API Key
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

# Load dataset
path = 'langchain/video_with_transcript.csv'
# FOR TEST
df = pd.read_csv(path).head(20) 


# 태그 설정
VALID_TAGS = [
    "대학 역사", "학교 사업", "캠퍼스 투어", "학과 및 전공 소개 (전공 탐구 및 커리큘럼 설명 포함)",
    "대학원 소개", "입학 전형 및 입시 관련 팁", "학생 생활", "대학생 브이로그", "기숙사",
    "학식 소개", "동아리/학회", "학생 복지 서비스 소개 (심리 상담, 의료 지원 등)",
    "선배 멘토링", "신입생 관련 정보", "연구 프로젝트", "학술 대회", "연구 성과 및 논문 발표",
    "학습 노하우", "수강신청", "국제교류", "교환학생 프로그램", "입학 전형 및 입시 관련 팁",
    "진로/취업 지원 (취업 설명회 및 박람회 포함)", "대학의 기업 연계 프로그램", "장학금",
    "학교 행사 (축제/체전/이벤트/행사)", "입학식", "졸업식", "학생 인터뷰", "동문 인터뷰",
    "교수 인터뷰", "교수 강연", "기타 자체 콘텐츠"
]


tagging_template = """
Extract the desired information from the given transcript. Transcript is related to university content from Youtube videos. Consider the whole context of the transcript when selecting informations. 

The transcript may contain both Korean and English words. 
Type-o should be corrected based on the context.

Only extract the properties mentioned in the 'Classification' function.
It should reflect the overall meaning and relevance of the content.

Transcript: "{input}"
"""

# 스키마 구성 및 분류
class Classification(BaseModel):
    # Category 1: 대학 정보
    university_info: list[str] = Field(
        default=[],
        description="Information related to the university itself",
        enum=["대학 역사", "대학 사업", "캠퍼스 투어", "입학식", "졸업식"]
    )
    
    # Category 2: 학과 및 전공 정보
    major_info: list[str] = Field(
        default=[],
        description="Information related to departments and major programs",
        enum=["전공 탐구 및 소개", "커리큘럼 설명", "대학원 소개"]
    )
    
    # Category 3: 입학 및 입시
    admissions: list[str] = Field(
        default=[],
        description="Information about admissions and entrance exams",
        enum=["입학 전형", "입시 관련 팁", "신입생 정보"]
    )
    
    # Category 4: 학생 생활
    student_life: list[str] = Field(
        default=[],
        description="Information about student life and resources",
        enum=["학생 생활 전반", "기숙사 소개", "학식 소개", "동아리/학회", "학생 복지 서비스", "선배 멘토링"]
    )
    
    # Category 5: 수업 및 학습 지원
    academic_support: list[str] = Field(
        default=[],
        description="Information about coursework and academic support",
        enum=["수강 신청", "학습 노하우", "연구 프로젝트", "학술 대회", "연구 성과 및 논문 발표"]
    )
    
    # Category 6: 국제 교류
    international_exchange: list[str] = Field(
        default=[],
        description="Information on international programs and exchange",
        enum=["교환학생 프로그램", "국제 교류 프로그램"]
    )
    
    # Category 7: 진로 및 취업 지원
    career_support: list[str] = Field(
        default=[],
        description="Career and employment support programs",
        enum=["취업 설명회 및 박람회", "진로 지원", "기업 연계 프로그램"]
    )
    
    # Category 8: 장학금 및 재정 지원
    financial_aid: list[str] = Field(
        default=[],
        description="Scholarship and financial support information",
        enum=["장학금 안내"]
    )
    
    # Category 9: 학교 행사
    events: list[str] = Field(
        default=[],
        description="Information on school events and activities",
        enum=["축제", "체전", "이벤트"]
    )
    
    # Category 10: 인터뷰 및 강연
    interviews_lectures: list[str] = Field(
        default=[],
        description="Interviews and lectures with students, alumni, and faculty",
        enum=["학생 인터뷰", "동문 인터뷰", "교수 인터뷰", "교수 강연"]
    )
  
# 프롬프트 템플릿 생성
tagging_prompt = PromptTemplate.from_template(tagging_template)

# LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1).with_structured_output(
  Classification
)

tagging_chain = tagging_prompt | llm


# 테스트 값
inp = "이번 취업 설명회는 삼성전자, LG전자, 현대자동차 등 다양한 기업의 채용 정보를 제공합니다. 추가로 기업 연계 프로그램에 대한 상세한 설명도 포함되어 있습니다. 또한, 기업이 제공하는 여러 금전적 지원 프로그램과 쟝핵금 혜택에 대한 정보도 제공합니다. 먼저 학생 인터뷰와 동문 그리고 교수와의 자문을 통해 설명회를 시작하도록 하겠습니다. ~~~"

res = tagging_chain.invoke({"input": inp})
res = res.dict()

print(type(res))
print(res)
print('-------------------')

combined_list = [item for sublist in res.values() for item in sublist]
print(combined_list)
print('-------------------')

result_str = '+'.join(combined_list)
print(result_str)
