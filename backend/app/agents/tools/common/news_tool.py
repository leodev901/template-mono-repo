import httpx
import json
import html
import re
from typing import Annotated
from langchain.tools import tool
from pydantic import Field, BaseModel
from loguru import logger

from app.core.config import settings
from app.base.http_client import get_httpx_client


class News(BaseModel):
    """뉴스 검색 결과를 담는 모델"""
    no: int = Field(description="뉴스 번호")
    title: str = Field(description="뉴스 제목")
    link: str = Field(description="뉴스 링크")
    description: str = Field(description="뉴스 요약 내용")
    # body: str = Field(description="뉴스 본문 내용")
    pubDate: str = Field(description="뉴스 발행 일시")



def clean_text(text):
    """네이버 API 결과에 포함된 HTML 태그(<b> 등) 및 특수문자 정적 정제"""
    if not text:
        return ""
    # HTML 엔티티 복원 (예: &quot; -> ")
    text = html.unescape(text)
    # <b>, </b> 등 모든 HTML 태그 제거
    clean_re = re.compile("<.*?>")

    return re.sub(clean_re, "", text)


@tool
async def search_news(
    query: str = Field( ..., description="뉴스 검색 키워드",examples=["삼성전자"]),
    display_count: int = Field(5,description="뉴스 검색 결과 개수, 기본 5건으로 호출",examples=[5]),
) -> list[dict]:
    """"최신 뉴스 검색이 필요할 때 사용하는 도구입니다. 키워드로 네이버 뉴스 검색 결과를 가져옵니다."""
    logger.debug(f"[search_news] called query={query}, display_count={display_count}")

    if not settings.NAVER_CLIENT_ID or not settings.NAVER_CLIENT_SECRET:
        logger.warning(f"[Warning] naver news api config not enoughf. NAVER_CLIENT_ID={settings.NAVER_CLIENT_ID}, NAVER_CLIENT_SECRET={settings.NAVER_CLIENT_SECRET}")
        return []
    
    naver_news_url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        "Content-Type": "application/json",
        "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": settings.NAVER_CLIENT_SECRET,
    }

    params = {"query": query, "display": display_count, "sort": "date"}
    client = await get_httpx_client()

    try:
        response = await client.get(
            naver_news_url,
            headers=headers,
            params=params,
        )
        response.raise_for_status()

        # 4. JSON 데이터 파싱
        data = response.json()
        print(f"\n=== '{query}' 최신 뉴스 검색 결과 ===")
        print(f"{json.dumps(data, indent=4, ensure_ascii=False)}")
        
        news_items:list[News] = []
        for idx, item in enumerate(data.get("items", []), 1):
            news_items.append(
                News(
                    no=idx,
                    title=clean_text(item.get("title", "")),
                    link=item.get("link", ""),
                    description=clean_text(item.get("description", "")),
                    # body=get_naver_news_body(item.get("link", ""),),
                    pubDate=item.get("pubDate", ""),    
                )
            )
        # 결과는 다시 json 리스트로 변환해서 반환    
        return json.dumps(
            [item.model_dump() for item in news_items],
            ensure_ascii=False
        )
    except httpx.HTTPStatusError as exc:
        # 4xx/5xx 응답은 여기로 들어옵니다.
        # 로그에는 상태 코드를 남겨야 장애 원인을 구분할 수 있습니다.
        logger.error(f"Embedding Server API error: {exc.response.status_code} - {exc.response.text}")
        raise
    except httpx.HTTPError as exc:
        # timeout, connect error 등 네트워크 계열 오류입니다.
        logger.error(f"Embedding server request failed: {type(exc).__name__}")
        raise ValueError("임베딩 서버에 연결할 수 없습니다.") from exc

    except Exception as e:
        logger.error(f"Unexpected error during embedding: {str(e)}")
        raise


