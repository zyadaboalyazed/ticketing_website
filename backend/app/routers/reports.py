from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models import User, Ticket, Contract, UserRole
from ..routers.auth import get_current_user, require_role
from ..services.pdf_service import generate_ticket_report_pdf, generate_contract_report_pdf
from ..services.csv_service import generate_tickets_csv, generate_contracts_csv

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/tickets/pdf")
def get_tickets_pdf_report(
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.AGENT])),
    db: Session = Depends(get_db)
):
    query = db.query(Ticket)
    
    # Agents can only export their assigned tickets
    if current_user.role == UserRole.AGENT:
        query = query.filter(Ticket.assigned_agent_id == current_user.id)
    
    tickets = query.all()
    ticket_dicts = [
        {
            "id": t.id,
            "title": t.title,
            "status": t.status,
            "priority": t.priority,
            "final_price": t.final_price,
            "created_at": str(t.created_at)
        }
        for t in tickets
    ]
    
    pdf_content = generate_ticket_report_pdf(ticket_dicts)
    
    return Response(
        content=pdf_content,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=tickets_report.pdf"}
    )


@router.get("/tickets/csv")
def get_tickets_csv_report(
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.AGENT])),
    db: Session = Depends(get_db)
):
    query = db.query(Ticket)
    
    # Agents can only export their assigned tickets
    if current_user.role == UserRole.AGENT:
        query = query.filter(Ticket.assigned_agent_id == current_user.id)
    
    tickets = query.all()
    ticket_dicts = [
        {
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "status": t.status,
            "priority": t.priority,
            "client_id": t.client_id,
            "assigned_agent_id": t.assigned_agent_id,
            "final_price": t.final_price,
            "created_at": str(t.created_at),
            "resolved_at": str(t.resolved_at) if t.resolved_at else None,
            "sla_breached": t.sla_breached
        }
        for t in tickets
    ]
    
    csv_content = generate_tickets_csv(ticket_dicts)
    
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=tickets_report.csv"}
    )


@router.get("/contracts/pdf")
def get_contracts_pdf_report(
    current_user: User = Depends(require_role([UserRole.ADMIN])),
    db: Session = Depends(get_db)
):
    contracts = db.query(Contract).all()
    contract_dicts = [
        {
            "id": c.id,
            "name": c.name,
            "client_id": c.client_id,
            "monthly_fee": c.monthly_fee,
            "is_active": c.is_active,
            "end_date": str(c.end_date)
        }
        for c in contracts
    ]
    
    pdf_content = generate_contract_report_pdf(contract_dicts)
    
    return Response(
        content=pdf_content,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=contracts_report.pdf"}
    )


@router.get("/contracts/csv")
def get_contracts_csv_report(
    current_user: User = Depends(require_role([UserRole.ADMIN])),
    db: Session = Depends(get_db)
):
    contracts = db.query(Contract).all()
    contract_dicts = [
        {
            "id": c.id,
            "name": c.name,
            "client_id": c.client_id,
            "start_date": str(c.start_date),
            "end_date": str(c.end_date),
            "monthly_fee": c.monthly_fee,
            "included_tickets": c.included_tickets,
            "price_per_extra_ticket": c.price_per_extra_ticket,
            "is_active": c.is_active
        }
        for c in contracts
    ]
    
    csv_content = generate_contracts_csv(contract_dicts)
    
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=contracts_report.csv"}
    )
