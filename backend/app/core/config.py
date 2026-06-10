from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Application
    APP_NAME: str = "Sample FastAPI"
    APP_VERSION: str = "0.1.0"
    APP_ENV: str = "local"
    APP_LOG_LEVEL: str = "DEBUG"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8080

    # llm api keys
    OPENAI_API_KEY: str | None = None
    GEMINI_API_KEY: str | None = None

    # supabase
    SUPABASE_URL: str | None = None
    SUPABASE_KEY: str | None = None
    # database


    # LangSmith 설정 (선택적 - 없으면 트레이싱 비활성화)
    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_ENDPOINT: str = "https://api.smith.langchain.com"
    LANGCHAIN_API_KEY: str = ""

    # NAVER - News API
    NAVER_CLIENT_ID: str | None = None
    NAVER_CLIENT_SECRET: str | None = None



settings = Settings()
    