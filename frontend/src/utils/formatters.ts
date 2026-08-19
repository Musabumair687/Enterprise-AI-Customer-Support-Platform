/**
 * Data formatting utilities — date, currency, duration, percentage, names.
 */

// ─── Date / Time ─────────────────────────────────────────────────────────────

export function formatDate(value: string | null | undefined): string {
  if (!value) return '—';
  try {
    return new Intl.DateTimeFormat('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    }).format(new Date(value));
  } catch {
    return value;
  }
}

export function formatDateTime(value: string | null | undefined): string {
  if (!value) return '—';
  try {
    return new Intl.DateTimeFormat('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    }).format(new Date(value));
  } catch {
    return value;
  }
}

export function formatRelativeTime(value: string | null | undefined): string {
  if (!value) return '—';
  try {
    const date = new Date(value);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffSec = Math.floor(diffMs / 1000);
    const diffMin = Math.floor(diffSec / 60);
    const diffHr = Math.floor(diffMin / 60);
    const diffDay = Math.floor(diffHr / 24);

    if (diffSec < 60) return 'just now';
    if (diffMin < 60) return `${diffMin}m ago`;
    if (diffHr < 24) return `${diffHr}h ago`;
    if (diffDay < 7) return `${diffDay}d ago`;
    return formatDate(value);
  } catch {
    return value;
  }
}

// ─── Currency ─────────────────────────────────────────────────────────────────

export function formatCurrency(
  value: string | number | null | undefined,
  currency = 'USD',
): string {
  if (value == null || value === '') return '—';
  const num = typeof value === 'string' ? parseFloat(value) : value;
  if (isNaN(num)) return '—';
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
    maximumFractionDigits: 0,
  }).format(num);
}

export function formatCurrencyShort(value: string | number | null | undefined): string {
  if (value == null || value === '') return '—';
  const num = typeof value === 'string' ? parseFloat(value) : value;
  if (isNaN(num)) return '—';
  if (num >= 1_000_000) return `$${(num / 1_000_000).toFixed(1)}M`;
  if (num >= 1_000) return `$${(num / 1_000).toFixed(1)}K`;
  return `$${num.toFixed(0)}`;
}

// ─── Percentage ───────────────────────────────────────────────────────────────

export function formatPercent(value: number | null | undefined, decimals = 1): string {
  if (value == null) return '—';
  return `${(value * 100).toFixed(decimals)}%`;
}

export function formatPercentInt(value: number | null | undefined): string {
  if (value == null) return '—';
  return `${Math.round(value)}%`;
}

// ─── Duration ─────────────────────────────────────────────────────────────────

export function formatMinutes(minutes: number): string {
  if (minutes < 60) return `${Math.round(minutes)}m`;
  const h = Math.floor(minutes / 60);
  const m = Math.round(minutes % 60);
  return m > 0 ? `${h}h ${m}m` : `${h}h`;
}

export function formatSeconds(seconds: number): string {
  if (seconds < 60) return `${Math.round(seconds)}s`;
  const m = Math.floor(seconds / 60);
  const s = Math.round(seconds % 60);
  return s > 0 ? `${m}m ${s}s` : `${m}m`;
}

// ─── Numbers ──────────────────────────────────────────────────────────────────

export function formatNumber(value: number | null | undefined): string {
  if (value == null) return '—';
  return new Intl.NumberFormat('en-US').format(value);
}

// ─── Strings ──────────────────────────────────────────────────────────────────

export function capitalize(s: string): string {
  if (!s) return s;
  return s.charAt(0).toUpperCase() + s.slice(1);
}

export function formatSnakeCase(s: string): string {
  return s.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
}

export function truncate(s: string, maxLength: number): string {
  if (s.length <= maxLength) return s;
  return s.slice(0, maxLength - 3) + '…';
}

export function initials(name: string): string {
  return name
    .split(' ')
    .map((n) => n[0])
    .slice(0, 2)
    .join('')
    .toUpperCase();
}

// ─── Trend ───────────────────────────────────────────────────────────────────

export function formatTrend(value: number): string {
  const abs = Math.abs(value).toFixed(1);
  return value >= 0 ? `↑ ${abs}%` : `↓ ${abs}%`;
}
