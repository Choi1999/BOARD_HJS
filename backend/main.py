from fastapi import FastAPI

import backend.models

from backend.routers.member_router import router as member_router
from backend.routers.board_router import router as board_router
from backend.routers.comment_router import router as comment_router
from backend.exceptions.custom_exception import (
    CustomException
)
from fastapi.middleware.cors import CORSMiddleware 

from backend.exceptions.exception_handler import (
    custom_exception_handler,
    global_exception_handler
)
app = FastAPI(
    title="Board API",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_exception_handler(
    CustomException,
    custom_exception_handler
)

app.add_exception_handler(
    Exception,
    global_exception_handler
)
app.include_router(member_router)
app.include_router(board_router)
app.include_router(comment_router)


@app.get("/")
def root():
    return {
        "message": "Board API Server Running"
    }