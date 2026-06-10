from fastapi import Request,Depends
from supabase import AsyncClient


# ============================================================================
# Repository Dependencies
# ============================================================================

async def get_supabase_client(request: Request) -> AsyncClient|None:
    """
    Request 객체에서 app.state에 저장된 supabase 비동기 클라이언트를 추출하여 반환합니다.
    """
    return getattr(request.app.state, "supabase", None)

 
# async def get_llm_client(request: Request) -> dict:
#     """
#     Request 객체에서 app.state에 저장된 llm 클라이언트를 추출하여 반환합니다.
#     """
    
#     return request.app.state.llm

# async def get_langchain_client(request: Request) -> dict:
#     """
#     Request 객체에서 app.state에 저장된 langchain 클라이언트를 추출하여 반환합니다.
#     """
#     return request.app.state.langchain

async def get_chat_models(request: Request) -> dict:
    """
    Request 객체에서 app.state에 저장된 chat models를 추출하여 반환합니다.
    """
    return getattr(request.app.state, "models", None)


# ============================================================================
# Service Dependencies
# ============================================================================

from app.services.health_service import HealthService
from app.repositories.health import *
async def get_health_service(
    # repository: HealthRepositoryProtocol = Depends(HealthMockRepository)
    repository: HealthRepositoryProtocol = Depends(HealthSupabaseRepository)
) -> HealthService:
    return HealthService(repository)