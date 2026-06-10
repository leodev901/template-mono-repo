from typing import Annotated
from pydantic import Field
from langchain.tools import tool
from loguru import logger


@tool
def get_weather(
    location: Annotated[str, Field(...,description="Weather lookup location, e.g. 서울")],
) -> str:
    """Get current weather information for a location."""
    logger.debug(f"[get_weather] called location={location}")

    return f"오늘 {location} 날씨는 자전거 입니다."

