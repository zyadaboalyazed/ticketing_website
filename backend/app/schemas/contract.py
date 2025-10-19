from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ContractBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    monthly_fee: float = 0.0
    included_tickets: int = 0
    price_per_extra_ticket: float = 0.0


class ContractCreate(ContractBase):
    client_id: int


class ContractUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    end_date: Optional[datetime] = None
    monthly_fee: Optional[float] = None
    included_tickets: Optional[int] = None
    price_per_extra_ticket: Optional[float] = None
    is_active: Optional[bool] = None


class ContractResponse(ContractBase):
    id: int
    client_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
