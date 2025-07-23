from pydantic import BaseModel, field_validator
from typing import Optional

class CleanStrModel(BaseModel):
  @field_validator("*", mode="before")
  def strip_and_validate_string(cls, v):
    if isinstance(v, str):
      v = v.strip()
      if not v:
        raise ValueError("This field cannot be blank or only spaces")
    return v

  @classmethod
  def validate_min_length(cls, value: Optional[str], min_length: int, field_name: str) -> Optional[str]:
      """Generic validator for minimum length"""
      if value is not None and len(value) < min_length:
          raise ValueError(f"{field_name} must be at least {min_length} characters long")
      return value

  @classmethod
  def validate_task_name(cls, v: Optional[str]) -> Optional[str]:
      """Specific validator for task names"""
      return cls.validate_min_length(v, 3, "Task name")

  @classmethod
  def validate_task_description(cls, v: Optional[str]) -> Optional[str]:
      """Specific validator for task descriptions"""
      return cls.validate_min_length(v, 3, "Task description")

  @classmethod
  def validate_project_name(cls, v: Optional[str]) -> Optional[str]:
      """Specific validator for project names"""
      return cls.validate_min_length(v, 3, "Project name")

  @classmethod
  def validate_project_description(cls, v: Optional[str]) -> Optional[str]:
      """Specific validator for project descriptions"""
      return cls.validate_min_length(v, 3, "Project description")

  @classmethod
  def validate_client_name(cls, v: Optional[str]) -> Optional[str]:
      """Specific validator for client names"""
      return cls.validate_min_length(v, 2, "Client name")

# Base class with automatic validators for multiple inheritance
class TaskValidators:
    """Class with automatic validators for tasks"""
    
    @field_validator('task_name')
    @classmethod
    def validate_task_name(cls, v):
        return CleanStrModel.validate_task_name(v)
    
    @field_validator('task_description')
    @classmethod
    def validate_task_description(cls, v):
        return CleanStrModel.validate_task_description(v)

class ProjectValidators:
    """Class with automatic validators for projects"""
    
    @field_validator('project_name')
    @classmethod
    def validate_project_name(cls, v):
        return CleanStrModel.validate_project_name(v)
    
    @field_validator('project_description')
    @classmethod
    def validate_project_description(cls, v):
        return CleanStrModel.validate_project_description(v)
    
    @field_validator('client_name')
    @classmethod
    def validate_client_name(cls, v):
        return CleanStrModel.validate_client_name(v)