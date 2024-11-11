# map reducing chain 2
# reduce template
# 요약1, 요약2, 요약3 ... 요약n --> 요약


reduce_template = """ You are a language expert who is tasked with summarizing a set of documents.
The follwing is a set of documents which are summaries of a transcript from a video written in Korean :\n {docs}\n
Take these and distill it into a final, consolidated summary of the main themes. If there are no valuable information in the summaries, just write "no valuable information".\n
Write the final summary within 10 sentences, in Korean.\n Final Summary:
"""



