import json

from fastapi import Depends
from langchain.agents import create_agent
from langchain.messages import AIMessage, ToolMessage
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from loguru import logger

from app.core.dependencies import get_chat_models
from app.schemas.chat import ChatRequest, ChatResponse
from app.agents.chat.prompts import build_system_prompt
from app.agents.chat.toolset import resolve_chat_tools
from app.agents.chat.custom_middleware import inject_tool_guidance
from app.core.llm_model import resolve_model_config



CHAT_CHECKPOINTER = InMemorySaver()

class ChatService:
    def __init__(
        self,
        models: dict = Depends(get_chat_models),
    ):
        self.models = models

    def setup_agent(self, payload: ChatRequest):
        resolved = resolve_model_config(payload.llm_config)
        logger.debug(f"provider: {resolved.provider}, model: {resolved.model}")
        config_model = self.models[resolved.provider].with_config(
            configurable={
                "model": resolved.model,
            }
        )
        tools = resolve_chat_tools(payload.tools)
        # tools = all_tools()


        return create_agent(
            model=config_model,
            tools=tools,
            checkpointer=CHAT_CHECKPOINTER,
            system_prompt=build_system_prompt(),
            middleware=[
                SummarizationMiddleware(
                    model=self.models["default"],
                    trigger=("messages", 12),
                    keep=("messages", 10),
                ),
                inject_tool_guidance
            ],
        )

    async def chat(self, payload: ChatRequest) -> ChatResponse:
        session_id = payload.session_id or "anonymous"
        agent = self.setup_agent(payload)

        results = await agent.ainvoke(
            {
                "messages": [{"role": "user", "content": payload.message}],
            },
            config={"configurable": {"thread_id": session_id}},
        )

        messages = results.get("messages")
        content = messages[-1].content if messages else None

        # logger.debug(messages)
        for idx, message in enumerate(messages, 1):
            logger.debug(f"\n====== message {idx}: {message.__class__.__name__} ====================================================\n{message}")

        # 모델에 따라서 AiMessage 객체의 content가 str이 아닌 경우가 존재함
        # dict(json) 결과인 경우 'test' 부분을 찾아서 반환 
        answer = ""
        if isinstance(content, str):
            answer = content
        elif isinstance(content, list):
            for item in content:
                if isinstance(item, str):
                    answer = item
                    break
                elif isinstance(item, dict):
                    text = item.get("text")
                    if text:
                        answer = text


        return ChatResponse(
            session_id=session_id,
            result=answer,
        )

    async def chat_stream(self, payload: ChatRequest):
        yield 'data: {"status": "processing", "message": "AI model is loading..."}\n\n'

        session_id = payload.session_id or "anonymous"
        agent = self.setup_agent(payload)

        async for mode, chunk in agent.astream(
            {
                "messages": [{"role": "user", "content": payload.message}],
            },
            config={"configurable": {"thread_id": session_id}},
            stream_mode=["messages", "updates"],
        ):
            print(mode)
            print(chunk)
            if mode == "messages":
                token, metadata = chunk

                # AiMeesage, ToolMessage 만 진행
                if not ( isinstance(token,AIMessage) or isinstance(token,ToolMessage)):
                    continue
                
                content = getattr(token, "content", None)
                if not content:
                    continue

                if isinstance(content, str):
                    text = content
                elif isinstance(content, list):
                    text = ""
                    for item in content:
                        if isinstance(item, str):
                            text = item
                        elif isinstance(item, dict):
                            text = item.get("text")

                if text:
                    yield f"data: {json.dumps({'type': 'token', 'data': text}, ensure_ascii=False)}\n\n"
                    
            elif mode == "updates":
                logger.debug("mode: updates")
                logger.debug(chunk)

        yield "data: [DONE]\n\n"
