from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ContractBase(BaseModel):
    name: str
    description: Optional[str] = None
    client_id: int
    base_rate: float = 0.0
    hourly_rate: float = 0.0
    included_hours: float = 0.0
    overage_rate: float = 0.0
    response_time_hours: int = 24
    resolution_time_hours: int = 72
    start_date: datetime
    end_date: datetime


class ContractCreate(ContractBase):
    pass


class ContractUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    base_rate: Optional[float] = None
    hourly_rate: Optional[float] = None
    included_hours: Optional[float] = None
    overage_rate: Optional[float] = None
    response_time_hours: Optional[int] = None
    resolution_time_hours: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: Optional[int] = None


class Contract(ContractBase):
    id: int
    is_active: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
