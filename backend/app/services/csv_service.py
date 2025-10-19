import pandas as pd
from typing import List, Dict
import io


def generate_tickets_csv(tickets: List[Dict]) -> bytes:
    """Generate CSV export for tickets"""
    df = pd.DataFrame(tickets)
    
    # Select and order columns
    columns = ['id', 'title', 'description', 'status', 'priority', 
               'client_id', 'assigned_agent_id', 'final_price', 
               'created_at', 'resolved_at', 'sla_breached']
    
    # Filter existing columns
    available_columns = [col for col in columns if col in df.columns]
    df = df[available_columns]
    
    # Convert to CSV
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False, encoding='utf-8')
    buffer.seek(0)
    return buffer.read()


def generate_contracts_csv(contracts: List[Dict]) -> bytes:
    """Generate CSV export for contracts"""
    df = pd.DataFrame(contracts)
    
    # Select and order columns
    columns = ['id', 'name', 'client_id', 'start_date', 'end_date',
               'monthly_fee', 'included_tickets', 'price_per_extra_ticket',
               'is_active']
    
    # Filter existing columns
    available_columns = [col for col in columns if col in df.columns]
    df = df[available_columns]
    
    # Convert to CSV
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False, encoding='utf-8')
    buffer.seek(0)
    return buffer.read()
