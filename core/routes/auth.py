from fastapi import APIRouter, Body, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional, List
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from core.models.auth import AuthModel, Token, TokenData
from core.models.restaurants import RestaurantModel
from core.config.config import db
from jose import JWTError, jwt
from passlib.context import CryptContext

router = APIRouter(
    prefix="/auth",
    tags=['Auth']
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Change secret Key Later
SECRET_KEY = "add986cf5fa42e2abfce7f35be057f7d3909b663d84deee789e362486cf6aa1c" # should not show here

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def get_account(email: str):
    if (account := await db["restaurants"].find_one({"email": email})) is not None:
        return account


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def authenticate_user(email: str, password: str):
    account = await get_account(email)
    if not account:
        return False
    if not verify_password(password, account["hashed_password"]):
        return False
    return account


# verify jwt
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # verify your jwt token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    account = await get_account(email=token_data.email)
    if account is None:
        raise credentials_exception
    return account


@router.post("/signup", response_description="Add new restaurant account", response_model=RestaurantModel)
async def create_restaurant(restaurant: RestaurantModel = Body(...)):
    restaurant = jsonable_encoder(restaurant)

    if (await db["restaurants"].find_one({"email": restaurant["email"]})) is None:
        restaurant['hashed_password'] = get_password_hash(restaurant['hashed_password'])
        new_restaurant = await db["restaurants"].insert_one(restaurant)
        created_restaurant = await db["restaurants"].find_one({"_id": new_restaurant.inserted_id})
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_restaurant)
    else:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content="Account already exists!")


# generate JWT Tokens
@router.post("/login", response_description="Login restaurant account", response_model=Token)
async def login_account(form_data: OAuth2PasswordRequestForm = Depends()):
    account = await authenticate_user(form_data.username, form_data.password)
    # if account does not exist
    if not account:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": account["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

"""
# Figure Out do u need this?

async def create_account(account):
    account['hashed_password'] = get_password_hash(account['hashed_password'])
    new_account = await db["accounts"].insert_one(account)
    created_account = await db["accounts"].find_one({"_id": new_account.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_account)
"""


