from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ..models import Ticket, SLA
from ..models.ticket import TicketStatus


def calculate_ticket_price(ticket: Ticket, db: Session) -> float:
    """Calculate weighted pricing for ticket"""
    base_price = 50.0  # Base price for a ticket
    
    # Priority multipliers
    priority_weights = {
        "low": 1.0,
        "medium": 1.5,
        "high": 2.0,
        "critical": 3.0
    }
    
    weight = priority_weights.get(ticket.priority, 1.0)
    
    # Check if ticket is part of a contract
    if ticket.contract:
        # Contract tickets may have different pricing
        if ticket.contract.included_tickets > 0:
            # Count tickets used in this contract
            tickets_count = db.query(Ticket).filter(
                Ticket.contract_id == ticket.contract_id,
                Ticket.id <= ticket.id
            ).count()
            
            if tickets_count <= ticket.contract.included_tickets:
                # Ticket is covered by contract
                return 0.0
            else:
                # Extra ticket - use contract's extra ticket price
                base_price = ticket.contract.price_per_extra_ticket
    
    final_price = base_price * weight
    return round(final_price, 2)


def assign_sla_to_ticket(ticket: Ticket, db: Session):
    """Assign appropriate SLA based on priority and calculate due date"""
    sla = db.query(SLA).filter(SLA.priority == ticket.priority).first()
    
    if sla:
        ticket.sla_id = sla.id
        ticket.due_date = ticket.created_at + timedelta(hours=sla.resolution_time_hours)
    
    return ticket


def check_sla_breach(ticket: Ticket) -> bool:
    """Check if ticket has breached SLA"""
    if not ticket.due_date:
        return False
    
    if ticket.status in [TicketStatus.RESOLVED, TicketStatus.CLOSED]:
        # Check if resolved before due date
        resolved_time = ticket.resolved_at or ticket.closed_at
        if resolved_time and resolved_time > ticket.due_date:
            return True
    else:
        # Check if current time has passed due date
        if datetime.utcnow() > ticket.due_date:
            return True
    
    return False


def update_ticket_pricing(ticket: Ticket, db: Session):
    """Update ticket pricing information"""
    ticket.base_price = 50.0
    
    priority_weights = {
        "low": 1.0,
        "medium": 1.5,
        "high": 2.0,
        "critical": 3.0
    }
    
    ticket.weight_multiplier = priority_weights.get(ticket.priority, 1.0)
    ticket.final_price = calculate_ticket_price(ticket, db)
