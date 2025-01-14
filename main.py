from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, create_engine


DATABASE_URL = "postgresql+psycopg2://postgres:admin@localhost/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    task = Column(String, index=True)

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a task

@app.post("/tasks/")
async def create_task(task: str, db=Depends(get_db)):
    new_task = Task(task=task)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"message": "Task created", "id": new_task.id}

# Read all tasks

@app.get("/tasks/")
async def read_tasks(db=Depends(get_db)):
    return db.query(Task).all()

# Read a specific task by ID

@app.get("/tasks/{task_id}")
async def read_task(task_id: int, db=Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Delete a task by ID

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db=Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}