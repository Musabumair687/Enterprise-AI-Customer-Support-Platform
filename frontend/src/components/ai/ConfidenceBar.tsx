interface ConfidenceBarProps {
  confidence: number;  // 0–1
  label?: string;
  showValue?: boolean;
}

function getConfidenceColor(confidence: number): string {
  if (confidence >= 0.75) return 'var(--color-success)';
  if (confidence >= 0.5)  return 'var(--color-warning)';
  return 'var(--color-danger)';
}

/**
 * Visual confidence bar for AI responses.
 * Color: green (≥75%), amber (50–74%), red (<50%).
 */
export default function ConfidenceBar({
  confidence,
  label = 'Confidence',
  showValue = true,
}: ConfidenceBarProps) {
  const pct = Math.round(confidence * 100);
  const color = getConfidenceColor(confidence);

  return (
    <div className="confidence-bar" role="meter" aria-valuenow={pct} aria-valuemin={0} aria-valuemax={100}>
      <div className="confidence-bar__header">
        <span className="confidence-bar__label">{label}</span>
        {showValue && (
          <span className="confidence-bar__value" style={{ color }}>
            {pct}%
          </span>
        )}
      </div>
      <div className="confidence-bar__track">
        <div
          className="confidence-bar__fill"
          style={{ width: `${pct}%`, background: color }}
        />
      </div>
    </div>
  );
}
