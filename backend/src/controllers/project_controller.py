# Validate business logic 
from fastapi import HTTPException, status
from sqlmodel import select

from src.schemas.ProjectSchema import ProjectCreate, ProjectUpdate
from src.models.models import Project
from src.core.db import AsyncSessionDependency
from src.core.logging import (
    log_operation_start,
    log_operation_success,
    log_entity_created,
    log_entity_updated
)

from src.errors.project_errors import (
  ProjectNotFoundError,
  NoFieldsToUpdateError
)


class ProjectController:
  def __init__(self, session: AsyncSessionDependency):
    self.session = session

  async def create_project(self, project_data: ProjectCreate):
    try: 
      log_operation_start("Creating project", project_data.project_name)
    
      # Create the project object
      project_data_dict = project_data.model_dump()
      project = Project(**project_data_dict) # Project object that will be created in the database
      self.session.add(project)
      await self.session.commit()
      await self.session.refresh(project)

      log_entity_created("Project", project.project_name, project.id)
      
      return {
        "message": "Project created successfully",
        "data": project.model_dump(),
        "status": "success"
      }
    
    except Exception as e:
      raise e

  async def get_all_projects(self):
    try:
      log_operation_start("Getting all projects")
      
      projects = await self.session.execute(select(Project).order_by(Project.id.asc()))
      projects_list = projects.scalars().all()
      
      # Check if no projects were found
      if not projects_list: 
        raise ProjectNotFoundError("No projects found")
      
      log_operation_success("Getting all projects")
      return projects_list
    
    except ProjectNotFoundError as e:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
      raise e

  async def get_project_by_id(self, project: Project):
    """
    Get project by ID. Project is already validated by middleware.
    
    Args:
        project: Project object validated by middleware
        
    Returns:
        Project: The project object
    """
    try: 
      log_operation_start("Getting project by ID", f"ID: {project.id}")
      log_operation_success("Getting project by ID", project.project_name)
      return project
    
    except Exception as e:
      raise e
    
  async def update_project(self, project: Project, project_data: ProjectUpdate):
    """
    Update project. Project is already validated by middleware.
    
    Args:
        project: Project object validated by middleware
        project_data: Data to update the project
        
    Returns:
        Project: The updated project object
    """
    try:
      log_operation_start("Updating project", f"ID: {project.id}")
      
      # Check if at least one field is provided to update the project
      if not any([
          project_data.project_name is not None,
          project_data.project_description is not None,
          project_data.client_name is not None
      ]):
        raise NoFieldsToUpdateError("At least one field must be provided to update the project")
        
      # Update only the fields that are provided (not None)
      update_data = {}
      if project_data.project_name is not None:
          update_data["project_name"] = project_data.project_name
      if project_data.project_description is not None:
          update_data["project_description"] = project_data.project_description
      if project_data.client_name is not None:
          update_data["client_name"] = project_data.client_name

      # Update the project only with the provided fields 
      for field, value in update_data.items():
        setattr(project, field, value)

      self.session.add(project)
      await self.session.commit()
      await self.session.refresh(project)

      log_entity_updated("Project", project.project_name, project.id)
      return project
    
    except NoFieldsToUpdateError as e:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
      raise e

