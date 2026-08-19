import { AlertTriangle, User } from 'lucide-react';
import type { ChatEscalation } from '@/types';
import ConfidenceBar from './ConfidenceBar';
import { formatSnakeCase } from '@/utils/formatters';

interface EscalationPanelProps {
  escalation: ChatEscalation;
  confidence?: number;
  reason?: string;
  /** Called when agent clicks "Escalate to Human" */
  onEscalate?: () => void;
  /** Called when agent clicks "Continue with AI" */
  onContinue?: () => void;
  /** If false (already escalated/ticket created), hide action buttons */
  showActions?: boolean;
}

/**
 * ⚠ Human Intervention Recommended panel.
 *
 * This is the star feature of Phase 13 — shown when the AI determines that
 * a human should take over the conversation.
 *
 * Displays: AI confidence, reason, recommended team, priority, assigned employee.
 * Action buttons: [Escalate to Human] [Continue with AI]
 */
export default function EscalationPanel({
  escalation,
  confidence,
  reason,
  onEscalate,
  onContinue,
  showActions = true,
}: EscalationPanelProps) {
  return (
    <div className="escalation-panel" role="alert" aria-live="polite">
      {/* Header */}
      <div className="escalation-panel__header">
        <AlertTriangle size={18} style={{ color: 'var(--color-danger)', flexShrink: 0 }} aria-hidden="true" />
        <span className="escalation-panel__title">⚠ Human Intervention Recommended</span>
      </div>

      {/* Confidence bar */}
      {confidence != null && (
        <div style={{ marginBottom: 'var(--space-4)' }}>
          <ConfidenceBar confidence={confidence} label="AI Confidence" />
        </div>
      )}

      {/* Metadata grid */}
      <div className="escalation-panel__grid">
        {reason && (
          <div className="escalation-panel__field" style={{ gridColumn: '1 / -1' }}>
            <span className="escalation-panel__field-label">Reason</span>
            <div className="escalation-panel__reason">{reason}</div>
          </div>
        )}

        {escalation.assigned_employee && (
          <>
            <div className="escalation-panel__field">
              <span className="escalation-panel__field-label">Recommended Team</span>
              <span className="escalation-panel__field-value">
                {escalation.assigned_employee.department}
              </span>
            </div>
            <div className="escalation-panel__field">
              <span className="escalation-panel__field-label">Assigned To</span>
              <span className="escalation-panel__field-value">
                <span className="flex items-center gap-2">
                  <User size={13} aria-hidden="true" />
                  {escalation.assigned_employee.name}
                </span>
              </span>
            </div>
          </>
        )}

        {escalation.ticket_id && (
          <div className="escalation-panel__field">
            <span className="escalation-panel__field-label">Ticket Created</span>
            <span className="escalation-panel__field-value">#{escalation.ticket_id}</span>
          </div>
        )}

        {escalation.reason && !reason && (
          <div className="escalation-panel__field" style={{ gridColumn: '1 / -1' }}>
            <span className="escalation-panel__field-label">Escalation Reason</span>
            <div className="escalation-panel__reason">
              {formatSnakeCase(escalation.reason)}
            </div>
          </div>
        )}
      </div>

      {/* Actions */}
      {showActions && (onEscalate || onContinue) && (
        <div className="escalation-panel__actions">
          {onEscalate && (
            <button
              id="escalate-to-human-btn"
              className="btn btn--danger"
              onClick={onEscalate}
            >
              <AlertTriangle size={14} />
              Escalate to Human
            </button>
          )}
          {onContinue && (
            <button
              id="continue-with-ai-btn"
              className="btn btn--secondary"
              onClick={onContinue}
            >
              Continue with AI
            </button>
          )}
        </div>
      )}

      {/* Already escalated state */}
      {!showActions && escalation.ticket_id && (
        <div className="alert alert--warning" style={{ marginTop: 'var(--space-2)' }}>
          <AlertTriangle size={14} aria-hidden="true" />
          Escalated — Ticket #{escalation.ticket_id} has been created and assigned.
        </div>
      )}
    </div>
  );
}
