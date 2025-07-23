from typing import Optional
from pydantic import ConfigDict
from src.schemas.base import CleanStrModel, TaskValidators
from sqlmodel import Field
from src.models.models import TaskStatus

class TaskBase(CleanStrModel): 
  task_name: str = Field(min_length=3, max_length=255)
  task_description: str = Field(min_length=3, max_length=255)
  status: TaskStatus = Field(default=TaskStatus.PENDING)

class TaskCreate(TaskBase, TaskValidators):
   pass

class TaskResponse(TaskBase):
  id: int
  project_id: int
  created_at: str
  updated_at: str

class TaskUpdate(TaskBase, TaskValidators):
  task_name: Optional[str] = Field(default=None, min_length=3, max_length=255)
  task_description: Optional[str] = Field(default=None, min_length=3, max_length=255)
  status: Optional[TaskStatus] = Field(default=None)

  # Pydantic config
  model_config = ConfigDict(from_attributes=True)

