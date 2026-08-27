from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import routes_content_stream

app = FastAPI(title="Project Y API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_content_stream.router)


@app.get("/health")
def health():
    return {"status": "ok"}
