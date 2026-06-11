from langchain.chat_models import init_chat_model
from pydantic import BaseModel
from loguru import logger
from app.core.config import settings
from app.schemas.chat import LlmConfig



# 요청 리퀘스트 alias에 대한 provider와 model 매핑
MODEL_CONFIG_ALIASES = {
  "gemini": {
        "provider": "google_genai",
        "models": {
            "fast": "gemini-2.5-flash-lite",
            # "fast": "gemini-2.5-flash",
            "advanced": "gemini-3-flash-preview",
            # "advanced": "gemini-3.5-flash",
        },
    },
    "chatgpt": {
        "provider": "openai",
        "models": {
            "fast": "gpt-5-nano",
            "advanced": "gpt-5",
        },
    },
    "grok": {
        "provider": "xai",
        "models": {
            "fast": "grok-beta"
        },
    },
}

# 서비스 기동시 provider 별 chat_model 초기화 setup
def create_chat_models():
    models = {}
    if getattr(settings,"OPENAI_API_KEY",None):
        models["openai"] = init_chat_model(
            model=getattr(settings,"OPENAI_MODEL","gpt-5-nano"),
            model_provider="openai",
            api_key=settings.OPENAI_API_KEY,
            configurable_fields=("model",)
            # temperature=0.7,
            # max_tokens=1000,
            # timeout=30,
        )
        logger.info("LangChain OpenAI Chat Models Created")
        
    if getattr(settings,"GEMINI_API_KEY",None):
        models["google_genai"] = init_chat_model(
            model=getattr(settings,"GEMINI_MODEL","gemini-2.5-flash-lite"),
            model_provider="google_genai",
            api_key=settings.GEMINI_API_KEY,
            configurable_fields=("model",)
            # temperature=0.7,
            # max_tokens=1000,
            # timeout=30,
        )
        #default model 무조건 생성 해야 함
        models["default"] = init_chat_model(
            model=getattr(settings,"GEMINI_MODEL","gemini-2.5-flash-lite"),
            model_provider="google_genai",
            api_key=settings.GEMINI_API_KEY,
            # temperature=0.7,
            # max_tokens=1000,
            # timeout=30,
        )
        logger.info("LangChain GEMINI Chat Models Created")
    return models

class ResolvedModelConfig(BaseModel):
    provider: str
    model: str

def resolve_model_config(request_config: LlmConfig) -> ResolvedModelConfig:
    provider_alias  = request_config.provider
    if not provider_alias in MODEL_CONFIG_ALIASES:
        raise ValueError(f"Unsupported provider: {provider_alias}")
    
    model_alias = request_config.model
    if not model_alias in MODEL_CONFIG_ALIASES[provider_alias]["models"]:
        raise ValueError(f"Unsupported model '{model_alias}' in provider '{provider_alias}'")
    
    return ResolvedModelConfig(
        provider=MODEL_CONFIG_ALIASES[provider_alias]["provider"],
        model=MODEL_CONFIG_ALIASES[provider_alias]["models"][model_alias]
    )
