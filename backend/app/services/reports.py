from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
import pandas as pd
from io import BytesIO
from typing import List
from ..models.ticket import Ticket


def generate_pdf_report(tickets: List[Ticket], filename: str = None) -> BytesIO:
    """Generate PDF report for tickets"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title = Paragraph("Tickets Report", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 0.3 * inch))
    
    # Summary
    summary_text = f"Total Tickets: {len(tickets)}"
    summary = Paragraph(summary_text, styles['Normal'])
    elements.append(summary)
    elements.append(Spacer(1, 0.2 * inch))
    
    # Table data
    data = [['ID', 'Title', 'Status', 'Priority', 'Created', 'Cost']]
    for ticket in tickets:
        data.append([
            str(ticket.id),
            ticket.title[:30],
            ticket.status,
            ticket.priority,
            ticket.created_at.strftime('%Y-%m-%d'),
            f"${ticket.total_cost:.2f}"
        ])
    
    # Create table
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table)
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer


def generate_csv_report(tickets: List[Ticket]) -> BytesIO:
    """Generate CSV report for tickets"""
    data = []
    for ticket in tickets:
        data.append({
            'ID': ticket.id,
            'Title': ticket.title,
            'Description': ticket.description,
            'Status': ticket.status,
            'Priority': ticket.priority,
            'Creator ID': ticket.creator_id,
            'Assignee ID': ticket.assignee_id,
            'Created At': ticket.created_at,
            'Updated At': ticket.updated_at,
            'SLA Due Date': ticket.sla_due_date,
            'SLA Breached': ticket.sla_breached,
            'Estimated Hours': ticket.estimated_hours,
            'Actual Hours': ticket.actual_hours,
            'Hourly Rate': ticket.hourly_rate,
            'Total Cost': ticket.total_cost
        })
    
    df = pd.DataFrame(data)
    buffer = BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    return buffer
