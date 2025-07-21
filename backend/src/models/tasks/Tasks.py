from sqlmodel import Field, SQLModel
from typing import Optional

class Task(SQLModel, table=True): 
  id: Optional[int] = Field(default=None, primary_key=True)
  task_name: str = Field(index=True, min_length=3, max_length=255)
  task_description: str = Field(min_length=3, max_length=255) 