import os

import uvicorn
from fastapi import FastAPI, HTTPException

import storage
from routes import router

app = FastAPI(title="ip-geolocation")
app.include_router(router)


@router.get("/health")
async def health_check():
    try:
        is_connected = await storage.r.ping()
        if is_connected:
            return {
                "status": "healthy",
                "redis": "connected",
            }
    except Exception as e:
        print(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Redis unavailable")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=os.getenv("DB_PORT", 8000),
        reload=True,
    )
