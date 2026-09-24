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