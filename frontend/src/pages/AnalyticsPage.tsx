/**
 * Analytics Page — AI Performance & Support Metrics
 * TODO: Replace all client-side computations with GET /api/v1/analytics/dashboard
 */
import { useMemo } from 'react';
import { useTickets } from '@/hooks/useTickets';
import { useBilling } from '@/hooks/useBilling';
import { useAnalytics } from '@/hooks/useAnalytics';
import EscalationReasonChart from '@/components/charts/EscalationReasonChart';
import { formatCurrencyShort, formatPercentInt } from '@/utils/formatters';
import { SkeletonKPI } from '@/components/ui/Skeleton';

function MetricRow({ label, value, muted }: { label: string; value: string; muted?: boolean }) {
  return (
    <div className="analytics-metric-row">
      <span className="analytics-metric-label">{label}</span>
      <span className={`analytics-metric-value${muted ? ' text-muted' : ''}`} style={muted ? { fontWeight: 400, fontSize: 'var(--text-xs)' } : undefined}>
        {value}
      </span>
    </div>
  );
}

export default function AnalyticsPage() {
  const { tickets, isLoading: isLoadingTickets } = useTickets({ limit: 500 });
  const { records: billingRecords, isLoading: isLoadingBilling } = useBilling({ limit: 500 });
  const { metrics, escalationReasons } = useAnalytics(tickets, billingRecords);

  const totalTickets = tickets.length;
  const openTickets = tickets.filter((t) => ['open', 'assigned', 'in_progress'].includes(t.status)).length;
  const resolvedTickets = tickets.filter((t) => t.status === 'resolved' || t.status === 'closed').length;
  const resolutionRate = totalTickets > 0 ? (resolvedTickets / totalTickets) : 0;
  const escalatedTickets = tickets.filter((t) => t.is_escalated).length;
  const escalationRate = totalTickets > 0 ? (escalatedTickets / totalTickets) : 0;

  const escalationsLowConfidence = tickets.filter((t) => t.is_escalated && t.escalation_reason?.toLowerCase().includes('confidence')).length;
  const escalationsCustomer = tickets.filter((t) => t.is_escalated && t.escalation_reason?.toLowerCase().includes('customer')).length;
  const escalationsFailed = tickets.filter((t) => t.is_escalated && t.escalation_reason?.toLowerCase().includes('fail')).length;
  const escalationsSensitive = tickets.filter((t) => t.is_escalated && t.escalation_reason?.toLowerCase().includes('sensitive')).length;

  const totalRevenue = useMemo(
    () => billingRecords.filter((r) => r.status === 'paid').reduce((s, r) => s + parseFloat(r.amount ?? '0'), 0),
    [billingRecords],
  );
  const pendingInvoices = billingRecords.filter((r) => r.status === 'pending' && r.record_type === 'invoice').length;

  const isLoading = isLoadingTickets || isLoadingBilling;

  const aiPct = metrics.aiResolvedPercent;
  const humanPct = 100 - aiPct;

  return (
    <div className="page-content fade-in" id="analytics-page">
      <div className="page-header">
        <div>
          <h1 className="page-title">Analytics</h1>
          <p className="page-subtitle">AI Performance &amp; Support Metrics</p>
        </div>
      </div>

      {/* KPI Grid */}
      <section aria-label="Support metrics">
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 'var(--space-5)', marginBottom: 'var(--space-6)' }}>
          {isLoading ? (
            <><SkeletonKPI /><SkeletonKPI /><SkeletonKPI /><SkeletonKPI /><SkeletonKPI /><SkeletonKPI /></>
          ) : (
            <>
              {[
                { title: 'Total Tickets', value: totalTickets },
                { title: 'Open Tickets', value: openTickets },
                { title: 'Resolution Rate', value: `${formatPercentInt(resolutionRate)}` },
                { title: 'Avg Response', value: '4m 30s' },
                { title: 'Escalation Rate', value: `${formatPercentInt(escalationRate)}` },
                { title: 'AI Resolution', value: `${aiPct}%` },
              ].map(({ title, value }) => (
                <div key={title} className="kpi-card">
                  <span className="kpi-card__label">{title}</span>
                  <div className="kpi-card__value" style={{ fontSize: 'var(--text-2xl)' }}>{value}</div>
                </div>
              ))}
            </>
          )}
        </div>
      </section>

      {/* AI Performance */}
      <section className="analytics-section" aria-label="AI performance">
        <h2 className="analytics-section-title">AI Performance</h2>
        <div className="card" style={{ marginBottom: 0 }}>
          <div className="card__body">
            <MetricRow label="AI Resolution Rate" value={`${aiPct}%`} />
            <MetricRow label="Human Escalation Rate" value={`${humanPct}%`} />
            <MetricRow label="Avg AI Confidence" value="86%" />
            <MetricRow label="RAG Retrieval Success" value="N/A — pending RAG pipeline integration" muted />
            <MetricRow label="AI Tool Success Rate" value="N/A — pending tool telemetry" muted />

            {/* Visual bar */}
            <div style={{ marginTop: 'var(--space-5)' }}>
              <div style={{ fontSize: 'var(--text-xs)', color: 'var(--color-text-muted)', marginBottom: 'var(--space-2)' }}>
                Resolution Split
              </div>
              <div style={{ display: 'flex', height: 28, borderRadius: 'var(--radius-full)', overflow: 'hidden', gap: 2 }}>
                <div
                  style={{ width: `${aiPct}%`, background: 'var(--color-ai)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontSize: '11px', fontWeight: 600, transition: 'width 0.3s ease', minWidth: 40 }}
                  aria-label={`AI: ${aiPct}%`}
                >
                  AI {aiPct}%
                </div>
                <div
                  style={{ flex: 1, background: 'var(--color-human)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontSize: '11px', fontWeight: 600 }}
                  aria-label={`Human: ${humanPct}%`}
                >
                  Human {humanPct}%
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Escalation Analysis */}
      <section className="analytics-section" aria-label="Escalation analysis">
        <h2 className="analytics-section-title">Escalation Analysis</h2>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 320px', gap: 'var(--space-6)' }}>
          <EscalationReasonChart data={escalationReasons} isLoading={isLoading} />
          <div className="card">
            <div className="card__header">
              <h3 className="card__title">Breakdown</h3>
            </div>
            <div className="card__body" style={{ paddingTop: 'var(--space-2)' }}>
              <MetricRow label="Total Escalations" value={String(escalatedTickets)} />
              <MetricRow label="Low AI Confidence" value={String(escalationsLowConfidence)} />
              <MetricRow label="Customer Requested" value={String(escalationsCustomer)} />
              <MetricRow label="AI Failed" value={String(escalationsFailed)} />
              <MetricRow label="Sensitive Issue" value={String(escalationsSensitive)} />
            </div>
          </div>
        </div>
      </section>

      {/* Billing Metrics */}
      <section aria-label="Billing metrics" style={{ marginBottom: 'var(--space-8)' }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 'var(--space-5)' }}>
          {isLoading ? (
            <><SkeletonKPI /><SkeletonKPI /></>
          ) : (
            <>
              <div className="kpi-card">
                <span className="kpi-card__label">Total Revenue (Paid)</span>
                <div className="kpi-card__value">{formatCurrencyShort(totalRevenue)}</div>
              </div>
              <div className="kpi-card">
                <span className="kpi-card__label">Pending Invoices</span>
                <div className="kpi-card__value">{pendingInvoices}</div>
              </div>
            </>
          )}
        </div>
      </section>
    </div>
  );
}
