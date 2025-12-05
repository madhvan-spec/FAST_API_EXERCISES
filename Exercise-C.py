# Task-1: Create a User model and POST endpoint to create users
# Task-2: Build a Product model with validation (name, price > 0, description)
# Task-4: Add email validation to user creation
from typing import Annotated
from fastapi import FastAPI , Path , HTTPException
from pydantic import BaseModel , EmailStr , Field

app = FastAPI()

class UserCreate(BaseModel):
    name : str
    email : EmailStr

class User(BaseModel):
    id : int
    name : str
    email : EmailStr

class ProductCreate(BaseModel):
    name : str
    price : float = Field(gt=0,title="Price must be Greater than zero")
    description: str | None = Field(
        default=None, title="The description of the item"
    )

class Product(BaseModel):
    id : int
    name : str
    price : float = Field(gt=0,title="Price must be Greater than zero")
    description: str | None = Field(
        default=None, title="The description of the item"
    )


users_db = []
next_id = 1
products_db = []
product_next_id = 1

@app.get("/")
async def root():
    return {"message" : "welcome!"}

@app.post("/users",response_model=User)
async def create_user(user : UserCreate):
    global next_id

    new_user = User(
        id = next_id,
        name = user.name,
        email=user.email
    )

    users_db.append(new_user)
    next_id +=1

    return new_user

@app.get("/users")
async def show_user():
    return users_db

@app.get("/users/{user_id}", response_model=User)
async def show_particular_user(
    user_id: Annotated[int, Path(gt=0, title="User ID must be greater than 0")]
):
    for user in users_db:
        if user.id == user_id:
            return user

    raise HTTPException(status_code=404, detail="User not found")

@app.post("/products",response_model=Product)
async def create_product(product : ProductCreate):
    global product_next_id

    new_product = Product(
        id=product_next_id,
        name=product.name,
        price=product.price,
        description=product.description
    )

    products_db.append(new_product)
    product_next_id +=1

    return new_product

@app.get("/products")
async def show_products():
    return products_db