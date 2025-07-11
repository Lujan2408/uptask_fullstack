import colorama
from src.schemas.ProjectSchema import Project, ProjectCreate
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
      return project
    except Exception as e:
      logger.error(f"{colorama.Fore.RED}Error creating project: {e}{colorama.Style.RESET_ALL}")
      raise e

  async def get_all_projects(self):
    return "Getting all projects"