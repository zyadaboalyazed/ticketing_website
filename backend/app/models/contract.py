from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base


class Contract(Base):
    __tablename__ = "contracts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Pricing
    base_rate = Column(Float, default=0.0)
    hourly_rate = Column(Float, default=0.0)
    included_hours = Column(Float, default=0.0)  # Monthly included hours
    overage_rate = Column(Float, default=0.0)  # Rate for hours beyond included
    
    # SLA settings
    response_time_hours = Column(Integer, default=24)  # Response time in hours
    resolution_time_hours = Column(Integer, default=72)  # Resolution time in hours
    
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    is_active = Column(Integer, default=1)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    client = relationship("User", back_populates="contracts")
    tickets = relationship("Ticket", back_populates="contract")
