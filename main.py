import fastapi
import uvicorn
import os
from fastapi import responses
from fastapi.middleware.cors import CORSMiddleware
from api.v1.routers import cars
from core.config import settings, tracker
from database import Base, engine

port = os.getenv("PORT", default=8000)
# initialize database
Base.metadata.create_all(bind=engine)

# initialize model on application startup
tracker.initialize_model()
origins = [
    "http://127.0.0.1:5500",
    "http://127.0.0.1:5000",
    "http://127.0.0.1:3000",
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]
app = fastapi.FastAPI(
    title=settings.APP_NAME,
    version=settings.releaseId,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)

app.include_router(cars.router, prefix=settings.API_V1_STR, tags=["Cars Operations"])


@app.get("/", include_in_schema=False)
async def index() -> responses.RedirectResponse:
    return responses.RedirectResponse(url="/docs")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info", debug=False)
