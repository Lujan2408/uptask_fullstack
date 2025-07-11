from pydantic import BaseModel, field_validator

class CleanStrModel(BaseModel):
  @field_validator("*", mode="before")
  def strip_and_validate_string(cls, v):
    if isinstance(v, str):
      v = v.strip()
      if not v:
        raise ValueError("This field cannot be blank or only spaces")
    return v