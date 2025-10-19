from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Contract terms
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    monthly_fee = Column(Float, default=0.0)
    included_tickets = Column(Integer, default=0)
    price_per_extra_ticket = Column(Float, default=0.0)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    client = relationship("User", back_populates="contracts")
    tickets = relationship("Ticket", back_populates="contract")
