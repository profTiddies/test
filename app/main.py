
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.user import userRouter
from app.routers.post import postRouter
from app.routers.vote import voteRouter
from app.auth import authRouter

app = FastAPI()

origins = [
    "http://localhost:8080",
    "http://localhost",
    "https://www.google.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(userRouter)
app.include_router(postRouter)
app.include_router(authRouter)
app.include_router(voteRouter)


