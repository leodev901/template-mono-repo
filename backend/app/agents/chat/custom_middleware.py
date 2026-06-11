from typing import Any
from langchain.agents.middleware import before_model, AgentState
from langchain.messages import SystemMessage, ToolMessage
from langgraph.runtime import Runtime
from loguru import logger

from app.agents.chat.prompts import build_common_tool_guide_prompt


@before_model
def inject_tool_guidance(
    state: AgentState,
    runtime: Runtime,
) -> dict[str,Any] | None:
    messages = state["messages"]

    if not messages:
        return None # 메시지 히스토리가 없으면 pass
    
    last_message = messages[-1]
    if not isinstance(last_message, ToolMessage):
        return None # 마지막 메세지가 ToolMessage가 아니면 pass
    
    tool_name = getattr(last_message, "name", None)
    
    guidance = build_common_tool_guide_prompt(tool_name)
    if not guidance:
        return None # guidance가 없는 tool 이라면 pass
    
    # tool에 해당하는 guidance prompt를 SystemMessage로 추가한다.
    return {
        "messages" : [
            SystemMessage(content=guidance)
        ]
    }
        