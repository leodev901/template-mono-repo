from supabase import create_async_client, AsyncClient

from app.core.config import settings
from loguru import logger



async def create_supabase_client() -> AsyncClient | None:
    """Supabase client 생성"""
    supabase_url = settings.SUPABASE_URL
    supabase_key = settings.SUPABASE_KEY

    if not supabase_url or not supabase_key:
        logger.warning("SUPABASE_URL or SUPABASE_KEY is not configured")
        return None

    logger.info("create Supabase client")
    return await create_async_client(supabase_url, supabase_key)
