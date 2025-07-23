from fastapi import APIRouter, status

from src.controllers.task_controller import TaskController
from src.schemas.TaskSchema import TaskCreate
from src.core.db import AsyncSessionDependency

api_router = APIRouter(prefix="/tasks", tags=["tasks"])

@api_router.post("/{project_id}/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(project_id: int, task_data: TaskCreate, session: AsyncSessionDependency):
   task_controller = TaskController(session)
   return await task_controller.create_task(project_id, task_data)