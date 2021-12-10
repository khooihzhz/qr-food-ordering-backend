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


class RestaurantModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    firstname: str = Field(...)
    lastname: str = Field(...)
    address: str = Field(...)
    gender: str = Field(...)
    icNo: str = Field(...)
    contactNo: str = Field(...)
    ssm: str = Field(...)
    restaurantName: str = Field(...)
    restaurantAddress: str = Field(...)
    emailAddress: str = Field(...)
    # password -> ?
    # username -> string?
    # email -> string?
    # SSM -> string?
    # phone number -> string?

    # restaurant urlstring -> string?
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UpdateRestaurantModel(BaseModel):
    name: Optional[str]
    address: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

