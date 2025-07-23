# Validate data 
from typing import Optional
from pydantic import ConfigDict
from src.schemas.base import CleanStrModel, ProjectValidators
from sqlmodel import Field

class ProjectBase(CleanStrModel):
  project_name: str = Field(min_length=3, max_length=255)
  project_description: str = Field(min_length=3, max_length=255)
  client_name: str = Field(min_length=3, max_length=255)

class ProjectCreate(ProjectBase, ProjectValidators):
  pass

class ProjectResponse(ProjectBase):
  id: int 

class ProjectUpdate(ProjectBase, ProjectValidators):
  project_name: Optional[str] = Field(default=None)
  project_description: Optional[str] = Field(default=None)
  client_name: Optional[str] = Field(default=None)

  # Pydantic config
  model_config = ConfigDict(from_attributes=True)