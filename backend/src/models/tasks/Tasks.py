from __future__ import annotations
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
  from ..projects.Project import Project

class Task(SQLModel, table=True): 
  """
  Task model representing individual tasks within a project.
  
  This model defines the structure for tasks in the system, including
  task details and a many-to-one relationship with projects.
  
  Attributes:
      id: Primary key identifier for the task
      task_name: Name of the task (indexed for faster queries)
      task_description: Detailed description of the task
      project_id: Foreign key reference to the parent project
      project: Many-to-one relationship with Project object
  """
  id: Optional[int] = Field(default=None, primary_key=True)
  task_name: str = Field(index=True, min_length=3, max_length=255)
  task_description: str = Field(min_length=3, max_length=255) 
  project_id: Optional[int] = Field(default=None, foreign_key="project.id") 
  project: Optional["Project"] = Relationship(back_populates="tasks")
  created_at: datetime = Field(default_factory=datetime.now)
  updated_at: datetime = Field(default_factory=datetime.now)