from fastapi import FastAPI
from core.routes import restaurants, users, menu, orders, payment, auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(restaurants.router)
app.include_router(users.router)
app.include_router(menu.router)
app.include_router(orders.router)
app.include_router(payment.router)
app.include_router(auth.router)

"""
# APIv2
app.include_router(users.router)
app.include_router(orders.router)
"""

