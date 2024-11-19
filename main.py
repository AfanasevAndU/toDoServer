from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import crud_couchbase as crud
import schemas

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate):
    return crud.create_task(task)

@app.get("/tasks/", response_model=list[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 10):
    tasks = crud.get_tasks(skip=skip, limit=limit)
    return tasks

@app.get("/tasks/{task_id}", response_model=schemas.Task)
def read_task(task_id: str):
    db_task = crud.get_task(task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.delete("/tasks/{task_id}", response_model=schemas.Task)
def delete_task(task_id: str):
    db_task = crud.delete_task(task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@app.get("/", response_class=HTMLResponse)
async def web_interface(request: Request):
    tasks = crud.get_tasks()  
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})

@app.post("/add", response_class=RedirectResponse)
async def add_task(name: str = Form(...), description: str = Form(None)):
    if not name:
        raise HTTPException(status_code=400, detail="Task name cannot be empty")
    crud.create_task(schemas.TaskCreate(title=name, description=description))  
    return RedirectResponse("/", status_code=302)

@app.post("/delete/{task_id}", response_class=RedirectResponse)
async def delete_task_from_web(task_id: str):
    result = crud.delete_task(task_id)
    return RedirectResponse("/", status_code=302)

