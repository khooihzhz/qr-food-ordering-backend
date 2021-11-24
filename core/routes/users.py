from fastapi import APIRouter, Body, status, HTTPException
from fastapi.responses import JSONResponse
from core.models.users import UserModel, UpdateUserModel
from typing import List
from fastapi.encoders import jsonable_encoder
from core.config.config import db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


# User API
@router.post("/", response_description="Create New User", response_model=UserModel)
async def create_user(user: UserModel = Body(...)):
    user = jsonable_encoder(user)
    new_user = await db["users"].insert_one(user)
    created_user = await db["users"].find_one({"_id": new_user.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)


@router.get("/", response_description="Get All User", response_model=List[UserModel])
async def list_users():
    users = await db["users"].find().to_list(1000)
    return users


@router.put("/{id}", response_description="Update Table Number", response_model=UserModel)
async def update_user(id: str, user: UpdateUserModel = Body(...)):
    user = {k: v for k, v in user.dict().items() if v is not None}

    # check request body length
    if len(user) >= 1:
        update_result = await db["users"].update_one({"_id": id}, {"$set": user})

        if update_result.modified_count == 1:
            if (updated_user := await db["users"].find_one({"_id": id})) is not None:
                return updated_user

    if (existing_user := await db["users"].find_one({"_id": id})) is not None:
        return existing_user

    raise HTTPException(status_code=404, detail=f"User {id} not found")


@router.get("/{id}", response_description="Get single user", response_model=UserModel)
async def show_user(id: str):
    if (user := await db["users"].find_one({"_id": id})) is not None:
        return user

    raise HTTPException(status_code=404, detail=f"user {id} not found!")
