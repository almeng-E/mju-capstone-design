import os
import asyncio
import pandas as pd
from typing import List, Dict, Any

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from api_key import OPENAI_API_KEY

os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY



# 프롬프트 템플릿 정의
tagging_template = """ You are a language expert who is tasked with tagging a document.
The following is a document which is a summary of a transcript from a video, related to university contents. 

When tagging the content, follow the instructions below:
1. Consider the title of the video as a reference to understand the context.
2. Read and understand the context of the transcript summary
3. Extract the desired information from the transcript summary
4. Only extract the properties mentioned in the 'Classification' output format. It should reflect the overall meaning and relevance of the content.
5. Ensure all output categories are lists, even if containing a single item.
6. If there are no valuable information in the transcript summary, do not tag anything.

BE AWARE 1. Do not go beyond the context of the transcript summary. 
2. Ensure all output categories are lists, even if containing a single item.


Title : "{title_input}"
Transcript Summary : "{summary_input}"

Tag the content based on the following categories:
"""

no_transcript_template = """ You are a language expert who is tasked to extract tags from a title of a video.
The video is related to university contents.
It may or may not represent the whole context of the video.
In order to prevent any misunderstanding, please choose the most appropriate tag passively based on the title information.

Title : "{title_input}"

Be aware and ensure all output categories are lists, even if containing a single item.
Tag the content based on the following categories:"""

prompt01 = ChatPromptTemplate.from_template(tagging_template)
prompt02 = ChatPromptTemplate.from_template(no_transcript_template)
# 스키마 구성 및 분류
class Classification(BaseModel):
    # Category 1: 대학 정보
    university_info: List[str] = Field(
        default=[],
        description="Information related to the university itself (e.g., university history, university projects, campus tours), Information related to departments and major programs and its studies (e.g., major exploration and introduction, curriculum explanation, graduate school introduction), Information about admissions and entrance exams (e.g., admission guidelines, entrance exam tips, freshman information)",
        enum=["대학 정보","학과 및 전공 정보","입학 및 입시"],
        strict=True
    )
    
    # # Category 2: 학과 및 전공 정보
    # major_info: List[str] = Field(
    #     default=[],
    #     description="Information related to departments and major programs and its studies (e.g., major exploration and introduction, curriculum explanation, graduate school introduction)",
    #     enum=["학과 및 전공 정보"],
    #     strict=True
    # )
    
    # # Category 3: 입학 및 입시
    # admissions: List[str] = Field(
    #     default=[],
    #     description="Information about admissions and entrance exams (e.g., admission guidelines, entrance exam tips, freshman information)",
    #     enum=["입학 및 입시"],
    #     strict=True
    # )
    
    # Category 4: 학생 생활
    student_life: List[str] = Field(
        default=[],
        description="Information about student life and resources (e.g., overall student life, dormitory introduction, cafeteria introduction, clubs/associations, student welfare services, senior mentoring),Information about coursework and academic support (e.g., course registration, study tips, research projects, academic conferences, research achievements and paper presentations),Information on international programs and exchange (e.g., exchange student programs, international exchange programs), Information on school events and activities (e.g., festivals, sports events, events, entrance ceremonies, graduation ceremonies)",
        enum=["학생 생활", "수업 및 학습 지원", "국제 교류", "학교 행사"],
        strict=True
    )
    
    # # Category 5: 수업 및 학습 지원
    # academic_support: List[str] = Field(
    #     default=[],
    #     description="Information about coursework and academic support (e.g., course registration, study tips, research projects, academic conferences, research achievements and paper presentations)",
    #     enum=["수업 및 학습 지원"],
    #     strict=True
    # )
    
    # # Category 6: 국제 교류
    # international_exchange: List[str] = Field(
    #     default=[],
    #     description="Information on international programs and exchange (e.g., exchange student programs, international exchange programs)",
    #     enum=["국제 교류"],
    #     strict=True
    # )
    
    # Category 7: 진로 및 취업 지원
    career_support: List[str] = Field(
        default=[],
        description="Career and employment support programs (e.g., job fairs and expos, career support, corporate partnership programs), Scholarship and financial support information (e.g., scholarship information), Interviews and lectures with students, alumni, and faculty (e.g., student interviews, alumni interviews, professor interviews, professor lectures)",
        enum=["진로 및 취업 지원", "장학금 및 재정 지원", "인터뷰 및 강연", "기타"],
        strict=True
    )
    
    # # Category 8: 장학금 및 재정 지원
    # financial_aid: List[str] = Field(
    #     default=[],
    #     description="Scholarship and financial support information (e.g., scholarship information)",
    #     enum=["장학금 및 재정 지원"],
    #     strict=True
    # )
    
    # # Category 9: 학교 행사
    # events: List[str] = Field(
    #     default=[],
    #     description="Information on school events and activities (e.g., festivals, sports events, events, entrance ceremonies, graduation ceremonies)",
    #     enum=["학교 행사"],
    #     strict=True
    # )
    
    # # Category 10: 인터뷰 및 강연
    # interviews_lectures: List[str] = Field(
    #     default=[],
    #     description="Interviews and lectures with students, alumni, and faculty (e.g., student interviews, alumni interviews, professor interviews, professor lectures)",
    #     enum=["인터뷰 및 강연"],
    #     strict=True
    # )

    # # Category 11: 기타
    # other: List[str] = Field(
    #     default=[],
    #     description="Other content not covered by the above categories (e.g., other original content, vlogs, school ambassadors)",
    #     enum=["기타"],
    #     strict=True
    # )



# ChatOpenAI 인스턴스 생성
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(Classification)


# 체인 정의
tagging_chain01 = prompt01 | llm  # w/ transcript
tagging_chain02 = prompt02 | llm  # w/o transcript


# total_rows = len(df)

# for index, row in df.iterrows():
#   if pd.isna(row['tags'] or row['tags'] == None):
#     ttl = row['title']
#     smr = row['summary']
#     if smr:
#       res = tagging_chain01.invoke({"title_input": ttl, "summary_input": smr})
#     else:
#       res = tagging_chain02.invoke({"title_input": ttl})
#     try:
#       res = res.dict()
#       print('######')
#       print(res)
#       print(res.values())
#       # Flatten nested lists in the response if necessary
#       combined_list = [item for sublist in res.values() for item in (sublist if isinstance(sublist, list) else [sublist]) if item is not None]
#       result_str = '+'.join(combined_list)      

#       # Update 'tags' in the DataFrame
#       df.at[index, 'tags'] = result_str

#       # Print progress message
#       print(f"Processed row {index + 1}/{total_rows} ({((index + 1) / total_rows) * 100:.2f}% complete)")

#     except Exception as e:
#       print(f"@@@@@@@@@@@@@@@@@Error processing row {index}: {e}")
#       df.at[index, 'tags'] = None

# # Save the updated DataFrame to CSV
# df.to_csv('TEST_tag.csv', index=False)
# print("Processing complete. Check file for results.")

async def process_row(row: pd.Series) -> Dict[str, Any]:
    if pd.isna(row['tags']) or row['tags'] == "N/A" or row['tags'] is None or row['tags'] == "":
        ttl = row['title']
        smr = row['summary']
        try:
            if pd.notna(smr) and smr != "N/A":
                res = await tagging_chain01.ainvoke({"title_input": ttl, "summary_input": smr})
            else:
                res = await tagging_chain02.ainvoke({"title_input": ttl})
            
            res = res.dict()
            combined_list = [item for sublist in res.values() for item in sublist if item]
            result_str = '+'.join(combined_list)

            return {"index": row.name, "tags": result_str}
        except Exception as e:
            print(f"Error processing row {row.name}: {e}")
            return {"index": row.name, "tags": 'N/A'}
    return {"index": row.name, "tags": row['tags']}

async def process_batch(batch: pd.DataFrame) -> List[Dict[str, Any]]:
    tasks = [process_row(row) for _, row in batch.iterrows()]
    return await asyncio.gather(*tasks)

async def main():
    # CSV 파일 로드
    df = pd.read_csv('summary_and_tags.csv')  # 파일 경로를 적절히 수정하세요

    # 배치 크기 설정
    batch_size = 10
    total_rows = len(df)
    processed_rows = 0

    # 배치 처리
    for i in range(0, total_rows, batch_size):
        batch = df.iloc[i:i+batch_size]
        results = await process_batch(batch)
        
        # 결과 업데이트
        for result in results:
            df.at[result['index'], 'tags'] = result['tags']
        
        processed_rows += len(batch)
        print(f"Processed {processed_rows}/{total_rows} rows ({processed_rows/total_rows*100:.2f}% complete)")

        # 9초 대기
        print("Waiting for 9 seconds...")
        await asyncio.sleep(9)
        print("Resuming processing...")


    # 결과 저장
    df.to_csv('summary_and_tags02.csv', index=False)
    print("Processing complete. Data saved csv'")

if __name__ == "__main__":
    asyncio.run(main())







