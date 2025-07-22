from __future__ import annotations
from enum import Enum
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from datetime import datetime
from sqlalchemy import Column
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.types import DateTime as SQLAlchemyDateTime
from src.helpers.format_date import now_without_microseconds

# Projects models

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
      created_at: Timestamp for when the project was created
      updated_at: Timestamp for when the project was last updated
  """
  __tablename__ = "projects"
  id: Optional[int] = Field(default=None, primary_key=True)
  project_name: str = Field(index=True, min_length=3, max_length=255)
  project_description: str = Field(min_length=3, max_length=255)
  client_name: str = Field(index=True, min_length=3, max_length=255)
  tasks: Mapped[List["Task"]] = Relationship(sa_relationship=relationship("Task", back_populates="project"))
  created_at: datetime = Field(
    default_factory=now_without_microseconds, 
    sa_column=Column(
    SQLAlchemyDateTime, 
    default=now_without_microseconds)
  )
  updated_at: datetime = Field(
    default_factory=now_without_microseconds, 
    sa_column=Column(
    SQLAlchemyDateTime, 
    default=now_without_microseconds, 
    onupdate=now_without_microseconds)  
  )

# Tasks models

class TaskStatus(str, Enum):
  """
  Enum representing the status of a task.
  """
  PENDING = "pending"
  ON_HOLD = "on_hold"
  IN_PROGRESS = "in_progress"
  UNDER_REVIEW = "under_review"
  COMPLETED = "completed"

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
      status: Current status of the task (pending, in_progress, etc.)
      created_at: Timestamp for when the task was created
      updated_at: Timestamp for when the task was last updated
  """
  __tablename__ = "tasks"
  id: Optional[int] = Field(default=None, primary_key=True)
  task_name: str = Field(index=True, min_length=3, max_length=255)
  task_description: str = Field(min_length=3, max_length=255) 
  project_id: Optional[int] = Field(default=None, foreign_key="projects.id") 
  project: Mapped[Optional["Project"]] = Relationship(sa_relationship=relationship("Project", back_populates="tasks"))
  status: TaskStatus = Field(default=TaskStatus.PENDING)