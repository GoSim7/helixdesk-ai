from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.admin.routes import router as admin_router
from app.api.runtime.routes import router as runtime_router
from app.db.bootstrap import init_db
from app.core.scheduler import scheduler_service


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    scheduler_service.start()
    try:
        yield
    finally:
        scheduler_service.shutdown()


app = FastAPI(
    title="AI Customer Platform Control API",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(admin_router, prefix="/api/admin", tags=["admin"])
app.include_router(runtime_router, prefix="/api/runtime", tags=["runtime"])


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "AI Customer Platform Control API"}
