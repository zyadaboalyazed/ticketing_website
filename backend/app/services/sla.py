from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ..models.ticket import Ticket
from ..models.contract import Contract


def calculate_sla_due_date(ticket: Ticket, contract: Contract = None) -> datetime:
    """Calculate SLA due date based on contract or default settings"""
    if contract:
        resolution_hours = contract.resolution_time_hours
    else:
        resolution_hours = 72  # Default 72 hours
    
    return ticket.created_at + timedelta(hours=resolution_hours)


def check_sla_breach(ticket: Ticket) -> bool:
    """Check if ticket has breached SLA"""
    if not ticket.sla_due_date:
        return False
    
    if ticket.status in ["resolved", "closed"]:
        return False
    
    return datetime.utcnow() > ticket.sla_due_date


def update_ticket_sla_status(db: Session, ticket: Ticket):
    """Update ticket SLA breach status"""
    if check_sla_breach(ticket):
        ticket.sla_breached = 1
        db.commit()


def calculate_ticket_cost(ticket: Ticket, contract: Contract = None) -> float:
    """Calculate weighted pricing for a ticket"""
    if not contract:
        # Use ticket's hourly rate if no contract
        return ticket.actual_hours * ticket.hourly_rate
    
    # Calculate cost based on contract
    base_cost = contract.base_rate
    
    if ticket.actual_hours <= contract.included_hours:
        # Within included hours
        return base_cost
    else:
        # Overage hours
        overage_hours = ticket.actual_hours - contract.included_hours
        overage_cost = overage_hours * contract.overage_rate
        return base_cost + overage_cost
