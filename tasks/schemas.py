from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    task: str = Field(..., min_length=3, max_length=100)
