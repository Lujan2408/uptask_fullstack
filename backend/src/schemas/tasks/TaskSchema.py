# from typing import Optional
# from pydantic import ConfigDict, field_validator
from src.schemas.base import CleanStrModel
from sqlmodel import Field

class TaskBase(CleanStrModel): 
  task_name: str = Field(min_length=3, max_length=255)
  task_description: str = Field(min_length=3, max_length=255)

