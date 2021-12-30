from fastapi import APIRouter, Body, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional, List
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from core.models.orders import OrderModel
from core.models.restaurants import RestaurantModel
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





