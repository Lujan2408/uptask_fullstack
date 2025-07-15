# Validate data 
from typing import Optional
from pydantic import ConfigDict, field_validator
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

class ProjectUpdate(ProjectBase):
  project_name: Optional[str] = Field(default=None)
  project_description: Optional[str] = Field(default=None)
  client_name: Optional[str] = Field(default=None)

  @field_validator('project_name')
  @classmethod
  def validate_project_name(cls, v):
      if v is not None and len(v) < 3:
          raise ValueError("Project name must be at least 3 characters long")
      return v

  @field_validator('project_description')
  @classmethod
  def validate_project_description(cls, v):
      if v is not None and len(v) < 3:
          raise ValueError("Project description must be at least 3 characters long")
      return v

  @field_validator('client_name')
  @classmethod
  def validate_client_name(cls, v):
      if v is not None and len(v) < 2:
          raise ValueError("Client name must be at least 2 characters long")
      return v

  # Pydantic config
  model_config = ConfigDict(from_attributes=True)