from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models import UserDB
from schemas import User

router = APIRouter(
    prefix="/api/v1",
    tags=["Users"]
)

# 🔹 conexión DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# 👤 USERS
# =========================

@router.post("/users")
def create_user(user: User, db: Session = Depends(get_db)):

    existing_user = db.query(UserDB).filter(UserDB.id == user.id).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    db_user = UserDB(id=user.id, name=user.name, email=user.email)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(UserDB).all()