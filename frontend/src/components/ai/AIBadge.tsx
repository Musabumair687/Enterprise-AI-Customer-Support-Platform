import { Sparkles } from 'lucide-react';

interface AIBadgeProps {
  label?: string;
  size?: 'sm' | 'md';
}

/**
 * ✦ AI Generated indicator — shown on all AI-authored messages and content.
 * Uses violet (--color-ai) as the AI visual identity color.
 */
export default function AIBadge({ label = 'AI Generated', size = 'sm' }: AIBadgeProps) {
  return (
    <span
      className="ai-badge"
      style={{ fontSize: size === 'sm' ? '11px' : 'var(--text-xs)' }}
      aria-label={label}
    >
      <Sparkles size={10} aria-hidden="true" />
      {label}
    </span>
  );
}
