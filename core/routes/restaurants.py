from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional, List
from core.models.restaurants import RestaurantModel
from core.config.config import db


router = APIRouter(
    prefix="/restaurants",
    tags=['Restaurants']
)


@router.post("/", response_description="Add new restaurant", response_model=RestaurantModel)
async def create_restaurant(restaurant: RestaurantModel = Body(...)):
    restaurant = jsonable_encoder(restaurant)
    new_restaurant = await db["restaurants"].insert_one(restaurant)
    created_restaurant = await db["restaurants"].find_one({"_id": new_restaurant.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_restaurant)


@router.get("/", response_description="List all restaurants", response_model=List[RestaurantModel])
async def list_restaurants():
    restaurants = await db["restaurants"].find().to_list(1000)
    return restaurants



'''
@app.get(
    "/{id}", response_description="Get a single student", response_model=StudentModel
)
async def show_student(id: str):
    if (student := await db["students"].find_one({"_id": id})) is not None:
        return student

    raise HTTPException(status_code=404, detail=f"Student {id} not found")


@app.put("/{id}", response_description="Update a student", response_model=StudentModel)
async def update_student(id: str, student: UpdateStudentModel = Body(...)):
    student = {k: v for k, v in student.dict().items() if v is not None}

    if len(student) >= 1:
        update_result = await db["students"].update_one({"_id": id}, {"$set": student})

        if update_result.modified_count == 1:
            if (
                updated_student := await db["students"].find_one({"_id": id})
            ) is not None:
                return updated_student

    if (existing_student := await db["students"].find_one({"_id": id})) is not None:
        return existing_student

    raise HTTPException(status_code=404, detail=f"Student {id} not found")


@app.delete("/{id}", response_description="Delete a student")
async def delete_student(id: str):
    delete_result = await db["students"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Student {id} not found")
'''

