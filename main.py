from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from database import enigine
from routers import posts, users, auth
# from config import settings
# import model

# model.Base.metadata.create_all(bind=enigine)
api = FastAPI()

origins=['https://www.google.com']

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@api.get("/")
def home():
    return {"message": "FastAPI is running"}

api.include_router(posts.router)
api.include_router(users.router)
api.include_router(auth.router)
