from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes import router as api_router

app = FastAPI(title="VeriTask API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

@app.get("/")
def root():
    return {
        "name": "VeriTask API",
        "product": "Human-only work marketplace for World App",
        "version": "0.1.0",
    }

app.include_router(api_router, prefix="/api/v1")
