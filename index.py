from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.user import user
from routes.auth import auth

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "authentication",
        "description": "Manage items. So _fancy_ they have their own docs.",
    },
]

app.include_router(user, tags=["users"],prefix="/api/users")
app.include_router(auth, tags=["authentication"], prefix="/api/auth")