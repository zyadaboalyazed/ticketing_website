import { TicketPriority } from './ticket';

export interface SLA {
  id: number;
  name: string;
  description?: string;
  priority: TicketPriority;
  response_time_hours: number;
  resolution_time_hours: number;
}

export interface SLACreate {
  name: string;
  description?: string;
  priority: TicketPriority;
  response_time_hours: number;
  resolution_time_hours: number;
}

export interface SLAUpdate {
  name?: string;
  description?: string;
  priority?: TicketPriority;
  response_time_hours?: number;
  resolution_time_hours?: number;
}
