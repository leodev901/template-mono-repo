import os

from langchain_naver_community.tool import (
    NaverNewsSearch,
    NaverBlogSearch,
    # NaverImageSearch,
    NaverSearchResults
)

from app.core.config import settings

os.environ["NAVER_CLIENT_ID"] = settings.NAVER_CLIENT_ID
os.environ["NAVER_CLIENT_SECRET"] = settings.NAVER_CLIENT_SECRET

def build_naver_search_tools():
    news_tool = NaverNewsSearch()
    blog_tool = NaverBlogSearch()
    web_tool = NaverSearchResults()

    news_tool.name = "news_search"
    news_tool.description = (
        "대한민국의 실시간 뉴스 기사, 시사 사건, 정치/경제 동향 및 공식 보도 자료를 검색할 때 이 도구를 사용하세요. "
        "최신 정보나 언론사의 정확한 보도가 필요한 질문에 적합합니다. 입력값은 한국어 검색어 문자열이어야 합니다."
    )

    blog_tool.name = "blog_search"
    blog_tool.description = (
        "한국 사용자들이 작성한 개인적인 후기, 내돈내산 리뷰, 로컬 맛집 및 여행 추천, 실제 경험담을 검색할 때 이 도구를 사용하세요. "
        "딱딱한 뉴스보다 친근하고 생생한 정보나 로컬 맥락이 필요할 때 적합합니다."
    )

    web_tool.name = "web_search"
    web_tool.description = (
        "특정 뉴스 기사나 블로그 후기 맥락이 필요하지 않을 때, 일반적인 한국어 웹 문서, 지식백과, 위키를 검색하기 위해 사용하세요. "
         "또한 뉴스 툴로 해결되지 않는 일반적인 실시간 날씨, 지역 정보, 생활 정보를 검색할 때도 사용합니다."
        "그리고 광범위한 일반 상식을 검색하기 위한 기본(Fallback) 도구로 사용하세요."
    )

    return [news_tool, blog_tool, web_tool]


TOOLS = build_naver_search_tools()