from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models.user import User
from ..models.ticket import Ticket
from ..utils.dependencies import get_current_agent_or_admin
from ..services.reports import generate_pdf_report, generate_csv_report

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/tickets/pdf")
def get_tickets_pdf_report(
    status: str = None,
    priority: str = None,
    current_user: User = Depends(get_current_agent_or_admin),
    db: Session = Depends(get_db)
):
    """Generate PDF report of tickets (Agent/Admin only)"""
    query = db.query(Ticket)
    
    if status:
        query = query.filter(Ticket.status == status)
    if priority:
        query = query.filter(Ticket.priority == priority)
    
    tickets = query.all()
    
    if not tickets:
        raise HTTPException(status_code=404, detail="No tickets found for report")
    
    pdf_buffer = generate_pdf_report(tickets)
    
    return Response(
        content=pdf_buffer.read(),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=tickets_report.pdf"}
    )


@router.get("/tickets/csv")
def get_tickets_csv_report(
    status: str = None,
    priority: str = None,
    current_user: User = Depends(get_current_agent_or_admin),
    db: Session = Depends(get_db)
):
    """Generate CSV report of tickets (Agent/Admin only)"""
    query = db.query(Ticket)
    
    if status:
        query = query.filter(Ticket.status == status)
    if priority:
        query = query.filter(Ticket.priority == priority)
    
    tickets = query.all()
    
    if not tickets:
        raise HTTPException(status_code=404, detail="No tickets found for report")
    
    csv_buffer = generate_csv_report(tickets)
    
    return Response(
        content=csv_buffer.read(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=tickets_report.csv"}
    )
