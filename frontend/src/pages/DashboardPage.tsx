import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  TrendingUp, TrendingDown, Ticket, Bot, AlertTriangle, Clock, CheckCircle,
} from 'lucide-react';
import { useAuth } from '@/context/AuthContext';
import { useTickets } from '@/hooks/useTickets';
import { useBilling } from '@/hooks/useBilling';
import { useAnalytics } from '@/hooks/useAnalytics';
import TicketVolumeChart from '@/components/charts/TicketVolumeChart';
import AIvsHumanChart from '@/components/charts/AIvsHumanChart';
import { formatRelativeTime } from '@/utils/formatters';
import { TicketStatusBadge, TicketPriorityBadge } from '@/components/ui/Badge';
import { SkeletonKPI } from '@/components/ui/Skeleton';

// ─── KPI Card ─────────────────────────────────────────────────────────────────

interface KPICardProps {
  title: string;
  value: string | number;
  icon: React.ReactNode;
  iconBg: string;
  trend: number;        // positive = up, negative = down
  trendPositiveIsGood?: boolean;
}

function KPICard({ title, value, icon, iconBg, trend, trendPositiveIsGood = true }: KPICardProps) {
  const isPositive = trend > 0;
  const isGood = trendPositiveIsGood ? isPositive : !isPositive;
  const color = isGood ? 'var(--color-success)' : 'var(--color-danger)';
  const TrendIcon = isPositive ? TrendingUp : TrendingDown;

  return (
    <div className="kpi-card">
      <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', marginBottom: 'var(--space-3)' }}>
        <span className="kpi-card__label">{title}</span>
        <div className="kpi-card__icon" style={{ background: iconBg }}>
          {icon}
        </div>
      </div>
      <div className="kpi-card__value">{value}</div>
      <div className={`kpi-card__trend ${isGood ? 'kpi-card__trend--up' : 'kpi-card__trend--down'}`} style={{ color }}>
        <TrendIcon size={12} aria-hidden="true" />
        {Math.abs(trend).toFixed(1)}% vs last period
      </div>
    </div>
  );
}

// ─── Dashboard Page ────────────────────────────────────────────────────────────

const DATE_FILTERS = ['Today', 'Last 7 Days', 'Last 30 Days'] as const;
type DateFilter = typeof DATE_FILTERS[number];

export default function DashboardPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [dateFilter, setDateFilter] = useState<DateFilter>('Last 7 Days');

  const { tickets, isLoading: isLoadingTickets } = useTickets({ limit: 500 });
  const { records: billing } = useBilling({ limit: 500 });
  const { metrics, ticketVolume, aiResolutionData } = useAnalytics(tickets, billing);

  // Time-aware greeting
  const hour = new Date().getHours();
  const greeting = hour < 12 ? 'Good morning' : hour < 18 ? 'Good afternoon' : 'Good evening';

  // Escalated open tickets for Human Attention table
  const humanAttentionTickets = tickets
    .filter((t) => t.is_escalated && t.status !== 'resolved' && t.status !== 'closed')
    .slice(0, 8);

  return (
    <div className="page-content fade-in" id="dashboard-page">
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', marginBottom: 'var(--space-6)' }}>
        <div className="dashboard-greeting">
          <h1 className="dashboard-greeting__title">{greeting}, {user?.name ?? 'there'}</h1>
          <p className="dashboard-greeting__subtitle">Here's what's happening with Corvex Support today.</p>
        </div>
        {/* Date filter */}
        <div className="dashboard-filters">
          {DATE_FILTERS.map((f) => (
            <button
              key={f}
              id={`date-filter-${f.replace(/\s+/g, '-').toLowerCase()}`}
              className={`date-filter-btn${dateFilter === f ? ' date-filter-btn--active' : ''}`}
              onClick={() => setDateFilter(f)}
              aria-pressed={dateFilter === f}
            >
              {f}
            </button>
          ))}
        </div>
      </div>

      {/* KPI Grid */}
      <div className="kpi-grid" role="region" aria-label="Key performance indicators">
        {isLoadingTickets ? (
          <>
            <SkeletonKPI /><SkeletonKPI /><SkeletonKPI /><SkeletonKPI />
          </>
        ) : (
          <>
            <KPICard
              title="Open Tickets"
              value={metrics.openTickets}
              icon={<Ticket size={18} style={{ color: 'var(--color-info)' }} />}
              iconBg="var(--color-info-bg)"
              trend={metrics.ticketTrend}
              trendPositiveIsGood={false}
            />
            <KPICard
              title="AI Resolved"
              value={`${metrics.aiResolvedPercent}%`}
              icon={<Bot size={18} style={{ color: 'var(--color-ai)' }} />}
              iconBg="var(--color-ai-bg)"
              trend={metrics.aiResolveTrend}
            />
            <KPICard
              title="Escalations"
              value={metrics.escalations}
              icon={<AlertTriangle size={18} style={{ color: 'var(--color-danger)' }} />}
              iconBg="var(--color-danger-bg)"
              trend={metrics.escalationTrend}
              trendPositiveIsGood={false}
            />
            <KPICard
              title="Avg Response"
              value={`${metrics.avgResponseMinutes.toFixed(0)}m`}
              icon={<Clock size={18} style={{ color: 'var(--color-success)' }} />}
              iconBg="var(--color-success-bg)"
              trend={metrics.responseTrend}
              trendPositiveIsGood={false}
            />
          </>
        )}
      </div>

      {/* Charts */}
      <div className="chart-grid" role="region" aria-label="Charts">
        <TicketVolumeChart data={ticketVolume} isLoading={isLoadingTickets} />
        <AIvsHumanChart data={aiResolutionData} isLoading={isLoadingTickets} />
      </div>

      {/* Human Attention Required */}
      <div
        className="card"
        role="region"
        aria-label="Tickets requiring human attention"
      >
        <div className="card__header">
          <div>
            <h2 className="card__title">
              <span style={{ color: 'var(--color-danger)', marginRight: 6 }}>⚠</span>
              Human Attention Required
            </h2>
            <p className="card__subtitle">Escalated tickets awaiting agent response</p>
          </div>
          {humanAttentionTickets.length > 0 && (
            <button
              id="view-all-escalations-btn"
              className="btn btn--ghost btn--sm"
              onClick={() => navigate('/tickets?view=escalated')}
            >
              View All
            </button>
          )}
        </div>
        <div className="card__body--no-pad">
          {isLoadingTickets ? (
            <div style={{ padding: 'var(--space-8)' }}>
              <div className="skeleton" style={{ height: 200 }} />
            </div>
          ) : humanAttentionTickets.length === 0 ? (
            <div className="empty-state">
              <div className="empty-state__icon" style={{ background: 'var(--color-success-bg)' }}>
                <CheckCircle size={24} style={{ color: 'var(--color-success)' }} />
              </div>
              <div className="empty-state__title">All caught up!</div>
              <p className="empty-state__desc">No tickets require immediate human attention.</p>
            </div>
          ) : (
            <div className="table-container" style={{ border: 'none', borderRadius: 0 }}>
              <table className="table">
                <thead>
                  <tr>
                    <th>Ticket</th>
                    <th>Subject</th>
                    <th>Status</th>
                    <th>Priority</th>
                    <th>Escalation Reason</th>
                    <th>Time</th>
                  </tr>
                </thead>
                <tbody>
                  {humanAttentionTickets.map((ticket) => (
                    <tr
                      key={ticket.id}
                      id={`dashboard-ticket-${ticket.id}`}
                      className="table-row--escalated"
                      onClick={() => navigate(`/tickets/${ticket.id}`)}
                      role="button"
                      tabIndex={0}
                      onKeyDown={(e) => { if (e.key === 'Enter') navigate(`/tickets/${ticket.id}`); }}
                      aria-label={`Open ticket ${ticket.id}: ${ticket.title}`}
                    >
                      <td style={{ color: 'var(--color-text-muted)', fontWeight: 500 }}>#{ticket.id}</td>
                      <td style={{ fontWeight: 500, maxWidth: 240 }} className="truncate">{ticket.title}</td>
                      <td><TicketStatusBadge status={ticket.status} isEscalated={ticket.is_escalated} /></td>
                      <td><TicketPriorityBadge priority={ticket.priority} /></td>
                      <td style={{ color: 'var(--color-text-muted)', fontSize: 'var(--text-xs)' }}>
                        {ticket.escalation_reason ?? '—'}
                      </td>
                      <td style={{ color: 'var(--color-text-muted)' }}>{formatRelativeTime(ticket.created_at)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
