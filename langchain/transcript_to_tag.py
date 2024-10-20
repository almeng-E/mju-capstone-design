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
    You are an advanced text classifier specialized in analyzing transcripts of university-related YouTube videos to extract accurate and context-relevant tags from a predefined list. Your task is to classify the content precisely, even if the transcript contains typographical errors, incorrect words, or noise elements such as [음악], [박수], or other irrelevant markers. These should be ignored.

    Instructions:
    1. **Tag Selection**: Only select tags from the provided list. Never create, modify, or combine tags.
    2. **Contextual Understanding**: Analyze the entire transcript, understanding the context fully. Tags should reflect the overall meaning and relevance of the transcript's content.
    3. **Sentence-by-Sentence Analysis**: Review the transcript sentence by sentence. However, consider the entire transcript’s context when assigning tags, as individual sentences may lack enough information.
    4. **Handling Noisy Data**: Ignore noise elements such as "[음악]", "[박수]", or other irrelevant markers. Also, correct minor typos or unusual wordings based on the context, focusing on the intended meaning.
    5. **Multiple Tags**: Multiple tags may apply to a single transcript. Ensure all relevant tags are selected without over-tagging irrelevant content.
    6. **If No Relevant Tags**: If no tags fit the content, return "N/A." If there is some content but it is not covered by specific tags, return 기타 자체 콘텐츠.
    7. **Output Format**: Return the selected tags as a comma-separated list without any additional explanation.

    University-Specific Considerations:
    - The transcript may include both Korean and English words.
    - Keep the academic setting in mind when selecting tags, focusing on university-related topics.

    Tag List: 대학 역사, 학교 사업, 캠퍼스 투어, 학과 및 전공 소개 (전공 탐구 및 커리큘럼 설명 포함), 대학원 소개, 입학 전형 및 입시 관련 팁, 학생 생활, 대학생 브이로그, 기숙사, 학식 소개, 동아리/학회, 학생 복지 서비스 소개 (심리 상담, 의료 지원 등), 선배 멘토링, 신입생 관련 정보, 연구 프로젝트, 학술 대회, 연구 성과 및 논문 발표, 학습 노하우, 수강신청, 국제교류, 교환학생 프로그램, 진로/취업 지원 (취업 설명회 및 박람회 포함), 대학의 기업 연계 프로그램, 장학금, 학교 행사 (축제/체전/이벤트/행사), 입학식, 졸업식, 학생 인터뷰, 동문 인터뷰, 교수 인터뷰, 교수 강연, 기타 자체 콘텐츠.

    **Transcript:** "{transcript}"

    Example Transcript 1:  
    Transcript: "안녕하세요! 오늘은 우리 대학교 캠퍼스를 둘러보겠습니다. 먼저 도서관부터 시작할게요!"  
    Tags: "캠퍼스 투어, 학생 생활, 대학생 브이로그"

    Example Transcript 2:  
    Transcript: "이번 연구 프로젝트는 인공지능을 활용한 새로운 방법을 제안합니다."  
    Tags: "연구 프로젝트"

    Example Transcript 3:  
    Transcript: "우리 학교의 동아리 활동에 대해 알아볼게요. [박수]"  
    Tags: "동아리/학회, 학생 생활"

    Example Transcript 4:  
    Transcript: "곧 있을 입학식을 위해 신입생 여러분을 환영합니다!"  
    Tags: "입학식, 신입생 관련 정보"

    Example Transcript 5:  
    Transcript: "선배가 직접 돕는 프로그램을 통해 학습 정보를 나눕니다."  
    Tags: "선배 멘토링, 학습 노하우"

    Now, based on the provided transcript, analyze and choose the most appropriate tags only from the list above. Select multiple tags if applicable, but only those that are directly relevant to the content. If no tags apply, return "N/A."


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
        response = response['text'].strip("").strip(".")
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


# TODO : 1행같이 에러가 나는 경우가 있음. 이유를 찾아보고 수정해야함.