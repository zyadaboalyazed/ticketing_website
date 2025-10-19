export interface Contract {
  id: number;
  name: string;
  description?: string;
  client_id: number;
  start_date: string;
  end_date: string;
  monthly_fee: number;
  included_tickets: number;
  price_per_extra_ticket: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface ContractCreate {
  name: string;
  description?: string;
  client_id: number;
  start_date: string;
  end_date: string;
  monthly_fee: number;
  included_tickets: number;
  price_per_extra_ticket: number;
}

export interface ContractUpdate {
  name?: string;
  description?: string;
  end_date?: string;
  monthly_fee?: number;
  included_tickets?: number;
  price_per_extra_ticket?: number;
  is_active?: boolean;
}
