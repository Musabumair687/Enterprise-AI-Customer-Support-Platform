import { Sparkles } from 'lucide-react';
import type { AIResponse } from '@/types';
import { formatSnakeCase } from '@/utils/formatters';

interface AIActivityPanelProps {
  response: AIResponse;
}

/**
 * Safe AI execution metadata panel — shows what the AI did WITHOUT exposing
 * internal chain-of-thought or private reasoning.
 *
 * Displays: intent, agent used, tools called, confidence.
 * All fields are optional — renders only available data.
 *
 * TODO: Populate confidence, intent, agent, tools_used from LangGraph when
 *       these fields are added to the POST /api/v1/chat response.
 */
export default function AIActivityPanel({ response }: AIActivityPanelProps) {
  const { intent, confidence, agent, tools_used, agents_used } = response;

  // Determine what to show
  const agentDisplay = agent ?? (agents_used.length > 0 ? agents_used[0] : null);
  const toolsDisplay = tools_used ?? [];
  const hasAnyMetadata = intent || confidence != null || agentDisplay || toolsDisplay.length > 0;

  if (!hasAnyMetadata) return null;

  return (
    <div className="ai-activity-panel" aria-label="AI execution details">
      <div className="ai-activity-panel__header">
        <Sparkles size={11} aria-hidden="true" />
        AI Activity
      </div>

      {intent && (
        <div className="ai-activity-row">
          <span className="ai-activity-row__key">Intent</span>
          <span className="ai-activity-row__value">{formatSnakeCase(intent)}</span>
        </div>
      )}

      {agentDisplay && (
        <div className="ai-activity-row">
          <span className="ai-activity-row__key">Agent</span>
          <span className="ai-activity-row__value">{formatSnakeCase(agentDisplay)}</span>
        </div>
      )}

      {agents_used.length > 1 && (
        <div className="ai-activity-row">
          <span className="ai-activity-row__key">Pipeline</span>
          <span className="ai-activity-row__value" style={{ fontSize: '11px' }}>
            {agents_used.map(formatSnakeCase).join(' → ')}
          </span>
        </div>
      )}

      {toolsDisplay.length > 0 && (
        <div className="ai-activity-row">
          <span className="ai-activity-row__key">Tools</span>
          <span className="ai-activity-row__value" style={{ fontSize: '11px' }}>
            {toolsDisplay.map(formatSnakeCase).join(', ')}
          </span>
        </div>
      )}

      {confidence != null && (
        <div className="ai-activity-row">
          <span className="ai-activity-row__key">Confidence</span>
          <span
            className="ai-activity-row__value"
            style={{
              color:
                confidence >= 0.75
                  ? 'var(--color-success)'
                  : confidence >= 0.5
                  ? 'var(--color-warning)'
                  : 'var(--color-danger)',
            }}
          >
            {Math.round(confidence * 100)}%
          </span>
        </div>
      )}
    </div>
  );
}
