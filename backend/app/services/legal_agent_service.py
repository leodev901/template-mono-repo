
from fastapi import Depends
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from loguru import logger

from app.core.llm_model import resolve_model_config
from app.core.dependencies import get_chat_models
from app.schemas.chat import ChatRequest
from app.schemas.legal import LegalChatResponse


class LegalAgentService:
    def __init__(
        self,
        models: dict = Depends(get_chat_models),
    ):
        self.models = models

    async def chat(self, payload: ChatRequest) -> LegalChatResponse:
        session_id = payload.session_id or "anonymous"
        
        # 여기서 부터는 langgraph 진행?
        # 1.법적 의도 분류
        # 2.관할권·날짜·사실관계 확인
        # 3.[법령 검색 Statute Repositor] & [판례 검색 Precedent Repository] & 내부 정책 검색 Internal Policy Repository
        # 4.증거 요약 구성
        # 5.초안 작성
        # 6.리스크 및 면책 검토
        # 7.최종 응답 + 출처 인용

        return LegalChatResponse(
            session_id=session_id,
            result="legal agent service",
        )