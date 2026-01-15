"""
models.py

Shared Pydantic models for the application.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class SensorReading(BaseModel):
    sensor_id: str = Field(..., description="Unique ID of the sensor (e.g., S1)")
    insert_timestamp: datetime = Field(default_factory=datetime.now, description="When the reading was recorded")
    type: str = Field(..., description="Type of measurement (e.g., temperature)")
    value: float = Field(..., description="Numerical value of the reading")
    unit: str = Field(..., description="Unit of measurement (e.g., C, %)")
    upload_freq: str = Field(..., description="Frequency metadata")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
