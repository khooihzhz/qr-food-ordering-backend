from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional


# to fix mongo object ID
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class MenuModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    price: int
    description: str
    categories: str
    image: str
    restaurant_id: PyObjectId

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "Product Name",
                "price": 5,
                "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam diam neque, fermentum eu sapien dignissim, facilisis ullamcorper lectus. Suspendisse vulputate vitae eros nec lobortis. Vivamus sagittis arcu vitae nulla placerat.",
                "categories": "Main Dishes",
                "image": "https://i.pravatar.cc",
                "restaurant_id": "61ce7fb31c634173c1853e6b"     # example remove later
            }
        }


class UpdateMenuModel(BaseModel):
    title: Optional[str]
    price: Optional[int]
    description: Optional[str]
    categories: Optional[str]
    image: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
