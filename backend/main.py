from fastapi import FastAPI

import backend.models

from backend.routers.member_router import router as member_router
from backend.routers.board_router import router as board_router
from backend.routers.comment_router import router as comment_router

app = FastAPI(
    title="Board API",
    version="1.0.0"
)

app.include_router(member_router)
app.include_router(board_router)
app.include_router(comment_router)


@app.get("/")
def root():
    return {
        "message": "Board API Server Running"
    }