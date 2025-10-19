from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
from typing import List, Dict
import io


def generate_ticket_report_pdf(tickets: List[Dict]) -> bytes:
    """Generate PDF report for tickets"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    # Title
    title = Paragraph("Ticket Report", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.3 * inch))
    
    # Report date
    date_text = f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    elements.append(Paragraph(date_text, styles['Normal']))
    elements.append(Spacer(1, 0.2 * inch))
    
    # Table data
    data = [['ID', 'Title', 'Status', 'Priority', 'Price', 'Created']]
    
    for ticket in tickets:
        data.append([
            str(ticket.get('id', '')),
            ticket.get('title', '')[:30],
            ticket.get('status', ''),
            ticket.get('priority', ''),
            f"${ticket.get('final_price', 0):.2f}",
            ticket.get('created_at', '')[:10] if ticket.get('created_at') else ''
        ])
    
    # Create table
    table = Table(data, colWidths=[0.7*inch, 2.5*inch, 1*inch, 1*inch, 1*inch, 1.3*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 0.3 * inch))
    
    # Summary
    total_tickets = len(tickets)
    total_price = sum(ticket.get('final_price', 0) for ticket in tickets)
    summary_text = f"Total Tickets: {total_tickets} | Total Value: ${total_price:.2f}"
    elements.append(Paragraph(summary_text, styles['Normal']))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer.read()


def generate_contract_report_pdf(contracts: List[Dict]) -> bytes:
    """Generate PDF report for contracts"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    # Title
    title = Paragraph("Contract Report", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.3 * inch))
    
    # Report date
    date_text = f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    elements.append(Paragraph(date_text, styles['Normal']))
    elements.append(Spacer(1, 0.2 * inch))
    
    # Table data
    data = [['ID', 'Name', 'Client ID', 'Monthly Fee', 'Active', 'End Date']]
    
    for contract in contracts:
        data.append([
            str(contract.get('id', '')),
            contract.get('name', '')[:25],
            str(contract.get('client_id', '')),
            f"${contract.get('monthly_fee', 0):.2f}",
            'Yes' if contract.get('is_active') else 'No',
            contract.get('end_date', '')[:10] if contract.get('end_date') else ''
        ])
    
    # Create table
    table = Table(data, colWidths=[0.7*inch, 2*inch, 1*inch, 1.2*inch, 1*inch, 1.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))
    
    elements.append(table)
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer.read()
