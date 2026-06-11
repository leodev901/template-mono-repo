from app.agents.tools.registry import get_common_tools, resolve_tools


def resolve_chat_tools(tool_names: list[str] | None):
    return resolve_tools(tool_names, get_common_tools())