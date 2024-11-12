# import os
# import sys
# import pandas as pd

# from langchain_openai import ChatOpenAI
# from api_key import OPENAI_API_KEY

# os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


# # ---------------------------------------------------------------------------------------- #

# from langchain_core.prompts import ChatPromptTemplate

# # 템플릿 정의
# summarize_template =  """ You are a language expert who is tasked with summarizing a document.
# The following transcript from a youtube video. The transcript is written in Korean or English. The video is related to university contents.
# Be aware of the typos and noises ([박수], [음악]) that the transcript may contain. 

# Follow the instructions below to summarize the content of the transcript.

# 1. Read and understand the context of the transcript
# 2. Rephrase typos in the transcript based on the context
# 3. If there are no significant information on the transcript, just write "no valuable information"
# 4. Start the summary with mentioning the type of content's conversation (e.g., lecture, interview, v-log, conference, news, presentation etc.)
# 5. Reply in Korean
# 6. Write the summary within 20 sentences

# Consider the title when writing the summary.
# Title : {title}
# Write a concise summary of the following : \n\n {context} \n\n 
# CONCISE SUMMARY: 
# """

# # 체인 정의
# prompt = ChatPromptTemplate.from_template(summarize_template)
# summarize_chain = prompt | llm

# # ---------------------------------------------------------------------------------------- #
# # import test_items
# # test_transcript = test_items.trans_long
# # test_title = test_items.title_long



# # result = summarize_chain.invoke({"title": test_title,"context": test_transcript})
# # print(result)
# # print(type(result))
# # print(type(result.content))
# # print('------------')
# # result = result.dict()
# # print(result)
# # print(type(result))
# # print(type(result['content']))



# # ---------------------------------------------------------------------------------------- #
# # Load the entire dataset
# path = 'your_file.csv'
# df = pd.read_csv(path)


# # Total rows for progress tracking
# total_rows = len(df)
# # 태그가 비어 있는 항목에 대해 작업을 진행
# for index, row in df.iterrows():
#     if pd.isna(row['summary']) or row['summary'] == "N/A":
#       ttl = row['title']
#       trs = row['transcript'] 
#       try:
#         # Call chain
#         res = summarize_chain.invoke({"title": ttl, "context": trs})
#         res = res.dict()
        
#         # Update 'summary' in the DataFrame
#         df.at[index, 'summary'] = res['content']

#         # Print progress message
#         print(f"Processed row {index + 1}/{total_rows} ({((index + 1) / total_rows) * 100:.2f}% complete)")
#       except Exception as e:
#         print(f"Error processing row {index}: {e}")
#         df.at[index, 'summary'] = ' '
# # Save the updated DataFrame to CSV
# df.to_csv('summary_only.csv', index=False)
# print('done! check the file')



import os
import asyncio
import pandas as pd
from langchain_openai import ChatOpenAI
from api_key import OPENAI_API_KEY
from langchain_core.prompts import ChatPromptTemplate

os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

# ChatOpenAI 인스턴스 생성
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 프롬프트 템플릿 정의
summarize_template = """ You are a language expert who is tasked with summarizing a document.
The following transcript from a youtube video. The transcript is written in Korean or English. The video is related to university contents.
Be aware of the typos and noises ([박수], [음악]) that the transcript may contain. 

Follow the instructions below to summarize the content of the transcript.

1. Read and understand the context of the transcript
2. Rephrase typos in the transcript based on the context
3. If there are no significant information on the transcript, just write "no valuable information"
4. Start the summary with mentioning the type of content's conversation (e.g., lecture, interview, v-log, conference, news, presentation etc.)
5. Reply in Korean
6. Write the summary within 20 sentences

Consider the title when writing the summary.
Title : {title}
Write a concise summary of the following : \n\n {context} \n\n 
CONCISE SUMMARY: 
"""

# 체인 정의
prompt = ChatPromptTemplate.from_template(summarize_template)
summarize_chain = prompt | llm

async def process_row(row):
    if pd.isna(row['summary']) or row['summary'] == "N/A":
        try:
            res = await summarize_chain.ainvoke({"title": row['title'], "context": row['transcript']})
            return res.dict()['content']
        except Exception as e:
            print(f"Error processing row: {e}")
            return ' '
    return row['summary']

async def process_batch(batch):
    tasks = [process_row(row) for _, row in batch.iterrows()]
    return await asyncio.gather(*tasks)

async def main():
    # CSV 파일 로드
    path = 'your_file.csv'
    df = pd.read_csv(path)

    # 배치 크기 설정
    batch_size = 10
    total_rows = len(df)
    processed_rows = 0

    # 배치 처리
    for i in range(0, total_rows, batch_size):
        batch = df.iloc[i:i+batch_size]
        summaries = await process_batch(batch)
        
        # 결과 업데이트
        df.iloc[i:i+batch_size, df.columns.get_loc('summary')] = summaries
        
        processed_rows += len(batch)
        print(f"Processed {processed_rows}/{total_rows} rows ({processed_rows/total_rows*100:.2f}% complete)")

    # 결과 저장
    df.to_csv('TEST_summary_only.csv', index=False)
    print('Done! Check the file')

# 메인 실행
if __name__ == "__main__":
    asyncio.run(main())