from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.user import user
from routes.auth import auth
from routes.ticket import ticket
from routes.cart import cart
from routes.booking import booking
from routes.voucher import voucher

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
app.include_router(ticket, tags=["tickets"], prefix="/api/tickets")
app.include_router(cart, tags=["cart"], prefix="/api/cart")
app.include_router(booking, tags=["booking"], prefix="/api/booking")
app.include_router(voucher, tags=["voucher"], prefix="/api/voucher")