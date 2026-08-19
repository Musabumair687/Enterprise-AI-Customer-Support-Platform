import type { TicketStatus, TicketPriority } from '@/types';

interface BadgeProps {
  children: React.ReactNode;
  className?: string;
  style?: React.CSSProperties;
}

export function Badge({ children, className = '', style }: BadgeProps) {
  return (
    <span className={`badge ${className}`} style={style}>
      {children}
    </span>
  );
}

// ─── Ticket Status ──────────────────────────────────────────────────────────────

const STATUS_CLASSES: Record<TicketStatus, string> = {
  open:             'badge--open badge--dot',
  assigned:         'badge--assigned badge--dot',
  in_progress:      'badge--in-progress badge--dot',
  waiting_customer: 'badge--waiting badge--dot',
  resolved:         'badge--resolved badge--dot',
  closed:           'badge--closed badge--dot',
};

const STATUS_LABELS: Record<TicketStatus, string> = {
  open:             'Open',
  assigned:         'Assigned',
  in_progress:      'In Progress',
  waiting_customer: 'Waiting',
  resolved:         'Resolved',
  closed:           'Closed',
};

interface TicketStatusBadgeProps {
  status: TicketStatus | string;
  isEscalated?: boolean;
}

export function TicketStatusBadge({ status, isEscalated }: TicketStatusBadgeProps) {
  if (isEscalated && status !== 'resolved' && status !== 'closed') {
    return <span className="badge badge--escalated badge--dot">Escalated</span>;
  }
  const cls = STATUS_CLASSES[status as TicketStatus] ?? 'badge--closed';
  const label = STATUS_LABELS[status as TicketStatus] ?? status;
  return <span className={`badge ${cls}`}>{label}</span>;
}

// ─── Ticket Priority ────────────────────────────────────────────────────────────

const PRIORITY_CLASSES: Record<TicketPriority, string> = {
  low:    'badge--low',
  medium: 'badge--medium',
  high:   'badge--high',
  urgent: 'badge--urgent',
};

interface TicketPriorityBadgeProps {
  priority: TicketPriority | string;
}

export function TicketPriorityBadge({ priority }: TicketPriorityBadgeProps) {
  const cls = PRIORITY_CLASSES[priority as TicketPriority] ?? 'badge--low';
  const label = priority.charAt(0).toUpperCase() + priority.slice(1);
  return <span className={`badge ${cls}`}>{label}</span>;
}

// ─── Plan Badge ─────────────────────────────────────────────────────────────────

interface PlanBadgeProps {
  plan: string | null | undefined;
}

export function PlanBadge({ plan }: PlanBadgeProps) {
  if (!plan) return <span className="badge badge--starter">—</span>;
  const lower = plan.toLowerCase();
  const cls = lower.includes('enterprise')
    ? 'badge--enterprise'
    : lower.includes('pro')
    ? 'badge--pro'
    : 'badge--starter';
  return <span className={`badge ${cls}`}>{plan}</span>;
}
