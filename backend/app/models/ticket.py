from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SQLEnum, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..core.database import Base


class TicketPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TicketStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    PENDING = "pending"
    RESOLVED = "resolved"
    CLOSED = "closed"


class Ticket(Base):
    __tablename__ = "tickets"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    priority = Column(SQLEnum(TicketPriority), default=TicketPriority.MEDIUM)
    status = Column(SQLEnum(TicketStatus), default=TicketStatus.OPEN)
    
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
    closed_at = Column(DateTime, nullable=True)
    
    # SLA tracking
    sla_due_date = Column(DateTime, nullable=True)
    sla_breached = Column(Integer, default=0)  # 0 = no breach, 1 = breached
    
    # Weighted pricing
    estimated_hours = Column(Float, default=0.0)
    actual_hours = Column(Float, default=0.0)
    hourly_rate = Column(Float, default=0.0)
    total_cost = Column(Float, default=0.0)
    
    # Relationships
    creator = relationship("User", back_populates="tickets_created", foreign_keys=[creator_id])
    assignee = relationship("User", back_populates="tickets_assigned", foreign_keys=[assignee_id])
    contract = relationship("Contract", back_populates="tickets")
    comments = relationship("TicketComment", back_populates="ticket", cascade="all, delete-orphan")


class TicketComment(Base):
    __tablename__ = "ticket_comments"
    
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    is_internal = Column(Integer, default=0)  # 0 = public, 1 = internal (only agents/admins)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    ticket = relationship("Ticket", back_populates="comments")
    user = relationship("User", back_populates="comments")
