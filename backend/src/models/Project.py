from sqlmodel import Field, SQLModel, Column
from typing import Optional

class Project(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  project_name: str = Field(index=True)
  project_description: str
  client_name: str = Field(index=True)