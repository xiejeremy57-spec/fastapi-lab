from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def index():
    return {"message": "Hello FastAPI"}
@app.get("/users/{user_id}")
async def user_profile(user_id:int):
    return {
        "id":user_id,
        "name":"zhangsan"
    }
@app.get("/search")
async def search_user(name:str,age:int):
    return{
        "name":name,
        "age":age
    }
@app.get("/products")
async def product(name:str,min_price:float,max_price:float|None=None):
    return {
    "name": "iphone",
    "min_price": 3000.0,
    "max_price": 8000.0
}