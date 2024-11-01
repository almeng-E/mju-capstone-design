import os
from typing import List

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
df = pd.read_csv(path).head(20) 


# 스키마 구성 및 분류
class Classification(BaseModel):
    # Category 1: 대학 정보
    university_info: List[str] = Field(
        default=[],
        description="Information related to the university itself",
        enum=["대학 역사", "대학 사업", "캠퍼스 투어"],
        strict=True
    )
    
    # Category 2: 학과 및 전공 정보
    major_info: List[str] = Field(
        default=[],
        description="Information related to departments and major programs and its studies",
        enum=["전공 탐구 및 소개", "커리큘럼 설명", "대학원 소개"],
        strict=True
    )
    
    # Category 3: 입학 및 입시
    admissions: List[str] = Field(
        default=[],
        description="Information about admissions and entrance exams",
        enum=["입학 전형 안내", "입시 관련 팁", "신입생 정보"],
        strict=True
    )
    
    # Category 4: 학생 생활
    student_life: List[str] = Field(
        default=[],
        description="Information about student life and resources",
        enum=["학생 생활 전반", "기숙사 소개", "학식 소개", "동아리/학회", "학생 복지 서비스", "선배 멘토링"],
        strict=True
    )
    
    # Category 5: 수업 및 학습 지원
    academic_support: List[str] = Field(
        default=[],
        description="Information about coursework and academic support",
        enum=["수강 신청", "학습 노하우", "연구 프로젝트", "학술 대회", "연구 성과 및 논문 발표"],
        strict=True
    )
    
    # Category 6: 국제 교류
    international_exchange: List[str] = Field(
        default=[],
        description="Information on international programs and exchange",
        enum=["교환학생 프로그램", "국제 교류 프로그램"],
        strict=True
    )
    
    # Category 7: 진로 및 취업 지원
    career_support: List[str] = Field(
        default=[],
        description="Career and employment support programs",
        enum=["취업 설명회 및 박람회", "진로 지원", "기업 연계 프로그램"],
        strict=True
    )
    
    # Category 8: 장학금 및 재정 지원
    financial_aid: List[str] = Field(
        default=[],
        description="Scholarship and financial support information",
        enum=["장학금 안내"],
        strict=True
    )
    
    # Category 9: 학교 행사
    events: List[str] = Field(
        default=[],
        description="Information on school events and activities",
        enum=["축제", "체전", "이벤트", "입학식", "졸업식"],
        strict=True
    )
    
    # Category 10: 인터뷰 및 강연
    interviews_lectures: List[str] = Field(
        default=[],
        description="Interviews and lectures with students, alumni, and faculty",
        enum=["학생 인터뷰", "동문 인터뷰", "교수 인터뷰", "교수 강연"],
        strict=True
    )

    # Category 11: 기타
    other: List[str] = Field(
        default=[],
        description="Other content not covered by the above categories",
        enum=["기타 자체 콘텐츠", "브이로그", "학교 홍보대사"],
        strict=True
    )


tagging_template = """
Extract the desired information from the given transcript. Transcript is related to university content from Youtube videos. Consider the whole context of the transcript when selecting informations. 

The transcript may contain both Korean and English words. 
Type-o should be corrected based on the context.

Only extract the properties mentioned in the 'Classification' function.
It should reflect the overall meaning and relevance of the content.

Use the video title as a reference to understand the context of the transcript.
Title: "{title_input}"
Transcript: "{transcript_input}"
Ensure all output categories are lists, even if containing a single item.
"""


# 프롬프트 템플릿 생성
tagging_prompt = PromptTemplate.from_template(tagging_template)

# LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1).with_structured_output(
  Classification
)

tagging_chain = tagging_prompt | llm


######################## TESTING CODE 1 : iterrow #############################
# 각 행에 대해 처리 
for index, row in df.iterrows():
    tit = row['title']
    inp = row['transcript']
    try:
        res = tagging_chain.invoke({"title_input": tit, "transcript_input": inp})
        res = res.dict()
        # 각 항목이 리스트가 아니면 리스트로 변환
        combined_list = [item for sublist in res.values() for item in sublist]
        result_str = '+'.join(combined_list)
        df.at[index, 'tags'] = result_str
    except Exception as e:
        print(f"Error processing row {index}: {e}")
        df.at[index, 'tags'] = 'N/A'

# 결과를 CSV로 저장
df.to_csv('tagged_videos.csv', index=False)

# [음악] n [음악] [음악] w [음악] [음악] n [음악] [박수] [ 음악] [박수] [ 음악] [음악] oh [음악]
###############################################################################
######################### TESTING CODE 2 : single input ########################
#
# # 테스트 값
# tit = "[시립대 후원의 집 가봄? | 서울시립대학교 홍보대사 이루미]"
# inp = "아 나 해외여행 가네음 너 해외 여행 가고 싶어 응 그러면 우리 학교 교환학생 신청해 보는 거 어때 어 교환학생 근데 그거 어떻게 하는 건데 우선 일반 공지에서 국제 처에서 작성한 해외파견 교환학생 선발 공고를 살펴봅니다 우리 학교는 75개국 약 570여 개의 학교와 학술 교류 협정을 맺고 있어 학생들의 더 넓은 세상으로의 도약을 돕고 있습니다 또한 일반 교환학생 프로그램뿐만 아니라 아이셉 saf 프로그램도 있는데요 여기서 아이란 엄격한 자격 기준에 의거하여 전 세계 약 380억에 회원 대학이 가입되어 있으며 아이셉 회원 교관 학생 교류를 하고 숙소와 식비가 지원되는 프로그램입니다 saf 스디 AB 파운데이션 프로그램으로 파견 기간 동안 본 및 대교에서 재학생 상태이 유지되어 학기를 인정받게 되며 파견 대학에서 취득한 학점을 우리대학 학칙에 준하여 본교 학점으로 인정합니다 교환학생 가이드북과 체험 수기 등 더 자세한 내용은 국제처 홈페이지에서 찾으실 수 있습니다 공고에서 원하는 나라의 대학을 고른 후 요구하는 공인 허학 점수를 갖춘 뒤에 지원 기간 동안 지에서 10까지의 학교를 지원합니다 합격 후에는 오리엔테이션 등을 통 통에 파견 준비를 하면 됩니다 안녕하세요 안세 아 오늘 굉장히 멋진 단복을 입고 오셨는데 혹시 어느 단체 소속이신가요 자기소개 부탁드려요 국제 교육원에서 국제 처로 승격된 국제 처의 홍보대사를 맡고 있는 어 서울 글로벌 앰바사더 sga 단원 이동준이 합니다 저희 sga 다른 대학교에서 교류를 오시는 교수님이나 총장님 등 이제 외인 분들이 오시면 의전 활동이나 캠퍼스투어를 담당하고 있고요 어 교환학생 같은 국제처 프로그램을 SNS 홍보하는 활동을 하고 있습니다 그럼 이렇게 국제처 소속으로 학생들의 교환학생 프로그램을 도울뿐만 아니라 실제 교환학생을 다녀오셨다고 들었는데 언제 어디서 공부하셨나요네 맞습니다 저는 어 딱 요맘 때쯤 캐나다 앨버타주의 캘거리는 도시로 교환학생을 다녀왔는데요 교환교 유시티 오 캘거리 캘거리대학교 있습니다 혹시 그럼 그 대학을 선택하신 이유 가 있으실까요 어 일단 첫 번째로는 캘거리는 도시가 스포츠의 도시라고 불리면 실내 빈 상장이나 그리고 수영장 뭐 클라이밍장 스포츠 활동을 많이 할 수 있는 그 학교 시설이 있다는 점에서 하나가 있었고 두 번째는 앨버타 주가 퇴근이 가장 싼 편이라서 경제적으로도 잘 갖다 올 수 있겠다 싶어서 세 번째로는 캘거리는 도시가 로키산맥 자락에 있는 도시인데 한시간 반 정도 거리밖에 안 걸려 어떤 학생들에게 캘거리 대학교를 추천하나요 자연을 좋아하고 자연에서 야생 동물을 보고 밤엔 별도 보고 오로라도 밤에 떠 가지고 야외에서 활동적인 걸 좋아하시는 분들에게 추천드리고싶습니다 제가 가야겠어요 그럼 교환 학생을 가기 위해서는 어학 점수가 필수잖아요 어떤 시험을 보셨는지 공고 비법이 있다면 공개 부탁드립 플을 준비를 했었고요 저는 주로 미드 보는 걸 좋아해 가지고 일상적인 회화도 많이 수 있 추거 같은 거를 잘 캐치 수 있어서 통 하는데 도움이 많이 던 것 같습니다 교환학생으로 선정된 후에는 어떤 준비가 필요한가요 어 먼저 제일 중요한 건 비자 거 같은데요 캐나다 같은 경우에는 6개월 미만의 경우에는 ETA 비자라 그래 가지고 7 캐네디언 달러만 내면 되는 비자 있고요 6개월 이상 교환학생을 계획하시고 있으시다면 스터디 퍼밋이 필요해서 교환학생 대상 버디 프로그램들이 있는지 꼭 확인해 보시면 될 거 같고 그럼 그 외에도 교환 학생을 준비하시거나 이제 가려고 하는 학생분들에게 하시고 싶은 말씀이 있으신가요 아 먼저 첫 번째는 세상이 얼마나 넓은지를 좀 느낄 수 있었어요 뭐든지 할 수 있을 것 같다는 장력도 싸울 수 있는 그런 경험이 됐던 거 같습니다네 오늘 이렇게 서울 글로벌 앰버서더 SJ 이동주 님과 함께 인터뷰 진행해 봤는데요 뭐 오늘 이야기를 들으니까 저도 너무 교환학생 가고 싶은데 여러분도 교환학생 가고 싶으시죠 그럼 여러분도 한번 도전해 보세요 세 안녕 안녕"
#
# res = tagging_chain.invoke({"title_input":tit, "transcript_input": inp})
# # 각 항목이 리스트가 아니면 리스트로 변환
# res = res.dict()
#
# print(type(res))
# print(res)
# print('-------------------')
#
# combined_list = [item for sublist in res.values() for item in sublist]
# print(combined_list)
# print('-------------------')
#
# result_str = '+'.join(combined_list)
# print(result_str)
################################################################################

############################# not used ############################
# # 태그 설정
# VALID_TAGS = [
#     "대학 역사", "학교 사업", "캠퍼스 투어", "학과 및 전공 소개 (전공 탐구 및 커리큘럼 설명 포함)",
#     "대학원 소개", "입학 전형 및 입시 관련 팁", "학생 생활", "대학생 브이로그", "기숙사",
#     "학식 소개", "동아리/학회", "학생 복지 서비스 소개 (심리 상담, 의료 지원 등)",
#     "선배 멘토링", "신입생 관련 정보", "연구 프로젝트", "학술 대회", "연구 성과 및 논문 발표",
#     "학습 노하우", "수강신청", "국제교류", "교환학생 프로그램", "입학 전형 및 입시 관련 팁",
#     "진로/취업 지원 (취업 설명회 및 박람회 포함)", "대학의 기업 연계 프로그램", "장학금",
#     "학교 행사 (축제/체전/이벤트/행사)", "입학식", "졸업식", "학생 인터뷰", "동문 인터뷰",
#     "교수 인터뷰", "교수 강연", "기타 자체 콘텐츠"
# ]