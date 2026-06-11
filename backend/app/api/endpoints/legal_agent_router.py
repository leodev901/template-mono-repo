from fastapi import APIRouter, Depends, Request

from app.schemas.response import CommonResponse
from app.schemas.chat import ChatRequest
from app.services.legal_agent_service import LegalAgentService

from app.base.sse import SafeGuardStreamingResponse

api_router = APIRouter(prefix="/api/v1/legal", tags=["legal_agent"])


@api_router.post("/chat", response_model=CommonResponse)
async def legal_chat(
    payload: ChatRequest, 
    legal_agent_service: LegalAgentService = Depends(LegalAgentService),
):

    result = await legal_agent_service.chat(payload)
    return CommonResponse.ok(result)



# @api_router.post("/chat/stream")
# async def legal_chat_stream(
#     request: Request,
#     payload: ChatRequest,
#     legal_agent_service: LegalAgentService = Depends(LegalAgentService),
# ):
#     # StreamingResponse 객체에 서비스의 제너레이터 함수를 통째로 넣어야 스트리밍 됨.
#     # streaMiddelaware에서 응답 갭체에 에러 바생시 에러 yield 하도록 구현 함
#     return SafeGuardStreamingResponse(
#         legal_agent_service.chat_stream(payload),
#         media_type="text/event-stream", # 브라우저에게 "이거 안 끝나는 실시간 이벤트야!" 명시해줌
#         trace_id=getattr(request.state, "trace_id", "unknown")
#     )

