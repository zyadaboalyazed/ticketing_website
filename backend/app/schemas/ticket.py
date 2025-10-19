from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from ..models.ticket import TicketPriority, TicketStatus


class TicketBase(BaseModel):
    title: str
    description: str
    priority: TicketPriority = TicketPriority.MEDIUM


class TicketCreate(TicketBase):
    contract_id: Optional[int] = None


class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[TicketPriority] = None
    status: Optional[TicketStatus] = None
    assigned_agent_id: Optional[int] = None


class TicketResponse(TicketBase):
    id: int
    status: TicketStatus
    client_id: int
    assigned_agent_id: Optional[int]
    contract_id: Optional[int]
    sla_id: Optional[int]
    base_price: float
    weight_multiplier: float
    final_price: float
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime]
    closed_at: Optional[datetime]
    due_date: Optional[datetime]
    sla_breached: bool

    class Config:
        from_attributes = True
