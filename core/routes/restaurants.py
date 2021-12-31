from fastapi import APIRouter, Body, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional, List
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from core.models.orders import OrderModel
from core.models.restaurants import RestaurantModel, UpdateRestaurantModel
from core.config.config import db
from core.models.menu import MenuModel
from core.routes.auth import get_current_user

router = APIRouter(
    prefix="/restaurant",
    tags=['Restaurant']
)


@router.get("/", response_description="List all restaurants", response_model=List[RestaurantModel])
async def list_restaurants():
    restaurants = await db["restaurants"].find().to_list(1000)
    return restaurants


@router.get("/orders/{id}", response_description="Get restaurant's order", response_model=OrderModel)
async def show_order(id: str, restaurant: RestaurantModel = Depends(get_current_user)):
    orders = await db["orders"].find({"restaurant_id": restaurant['_id']}).to_list(1000)
    return orders


@router.get("/menu/{id}", response_description='List all menu Item from the restaurant', response_model=List[MenuModel])
async def list_menuitem(id: str):
    menu_items = await db["menu"].find({"restaurant_id": id}).to_list(1000)
    return menu_items


@router.get("/profile", response_description="get restaurant details", response_model=RestaurantModel)
async def show_profile(restaurant: RestaurantModel = Depends(get_current_user)):
    return restaurant


@router.put("/profile", response_description="Update restaurant profile", response_model=RestaurantModel)
async def update_profile(update_restaurant: UpdateRestaurantModel = Body(...),
                         restaurant: RestaurantModel = Depends(get_current_user)):
    update_restaurant = {k: v for k, v in update_restaurant.dict().items() if v is not None}
    if len(update_restaurant) >= 1:
        update_result = await db["restaurants"].update_one({"_id":  restaurant['_id']}, {"$set": update_restaurant})
        if update_result.modified_count == 1:
            if (updated_restaurant := await db["restaurants"].find_one({"_id": restaurant['_id']})) is not None:
                return updated_restaurant

    if (existing_profile := await db["restaurants"].find_one({"_id": restaurant['_id']})) is not None:
        return existing_profile

    raise HTTPException(status_code=404, detail=f"item {id} not found")

