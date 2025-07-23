from fastapi import APIRouter, status, Depends

from src.controllers.task_controller import TaskController
from src.schemas.TaskSchema import TaskCreate
from src.core.db import AsyncSessionDependency
from src.middleware.project import validate_existing_project
from src.models.models import Project

api_router = APIRouter(prefix="/tasks", tags=["tasks"])

@api_router.post("/{project_id}/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(task_data: TaskCreate, session: AsyncSessionDependency, project: Project = Depends(validate_existing_project)):
   task_controller = TaskController(session)
   return await task_controller.create_task(project.id, task_data)