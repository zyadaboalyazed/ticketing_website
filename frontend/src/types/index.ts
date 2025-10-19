export interface User {
  id: number;
  email: string;
  username: string;
  full_name?: string;
  role: 'admin' | 'agent' | 'client';
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Ticket {
  id: number;
  title: string;
  description?: string;
  priority: 'low' | 'medium' | 'high' | 'critical';
  status: 'open' | 'in_progress' | 'pending' | 'resolved' | 'closed';
  creator_id: number;
  assignee_id?: number;
  contract_id?: number;
  created_at: string;
  updated_at: string;
  resolved_at?: string;
  closed_at?: string;
  sla_due_date?: string;
  sla_breached: number;
  estimated_hours: number;
  actual_hours: number;
  hourly_rate: number;
  total_cost: number;
}

export interface Contract {
  id: number;
  name: string;
  description?: string;
  client_id: number;
  base_rate: number;
  hourly_rate: number;
  included_hours: number;
  overage_rate: number;
  response_time_hours: number;
  resolution_time_hours: number;
  start_date: string;
  end_date: string;
  is_active: number;
  created_at: string;
  updated_at: string;
}

export interface TicketComment {
  id: number;
  ticket_id: number;
  user_id: number;
  content: string;
  is_internal: number;
  created_at: string;
}
