from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from ..models.ticket import TicketPriority, TicketStatus


class TicketBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: TicketPriority = TicketPriority.MEDIUM
    contract_id: Optional[int] = None


class TicketCreate(TicketBase):
    pass


class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[TicketPriority] = None
    status: Optional[TicketStatus] = None
    assignee_id: Optional[int] = None
    estimated_hours: Optional[float] = None
    actual_hours: Optional[float] = None


class Ticket(TicketBase):
    id: int
    status: TicketStatus
    creator_id: int
    assignee_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime]
    closed_at: Optional[datetime]
    sla_due_date: Optional[datetime]
    sla_breached: int
    estimated_hours: float
    actual_hours: float
    hourly_rate: float
    total_cost: float
    
    class Config:
        from_attributes = True


class TicketCommentBase(BaseModel):
    content: str
    is_internal: int = 0


class TicketCommentCreate(TicketCommentBase):
    pass


class TicketComment(TicketCommentBase):
    id: int
    ticket_id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
