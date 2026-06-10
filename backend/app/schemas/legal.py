from app.schemas.chat import ChatResponse


class LegalChatResponse(ChatResponse):

    citations: list[str] = []       # 법령/판례/내부문서 출처
    risk_level: str | None = None # low / medium / high
    disclaimer: str | None = None # 법률 자문 아님 고지