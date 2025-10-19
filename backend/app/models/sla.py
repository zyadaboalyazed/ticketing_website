from sqlalchemy import Column, Integer, String, Enum, Float, Text
from sqlalchemy.orm import relationship
import enum
from ..core.database import Base
from .ticket import TicketPriority


class SLA(Base):
    __tablename__ = "slas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text)
    priority = Column(Enum(TicketPriority), nullable=False)
    
    # Response and resolution times in hours
    response_time_hours = Column(Float, nullable=False)
    resolution_time_hours = Column(Float, nullable=False)
    
    # Relationships
    tickets = relationship("Ticket", back_populates="sla")
