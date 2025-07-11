from fastapi import APIRouter, Depends
from src.controllers.ProjectController import ProjectController
from src.core.db import AsyncSessionDependency

api_router = APIRouter()

@api_router.get("/")
async def get_all_projects(session: AsyncSessionDependency):
  project_controller = ProjectController(session)
  return await project_controller.get_all_projects()