import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
from ..core.config import settings


async def send_email(to_email: str, subject: str, body: str):
    """Send an email notification"""
    message = MIMEMultipart("alternative")
    message["From"] = settings.EMAIL_FROM
    message["To"] = to_email
    message["Subject"] = subject
    
    html_part = MIMEText(body, "html")
    message.attach(html_part)
    
    try:
        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            start_tls=True,
        )
    except Exception as e:
        print(f"Error sending email: {e}")


async def send_ticket_created_notification(ticket, creator_email: str):
    """Send notification when a ticket is created"""
    subject = f"Ticket #{ticket.id} Created: {ticket.title}"
    body = f"""
    <html>
    <body>
        <h2>New Ticket Created</h2>
        <p><strong>Ticket ID:</strong> {ticket.id}</p>
        <p><strong>Title:</strong> {ticket.title}</p>
        <p><strong>Priority:</strong> {ticket.priority}</p>
        <p><strong>Status:</strong> {ticket.status}</p>
        <p><strong>Description:</strong> {ticket.description}</p>
        <p>You can view and manage this ticket in the ticketing system.</p>
    </body>
    </html>
    """
    await send_email(creator_email, subject, body)


async def send_ticket_assigned_notification(ticket, assignee_email: str):
    """Send notification when a ticket is assigned"""
    subject = f"Ticket #{ticket.id} Assigned to You: {ticket.title}"
    body = f"""
    <html>
    <body>
        <h2>Ticket Assigned</h2>
        <p><strong>Ticket ID:</strong> {ticket.id}</p>
        <p><strong>Title:</strong> {ticket.title}</p>
        <p><strong>Priority:</strong> {ticket.priority}</p>
        <p><strong>Status:</strong> {ticket.status}</p>
        <p><strong>Description:</strong> {ticket.description}</p>
        <p>This ticket has been assigned to you. Please review and take action.</p>
    </body>
    </html>
    """
    await send_email(assignee_email, subject, body)


async def send_ticket_status_update_notification(ticket, user_email: str):
    """Send notification when ticket status changes"""
    subject = f"Ticket #{ticket.id} Status Updated: {ticket.status}"
    body = f"""
    <html>
    <body>
        <h2>Ticket Status Updated</h2>
        <p><strong>Ticket ID:</strong> {ticket.id}</p>
        <p><strong>Title:</strong> {ticket.title}</p>
        <p><strong>New Status:</strong> {ticket.status}</p>
        <p>The status of your ticket has been updated.</p>
    </body>
    </html>
    """
    await send_email(user_email, subject, body)


async def send_sla_breach_notification(ticket, admin_email: str):
    """Send notification when SLA is breached"""
    subject = f"SLA BREACH - Ticket #{ticket.id}: {ticket.title}"
    body = f"""
    <html>
    <body>
        <h2 style="color: red;">SLA BREACH ALERT</h2>
        <p><strong>Ticket ID:</strong> {ticket.id}</p>
        <p><strong>Title:</strong> {ticket.title}</p>
        <p><strong>Priority:</strong> {ticket.priority}</p>
        <p><strong>SLA Due Date:</strong> {ticket.sla_due_date}</p>
        <p>This ticket has breached its SLA. Immediate action required!</p>
    </body>
    </html>
    """
    await send_email(admin_email, subject, body)
