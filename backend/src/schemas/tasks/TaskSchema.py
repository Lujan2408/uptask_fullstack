from typing import Optional
from pydantic import ConfigDict, field_validator
from src.schemas.base import CleanStrModel
from sqlmodel import Field
from src.models.tasks.Tasks import TaskStatus

class TaskBase(CleanStrModel): 
  task_name: str = Field(min_length=3, max_length=255)
  task_description: str = Field(min_length=3, max_length=255)
  status: TaskStatus = Field(default=TaskStatus.PENDING)

class TaskCreate(TaskBase):
  project_id: int

class TaskResponse(TaskBase):
  id: int
  project_id: int
  created_at: str
  updated_at: str

class TaskUpdate(CleanStrModel):
  task_name: Optional[str] = Field(default=None, min_length=3, max_length=255)
  task_description: Optional[str] = Field(default=None, min_length=3, max_length=255)
  status: Optional[TaskStatus] = Field(default=None)

  @field_validator('task_name')
  @classmethod
  def validate_task_name(cls, v):
      if v is not None and len(v) < 3:
          raise ValueError("Task name must be at least 3 characters long")
      return v

  @field_validator('task_description')
  @classmethod
  def validate_task_description(cls, v):
      if v is not None and len(v) < 3:
          raise ValueError("Task description must be at least 3 characters long")
      return v

  # Pydantic config
  model_config = ConfigDict(from_attributes=True)

