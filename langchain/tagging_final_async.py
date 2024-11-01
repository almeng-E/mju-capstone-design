import os
import pandas as pd
import asyncio
from typing import List

from langchain_openai import ChatOpenAI
from langchain.chains import create_tagging_chain
from langchain_core.prompts import PromptTemplate

from pydantic import BaseModel, Field

from api_key import OPENAI_API_KEY

# Setup API Key
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

# Load the entire dataset
path = 'langchain/video_with_transcript.csv'
df = pd.read_csv(path)


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
        description="Other content related value not covered by the above categories",
        enum=["기타 자체 콘텐츠", "브이로그", "학교 홍보대사"],
        strict=True
    )



# Create the tagging prompt
tagging_template = """
Extract the desired information from the given transcript. Transcript is related to university content from YouTube videos. Consider the whole context of the transcript when selecting information.

The transcript may contain both Korean and English words.
Typos should be corrected based on the context.

Only extract the properties mentioned in the 'Classification' function.
It should reflect the overall meaning and relevance of the content.

Use the video title as a reference to understand the context of the transcript.
Title: "{title_input}"
Transcript: "{transcript_input}"
Ensure all output categories are lists, even if containing a single item.
"""

tagging_prompt = PromptTemplate.from_template(tagging_template)

# LLM , 체인 생성
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2).with_structured_output(
    Classification
)

tagging_chain = tagging_prompt | llm



# Process batch of data with blank check
async def process_batch(inputs, batch_index, batch_size, total_batches):
    try:
        # Filter out inputs with blank or NaN transcripts
        filtered_inputs = []
        row_indices = []
        
        for idx, input_data in enumerate(inputs):
            transcript = input_data.get("transcript_input", "")
            if pd.isna(transcript) or not str(transcript).strip():  # Check for NaN or empty transcript
                row_index = batch_index * batch_size + idx
                df.at[row_index, 'tags'] = 'No Transcript'
                print(f"Row {row_index}: No Transcript")
            else:
                filtered_inputs.append(input_data)
                row_indices.append(batch_index * batch_size + idx)
        
        # Process non-blank, non-NaN transcripts
        if filtered_inputs:
            results = await tagging_chain.abatch(filtered_inputs, return_exceptions=True)
            for idx, result in enumerate(results):
                row_index = row_indices[idx]
                if isinstance(result, Exception):
                    print(f"Error in row {row_index}: {result}")
                    df.at[row_index, 'tags'] = 'N/A'
                else:
                    combined_list = [item for sublist in result.dict().values() for item in sublist]
                    df.at[row_index, 'tags'] = '+'.join(combined_list)

        print(f"Processed batch {batch_index + 1}/{total_batches} ({(batch_index + 1) / total_batches * 100:.2f}% complete) ~~~~@")
    except Exception as e:
        print(f"Batch {batch_index} failed with error: {e}")

# Process all rows in batches
async def process_rows():
    batch_size = 30
    total_rows = len(df)
    total_batches = (total_rows + batch_size - 1) // batch_size
    
    tasks = []
    for batch_index in range(total_batches):
        start = batch_index * batch_size
        end = min(start + batch_size, total_rows)
        
        inputs = [
            {"title_input": row['title'], "transcript_input": row['transcript']}
            for _, row in df.iloc[start:end].iterrows()
        ]
        
        tasks.append(process_batch(inputs, batch_index, batch_size, total_batches))
    
    await asyncio.gather(*tasks)
    df.to_csv('tagged_videos.csv', index=False)
    print("done!")

# Run async loop
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(process_rows())