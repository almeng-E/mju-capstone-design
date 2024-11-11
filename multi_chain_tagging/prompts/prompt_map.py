# map reducing chain 1
# map template
# 대본 --> 요약1, 요약2, 요약3 ... 요약n


map_template = """ You are a language expert who is tasked with summarizing a set of documents.
The following is a set of documents which are portions of transcript from a video. The transcript is written in Korean or English. The video is related to university contents.
The transcript may contain noises ([박수], [음악]) and typos. 

Follow the instructions below to summarize the content of the transcript.

1. Read and understand the context of the transcript
2. Rephrase typos in the transcript based on the context
3. If there are no significant information on the transcript, just write "no valuable information"
4. Reply in Korean
5. Write the summary within 10 sentences

Write a concise summary of the following : \n\n {context} \n\n 
CONCISE SUMMARY: 
"""




