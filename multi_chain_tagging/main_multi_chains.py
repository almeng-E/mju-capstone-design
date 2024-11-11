from langchain_text_splitters import CharacterTextSplitter
from langchain_core.documents import Document
import trans_for_test
from prompts import prompt_map, prompt_reduce

documents = [Document(page_content=trans_for_test.trans_kor)]
print(documents)
text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
  chunk_size=1000, chunk_overlap=0
  )
split_docs = text_splitter.split_documents(documents)
print(f"Generated {len(split_docs)} documents.")