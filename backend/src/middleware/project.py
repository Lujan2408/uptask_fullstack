from fastapi import HTTPException, status
from sqlmodel import select

from src.models.models import Project
from src.errors.project_errors import ProjectNotFoundError, DuplicateProjectNameError
from src.core.db import AsyncSessionDependency
from src.core.logging import log_operation_start, log_operation_success

async def validate_existing_project(project_id: int, session: AsyncSessionDependency) -> Project:
  """
  Dependency to validate that a project exists.
  
  Args:
      project_id: The ID of the project to validate
      session: Database session dependency
      
  Returns:
      Project: The validated project object
      
  Raises:
      HTTPException: 404 if project not found, 400 if invalid ID format
  """
  try:
    log_operation_start("Validating project existence", f"ID: {project_id}")
    
    # Validate and convert project_id to int
    try:
      project_id_int = int(project_id)
    except (ValueError, TypeError):
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail=f"Invalid project ID format: {project_id}. Must be a valid integer."
      )
    
    # Validate project_id is positive
    if project_id_int <= 0:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail=f"Project ID must be a positive integer, got: {project_id_int}"
      )
    
    # Get project from database
    project = await session.get(Project, project_id_int)
    
    if not project: 
      raise ProjectNotFoundError(f"Project with ID {project_id_int} not found or does not exist")
  
    log_operation_success("Project validation", f"Project: {project.project_name}")
    return project
  
  except ProjectNotFoundError as e:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
  except Exception as e:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
      detail=f"Error validating project: {str(e)}"
    )

async def validate_project_name_not_exists(project_name: str, session: AsyncSessionDependency, exclude_project_id: int = None) -> None:
  """
  Dependency to validate that a project name doesn't already exist.
  
  Args:
      project_name: The project name to validate
      session: Database session dependency
      exclude_project_id: Optional project ID to exclude from validation (for updates)
      
  Raises:
      HTTPException: 400 if project name already exists
  """
  try:
    log_operation_start("Validating project name uniqueness", f"Name: {project_name}")
    
    # Validate project name length
    if len(project_name) < 3:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Project name must be at least 3 characters long"
      )
    
    # Build query to check for existing project with same name
    query = select(Project).where(Project.project_name == project_name)
    
    # If updating, exclude current project from validation
    if exclude_project_id is not None:
      query = query.where(Project.id != exclude_project_id)
    
    existing_project = await session.execute(query)
    
    if existing_project.scalars().first():
      raise DuplicateProjectNameError(f"A project with the name '{project_name}' already exists")
    
    log_operation_success("Project name validation", f"Name '{project_name}' is available")
    
  except DuplicateProjectNameError as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
  except HTTPException:
    raise
  except Exception as e:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail=f"Error validating project name: {str(e)}"
    )