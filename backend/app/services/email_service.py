import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List
from ..core.config import settings


async def send_email(to_email: List[str], subject: str, body: str, html: bool = False):
    """Send email notification"""
    try:
        message = MIMEMultipart("alternative")
        message["From"] = settings.EMAIL_FROM
        message["To"] = ", ".join(to_email)
        message["Subject"] = subject

        if html:
            part = MIMEText(body, "html")
        else:
            part = MIMEText(body, "plain")
        
        message.attach(part)

        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            start_tls=True,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False


async def send_ticket_created_notification(ticket_id: int, title: str, client_email: str):
    """Send notification when ticket is created"""
    subject = f"Ticket #{ticket_id} Created: {title}"
    body = f"""
    Your ticket has been created successfully.
    
    Ticket ID: #{ticket_id}
    Title: {title}
    
    You will be notified when an agent is assigned to your ticket.
    
    Thank you for using our ticketing system.
    """
    await send_email([client_email], subject, body)


async def send_ticket_assigned_notification(ticket_id: int, title: str, agent_email: str, client_email: str):
    """Send notification when ticket is assigned"""
    subject = f"Ticket #{ticket_id} Assigned"
    body = f"""
    A ticket has been assigned to you.
    
    Ticket ID: #{ticket_id}
    Title: {title}
    
    Please review and update the ticket status accordingly.
    """
    await send_email([agent_email], subject, body)
    
    # Notify client
    client_body = f"""
    Your ticket has been assigned to an agent.
    
    Ticket ID: #{ticket_id}
    Title: {title}
    
    Our team is working on resolving your issue.
    """
    await send_email([client_email], f"Ticket #{ticket_id} Update", client_body)


async def send_ticket_status_update_notification(ticket_id: int, title: str, status: str, client_email: str):
    """Send notification when ticket status changes"""
    subject = f"Ticket #{ticket_id} Status Updated"
    body = f"""
    Your ticket status has been updated.
    
    Ticket ID: #{ticket_id}
    Title: {title}
    New Status: {status}
    
    Thank you for your patience.
    """
    await send_email([client_email], subject, body)


async def send_sla_breach_notification(ticket_id: int, title: str, admin_emails: List[str]):
    """Send notification when SLA is breached"""
    subject = f"SLA BREACH: Ticket #{ticket_id}"
    body = f"""
    ALERT: SLA has been breached for the following ticket.
    
    Ticket ID: #{ticket_id}
    Title: {title}
    
    Immediate attention required.
    """
    await send_email(admin_emails, subject, body)
