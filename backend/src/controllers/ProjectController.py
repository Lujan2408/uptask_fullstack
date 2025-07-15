# Validate business logic 
from fastapi import HTTPException
from sqlmodel import select
import colorama
from src.schemas.ProjectSchema import ProjectCreate, ProjectResponse, ProjectUpdate
from src.models.Project import Project
from src.core.db import AsyncSessionDependency
from src.core.logging import logger

class ProjectController:
  def __init__(self, session: AsyncSessionDependency):
    self.session = session

  async def create_project(self, project_data: ProjectCreate):
    try: 
      logger.info(f"Creating project: {colorama.Fore.YELLOW}{project_data.project_name}{colorama.Style.RESET_ALL}")
    
      if len(project_data.project_name) < 3: 
        raise HTTPException(status_code=400, detail="Project name must be at least 3 characters long")

      project_data_dict = project_data.model_dump()
      project = Project(**project_data_dict) # Project object that will be created in the database
      self.session.add(project)
      await self.session.commit()
      await self.session.refresh(project)

      logger.info(f"{colorama.Fore.GREEN}Project created successfully: {project.project_name}✅{colorama.Style.RESET_ALL}")
      return {
        "message": "Project created successfully",
        "data": ProjectResponse.model_validate(project).model_dump(),
        "status": "success"
      }
    except Exception as e:
      raise e

  async def get_all_projects(self):
    try: 
      logger.info(f"{colorama.Fore.YELLOW}Getting all projects{colorama.Style.RESET_ALL}")
      
      projects = await self.session.execute(select(Project).order_by(Project.id.asc()))
      return projects.scalars().all()
    
    except Exception as e:
      raise e

  async def get_project_by_id(self, project_id: int):
    try: 
      logger.info(f"{colorama.Fore.YELLOW}Getting project by id: {colorama.Style.RESET_ALL}")

      project = await self.session.get(Project, project_id)
      
      if not project: 
        raise HTTPException(status_code=404, detail="Project not found or does not exist")
      
      return project
    
    except Exception as e:
      raise e
    
  async def update_project(self, project_id: int, project_data: ProjectUpdate):
    try:
      logger.info(f"{colorama.Fore.YELLOW}Updating project: {colorama.Style.RESET_ALL}")

      project = await self.session.get(Project, project_id)

      if not project: 
        raise HTTPException(status_code=404, detail="Project not found or does not exist")
      
      # Check if at least one field is provided to update the product
      if not any([
          project_data.project_name is not None,
          project_data.project_description is not None,
          project_data.client_name is not None
      ]):
        raise HTTPException(status_code=400, detail="At least one field must be provided to update the project")
      
      # check if already exists a project with the same name
      if project_data.project_name and project_data.project_name != project.project_name:
        existing_project = await self.session.execute(select(Project).where(Project.project_name == project_data.project_name))
        if existing_project.scalars().first():
          raise HTTPException(status_code=400, detail="A project with this name already exists")
        
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
    
    except Exception as e:
      raise e
  
      
      