from pydantic import BaseModel
from typing import Optional
from ..models.ticket import TicketPriority


class SLABase(BaseModel):
    name: str
    description: Optional[str] = None
    priority: TicketPriority
    response_time_hours: float
    resolution_time_hours: float


class SLACreate(SLABase):
    pass


class SLAUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[TicketPriority] = None
    response_time_hours: Optional[float] = None
    resolution_time_hours: Optional[float] = None


class SLAResponse(SLABase):
    id: int

    class Config:
        from_attributes = True
