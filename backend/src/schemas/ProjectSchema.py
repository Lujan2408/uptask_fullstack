# Validate data 
from pydantic import ConfigDict
from src.schemas.base import CleanStrModel
from sqlmodel import Field

class ProjectBase(CleanStrModel):
  project_name: str = Field(min_length=3, max_length=255)
  project_description: str = Field(min_length=3, max_length=255)
  client_name: str = Field(min_length=3, max_length=255)

class ProjectCreate(ProjectBase):
  pass

class ProjectResponse(ProjectBase):
  id: int 

  # Pydantic config
  model_config = ConfigDict(from_attributes=True)