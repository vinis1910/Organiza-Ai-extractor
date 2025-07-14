from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.services.monitor_middleware import ResourceMonitorMiddleware
from src.api.extract_routes import router as extract_router

app = FastAPI(version="0.1.0")

origins = ["http://localhost:8000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["*"],
)
app.add_middleware(ResourceMonitorMiddleware)


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}


app.include_router(extract_router, prefix="/api")
