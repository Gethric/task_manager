from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from db.models import Task
from db.session import get_db
from tasks.schemas import TaskCreate

router = APIRouter()

# Create a new task
@router.post("/")
async def create_task(task: TaskCreate = Body(...), db: Session = Depends(get_db)):
    new_task = Task(task=task.task)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"message": "Task created", "id": new_task.id}

# List all tasks
@router.get("/")
async def read_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks

# Get a specific task by ID
@router.get("/{task_id}")
async def read_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found.")
    return task

# Delete a task by ID
@router.delete("/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found.")
    db.delete(task)
    db.commit()
    return {"message": f"Task with ID {task_id} deleted successfully."}
