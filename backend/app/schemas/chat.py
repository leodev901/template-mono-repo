from typing import Literal
from pydantic import BaseModel, Field


class LlmConfig(BaseModel):
    provider: str | None = Field(None, description="Provider", example="gemini")
    model:str | None = Field(None, description="Model", example="fast")

class UserInfo(BaseModel):
    user_id: str | None = Field(None, description="사용자 ID", example="user-1234567890")
    user_name: str | None = Field(None, description="사용자 이름", example="홍길동")
    user_email: str | None = Field(None, description="사용자 Email", example="test@sample.com")
    user_role: Literal["guest", "standard", "pro", "admin"] = Field("guest", description="사용자 등급", example="guest")


class ChatRequest(BaseModel):
    session_id: str | None = Field(None, description="Session ID", example="session-1234567890") 
    llm_config: LlmConfig | None = Field(None, description="LLM Config")
    user_info: UserInfo | None = Field(None, description="요청 사용자 정보")
    message: str = Field(..., description="Message", example="간략히 자기소개를 해주세요")
    tools: list[str] = Field(None, description="호출 도구 목록",example=["news_search","blog_search","web_search"])

class ChatResponse(BaseModel):
    session_id: str
    result: str
    