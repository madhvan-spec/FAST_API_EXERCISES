# Task-5: Create a /users/{user_id} endpoint to fetch user details
# Task-6: Build a /search endpoint with query parameters for filtering
# Task-7: Create a /products endpoint with pagination (page, limit)
from fastapi import FastAPI , Query
from typing import Annotated

app = FastAPI()


users_db = {
    1: {"id": 1, "name": "Madhvan", "email": "madhvan@xylisys.com"},
    2: {"id": 2, "name": "Het", "email": "het@xylisys.com"},
}

@app.get("/")
async def root():
    return {"Message" : "Welcome to FASTAPI"}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id not in users_db:
        return {"Error" : "Not Found"}
    else:
        return users_db[user_id]


items_db = [
    {"id": 1, "name": "Laptop", "category": "electronics", "price": 1200},
    {"id": 2, "name": "Headphones", "category": "electronics", "price": 150},
    {"id": 3, "name": "Shirt", "category": "clothing", "price": 30},
    {"id": 4, "name": "Shoes", "category": "clothing", "price": 75},
    {"id": 5, "name": "Keyboard", "category": "electronics", "price": 90},
    {"id": 6, "name": "Mouse", "category": "electronics", "price": 40},
    {"id": 7, "name": "Monitor", "category": "electronics", "price": 300},
    {"id": 8, "name": "Jacket", "category": "clothing", "price": 120},
    {"id": 9, "name": "Backpack", "category": "clothing", "price": 60},
    {"id": 10, "name": "Smartphone", "category": "electronics", "price": 900},
    {"id": 11, "name": "Tablet", "category": "electronics", "price": 450},
    {"id": 12, "name": "Sweater", "category": "clothing", "price": 50},
    {"id": 13, "name": "Watch", "category": "electronics", "price": 250},
    {"id": 14, "name": "Jeans", "category": "clothing", "price": 45},
    {"id": 15, "name": "Camera", "category": "electronics", "price": 800},
    {"id": 16, "name": "Speakers", "category": "electronics", "price": 180},
    {"id": 17, "name": "Hat", "category": "clothing", "price": 20},
    {"id": 18, "name": "Socks", "category": "clothing", "price": 10},
    {"id": 19, "name": "Drone", "category": "electronics", "price": 650},
    {"id": 20, "name": "Fitness Tracker", "category": "electronics", "price": 130},
]

@app.get("/search")
async def search_items(
    name: str | None = None,
    category: str | None = None,
    max_price: int | None = None,
    min_price: int | None = None,
):
    results = items_db

    if name:
        results = [i for i in results if name.lower() in i["name"].lower()]
    if category:
        results = [i for i in results if i["category"] == category]
    if min_price is not None:
        results = [i for i in results if i["price"] >= min_price]
    if max_price is not None:
        results = [i for i in results if i["price"] <= max_price]

    return results

from fastapi import FastAPI, Query

@app.get("/items")
async def get_products(
    page: int | None = 0,
    limit: int | None = 0 ,
):
    start = (page - 1) * limit
    end = start + limit
    data = items_db[start:end]

    return {
        "page": page,
        "limit": limit,
        "total": len(items_db),
        "items": data,
    }

@app.get("/validate/{num1}/{num2}")
async def validate(num1 : int , num2 : int):
    if(num1<0 or num2<0):
        return {"Error" : "Numeric Values cannot be less than zero"}
    else:
        return {"Number1" : num1 , "Number2" : num2}
    
