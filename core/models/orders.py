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
    user: PyObjectId
    amount: float = Field(...)
    paid: bool = Field(...)
    done: bool = Field(...)
    payment: Optional[PyObjectId]
    orders: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UpdateOrderModel(BaseModel):
    user: Optional[PyObjectId]
    amount: Optional[float]
    payment: Optional[PyObjectId]
    paid: Optional[bool]
    done: Optional[bool]
    orders: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


