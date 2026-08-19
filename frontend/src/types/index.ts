/**
 * TypeScript interfaces aligned to FastAPI schemas in backend/app/schemas/api.py
 * and designed for future LangGraph output integration.
 *
 * RULE: All interfaces must match the actual backend. Optional fields (marked ?)
 * are future LangGraph fields — components handle undefined gracefully.
 */

// ─── API Wrapper ──────────────────────────────────────────────────────────────

export interface APIResponse<T> {
  success: boolean;
  message: string;
  data: T;
}

// ─── RAG Sources (ready for hybrid RAG pipeline) ──────────────────────────────

export interface RAGSource {
  title: string;        // e.g. "CloudDesk API Manual"
  section?: string;     // e.g. "Authentication / OAuth"
  relevance?: number;   // e.g. 0.92  (0–1)
  document_id?: string;
}

// ─── AI Response (matches ChatResponse + future LangGraph fields) ─────────────

export interface EscalationAssignee {
  id: number;
  name: string;
  department: string;
}

export interface ChatEscalation {
  ticket_id: number | null;
  reason: string | null;
  assigned_employee: EscalationAssignee | null;
}

export interface AIResponse {
  // Current backend fields (from ChatResponse schema)
  response: string;
  session_id: string;
  agents_used: string[];
  escalated: boolean;
  escalation: ChatEscalation | null;

  // Future LangGraph fields — optional until backend provides them
  intent?: string;             // e.g. "technical_support"
  confidence?: number;         // 0–1, e.g. 0.91
  agent?: string;              // e.g. "technical_agent"
  sources?: RAGSource[];       // RAG retrieval results
  tools_used?: string[];       // e.g. ["known_issue_lookup", "billing_tool"]
}

// ─── Chat Request ─────────────────────────────────────────────────────────────

export interface ChatRequest {
  message: string;
  session_id?: string;
  customer_id?: number;
}

// ─── Customer ─────────────────────────────────────────────────────────────────

export interface Customer {
  id: number;
  external_id: string | null;
  name: string;
  email: string;
  company: string | null;
  phone: string | null;
  country: string | null;
  timezone: string | null;
  subscription_plan: string | null;
  status: string;
  registration_date: string | null;
  renewal_date: string | null;
  last_login: string | null;
  preferred_language: string | null;
  support_tier: string | null;
  account_manager: string | null;
  monthly_revenue: string | null;
  lifetime_value: string | null;
  created_at: string;
  updated_at: string;
}

// ─── Employee ─────────────────────────────────────────────────────────────────

export interface Employee {
  id: number;
  name: string;
  email: string;
  role: string;
  is_active: boolean;
  created_at: string;
}

// ─── Ticket ───────────────────────────────────────────────────────────────────

export type TicketStatus =
  | 'open'
  | 'assigned'
  | 'in_progress'
  | 'waiting_customer'
  | 'resolved'
  | 'closed';

export type TicketPriority = 'low' | 'medium' | 'high' | 'urgent';

export interface Ticket {
  id: number;
  external_id: string | null;
  customer_id: number;
  title: string;
  description: string;
  status: TicketStatus;
  priority: TicketPriority;
  department: string | null;
  category: string | null;
  assigned_agent_name: string | null;
  escalation_reason: string | null;
  resolution: string | null;
  sentiment: string | null;
  resolution_time_hours: string | null;
  is_escalated: boolean;
  assigned_employee_id: number | null;
  product_id: number | null;
  created_at: string;
  updated_at: string;
  resolved_at: string | null;
}

export interface TicketCreate {
  customer_id: number;
  title: string;
  description: string;
  status?: string;
  priority?: string;
  department?: string | null;
  category?: string | null;
  assigned_agent_name?: string | null;
  escalation_reason?: string | null;
  is_escalated?: boolean;
  assigned_employee_id?: number | null;
}

export interface TicketUpdate {
  title?: string;
  description?: string;
  status?: string;
  priority?: string;
  department?: string | null;
  assigned_agent_name?: string | null;
  resolution?: string | null;
  is_escalated?: boolean;
  escalation_reason?: string | null;
  assigned_employee_id?: number | null;
}

// ─── Billing ─────────────────────────────────────────────────────────────────

export type BillingStatus = 'paid' | 'pending' | 'overdue' | 'failed' | 'refunded' | 'partial';
export type BillingRecordType = 'invoice' | 'payment' | 'refund' | 'credit';

export interface BillingRecord {
  id: number;
  customer_id: number;
  invoice_number: string | null;
  plan: string | null;
  amount: string;
  currency: string;
  status: string;
  record_type: string;
  payment_method: string | null;
  due_date: string | null;
  paid_date: string | null;
  refund_status: string | null;
  created_at: string;
}

// ─── Conversation ─────────────────────────────────────────────────────────────

export type SenderRole = 'customer' | 'ai' | 'agent' | 'system';

export interface Conversation {
  id: number;
  customer_id: number;
  ticket_id: number | null;
  session_id: string;
  sender_role: SenderRole;
  content: string;
  created_at: string;
}

// ─── Dashboard Metrics (computed client-side — Phase 1) ──────────────────────
// TODO: Replace with GET /api/v1/analytics/dashboard when backend endpoint is built

export interface DashboardMetrics {
  openTickets: number;
  aiResolvedPercent: number;
  escalations: number;
  avgResponseMinutes: number;
  ticketTrend: number;      // % change from prior period
  aiResolveTrend: number;
  escalationTrend: number;
  responseTrend: number;
}

export interface TicketVolumeDataPoint {
  day: string;
  tickets: number;
  resolved: number;
}

export interface EscalationReasonData {
  reason: string;
  count: number;
}

// ─── AI Settings (read-only, reflects backend config) ────────────────────────
// TODO: Bind to GET /api/v1/settings/ai when available

export interface AISettings {
  llm_provider: string;
  fallback_provider: string;
  gemini_model: string;
  groq_model: string;
  confidence_threshold: number;
  human_escalation_enabled: boolean;
  rag_top_k: number;
  reranker_enabled: boolean;
  max_agent_steps: number;
  llm_timeout_seconds: number;
}

// ─── Auth ─────────────────────────────────────────────────────────────────────

export interface AuthUser {
  id: number;
  name: string;
  email: string;
  role: string;
  avatar?: string;
}
