from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models import AccountDB, UserDB
from schemas import Account

router = APIRouter(
    prefix="/api/v1",
    tags=["Accounts"]
)

# 🔹 conexión DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# 💳 ACCOUNTS
# =========================

@router.post("/accounts")
def create_account(account: Account, db: Session = Depends(get_db)):

    # validar usuario
    user = db.query(UserDB).filter(UserDB.id == account.user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # evitar duplicados
    existing_account = db.query(AccountDB).filter(AccountDB.id == account.id).first()

    if existing_account:
        raise HTTPException(status_code=400, detail="Account already exists")

    db_account = AccountDB(
        id=account.id,
        user_id=account.user_id,
        balance=account.balance
    )

    db.add(db_account)
    db.commit()
    db.refresh(db_account)

    return db_account


@router.get("/accounts")
def get_accounts(db: Session = Depends(get_db)):
    return db.query(AccountDB).all()


@router.get("/accounts/{account_id}")
def get_account(account_id: int, db: Session = Depends(get_db)):

    account = db.query(AccountDB).filter(AccountDB.id == account_id).first()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    return account