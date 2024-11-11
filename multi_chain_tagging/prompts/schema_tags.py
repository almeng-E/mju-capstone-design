# 태그 스키마 정의

from typing import List
from pydantic import BaseModel, Field


# 스키마 구성 및 분류
class Classification(BaseModel):
    video_info: List[str] = Field(
      default=None,
      description="Information related to the video's content",
      enum=["대학 정보, 학과 및 전공 정보, 입학 및 입시, 학생 생활, 수업 및 학습 지원, 국제 교류, 진로 및 취업 지원, 장학금 및 재정 지원, 학교 행사, 인터뷰 및 강연, 기타"],
      strict=True
    ) 




# 나중에 그냥 원래 코드에 합치기