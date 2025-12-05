from typing import Annotated
from fastapi import Body, FastAPI , Path , Query , HTTPException , status
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

app = FastAPI()

class TaskStatus(str , Enum):
    todo = "todo"
    ongoing = "ongoing"
    finished = "finished"

class TaskCreate(BaseModel):
    title : str = Field(min_length=1,max_length=50,description="Title of the Task")
    description : str  = Field(None,max_length=100,description="Description of Task")
    due_date  : datetime = Field(None,description="Due Date of Task")
    status : TaskStatus = Field(TaskStatus.todo,description="Current Status of Task")

class Task(TaskCreate):
    task_id : int
    created_at : datetime
    updated_at : datetime 


tasks_db : list[Task] = []
task_next_id = 1

@app.get("/")
async def root():
    return {"message" : "Welcome to Task Management API"}

@app.post("/tasks",response_model=Task)
async def create_task(task:TaskCreate):
    global task_next_id

    new_task = Task(
        task_id=task_next_id,
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        status=task.status,
        created_at=datetime.now(),
        updated_at= datetime.now()
    )

    tasks_db.append(new_task)
    task_next_id+=1
    return new_task

@app.get("/tasks",response_model=list[Task])
async def show_all_tasks():
    return tasks_db

@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int = Path(..., gt=0, description="ID of the task to retrieve")):
    for task in tasks_db:
        if task.task_id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(
    task_id: int = Path(..., gt=0, description="ID of the task to update"),
    updated_task: TaskCreate = Body(...)
):
    for index, task in enumerate(tasks_db):
        if task.task_id == task_id:
            task_data = updated_task.model_dump()
            task_data["task_id"] = task.task_id
            task_data["created_at"] = task.created_at
            task_data["updated_at"] = datetime.now()
            tasks_db[index] = Task(**task_data)
            return tasks_db[index]
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}", response_model=dict)
async def delete_task(task_id: int = Path(..., gt=0, description="ID of the task to delete")):
    for index, task in enumerate(tasks_db):
        if task.task_id == task_id:
            tasks_db.pop(index)
            return {"detail": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")