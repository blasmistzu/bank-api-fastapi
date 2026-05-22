from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import engine, SessionLocal
from models import Base, UserDB, AccountDB
from routes.users import router as users_router
from routes.accounts import router as accounts_router
from routes.transactions import router as transactions_router

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users_router)
app.include_router(accounts_router)
app.include_router(transactions_router)

# 🔹 MODELOS (validación)


# 🔹 DEPENDENCIA DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔹 ROOT
@app.get("/")
def home():
    return {"message": "Bank API running"}


# =========================
# 👤 USERS
# =========================
# =========================
# 💳 ACCOUNTS
# =========================
# =========================
# 💰 DEPOSIT
# =========================
# =========================
# 🔄 TRANSFER
# =========================