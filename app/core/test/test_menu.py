from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

"""
---- Menu Model ---- 
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    price: int
    description: str
    categories: str
    image: str
    restaurant_id: PyObjectId
"""

"""
{
    "title": "Product Name",
    "price": 5,
    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam diam neque, fermentum eu sapien dignissim, facilisis ullamcorper lectus. Suspendisse vulputate vitae eros nec lobortis. Vivamus sagittis arcu vitae nulla placerat.",
    "categories": "Main Dishes",
    "image": "https://i.pravatar.cc",
    "restaurant_id": "61ce7fb31c634173c1853e6b"     # example remove later
}
"""


def test_create_menu():
    # Login to get JWT
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
    response = client.get('/restaurant/profile', headers=headers)
    restaurant_id = response.json()['_id']
    sample_item = {
        "title": "Product Name",
        "price": 5,
        "description": "Lorem ipsum dolor sit amet",
        "categories": "Main Dishes",
        "image": "https://i.pravatar.cc",
        "restaurant_id": restaurant_id  # example remove later
    }
    for i in range(2):
        sample_item['title'] = f"Product Name {i}"
        response = client.post("/menu/", headers=headers, json=sample_item)
        assert response.status_code == 201
        assert response.json() == {
            "_id": response.json()['_id'],
            "title": f"Product Name {i}",
            "price": 5,
            "description": "Lorem ipsum dolor sit amet",
            "categories": "Main Dishes",
            "image": "https://i.pravatar.cc",
            "restaurant_id": restaurant_id
        }


