from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.api.endpoints.health_router import api_router as health_router
from app.api.endpoints.chat_router import api_router as chat_router
from app.api.endpoints.legal_agent_router import api_router as legal_agent_router






def register_routes(app:FastAPI):

    app.include_router(health_router)
    app.include_router(chat_router)
    app.include_router(legal_agent_router)

    @app.get("/")
    async def root():
        return RedirectResponse(url="/docs")



    
    

    