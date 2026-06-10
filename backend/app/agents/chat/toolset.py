from app.agents.tools.registry import COMMON_TOOLS

# setup common chat tools

CHAT_TOOL_NAMES = [
    "get_weather",
    "search_news",
]

def resolve_tools(tool_names: list[str] | None):
    allowed = {name: COMMON_TOOLS[name] for name in CHAT_TOOL_NAMES}
    if not tool_names:
        return []

    return [allowed[name] for name in tool_names if name in allowed]
