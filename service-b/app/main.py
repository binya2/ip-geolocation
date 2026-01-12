import os

import uvicorn
from fastapi import FastAPI

from routes import router

app = FastAPI(title="ip-geolocation")
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=os.getenv("DB_PORT", 8000),
        reload=True,
    )
