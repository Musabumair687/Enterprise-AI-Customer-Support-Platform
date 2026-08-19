import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Cell } from 'recharts';
import type { EscalationReasonData } from '@/types';
import { Skeleton } from '@/components/ui/Skeleton';

interface Props {
  data: EscalationReasonData[];
  isLoading: boolean;
}

export default function EscalationReasonChart({ data, isLoading }: Props) {
  return (
    <div className="card">
      <div className="card__header">
        <div>
          <h3 className="card__title">Escalation Reasons</h3>
          <p className="card__subtitle">Breakdown by category</p>
        </div>
      </div>
      <div className="card__body" style={{ paddingTop: 'var(--space-2)' }}>
        {isLoading ? (
          <Skeleton height={200} />
        ) : data.length === 0 ? (
          <div style={{ textAlign: 'center', padding: 'var(--space-8)', color: 'var(--color-text-muted)', fontSize: 'var(--text-sm)' }}>
            No escalation data
          </div>
        ) : (
          <ResponsiveContainer width="100%" height={Math.max(140, data.length * 36)}>
            <BarChart
              data={data}
              layout="vertical"
              margin={{ top: 0, right: 16, left: 0, bottom: 0 }}
            >
              <XAxis type="number" hide />
              <YAxis
                dataKey="reason"
                type="category"
                tick={{ fontSize: 11, fill: 'var(--color-text-muted)' }}
                width={140}
                axisLine={false}
                tickLine={false}
                tickFormatter={(val: string) => val.length > 22 ? val.slice(0, 22) + '…' : val}
              />
              <Tooltip
                contentStyle={{
                  background: 'var(--color-surface)',
                  border: '1px solid var(--color-border)',
                  borderRadius: 8,
                  fontSize: 12,
                }}
              />
              <Bar dataKey="count" name="Escalations" radius={[0, 4, 4, 0]} maxBarSize={16}>
                {data.map((_, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={index === 0 ? 'var(--color-danger)' : `rgba(240, 68, 56, ${0.7 - index * 0.1})`}
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
}
