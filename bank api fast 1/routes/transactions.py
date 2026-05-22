from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models import AccountDB

router = APIRouter(
    prefix="/api/v1",
    tags=["Transactions"]
)

# conexión DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# 💰 DEPOSIT
# =========================
@router.post("/deposit")
def deposit(account_id: int, amount: float, db: Session = Depends(get_db)):

    account = db.query(AccountDB).filter(AccountDB.id == account_id).first()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    if amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid amount")

    account.balance += amount
    db.commit()

    return {"message": "Deposit successful", "balance": account.balance}


# =========================
# 🔄 TRANSFER
# =========================
@router.post("/transfer")
def transfer(from_account: int, to_account: int, amount: float, db: Session = Depends(get_db)):

    from_acc = db.query(AccountDB).filter(AccountDB.id == from_account).first()
    to_acc = db.query(AccountDB).filter(AccountDB.id == to_account).first()

    if not from_acc or not to_acc:
        raise HTTPException(status_code=404, detail="Account not found")

    if amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid amount")

    if from_acc.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    from_acc.balance -= amount
    to_acc.balance += amount

    db.commit()

    return {"message": "Transfer successful"}