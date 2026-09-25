
from fastapi import FastAPI
from agent_tool import router as user_router
app = FastAPI()
app.include_router(user_router)


