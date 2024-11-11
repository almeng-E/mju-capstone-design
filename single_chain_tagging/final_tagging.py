import os
import pandas as pd
# import asyncio
from typing import List

from langchain_openai import ChatOpenAI
from langchain.chains import create_tagging_chain
from langchain_core.prompts import PromptTemplate

from pydantic import BaseModel, Field

from api_key import OPENAI_API_KEY

# Setup API Key
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

# Load the entire dataset
path = '최종 파일들/tagged_final_classified.csv'
df = pd.read_csv(path)


# 스키마 구성 및 분류
class Classification(BaseModel):
    # Category 1: 대학 정보
    university_info: List[str] = Field(
        default=None,
        description="Information related to the university itself (e.g., university history, university projects, campus tours)",
        enum=["대학 정보"],
        strict=True
    )
    
    # Category 2: 학과 및 전공 정보
    major_info: List[str] = Field(
        default=None,
        description="Information related to departments and major programs and its studies (e.g., major exploration and introduction, curriculum explanation, graduate school introduction)",
        enum=["학과 및 전공 정보"],
        strict=True
    )
    
    # Category 3: 입학 및 입시
    admissions: List[str] = Field(
        default=None,
        description="Information about admissions and entrance exams (e.g., admission guidelines, entrance exam tips, freshman information)",
        enum=["입학 및 입시"],
        strict=True
    )
    
    # Category 4: 학생 생활
    student_life: List[str] = Field(
        default=None,
        description="Information about student life and resources (e.g., overall student life, dormitory introduction, cafeteria introduction, clubs/associations, student welfare services, senior mentoring)",
        enum=["학생 생활"],
        strict=True
    )
    
    # Category 5: 수업 및 학습 지원
    academic_support: List[str] = Field(
        default=None,
        description="Information about coursework and academic support (e.g., course registration, study tips, research projects, academic conferences, research achievements and paper presentations)",
        enum=["수업 및 학습 지원"],
        strict=True
    )
    
    # Category 6: 국제 교류
    international_exchange: List[str] = Field(
        default=None,
        description="Information on international programs and exchange (e.g., exchange student programs, international exchange programs)",
        enum=["국제 교류"],
        strict=True
    )
    
    # Category 7: 진로 및 취업 지원
    career_support: List[str] = Field(
        default=None,
        description="Career and employment support programs (e.g., job fairs and expos, career support, corporate partnership programs)",
        enum=["진로 및 취업 지원"],
        strict=True
    )
    
    # Category 8: 장학금 및 재정 지원
    financial_aid: List[str] = Field(
        default=None,
        description="Scholarship and financial support information (e.g., scholarship information)",
        enum=["장학금 및 재정 지원"],
        strict=True
    )
    
    # Category 9: 학교 행사
    events: List[str] = Field(
        default=None,
        description="Information on school events and activities (e.g., festivals, sports events, events, entrance ceremonies, graduation ceremonies)",
        enum=["학교 행사"],
        strict=True
    )
    
    # Category 10: 인터뷰 및 강연
    interviews_lectures: List[str] = Field(
        default=None,
        description="Interviews and lectures with students, alumni, and faculty (e.g., student interviews, alumni interviews, professor interviews, professor lectures)",
        enum=["인터뷰 및 강연"],
        strict=True
    )

    # Category 11: 기타
    other: List[str] = Field(
        default=None,
        description="Other content not covered by the above categories (e.g., other original content, vlogs, school ambassadors)",
        enum=["기타"],
        strict=True
    )



# Create the tagging prompt
tagging_template = """
Extract the desired information from the given title. Title is related to university content from YouTube videos. Guess the whole context of the video upon the given title information when selecting information.


Only extract the properties mentioned in the 'Classification' function.
It should reflect the overall meaning and relevance of the content.

Consider the video title as a reference to understand the context.
In this case, the title should be the primary source of information.
Title: "{title_input}"
Ensure all output categories are lists, even if containing a single item.
"""

tagging_prompt = PromptTemplate.from_template(tagging_template)



# LLM , 체인 생성
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3).with_structured_output(
    Classification
)

tagging_chain = tagging_prompt | llm

# Total rows for progress tracking
total_rows = len(df)
# 태그가 비어 있는 항목에 대해 작업을 진행
for index, row in df.iterrows():
    if pd.isna(row['tags']) or row['tags'] == "N/A":
        tit = row['title']
        try:
            # Call the tagging chain API
            res = tagging_chain.invoke({"title_input": tit})
            res = res.dict()

            # Flatten nested lists in the response if necessary
            combined_list = [item for sublist in res.values() for item in (sublist if isinstance(sublist, list) else [sublist]) if item is not None]
            result_str = '+'.join(combined_list)

            # Update 'tags' in the DataFrame
            df.at[index, 'tags'] = result_str
            
            # Print progress message
            print(f"Processed row {index + 1}/{total_rows} ({((index + 1) / total_rows) * 100:.2f}% complete)")
    
        except Exception as e:
            print(f"Error processing row {index}: {e}")
            df.at[index, 'tags'] = 'N/A'

# Save the updated DataFrame to CSV
df.to_csv('title_to_tags.csv', index=False)
print("Processing complete. Data saved to 'title_to_tags.csv'")