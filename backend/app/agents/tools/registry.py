# app/agents/tools/registry.py

from app.agents.tools.common.weather_tool import TOOLS as WEATHER_TOOLS
from app.agents.tools.common.news_tool import TOOLS as NEWS_TOOLS
from app.agents.tools.common.naver_search_tools import TOOLS as NAVER_TOOLS


COMMON_TOOLS = [
    *WEATHER_TOOLS,
    *NEWS_TOOLS,
    *NAVER_TOOLS,
]

def list_tools():
    all_tools = [
        *COMMON_TOOLS
    ]
    return [
        {
            "name": tool.name,
            "description": tool.description,
        }
        for tool in all_tools
    ]


def get_common_tools():
    return COMMON_TOOLS


# def get_legal_tools():
#     return LEGAL_TOOLS


def resolve_tools(tool_names: list[str] | None, candidates: list):
    if not tool_names:
        return []

    tool_map = {tool.name: tool for tool in candidates}

    return [
        tool_map[name]
        for name in tool_names
        if name in tool_map
    ]