import { AlertCircle, WifiOff, RefreshCw } from 'lucide-react';
import type { AppError } from '@/utils/errors';

interface EmptyStateProps {
  icon?: React.ReactNode;
  title: string;
  description?: string;
  action?: React.ReactNode;
}

export function EmptyState({ icon, title, description, action }: EmptyStateProps) {
  return (
    <div className="empty-state" role="status">
      {icon && <div className="empty-state__icon">{icon}</div>}
      <div className="empty-state__title">{title}</div>
      {description && <p className="empty-state__desc">{description}</p>}
      {action && <div style={{ marginTop: 'var(--space-4)' }}>{action}</div>}
    </div>
  );
}

interface ErrorStateProps {
  error: AppError;
  onRetry?: () => void;
}

export function ErrorState({ error, onRetry }: ErrorStateProps) {
  const isNetwork = error.code === 'NETWORK_ERROR' || error.code === 'TIMEOUT';
  const Icon = isNetwork ? WifiOff : AlertCircle;

  return (
    <div className="empty-state" role="alert" aria-live="polite">
      <div className="empty-state__icon" style={{ background: 'var(--color-danger-bg)' }}>
        <Icon size={24} style={{ color: 'var(--color-danger)' }} />
      </div>
      <div className="empty-state__title">
        {isNetwork ? 'Unable to connect' : 'Something went wrong'}
      </div>
      <p className="empty-state__desc">{error.message}</p>
      {onRetry && (
        <button className="btn btn--secondary" onClick={onRetry} style={{ marginTop: 'var(--space-4)' }}>
          <RefreshCw size={14} />
          Try again
        </button>
      )}
    </div>
  );
}
