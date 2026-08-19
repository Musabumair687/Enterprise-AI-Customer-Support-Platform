import {
  ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip,
} from 'recharts';
import type { TicketVolumeDataPoint } from '@/types';
import { Skeleton } from '@/components/ui/Skeleton';

interface Props {
  data: TicketVolumeDataPoint[];
  isLoading: boolean;
}

export default function TicketVolumeChart({ data, isLoading }: Props) {
  return (
    <div className="card">
      <div className="card__header">
        <div>
          <h3 className="card__title">Ticket Volume</h3>
          <p className="card__subtitle">This week</p>
        </div>
      </div>
      <div className="card__body" style={{ paddingTop: 'var(--space-4)' }}>
        {isLoading ? (
          <Skeleton height={200} />
        ) : (
          <ResponsiveContainer width="100%" height={200}>
            <AreaChart data={data} margin={{ top: 4, right: 4, left: -20, bottom: 0 }}>
              <XAxis
                dataKey="day"
                tick={{ fontSize: 11, fill: 'var(--color-text-muted)' }}
                axisLine={false}
                tickLine={false}
              />
              <YAxis
                tick={{ fontSize: 11, fill: 'var(--color-text-muted)' }}
                axisLine={false}
                tickLine={false}
              />
              <Tooltip
                contentStyle={{
                  background: 'var(--color-surface)',
                  border: '1px solid var(--color-border)',
                  borderRadius: 8,
                  fontSize: 12,
                  boxShadow: 'var(--shadow-md)',
                }}
                labelStyle={{ fontWeight: 600, color: 'var(--color-text-primary)' }}
              />
              <Area
                type="monotone"
                dataKey="tickets"
                name="Total"
                stroke="#111827"
                strokeWidth={2}
                fill="rgba(17,24,39,0.06)"
                dot={false}
              />
              <Area
                type="monotone"
                dataKey="resolved"
                name="Resolved"
                stroke="#12B76A"
                strokeWidth={2}
                fill="rgba(18,183,106,0.06)"
                dot={false}
              />
            </AreaChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
}
