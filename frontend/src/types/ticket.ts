export enum TicketPriority {
  LOW = "low",
  MEDIUM = "medium",
  HIGH = "high",
  CRITICAL = "critical",
}

export enum TicketStatus {
  OPEN = "open",
  IN_PROGRESS = "in_progress",
  RESOLVED = "resolved",
  CLOSED = "closed",
  ON_HOLD = "on_hold",
}

export interface Ticket {
  id: number;
  title: string;
  description: string;
  priority: TicketPriority;
  status: TicketStatus;
  client_id: number;
  assigned_agent_id?: number;
  contract_id?: number;
  sla_id?: number;
  base_price: number;
  weight_multiplier: number;
  final_price: number;
  created_at: string;
  updated_at: string;
  resolved_at?: string;
  closed_at?: string;
  due_date?: string;
  sla_breached: boolean;
}

export interface TicketCreate {
  title: string;
  description: string;
  priority: TicketPriority;
  contract_id?: number;
}

export interface TicketUpdate {
  title?: string;
  description?: string;
  priority?: TicketPriority;
  status?: TicketStatus;
  assigned_agent_id?: number;
}
