# 태깅 프롬프트 2
# 대본없음 / 제목만으로 태그 추출

from langchain_core.prompts import PromptTemplate

template = """ You are a language expert who is tasked to extract tags from a title of a video.
The video is related to university contents.
It may or may not represent the whole context of the video.
In order to prevent any misunderstanding, please choose the most appropriate tag passively based on the title information.

Title : "{title_input}"

Tag the content based on the following categories:
"""

   
prompt = PromptTemplate.from_template(template)

