import colorama
from fastapi import HTTPException, status
from sqlmodel import select

from src.schemas.TaskSchema import TaskCreate
from src.models.models import Task
from src.core.db import AsyncSessionDependency
from src.core.logging import logger

from src.errors.project_errors import (
  ProjectNotFoundError, 
  ProjectNameTooShortError, 
  DuplicateProjectNameError, 
  NoFieldsToUpdateError
)


class TaskController: 
  def __init__(self, session: AsyncSessionDependency):
    self.session = session

  async def create_task(self, project_id: int, task_data: TaskCreate): 
    return project_id, task_data