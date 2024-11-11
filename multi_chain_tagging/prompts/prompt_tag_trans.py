# 태깅 프롬프트 1
# 제목 + Final 대본 --> 태그 추출

from langchain_core.prompts import PromptTemplate

template = """ You are a language expert who is tasked with tagging a set of documents.
The following is a document which is a summary of a transcript from a video, related to university contents. 

When tagging the content, follow the instructions below:
1. Consider the title of the video as a reference to understand the context.
2. Read and understand the context of the transcript summary
3. Extract the desired information from the transcript summary
4. Only extract the properties mentioned in the 'Classification' function. It should reflect the overall meaning and relevance of the content.
5. Ensure all output categories are lists, even if containing a single item.
6. If there are no valuable information in the transcript summary, do not tag anything.

Title : "{title_input}"
Transcript Summary : "{transcript_summary_input}"

Tag the content based on the following categories:
"""

   
prompt = PromptTemplate.from_template(template)
