import os
import pandas as pd
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.schema import StrOutputParser

from api_key import OPENAI_API_KEY

# Step 1: Setup your API Key
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

# Step 2: Load the dataset and select the top 20 rows
df = pd.read_csv('langchain/video_with_transcript.csv').head(20)

# Step 3: Define the valid tags
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

# Step 4: Define the tagging prompt template
prompt_template = """
You are a strict text classifier and your task is to analyze the transcript of a university YouTube video and extract relevant tags based on the content. The script may contain typos, incorrect words, or noise such as [음악], [박수], but you must understand the context and choose the correct tags based on the whole context. 
You should only select tags from the provided valid tag list, and NEVER create or modify new tags. 
The tags should be returned as a comma-separated list.
    
One script may contain several tags. Script can be long. Read the script sentence by sentence and understand the whole context when classifying.
If there are no relevant tags, consider whether "기타 자체 콘텐츠" is appropriate, or if it contains nothing applicable, return "N/A". Do not provide explanations on output.
Also, consider the context of the video and the university setting when selecting tags. The script may contain Korean language and English words. And some are conversatinal.
Now, read the transcript and select the most appropriate tags.

Valid tags:
대학 역사, 학교 사업, 캠퍼스 투어, 학과 및 전공 소개 (전공 탐구 및 커리큘럼 설명 포함), 대학원 소개, 입학 전형 및 입시 관련 팁, 학생 생활, 대학생 브이로그, 기숙사, 학식 소개, 동아리/학회, 학생 복지 서비스 소개 (심리 상담, 의료 지원 등), 선배 멘토링, 신입생 관련 정보, 연구 프로젝트, 학술 대회, 연구 성과 및 논문 발표, 학습 노하우, 수강신청, 국제교류, 교환학생 프로그램, 입학 전형 및 입시 관련 팁, 진로/취업 지원 (취업 설명회 및 박람회 포함), 대학의 기업 연계 프로그램, 장학금, 학교 행사 (축제/체전/이벤트/행사), 입학식, 졸업식, 학생 인터뷰, 동문 인터뷰, 교수 인터뷰, 교수 강연, 기타 자체 콘텐츠

**Transcript:** "{transcript}"

Example 1  
transcript: "안녕하데여! 오는은 우리 대sk학의 캠푸스를 투어해 보겠습니당. 먼저 도서관을 방문할 거예요!"  
tags: "캠퍼스 투어, 학생 생활, 대학생 브이로그"

Example 2  
transcript: "이번 연구 프로젝트는 인공지능을 활용한 새로운 방법을 제안합니더"  
tags: "연구 프로젝트"

Example 3  
transcript: "우리 학교의 동아리/학회 활동에 대해 알아보겠습니당. [박수]"  
tags: "동아리/학회, 학생 생활"

Example 4  
transcript: "곧 있을 입학식을 위해 신입생 여러부늘 환영합니다!"  
tags: "입학식, 신입생 관련 정보"

Example 5  
transcript: "선배가 직접 돕는 프로그램을 통해 학습 정보를 공유합니다"  
tags: "선배 멘토링, 학습 노하우"


Based on the transcript, provide the most suitable tags **only from the list above**. 
Use multiple tags if necessary but only those that best match the content. 
If no tags are relevant, return "N/A". Do not add explanations.
"""

# Step 5: Initialize the model and prompt
model = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
prompt = ChatPromptTemplate.from_template(prompt_template)
output_parser = StrOutputParser()

# Step 6: Create an LLM chain
llm_chain = LLMChain(prompt=prompt, llm=model, output_parser=output_parser)

# Step 7: Function to validate and generate tags for each transcript
def validate_tags(tags):
    """Filter out invalid tags and return only valid tags."""
    valid_tags = [tag.strip() for tag in tags.split(",") if tag.strip() in VALID_TAGS]
    return ",".join(valid_tags) if valid_tags else "Error: Invalid tags"

def generate_tags(transcript):
    """Generate tags using the LLM and validate them."""
    if pd.isna(transcript):
        return "N/A"
    try:
        response = llm_chain.invoke({"transcript": transcript})
        print(response)
        print(type(response))
        response = response['text']
        output = validate_tags(response)
        print(output)
        return output
    except Exception as e:
        print(f"Error processing transcript: {e}")
        return "Error"

# Step 8: Apply the function to the top 20 rows
df['tags'] = df['transcript'].apply(generate_tags)

# Step 9: Display the result for review
print(df[['transcript', 'tags']])

# Optional: Save the trial results to a CSV
df.to_csv('trial2.csv', index=False)

print("Tag generation trial completed and saved to trial.csv")
