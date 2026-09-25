from pydantic import BaseModel, Field, EmailStr, ConfigDict


class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    age: int = Field(ge=18, le=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=20)
class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    age: int
    email: EmailStr