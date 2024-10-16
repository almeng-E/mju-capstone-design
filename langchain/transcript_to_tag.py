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
    "학교 소개", "홍보 영상", "동아리 소개", "학교 사업 소개", "학교 행사 소개", 
    "학과 소개", "축제 관련 콘텐츠", "기타 자체 콘텐츠", "입시정보", "동문 인터뷰", 
    "수강신청", "브이로그", "신입생 대상 콘텐츠", "대학원 관련 콘텐츠"
]

# Step 4: Define the tagging prompt template
prompt_template = """
You are a strict classifier that reads YouTube video transcripts and assigns appropriate tags based on their content.
Use **only the following valid tags** from the list below. Do not create new tags or modify them. Return tags as a comma-separated list.

Valid tags:
학교 소개, 홍보 영상, 동아리 소개, 학교 사업 소개, 학교 행사 소개, 학과 소개, 축제 관련 콘텐츠,
기타 자체 콘텐츠, 입시정보, 동문 인터뷰, 수강신청, 브이로그, 신입생 대상 콘텐츠, 대학원 관련 콘텐츠

**Transcript:** "{transcript}"

Based on the transcript, provide the most suitable tags **only from the list above**. 
Use multiple tags if necessary but only those that best match the content. 
If no tags are relevant, return "N/A". Do not add explanations.
"""

# Step 5: Initialize the model and prompt
model = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
prompt = ChatPromptTemplate.from_template(prompt_template)
output_parser = StrOutputParser()

# Step 6: Create an LLM chain
llm_chain = LLMChain(prompt=prompt, llm=model, output_parser=output_parser)

# Step 7: Function to validate and generate tags for each transcript
def validate_tags(tags):
    """Check if all tags are valid."""
    return all(tag.strip() in VALID_TAGS for tag in tags.split(","))

def generate_tags(transcript):
    """Generate tags using the LLM and validate them."""
    if pd.isna(transcript):
        return "N/A"
    try:
        response = llm_chain.run({"transcript": transcript}).strip()
        if validate_tags(response):
            return response
        else:
            return "Error: Invalid tags"
    except Exception as e:
        print(f"Error processing transcript: {e}")
        return "Error"

# Step 8: Apply the function to the top 20 rows
df['tags'] = df['transcript'].apply(generate_tags)

# Step 9: Display the result for review
print(df[['transcript', 'tags']])

# Optional: Save the trial results to a CSV
df.to_csv('trial.csv', index=False)

print("Tag generation trial completed and saved to trial.csv")
