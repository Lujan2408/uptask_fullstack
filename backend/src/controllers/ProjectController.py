# Validate business logic 
from fastapi import HTTPException
from sqlmodel import select
import colorama
from src.schemas.ProjectSchema import ProjectCreate, ProjectResponse
from src.models.Project import Project
from src.core.db import AsyncSessionDependency
from src.core.logging import logger

class ProjectController:
  def __init__(self, session: AsyncSessionDependency):
    self.session = session

  async def create_project(self, project_data: ProjectCreate):
    try: 
      logger.info(f"Creating project: {colorama.Fore.YELLOW}{project_data.project_name}{colorama.Style.RESET_ALL}")
    
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
      
      return ProjectResponse.model_validate(project).model_dump()
    
    except Exception as e:
      raise e