from fastapi import APIRouter, status

from src.controllers.project_controller import ProjectController
from src.core.db import AsyncSessionDependency
from src.schemas.ProjectSchema import ProjectCreate, ProjectUpdate

api_router = APIRouter(prefix="/projects", tags=["projects"])

@api_router.post("/", status_code=status.HTTP_201_CREATED)
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

@api_router.patch("/{project_id}")
async def update_project(project_id: int, project_data: ProjectUpdate, session: AsyncSessionDependency):
  project_controller = ProjectController(session)
  return await project_controller.update_project(project_id, project_data)