from sqlalchemy import Column, Integer, String, Enum, DateTime, Boolean
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
    full_name = Column(String)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.CLIENT, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    tickets_created = relationship("Ticket", foreign_keys="Ticket.client_id", back_populates="client")
    tickets_assigned = relationship("Ticket", foreign_keys="Ticket.assigned_agent_id", back_populates="assigned_agent")
    contracts = relationship("Contract", back_populates="client")
