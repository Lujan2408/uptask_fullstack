from src.schemas.TaskSchema import TaskCreate
from src.models.models import Task
from src.core.db import AsyncSessionDependency
from src.core.logging import (
    log_operation_start,
    log_entity_created
)


class TaskController: 
  def __init__(self, session: AsyncSessionDependency):
    self.session = session

  async def create_task(self, project_id: int, task_data: TaskCreate):     
    try: 
      log_operation_start("Creating task", f"{task_data.task_name} for project {project_id}")

      # Create the task object
      task = Task(**task_data.model_dump(), project_id=project_id)
      self.session.add(task)
      await self.session.commit()
      await self.session.refresh(task)

      log_entity_created("Task", task.task_name, task.id)

      return {
        "message": "Task created successfully",
        "data": task.model_dump(),
        "status": "success"
      }
      
    except Exception as e:
      raise e