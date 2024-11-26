from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: str | None = None
    completed: bool | None = None
    category_id: str | None = None


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: str

    class Config:
        from_attributes = True


class Category(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True
