import datetime
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from database import SessionLocal
from typing import List
import models

app = FastAPI()


class DTO(BaseModel):
    description: str


class Task(BaseModel):
    id: int
    description: str
    is_done: bool
    created_at: datetime.datetime

    # deleted_at:datetime.datetime | None

    class Config:
        orm_mode = True


db = SessionLocal()


@app.get("/ap1/v1/tasks", response_model=List[Task], status_code=200)
async def get_tasks(is_deleted:bool = False):
    if is_deleted:
        tasks = db.query(models.Task).order_by(models.Task.id).all()
        return tasks

    tasks = db.query(models.Task).filter(models.Task.deleted_at.is_(None))
    return tasks.all()


# show one task
@app.get("/ap1/v1/task/{task_id}", response_model=Task, status_code=status.HTTP_200_OK)
async def get_task(task_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task.deleted_at is None:
        return task
    raise HTTPException(
        status_code=404,
        detail=f"Task with id {task_id} does not exist"
    )


@app.post("/ap1/v1/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
async def add_task(task: DTO):
    new_task = models.Task(
        description=task.description
    )
    # add new date to our database
    db.add(new_task)
    # save changes in our database
    db.commit()

    return new_task


@app.put("/ap1/v1/tasks/{task_id}", response_model=Task, status_code=status.HTTP_200_OK)
async def completed_task(task_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    task.is_done = True

    db.commit()

    return task


@app.delete("/ap1/v1/tasks/{task_id}")
async def delete_task(task_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task.deleted_at is None:
        task.deleted_at = datetime.datetime.utcnow()
        db.commit()
        return task

    raise HTTPException(
        status_code=404,
        detail=f"Task with id {task_id} does not exist")

# hi
