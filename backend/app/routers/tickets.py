from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ..core.database import get_db
from ..models import User, Ticket, UserRole
from ..models.ticket import TicketStatus
from ..schemas import TicketCreate, TicketUpdate, TicketResponse
from ..routers.auth import get_current_user, require_role
from ..services.ticket_service import calculate_ticket_price, assign_sla_to_ticket, check_sla_breach, update_ticket_pricing
from ..services.email_service import send_ticket_created_notification, send_ticket_assigned_notification, send_ticket_status_update_notification, send_sla_breach_notification

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post("", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
async def create_ticket(
    ticket: TicketCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Only clients can create tickets for themselves, admins can create for any client
    db_ticket = Ticket(
        title=ticket.title,
        description=ticket.description,
        priority=ticket.priority,
        client_id=current_user.id,
        contract_id=ticket.contract_id
    )
    
    # Assign SLA and calculate pricing
    assign_sla_to_ticket(db_ticket, db)
    update_ticket_pricing(db_ticket, db)
    
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    
    # Send notification
    await send_ticket_created_notification(db_ticket.id, db_ticket.title, current_user.email)
    
    return db_ticket


@router.get("", response_model=List[TicketResponse])
def list_tickets(
    status_filter: Optional[TicketStatus] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Ticket)
    
    # Role-based filtering
    if current_user.role == UserRole.CLIENT:
        query = query.filter(Ticket.client_id == current_user.id)
    elif current_user.role == UserRole.AGENT:
        query = query.filter(
            (Ticket.assigned_agent_id == current_user.id) | 
            (Ticket.assigned_agent_id == None)
        )
    # Admins can see all tickets
    
    if status_filter:
        query = query.filter(Ticket.status == status_filter)
    
    tickets = query.all()
    
    # Check for SLA breaches
    for ticket in tickets:
        if check_sla_breach(ticket) and not ticket.sla_breached:
            ticket.sla_breached = True
            db.commit()
    
    return tickets


@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(
    ticket_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Check permissions
    if current_user.role == UserRole.CLIENT and ticket.client_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this ticket")
    
    if current_user.role == UserRole.AGENT and ticket.assigned_agent_id != current_user.id and ticket.assigned_agent_id is not None:
        raise HTTPException(status_code=403, detail="Not authorized to view this ticket")
    
    # Check SLA breach
    if check_sla_breach(ticket) and not ticket.sla_breached:
        ticket.sla_breached = True
        db.commit()
    
    return ticket


@router.put("/{ticket_id}", response_model=TicketResponse)
async def update_ticket(
    ticket_id: int,
    ticket_update: TicketUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Check permissions
    if current_user.role == UserRole.CLIENT:
        # Clients can only update their own tickets and limited fields
        if ticket.client_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized")
        # Clients cannot change status or assign agents
        if ticket_update.status or ticket_update.assigned_agent_id:
            raise HTTPException(status_code=403, detail="Not authorized to change status or assignment")
    
    update_data = ticket_update.dict(exclude_unset=True)
    
    # Track status change for notification
    old_status = ticket.status
    old_agent = ticket.assigned_agent_id
    
    for field, value in update_data.items():
        setattr(ticket, field, value)
    
    # Recalculate pricing if priority changed
    if ticket_update.priority:
        update_ticket_pricing(ticket, db)
    
    # Update resolved/closed timestamps
    if ticket.status == TicketStatus.RESOLVED and old_status != TicketStatus.RESOLVED:
        from datetime import datetime
        ticket.resolved_at = datetime.utcnow()
    
    if ticket.status == TicketStatus.CLOSED and old_status != TicketStatus.CLOSED:
        from datetime import datetime
        ticket.closed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(ticket)
    
    # Send notifications
    client = db.query(User).filter(User.id == ticket.client_id).first()
    
    if ticket_update.assigned_agent_id and old_agent != ticket.assigned_agent_id:
        agent = db.query(User).filter(User.id == ticket.assigned_agent_id).first()
        if agent and client:
            await send_ticket_assigned_notification(ticket.id, ticket.title, agent.email, client.email)
    
    if ticket_update.status and old_status != ticket.status and client:
        await send_ticket_status_update_notification(ticket.id, ticket.title, ticket.status, client.email)
    
    # Check for SLA breach
    if check_sla_breach(ticket) and not ticket.sla_breached:
        ticket.sla_breached = True
        db.commit()
        # Notify admins
        admins = db.query(User).filter(User.role == UserRole.ADMIN).all()
        admin_emails = [admin.email for admin in admins]
        if admin_emails:
            await send_sla_breach_notification(ticket.id, ticket.title, admin_emails)
    
    return ticket


@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(
    ticket_id: int,
    current_user: User = Depends(require_role([UserRole.ADMIN])),
    db: Session = Depends(get_db)
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    db.delete(ticket)
    db.commit()
    return None
