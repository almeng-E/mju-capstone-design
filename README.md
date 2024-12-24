# mju-capstone-design

## 명지대학교 24-2 융합 캡스톤디자인 실행파일.

### 주제 : 유튜브 대본 기반 채널 분석 서비스 (대학교 채널)


### 데이터 수집 단계 : 
1. youtube API 활용하여 대학교 채널 데이터, 영상 데이터 불러오기
2. youtube_transcript_api 활용하여 영상 별 대본 불러오기
   우선순위 : 수동 번역 한국어 자막 > 수동 번역 영어 자막 > 자동 생성된 한국어 자막 > 자동 생성된 영어 자막
   이외 : NA
3. langchain 활용하여 대본 -> tag / summary 작성하기. (대본의 실제 내용 기반)
   RAG를 위한 기반 데이터 만들기
4. langchain RAG

![전체 메모 이미지](https://github.com/user-attachments/assets/2071681d-fb82-413a-9d4b-616d0547cf4c)
