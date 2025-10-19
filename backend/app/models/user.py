from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..core.database import Base


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    AGENT = "agent"
    CLIENT = "client"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(SQLEnum(UserRole), default=UserRole.CLIENT)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tickets_created = relationship("Ticket", back_populates="creator", foreign_keys="Ticket.creator_id")
    tickets_assigned = relationship("Ticket", back_populates="assignee", foreign_keys="Ticket.assignee_id")
    contracts = relationship("Contract", back_populates="client")
    comments = relationship("TicketComment", back_populates="user")
