from sqlmodel import Field, SQLModel
from typing import Optional

class Project(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  project_name: str = Field(index=True, min_length=3, max_length=255)
  project_description: str = Field(min_length=3, max_length=255)
  client_name: str = Field(index=True, min_length=3, max_length=255)