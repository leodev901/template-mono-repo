from fastapi import Depends
from supabase import AsyncClient
from app.core.dependencies import get_supabase_client

class HealthSupabaseRepository:
    def __init__(self, supabase: AsyncClient = Depends(get_supabase_client)):
        self.supabase = supabase

    async def select_one(self, schema_name:str, table_name:str):
        """요청 받은 '스미카'와 '테이블'의 데이터를 1건 조회 한다 -> health check"""
        resp = await self.supabase.schema(schema_name).table(table_name).select("*").limit(1).execute()
        return resp.data    