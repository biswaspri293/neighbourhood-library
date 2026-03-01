from fastapi import FastAPI
import uvicorn
import logging
from app.utils.logging_config import setup_logging
from app.routers import books, members, borrowings
from fastapi.middleware.cors import CORSMiddleware
from app.utils.db import close_pool
from app.utils.db_middleware import db_session_middleware

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="Neighborhood Library Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(db_session_middleware)

@app.on_event("shutdown")
def shutdown_event():
    close_pool()

app.include_router(books.router, prefix="/api/books", tags=["Books"])
app.include_router(members.router, prefix="/api/members", tags=["Members"])
app.include_router(borrowings.router, prefix="/api/borrowings", tags=["Borrowings"])

@app.get("/health", tags=["Health"])
def health_check():
    logger.info("Health check endpoint called")
    return {"status": "ok"}


# Entry point for: python -m app.main
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )