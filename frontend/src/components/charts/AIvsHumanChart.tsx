import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip } from 'recharts';
import { Skeleton } from '@/components/ui/Skeleton';

interface DataItem {
  name: string;
  value: number;
  color: string;
}

interface Props {
  data: DataItem[];
  isLoading: boolean;
}

export default function AIvsHumanChart({ data, isLoading }: Props) {
  const total = data.reduce((s, d) => s + d.value, 0);
  const aiItem = data.find((d) => d.name.toLowerCase().includes('ai'));
  const aiPercent = total > 0 && aiItem ? Math.round((aiItem.value / total) * 100) : 0;

  return (
    <div className="card">
      <div className="card__header">
        <div>
          <h3 className="card__title">AI vs Human Resolution</h3>
          <p className="card__subtitle">Resolved tickets</p>
        </div>
      </div>
      <div className="card__body" style={{ paddingTop: 'var(--space-4)' }}>
        {isLoading ? (
          <Skeleton height={200} />
        ) : total === 0 ? (
          <div style={{ textAlign: 'center', padding: 'var(--space-8)', color: 'var(--color-text-muted)', fontSize: 'var(--text-sm)' }}>
            No resolved tickets yet
          </div>
        ) : (
          <>
            <div style={{ position: 'relative', height: 180 }}>
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={data}
                    cx="50%"
                    cy="50%"
                    innerRadius={55}
                    outerRadius={78}
                    dataKey="value"
                    paddingAngle={3}
                    startAngle={90}
                    endAngle={-270}
                  >
                    {data.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} strokeWidth={0} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      background: 'var(--color-surface)',
                      border: '1px solid var(--color-border)',
                      borderRadius: 8,
                      fontSize: 12,
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
              {/* Center label */}
              <div style={{
                position: 'absolute', top: '50%', left: '50%',
                transform: 'translate(-50%, -50%)',
                textAlign: 'center', pointerEvents: 'none',
              }}>
                <div style={{ fontSize: 'var(--text-2xl)', fontWeight: 'var(--fw-bold)', color: 'var(--color-ai)' }}>
                  {aiPercent}%
                </div>
                <div style={{ fontSize: 'var(--text-xs)', color: 'var(--color-text-muted)' }}>AI</div>
              </div>
            </div>
            {/* Legend */}
            <div style={{ display: 'flex', justifyContent: 'center', gap: 'var(--space-5)', marginTop: 'var(--space-3)' }}>
              {data.map((entry) => (
                <div key={entry.name} style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                  <div style={{ width: 8, height: 8, borderRadius: '50%', background: entry.color }} />
                  <span style={{ fontSize: 'var(--text-xs)', color: 'var(--color-text-muted)', fontWeight: 500 }}>
                    {entry.name} <span style={{ color: 'var(--color-text-primary)' }}>({entry.value})</span>
                  </span>
                </div>
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
}
