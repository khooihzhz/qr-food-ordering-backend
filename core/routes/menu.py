from fastapi import APIRouter, Body, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional, List
from core.models.menu import MenuModel, UpdateMenuModel
from core.config.config import db
from core.models.restaurants import RestaurantModel
from core.routes.auth import get_current_user

router = APIRouter(
    prefix='/menu',
    tags=['Menu']
)


@router.post('/', response_description="Add menu item", response_model=MenuModel)
async def create_menuitem(menuitem: MenuModel = Body(...), restaurant: RestaurantModel = Depends(get_current_user)):
    menuitem = jsonable_encoder(menuitem) # dictionary
    menuitem['restaurant_id'] = restaurant['_id']
    new_menuitem = await db["menu"].insert_one(menuitem)
    created_menuitem = await db["menu"].find_one({"_id": new_menuitem.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_menuitem)


@router.put("/{id}", response_description="Update menu item", response_model=MenuModel)
async def update_menu(id: str, menu: UpdateMenuModel = Body(...), restaurant: RestaurantModel = Depends(get_current_user)):
    menu = {k: v for k, v in menu.dict().items() if v is not None}
    if len(menu) >= 1:
        update_result = await db["menu"].update_one({"_id":  id}, {"$set": menu})
        if update_result.modified_count == 1:
            if (updated_menu := await db["menu"].find_one({"_id": id})) is not None:
                return updated_menu

    if (existing_menu_item := await db["menu"].find_one({"_id": id})) is not None:
        return existing_menu_item

    raise HTTPException(status_code=404, detail=f"item {id} not found")


@router.delete("/{id}", response_description="Delete a menu item")
async def delete_menu_item(id: str, restaurant: RestaurantModel = Depends(get_current_user)):
    delete_result = await db["menu"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"item {id} not found")