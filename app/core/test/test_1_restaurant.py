from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# model
"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    firstname: str = Field(...)
    lastname: str = Field(...)
    gender: str = Field(...)
    icNo: str = Field(...)
    contactNo: str = Field(...)
    ssm: str = Field(...)
    restaurantName: str = Field(...)
    restaurantAddress: str = Field(...)
    email: str = Field(...)
    hashed_password: str = Field(...)
"""


# try to sign up
def test_create_restaurant():
    response = client.post("/auth/signup",
                           json={
                                "firstname": "FirstName",
                                "lastname": "LastName",
                                "gender": "male",
                                "icNo": "990804081234",
                                "contactNo": "01234567890",
                                "ssm": "Test-123456",
                                "restaurantName": "The Test",
                                "restaurantAddress": "Test, Test Location",
                                "email": "test@test.com",
                                "hashed_password": "test123"
                           })
    assert response.status_code == 201
    assert response.json() == {
        "_id": response.json()['_id'],
        "firstname": "FirstName",
        "lastname": "LastName",
        "gender": "male",
        "icNo": "990804081234",
        "contactNo": "01234567890",
        "ssm": "Test-123456",
        "restaurantName": "The Test",
        "restaurantAddress": "Test, Test Location",
        "email": "test@test.com",
        "hashed_password": response.json()['hashed_password']
    }


# create account that already existed
def test_create_account_ald_existed():
    response = client.post("/auth/signup",
                           json={
                                "firstname": "FirstName",
                                "lastname": "LastName",
                                "gender": "male",
                                "icNo": "990804081234",
                                "contactNo": "01234567890",
                                "ssm": "Test-123456",
                                "restaurantName": "The Test",
                                "restaurantAddress": "Test, Test Location",
                                "email": "test@test.com",
                                "hashed_password": "test123"
                           })
    assert response.status_code == 409
    assert response.json() == 'Account already exists!'


# login account that is wrong password / username
def test_login_wrong_password():
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = "'grant_type=&username='test@test.com'&password='wrongPassword'&scope=&client_id=&client_secret='"
    response = client.post("/auth/login", headers=headers, data=data)
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Incorrect username or password"
    }


def test_login_wrong_account():
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # dont forget to URL encode it :(
    data = 'grant_type=&username=wrongUserName%40test.com&password=test123&scope=&client_id=&client_secret='
    response = client.post("/auth/login", headers=headers, data=data)
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Incorrect username or password"
    }


# login correctly and get
def test_correct_account():
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = 'grant_type=&username=test%40test.com&password=test123&scope=&client_id=&client_secret='
    response = client.post("/auth/login", headers=headers, data=data)
    assert response.status_code == 200
    assert response.json() == {
        "access_token": response.json()['access_token'],
        "token_type": "bearer"
    }


def test_valid_token_routes():
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = 'grant_type=&username=test%40test.com&password=test123&scope=&client_id=&client_secret='
    response = client.post("/auth/login", headers=headers, data=data)
    jwt_token = response.json()['access_token']
    # test profile here
    headers = {
        "Authorization": "Bearer " + jwt_token
    }

    # get
    response = client.get('/restaurant/profile', headers=headers)
    assert response.status_code == 200
    assert response.json() == {
        "_id": response.json()['_id'],
        "firstname": "FirstName",
        "lastname": "LastName",
        "gender": "male",
        "icNo": "990804081234",
        "contactNo": "01234567890",
        "ssm": "Test-123456",
        "restaurantName": "The Test",
        "restaurantAddress": "Test, Test Location",
        "email": "test@test.com",
        "hashed_password": response.json()['hashed_password']
    }

    # update profile
    response = client.put('/restaurant/profile', headers=headers, json={
        "firstname": "updated_name"
    })

    assert response.status_code == 200
    assert response.json() == {
        "_id": response.json()['_id'],
        "firstname": "updated_name",
        "lastname": "LastName",
        "gender": "male",
        "icNo": "990804081234",
        "contactNo": "01234567890",
        "ssm": "Test-123456",
        "restaurantName": "The Test",
        "restaurantAddress": "Test, Test Location",
        "email": "test@test.com",
        "hashed_password": response.json()['hashed_password']
    }







