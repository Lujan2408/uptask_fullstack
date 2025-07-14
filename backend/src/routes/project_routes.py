
from fastapi import APIRouter
from src.controllers.ProjectController import ProjectController
from src.core.db import AsyncSessionDependency
from src.schemas.ProjectSchema import ProjectCreate

api_router = APIRouter(prefix="/projects", tags=["projects"])

@api_router.post("/")
async def create_project(project_data: ProjectCreate, session: AsyncSessionDependency):
    project_controller = ProjectController(session)
    return await project_controller.create_project(project_data)
    
@api_router.get("/")
async def get_all_projects(session: AsyncSessionDependency):
  project_controller = ProjectController(session)
  return await project_controller.get_all_projects()

@api_router.get("/{project_id}")
async def get_project_by_id(project_id: int, session: AsyncSessionDependency):
   project_controller = ProjectController(session)
   return await project_controller.get_project_by_id(project_id)
