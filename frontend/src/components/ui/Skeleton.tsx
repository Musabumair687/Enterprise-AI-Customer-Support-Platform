interface SkeletonProps {
  width?: string | number;
  height?: string | number;
  borderRadius?: string;
  style?: React.CSSProperties;
}

export function Skeleton({ width = '100%', height = 16, borderRadius, style }: SkeletonProps) {
  return (
    <div
      className="skeleton"
      style={{ width, height, borderRadius, ...style }}
      aria-hidden="true"
    />
  );
}

export function SkeletonText({ lines = 3 }: { lines?: number }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
      {Array.from({ length: lines }).map((_, i) => (
        <Skeleton key={i} width={i === lines - 1 ? '60%' : '100%'} height={14} />
      ))}
    </div>
  );
}

export function SkeletonCard() {
  return (
    <div className="card" style={{ padding: 'var(--space-5) var(--space-6)' }}>
      <div style={{ display: 'flex', gap: 'var(--space-3)', marginBottom: 'var(--space-4)' }}>
        <Skeleton width={36} height={36} borderRadius="8px" />
        <div style={{ flex: 1 }}>
          <Skeleton width="50%" height={14} style={{ marginBottom: 8 }} />
          <Skeleton width="30%" height={12} />
        </div>
      </div>
      <Skeleton height={32} style={{ marginBottom: 8 }} />
      <Skeleton width="40%" height={12} />
    </div>
  );
}

export function SkeletonTable({ rows = 5, cols = 4 }: { rows?: number; cols?: number }) {
  return (
    <div className="table-container">
      <table className="table">
        <thead>
          <tr>
            {Array.from({ length: cols }).map((_, i) => (
              <th key={i}>
                <Skeleton width={60 + i * 10} height={12} />
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {Array.from({ length: rows }).map((_, r) => (
            <tr key={r} style={{ cursor: 'default' }}>
              {Array.from({ length: cols }).map((_, c) => (
                <td key={c}>
                  <Skeleton width={`${60 + ((r + c) * 7) % 40}%`} height={14} />
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export function SkeletonKPI() {
  return (
    <div className="kpi-card">
      <Skeleton width="50%" height={12} style={{ marginBottom: 12 }} />
      <Skeleton width="60%" height={32} style={{ marginBottom: 10 }} />
      <Skeleton width="40%" height={12} />
    </div>
  );
}
