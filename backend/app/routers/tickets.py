from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ..core.database import get_db
from ..models.user import User, UserRole
from ..models.ticket import Ticket, TicketComment, TicketStatus
from ..models.contract import Contract
from ..schemas.ticket import (
    Ticket as TicketSchema,
    TicketCreate,
    TicketUpdate,
    TicketComment as TicketCommentSchema,
    TicketCommentCreate
)
from ..utils.dependencies import get_current_user, get_current_agent_or_admin
from ..services.email import (
    send_ticket_created_notification,
    send_ticket_assigned_notification,
    send_ticket_status_update_notification
)
from ..services.sla import calculate_sla_due_date, update_ticket_sla_status, calculate_ticket_cost

router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.post("/", response_model=TicketSchema, status_code=status.HTTP_201_CREATED)
async def create_ticket(
    ticket_data: TicketCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new ticket"""
    # Get contract if specified
    contract = None
    if ticket_data.contract_id:
        contract = db.query(Contract).filter(Contract.id == ticket_data.contract_id).first()
        if not contract:
            raise HTTPException(status_code=404, detail="Contract not found")
    
    # Create ticket
    db_ticket = Ticket(
        title=ticket_data.title,
        description=ticket_data.description,
        priority=ticket_data.priority,
        creator_id=current_user.id,
        contract_id=ticket_data.contract_id,
        hourly_rate=contract.hourly_rate if contract else 0.0
    )
    
    # Calculate SLA due date
    db_ticket.sla_due_date = calculate_sla_due_date(db_ticket, contract)
    
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    
    # Send notification
    try:
        await send_ticket_created_notification(db_ticket, current_user.email)
    except Exception as e:
        print(f"Failed to send email: {e}")
    
    return db_ticket


@router.get("/", response_model=List[TicketSchema])
def list_tickets(
    skip: int = 0,
    limit: int = 100,
    status: str = None,
    priority: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List tickets based on user role"""
    query = db.query(Ticket)
    
    # Filter based on role
    if current_user.role == UserRole.CLIENT:
        query = query.filter(Ticket.creator_id == current_user.id)
    elif current_user.role == UserRole.AGENT:
        query = query.filter(
            (Ticket.assignee_id == current_user.id) | (Ticket.assignee_id == None)
        )
    # Admin can see all tickets
    
    # Apply filters
    if status:
        query = query.filter(Ticket.status == status)
    if priority:
        query = query.filter(Ticket.priority == priority)
    
    tickets = query.offset(skip).limit(limit).all()
    
    # Update SLA status for each ticket
    for ticket in tickets:
        update_ticket_sla_status(db, ticket)
    
    return tickets


@router.get("/{ticket_id}", response_model=TicketSchema)
def get_ticket(
    ticket_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get ticket by ID"""
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Check permissions
    if current_user.role == UserRole.CLIENT and ticket.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this ticket")
    
    update_ticket_sla_status(db, ticket)
    return ticket


@router.put("/{ticket_id}", response_model=TicketSchema)
async def update_ticket(
    ticket_id: int,
    ticket_update: TicketUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update ticket"""
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Check permissions
    if current_user.role == UserRole.CLIENT:
        # Clients can only update their own tickets and only specific fields
        if ticket.creator_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized")
        # Clients cannot change status or assignee
        if ticket_update.status or ticket_update.assignee_id:
            raise HTTPException(status_code=403, detail="Cannot modify status or assignee")
    
    old_status = ticket.status
    old_assignee_id = ticket.assignee_id
    
    update_data = ticket_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(ticket, field, value)
    
    # Update timestamps based on status
    if ticket_update.status:
        if ticket_update.status == TicketStatus.RESOLVED:
            ticket.resolved_at = datetime.utcnow()
        elif ticket_update.status == TicketStatus.CLOSED:
            ticket.closed_at = datetime.utcnow()
    
    # Update cost if actual hours changed
    if ticket_update.actual_hours:
        contract = db.query(Contract).filter(Contract.id == ticket.contract_id).first() if ticket.contract_id else None
        ticket.total_cost = calculate_ticket_cost(ticket, contract)
    
    db.commit()
    db.refresh(ticket)
    
    # Send notifications
    try:
        if ticket_update.assignee_id and ticket_update.assignee_id != old_assignee_id:
            assignee = db.query(User).filter(User.id == ticket.assignee_id).first()
            if assignee:
                await send_ticket_assigned_notification(ticket, assignee.email)
        
        if ticket_update.status and ticket_update.status != old_status:
            creator = db.query(User).filter(User.id == ticket.creator_id).first()
            if creator:
                await send_ticket_status_update_notification(ticket, creator.email)
    except Exception as e:
        print(f"Failed to send email: {e}")
    
    return ticket


@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(
    ticket_id: int,
    current_user: User = Depends(get_current_agent_or_admin),
    db: Session = Depends(get_db)
):
    """Delete ticket (Agent/Admin only)"""
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    db.delete(ticket)
    db.commit()
    return None


@router.post("/{ticket_id}/comments", response_model=TicketCommentSchema, status_code=status.HTTP_201_CREATED)
def create_comment(
    ticket_id: int,
    comment_data: TicketCommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a comment to a ticket"""
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Check permissions
    if current_user.role == UserRole.CLIENT and ticket.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Clients cannot create internal comments
    if current_user.role == UserRole.CLIENT and comment_data.is_internal:
        raise HTTPException(status_code=403, detail="Cannot create internal comments")
    
    db_comment = TicketComment(
        ticket_id=ticket_id,
        user_id=current_user.id,
        content=comment_data.content,
        is_internal=comment_data.is_internal
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


@router.get("/{ticket_id}/comments", response_model=List[TicketCommentSchema])
def list_comments(
    ticket_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List comments for a ticket"""
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Check permissions
    if current_user.role == UserRole.CLIENT and ticket.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    query = db.query(TicketComment).filter(TicketComment.ticket_id == ticket_id)
    
    # Clients cannot see internal comments
    if current_user.role == UserRole.CLIENT:
        query = query.filter(TicketComment.is_internal == 0)
    
    comments = query.all()
    return comments
