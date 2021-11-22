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


class OrderModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    done: bool = Field(...)
    amount: int = Field(...)
    user: PyObjectId
    payment: Optional[PyObjectId]
    orders: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UpdateOrderModel(BaseModel):
    user: Optional[PyObjectId]
    amount: Optional[int]
    payment: Optional[PyObjectId]
    done: Optional[bool]
    orders: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}