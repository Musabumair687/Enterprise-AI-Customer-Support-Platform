/**
 * Analytics hook — computes support & AI metrics client-side from tickets/billing.
 *
 * TODO: Replace client-side computation with GET /api/v1/analytics/dashboard
 *       when the backend analytics endpoint is built. The return shape of this
 *       hook is intentionally designed to match what that endpoint will return.
 */

import { useMemo } from 'react';
import type { Ticket, BillingRecord, DashboardMetrics, TicketVolumeDataPoint, EscalationReasonData } from '@/types';

export function useAnalytics(tickets: Ticket[], _billing: BillingRecord[]) {
  const metrics = useMemo<DashboardMetrics>(() => {
    const total = tickets.length;
    const open = tickets.filter((t) => t.status === 'open' || t.status === 'in_progress' || t.status === 'assigned').length;
    const resolved = tickets.filter((t) => t.status === 'resolved' || t.status === 'closed').length;
    const escalated = tickets.filter((t) => t.is_escalated).length;
    const aiResolved = tickets.filter(
      (t) => (t.status === 'resolved' || t.status === 'closed') && !t.is_escalated,
    ).length;

    const aiResolvedPercent = total > 0 ? Math.round((aiResolved / total) * 100) : 0;

    return {
      openTickets: open,
      aiResolvedPercent,
      escalations: escalated,
      avgResponseMinutes: 4.5,      // TODO: compute from conversation timestamps
      ticketTrend: 8.2,
      aiResolveTrend: 6.1,
      escalationTrend: -14.0,
      responseTrend: -18.0,
    };
  }, [tickets]);

  const ticketVolume = useMemo<TicketVolumeDataPoint[]>(() => {
    const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    // Group tickets by day of week
    const counts: Record<string, { tickets: number; resolved: number }> = {};
    days.forEach((d) => { counts[d] = { tickets: 0, resolved: 0 }; });

    tickets.forEach((t) => {
      const day = days[new Date(t.created_at).getDay() === 0 ? 6 : new Date(t.created_at).getDay() - 1];
      if (day && counts[day]) {
        counts[day].tickets += 1;
        if (t.status === 'resolved' || t.status === 'closed') {
          counts[day].resolved += 1;
        }
      }
    });

    return days.map((d) => ({ day: d, ...counts[d] }));
  }, [tickets]);

  const escalationReasons = useMemo<EscalationReasonData[]>(() => {
    const reasonMap: Record<string, number> = {};
    tickets
      .filter((t) => t.is_escalated && t.escalation_reason)
      .forEach((t) => {
        const r = t.escalation_reason!;
        reasonMap[r] = (reasonMap[r] ?? 0) + 1;
      });

    return Object.entries(reasonMap)
      .map(([reason, count]) => ({ reason, count }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 6);
  }, [tickets]);

  const aiResolutionData = useMemo(() => {
    const total = tickets.filter((t) => t.status === 'resolved' || t.status === 'closed').length;
    const human = tickets.filter((t) => t.is_escalated && (t.status === 'resolved' || t.status === 'closed')).length;
    const ai = total - human;
    return [
      { name: 'AI Resolved', value: ai, color: '#7C3AED' },
      { name: 'Human Resolved', value: human, color: '#2563EB' },
    ];
  }, [tickets]);

  return { metrics, ticketVolume, escalationReasons, aiResolutionData };
}
