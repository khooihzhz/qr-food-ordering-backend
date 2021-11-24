from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional, List
from core.models.payment import PaymentModel
from core.models.orders import OrderModel
from core.config.config import db

router = APIRouter(
    prefix="/payment",
    tags=['Payment']
)


@router.post("/", response_description="add new payment", response_model=PaymentModel)
async def create_payment(payment: PaymentModel,
                         order: OrderModel = Body(...)):
    payment = jsonable_encoder(payment)
    new_payment = await db["payments"].insert_one(payment)
    created_payment = await db['payments'].find_one({"_id":new_payment.inserted_id})



