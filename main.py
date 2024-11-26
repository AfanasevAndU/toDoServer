from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import crud_couchbase as crud
import schemas

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    from crud_couchbase import seed_data
    seed_data()



@app.get("/", response_class=HTMLResponse)
async def web_interface(request: Request, page: int = 1, category_id: str | None = None):
    tasks_per_page = 10
    skip = (page - 1) * tasks_per_page

    # Получение задач и общего числа
    if category_id:
        tasks = crud.get_tasks_by_category(category_id=category_id, skip=skip, limit=tasks_per_page)
        total_tasks = crud.count_tasks(category_id=category_id)
    else:
        tasks = crud.get_tasks_with_categories(skip=skip, limit=tasks_per_page)
        total_tasks = crud.count_tasks()

    categories = crud.get_categories()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "tasks": tasks,
            "categories": categories,
            "current_page": page,
            "total_tasks": total_tasks,
            "tasks_per_page": tasks_per_page,
            "current_category": category_id,
        },
    )


@app.post("/add", response_class=RedirectResponse)
async def create_task(name: str = Form(...), description: str = Form(None), category_id: str = Form(...)):
    if not name:
        raise HTTPException(status_code=400, detail="Task name cannot be empty")
    crud.create_task(schemas.TaskCreate(title=name, description=description, category_id=category_id))
    return RedirectResponse("/", status_code=302)


@app.post("/delete/{task_id}", response_class=RedirectResponse)
async def delete_task_from_web(task_id: str):
    result = crud.delete_task(task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return RedirectResponse("/", status_code=302)
