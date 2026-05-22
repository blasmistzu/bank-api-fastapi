from pydantic import BaseModel

# 🔹 USER
class User(BaseModel):
    id: int
    name: str
    email: str


# 🔹 ACCOUNT
class Account(BaseModel):
    id: int
    user_id: int
    balance: float