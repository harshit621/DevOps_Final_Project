from pydantic import BaseModel, ConfigDict
from typing import Optional

class AssetCreate(BaseModel):
    name: str
    category: str
    serial_number: str
    status: Optional[str] = "Available"

class AssetUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None

class AssetResponse(AssetCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)