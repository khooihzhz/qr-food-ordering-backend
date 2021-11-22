from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional, List
from core.models.menu import MenuModel, UpdateMenuModel
from core.config.config import db

router = APIRouter(
    prefix='/menu',
    tags=['Menu']
)


@router.post('/', response_description="Add menu item", response_model=MenuModel)
async def create_menuItem(menuItem: MenuModel = Body(...)):
    menuItem = jsonable_encoder(menuItem)
    new_menuItem = await db["menu"].insert_one(menuItem)
    created_menuItem = await db["menu"].find_one({"_id": new_menuItem.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_menuItem)


@router.get("/", response_description='List all menu Item', response_model=List[MenuModel])
async def list_menuItem():
    menuItems = await db["menu"].find().to_list(1000)
    return menuItems
