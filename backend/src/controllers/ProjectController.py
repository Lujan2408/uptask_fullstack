from src.core.db import AsyncSessionDependency

class ProjectController:
  def __init__(self, session: AsyncSessionDependency):
    self.session = session

  async def get_all_projects(self):
    return {"message": "Hello World from ProjectController"}