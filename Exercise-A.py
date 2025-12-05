# Task-1: Create a "Hello World" API with a root endpoint
# Task-2: Build an API with multiple endpoints (/, /about, /contact)
# Task-3: Create a /greet/{name} endpoint that returns a personalized greeting
# Task-4: Add a /calculate/{operation}/{num1}/{num2} endpoint

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message" : "Hello World"}

@app.get("/about")
async def about():
    return {"message": "Hello, this is my first time using FastAPI"}

@app.get("/contact")
async def contact():
   return {
        "message": "Hello, this is Madhvan. You can connect with me on",
        "phone": "9313124489",
        "email": "madhvan@xylisys.com"
    }
    
@app.get("/greet/{name}")
async def greet(name):
    return {
        "message" : f"Hello!\nWelcome to Xylisys.com {name}"
    }

@app.get("/calculate/{operation}/{num1}/{num2}")
async def calc(operation: str, num1: int, num2: int):
    if operation not in ["add", "sub", "mul", "div"]:
        return {"error": "Invalid Operation"}

    if operation == "add":
        ans = num1 + num2
    elif operation == "sub":
        ans = num1 - num2
    elif operation == "mul":
        ans = num1 * num2
    elif operation == "div":
        if num2 == 0:
            return {"error": "Division by zero"}
        ans = num1 / num2

    return {"result": f"{num1} {operation} {num2} = {ans}"}
