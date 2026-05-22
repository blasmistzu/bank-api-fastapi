from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import Base, UserDB, TaskDB
from schemas import User, Task

app = FastAPI()

Base.metadata.create_all(bind=engine)


# DATABASE SESSION
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# USERS
# =========================

@app.post("/users")
def create_user(user: User, db: Session = Depends(get_db)):

    db_user = UserDB(
        id=user.id,
        name=user.name,
        email=user.email
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@app.get("/users")
def get_users(db: Session = Depends(get_db)):

    return db.query(UserDB).all()


# =========================
# TASKS
# =========================

@app.post("/tasks")
def create_task(task: Task, db: Session = Depends(get_db)):

    user = db.query(UserDB).filter(UserDB.id == task.user_id).first()

    if not user:
        return {"error": "User not found"}

    db_task = TaskDB(
        id=task.id,
        title=task.title,
        description=task.description,
        user_id=task.user_id,
        status=task.status
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):

    return db.query(TaskDB).all()


@app.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    status: str,
    db: Session = Depends(get_db)
):

    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()

    if not task:
        return {"error": "Task not found"}

    task.status = status

    db.commit()
    db.refresh(task)

    return {
        "message": "Task updated",
        "task": task
    }


@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):

    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()

    if not task:
        return {"error": "Task not found"}

    db.delete(task)
    db.commit()

    return {"message": "Task deleted"}


# =========================
# HOME
# =========================

@app.get("/")
def home():

    return {"message": "Task Manager API running"}