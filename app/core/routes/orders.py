from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List
from app.core.models.orders import OrderModel, UpdateOrderModel
from app.core.config.config import db

router = APIRouter(
    prefix="/api/orders",
    tags=['Orders']
)


@router.post("/", response_description="Add new Orders", response_model=OrderModel)
async def create_order(order: OrderModel = Body(...)):
    order = jsonable_encoder(order)
    new_order = await db["orders"].insert_one(order)
    created_order = await db["orders"].find_one({"_id": new_order.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_order)


@router.get("/", response_description="List all orders", response_model=List[OrderModel])
async def list_orders():
    orders = await db["orders"].find().to_list(1000)
    return orders


@router.put("/{id}", response_description="Update an order", response_model=OrderModel)
async def update_order(id: str, order: UpdateOrderModel = Body(...)):
    order = {k: v for k, v in order.dict().items() if v is not None}
    if len(order) >= 1:
        update_result = await db["orders"].update_one({"_id":  id}, {"$set": order})
        if update_result.modified_count == 1:
            if (updated_order := await db["orders"].find_one({"_id": id})) is not None:
                return updated_order

    if (existing_order := await db["orders"].find_one({"_id": id})) is not None:
        return existing_order

    raise HTTPException(status_code=404, detail=f"order {id} not found")


@router.get("/{id}", response_description="Get single order", response_model=OrderModel)
async def show_order(id: str):
    if (order := await db["orders"].find_one({"_id": id})) is not None:
        return order

    raise HTTPException(status_code=404, detail=f"order {id} not found")