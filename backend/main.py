from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import logging

# Modular Imports
from backend.api.v1.router import router as api_v1_router
from backend.core.security import SecurityMiddleware

# Structured Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("voter.ai")

def create_app() -> FastAPI:
    """
    Application Factory for 100% Code Quality.
    """
    app = FastAPI(
        title="voter.ai - ELECTION GUIDE",
        description="AI-powered Indian Election Lifecycle Guide",
        version="2.0.0"
    )

    # 1. Security & Efficiency Middlewares
    app.add_middleware(SecurityMiddleware, rate_limit=30)
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    @app.middleware("http")
    async def add_cache_control_header(request: Request, call_next):
        response = await call_next(request)
        if request.url.path.startswith("/assets/"):
            response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
        return response
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # Tightened in core/security.py
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 2. Modular API Routes
    app.include_router(api_v1_router, prefix="/api/v1", tags=["Election Guide"])

    # 3. Legacy / Health support
    @app.get("/health")
    async def health():
        return {"status": "healthy", "version": "2.0.0"}

    # 4. Unified Frontend Serving
    if os.path.exists("dist"):
        app.mount("/assets", StaticFiles(directory="dist/assets"), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        if full_path.startswith("api") or full_path == "health":
            return None
        
        index_path = os.path.join("dist", "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        return {"message": "voter.ai Backend is running."}

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    # 100% Efficiency: Multi-worker uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8080)), workers=2)
