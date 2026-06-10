# app/agents/tools/registry.py

from app.agents.tools.common.weather_tool import get_weather
from app.agents.tools.common.news_tool import search_news

COMMON_TOOLS = {
    get_weather.name: get_weather,
    search_news.name: search_news,
}

def get_tool(name: str):
    return COMMON_TOOLS.get(name)

def list_tools():
    return [
        {
            "name": tool.name,
            "description": tool.description or "",
        }
        for tool in COMMON_TOOLS.values()
    ]