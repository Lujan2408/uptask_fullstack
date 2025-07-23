import colorama
from fastapi import HTTPException, status
from sqlmodel import select

from src.schemas.TaskSchema import TaskCreate
from src.models.models import Task, Project
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
    try: 
      logger.info(f"Creating task: {colorama.Fore.YELLOW}{task_data.task_name}{colorama.Style.RESET_ALL} for project: {colorama.Fore.YELLOW}{project_id}{colorama.Style.RESET_ALL}")

      # Check if the project exists
      project = await self.session.get(Project, project_id)
      if not project: 
        raise ProjectNotFoundError("Project not found or does not exist")

      # Create the task object
      task = Task(**task_data.model_dump(), project_id=project.id)
      self.session.add(task)
      await self.session.commit()
      await self.session.refresh(task)

      logger.info(f"Task created successfully: {colorama.Fore.GREEN}{task.task_name}{colorama.Style.RESET_ALL} for project: {colorama.Fore.GREEN}{project.project_name}{colorama.Style.RESET_ALL}")

      return {
        "message": "Task created successfully",
        "data": task.model_dump(),
        "status": "success"
      }
      
    except ProjectNotFoundError as e:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
      raise e