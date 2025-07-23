from fastapi import APIRouter, status, Depends

from src.controllers.project_controller import ProjectController
from src.core.db import AsyncSessionDependency
from src.schemas.ProjectSchema import ProjectCreate, ProjectUpdate
from src.middleware.project import (
    validate_existing_project,
    validate_project_name_not_exists
)
from src.models.models import Project

api_router = APIRouter(prefix="/projects", tags=["projects"])

@api_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    session: AsyncSessionDependency
):
    await validate_project_name_not_exists(project_data.project_name, session)

    project_controller = ProjectController(session)
    return await project_controller.create_project(project_data)
    
@api_router.get("/")
async def get_all_projects(session: AsyncSessionDependency):
  project_controller = ProjectController(session)
  return await project_controller.get_all_projects()

@api_router.get("/{project_id}")
async def get_project_by_id(
    session: AsyncSessionDependency,
    project: Project = Depends(validate_existing_project)
):
    project_controller = ProjectController(session)
    return await project_controller.get_project_by_id(project)

@api_router.patch("/{project_id}")
async def update_project(
    project_data: ProjectUpdate,
    session: AsyncSessionDependency,
    project: Project = Depends(validate_existing_project)
):
    if project_data.project_name:
        await validate_project_name_not_exists(project_data.project_name, session, project.id)

    project_controller = ProjectController(session)
    return await project_controller.update_project(project, project_data)