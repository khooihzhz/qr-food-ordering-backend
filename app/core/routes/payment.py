from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List
from app.core.models.payment import PaymentModel, UpdatePaymentModel
from app.core.config.config import db

router = APIRouter(
    prefix="/payment",
    tags=['Payment']
)


@router.post("/", response_description="add new payment", response_model=PaymentModel)
async def create_payment(payment: PaymentModel = Body(...)):
    payment = jsonable_encoder(payment)
    new_payment = await db["payments"].insert_one(payment)
    created_payment = await db['payments'].find_one({"_id":new_payment.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_payment)


@router.get("/", response_description="Get all payment", response_model=List[PaymentModel])
async def list_payment():
    payments = await db["payments"].find().to_list(1000)
    return payments


@router.put('/{id}', response_description="Update Payment", response_model=PaymentModel)
async def update_payment(id: str, payment: UpdatePaymentModel):
    payment = {k: v for k, v in payment.dict().items() if v is not None}

    if len(payment) >= 1:
        update_result = await db["payments"].update({"_id": id}, {"$set": payment})
        if update_result.modified_count == 1:
            if(updated_payment := await db["payments"].find_one({"_id": id})) is not None:
                return updated_payment

    if (existing_payment := await db["payments"].find_one({"_id": id})) is not None:
        return existing_payment

    raise HTTPException(status_code=404, detail=f"payment {id} not found")


@router.get("/{id}", response_description="get single payment", response_model=PaymentModel)
async def show_payment(id: str):
    if (payment := await db["payments"].find_one({"_id": id})) is not None:
        print(payment)
        return payment

    raise HTTPException(status_code=404, detail=f"payment {id} not found")


