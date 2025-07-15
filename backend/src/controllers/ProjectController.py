# Validate business logic 
from fastapi import HTTPException, status
from sqlmodel import select

from src.schemas.ProjectSchema import ProjectCreate, ProjectResponse, ProjectUpdate
from src.models.Project import Project
from src.core.db import AsyncSessionDependency
from src.core.logging import logger

from src.errors.project_errors import (
  ProjectNotFoundError, 
  ProjectNameTooShortError, 
  DuplicateProjectNameError, 
  NoFieldsToUpdateError

)
import colorama


class ProjectController:
  def __init__(self, session: AsyncSessionDependency):
    self.session = session

  async def create_project(self, project_data: ProjectCreate):
    try: 
      logger.info(f"Creating project: {colorama.Fore.YELLOW}{project_data.project_name}{colorama.Style.RESET_ALL}")
    
      # Validate project name length
      if len(project_data.project_name) < 3: 
        raise ProjectNameTooShortError("Project name must be at least 3 characters long")
      
      # Check if a project already exists with the same name
      existing_project = await self.session.execute(select(Project).where(Project.project_name == project_data.project_name))
      if existing_project.scalars().first(): 
        raise DuplicateProjectNameError("A project with this name already exists")

      # Create the project object
      project_data_dict = project_data.model_dump()
      project = Project(**project_data_dict) # Project object that will be created in the database
      self.session.add(project)
      await self.session.commit()
      await self.session.refresh(project)

      logger.info(f"{colorama.Fore.GREEN}Project created successfully: {project.project_name}✅{colorama.Style.RESET_ALL}")
      return {
        "message": "Project created successfully",
        "data": project.model_dump(),
        "status": "success"
      }
    
    except ProjectNameTooShortError as e:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DuplicateProjectNameError as e:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
      raise e

  async def get_all_projects(self):
    try: 
      logger.info(f"{colorama.Fore.YELLOW}Getting all projects{colorama.Style.RESET_ALL}")
      
      projects = await self.session.execute(select(Project).order_by(Project.id.asc()))
      # Check if no projects were found
      if not projects.scalars().all(): 
        raise ProjectNotFoundError("No projects found")
      
      return projects.scalars().all()
    
    except ProjectNotFoundError as e:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
      raise e

  async def get_project_by_id(self, project_id: int):
    try: 
      logger.info(f"{colorama.Fore.YELLOW}Getting project by id: {colorama.Style.RESET_ALL}")

      project = await self.session.get(Project, project_id)
      
      if not project: 
        raise ProjectNotFoundError("Project not found or does not exist")
      
      return project
    
    except ProjectNotFoundError as e:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
      raise e
    
  async def update_project(self, project_id: int, project_data: ProjectUpdate):
    try:
      logger.info(f"{colorama.Fore.YELLOW}Updating project: {colorama.Style.RESET_ALL}")

      project = await self.session.get(Project, project_id)

      if not project: 
        raise ProjectNotFoundError("Project not found or does not exist")
      
      # Check if at least one field is provided to update the product
      if not any([
          project_data.project_name is not None,
          project_data.project_description is not None,
          project_data.client_name is not None
      ]):
        raise NoFieldsToUpdateError("At least one field must be provided to update the project")
      
      # check if already exists a project with the same name
      if project_data.project_name and project_data.project_name != project.project_name:
        existing_project = await self.session.execute(select(Project).where(Project.project_name == project_data.project_name))
        if existing_project.scalars().first():
          raise DuplicateProjectNameError("A project with this name already exists")
        
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

      return project
    
    except ProjectNotFoundError as e:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except NoFieldsToUpdateError as e:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DuplicateProjectNameError as e:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
      raise e

