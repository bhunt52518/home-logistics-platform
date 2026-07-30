from pydantic import BaseModel, ConfigDict




class LocationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    household_id: int
    name: str
    