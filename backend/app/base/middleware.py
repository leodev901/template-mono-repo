# app/base/middleware.py
import time
import uuid
import json
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger

from app.base.context import bind_trace_id, reset_trace_id


# 로깅 제외 경로
EXCLUDE_PATHS = {
    "/health",
    "/healthz",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/openapi.yaml",
}

# 민감 정보는 로그에 그대로 남기지 않기 위해 별도 상수로 관리합니다.
SENSITIVE_HEADERS = {
    "authorization",
    "cookie",
    "set-cookie",
    "x-api-key",
    "proxy-authorization",
}

def _mask_sensitive_headers(headers: dict) -> dict:
    # 민감정보를 포함한 헤더는 마스킹 합니다. 
    masked_header: dict[str,any] = {}

    for key, value in headers.items():
        if key.lower() in SENSITIVE_HEADERS:
            masked_header[key] = "***MASKED***"
        else:
            masked_header[key] = value
    
    return masked_header

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1.CORS Preflight 요청 등 로깅이 불필요한 요청은 바로 패스
        if request.method == "OPTIONS":
            return await call_next(request)
        
        # 2.health check, docs 등은 트래픽이 많고 신호 대비 잡음이 커서 skip
        if request.url.path in EXCLUDE_PATHS:
            return await call_next(request)

        # 3.고유 추적 TRACE_ID 생성 및 요청 시작 시간 기록
        trace_id = request.headers.get("x-trace-id") or str(uuid.uuid4())
        request.state.trace_id = trace_id # 뒤에 실행될 라우터에서 쓸 수 있게 저장
        context_token = bind_trace_id(trace_id) # context_var 에서도 추적 id 를 사용할 수 있게 저장
        start_time = time.time()

        # [요청 로깅] Request 요청 로깅
        query_params = request.url.query
        logger.info(f"Request-[{trace_id}] <--- {request.method} {request.url.path} {request.client.host if request.client else 'unknown'} | Query: {query_params}")
        logger.info(f"Headers-[{trace_id}] <--- {json.dumps(dict(_mask_sensitive_headers(request.headers)), indent=2, ensure_ascii=False)}")
       
        # 4. 다음 미들웨어나 실제 API 함수 호출
        try:
            # awiat 비동 작업중 응답을 받지 못할 경우를 고려하여 응답 객체를 None으로 먼저 초기화합니다.
            response = None
            response = await call_next(request)
            return response
        except Exception:
            # exception.py 에서 예외를 핸들링 하기 때문에 그대로 넘깁니다.
            raise
        finally:
            # ===============================================================
            # 5. 소요 시간 계산 및 상태값 산출
            duration = (time.perf_counter() - start_time) * 1000

            if response:
                status_str = "SUCCESS" if response.status_code < 400 else "FAIL"
                status_code = response.status_code if response else "error"

                # [응답 헤더 세팅] 클라이언트도 자기가 무슨 ID로 요청했는지 알도록 헤더에 박아줌
                response.headers["X-Request-ID"] = trace_id
                response.headers["X-Duration-Time"] = f"{duration:.4f}"
            
            else: # response is none
                status_str = "FAIL"
                status_code = "error"

            # [응답 로깅] 
            logger.info(f"Response-[{trace_id}] ---> ({status_str}) {status_code} | Time: {duration:.2f}s")

            reset_trace_id(context_token)

