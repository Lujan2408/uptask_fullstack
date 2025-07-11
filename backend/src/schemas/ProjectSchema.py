from typing import Optional
from pydantic import ConfigDict, field_validator
from sqlmodel import SQLModel, Field

class ProjectBase(SQLModel):
  project_name: str
  project_description: str
  client_name: str

class ProjectCreate(ProjectBase):
  pass

class Project(ProjectBase, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)

  model_config = ConfigDict(from_attributes=True)

  @field_validator("project_name")
  def project_name_with_no_blank_spaces(cls, v):
    if v is not None:
      v = v.strip()
      if v == "":
        raise ValueError("Project name cannot be blank")
      return v
    return v