from __future__ import annotations
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
  from ..tasks.Tasks import Task

class Project(SQLModel, table=True):
  """
  Project model representing a client project with multiple tasks.
  
  This model defines the structure for projects in the system, including
  project details and a one-to-many relationship with tasks.
  
  Attributes:
      id: Primary key identifier for the project
      project_name: Name of the project (indexed for faster queries)
      project_description: Detailed description of the project
      client_name: Name of the client (indexed for faster queries)
      tasks: One-to-many relationship with Task objects
  """
  id: Optional[int] = Field(default=None, primary_key=True)
  project_name: str = Field(index=True, min_length=3, max_length=255)
  project_description: str = Field(min_length=3, max_length=255)
  client_name: str = Field(index=True, min_length=3, max_length=255)
  tasks: List["Task"] = Relationship(back_populates="project")
  created_at: datetime = Field(default_factory=datetime.now)
  updated_at: datetime = Field(default_factory=datetime.now)