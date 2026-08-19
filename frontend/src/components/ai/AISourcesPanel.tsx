import { useState } from 'react';
import { BookOpen, ChevronDown, ChevronUp } from 'lucide-react';
import type { RAGSource } from '@/types';

interface AISourcesPanelProps {
  sources: RAGSource[];
  /** Set to false when backend RAG pipeline doesn't yet return sources */
  available?: boolean;
}

/**
 * Displays RAG retrieval sources for an AI response.
 * Ready for the hybrid RAG pipeline (BM25 + vector + RRF + cross-encoder).
 * Each source shows: title, section, relevance score.
 *
 * If available=false, shows a placeholder indicating sources will appear
 * once the RAG pipeline is connected.
 */
export default function AISourcesPanel({ sources, available = true }: AISourcesPanelProps) {
  const [expanded, setExpanded] = useState(false);

  if (!available || sources.length === 0) {
    return (
      <div className="ai-sources-panel" style={{ opacity: 0.7 }}>
        <div className="ai-sources-panel__header">
          <BookOpen size={12} style={{ color: 'var(--color-ai-text)' }} />
          <span className="ai-sources-panel__title">Knowledge Sources</span>
        </div>
        <p style={{ fontSize: '11px', color: 'var(--color-text-muted)' }}>
          {!available
            ? 'Sources will be shown when RAG pipeline returns retrieval metadata.'
            : 'No sources retrieved for this response.'}
        </p>
      </div>
    );
  }

  const displayed = expanded ? sources : sources.slice(0, 3);

  return (
    <div className="ai-sources-panel">
      <div className="ai-sources-panel__header">
        <BookOpen size={12} style={{ color: 'var(--color-ai-text)' }} aria-hidden="true" />
        <span className="ai-sources-panel__title">Knowledge Sources</span>
        <span
          style={{
            marginLeft: 'auto',
            fontSize: '11px',
            color: 'var(--color-ai-text)',
            fontWeight: 500,
          }}
        >
          {sources.length} {sources.length === 1 ? 'source' : 'sources'}
        </span>
      </div>

      <div className="ai-sources-panel__list" role="list">
        {displayed.map((source, i) => (
          <div
            key={i}
            className="ai-source-item"
            role="listitem"
            aria-label={`Source ${i + 1}: ${source.title}`}
          >
            <span className="ai-source-item__number">{i + 1}</span>
            <div className="ai-source-item__info">
              <div className="ai-source-item__title" title={source.title}>
                {source.title}
              </div>
              {source.section && (
                <div className="ai-source-item__section">§ {source.section}</div>
              )}
            </div>
            {source.relevance != null && (
              <span className="ai-source-item__relevance" aria-label={`Relevance ${Math.round(source.relevance * 100)}%`}>
                {source.relevance.toFixed(2)}
              </span>
            )}
          </div>
        ))}
      </div>

      {sources.length > 3 && (
        <button
          onClick={() => setExpanded((e) => !e)}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 4,
            fontSize: '11px',
            color: 'var(--color-ai-text)',
            fontWeight: 500,
            marginTop: 'var(--space-2)',
            padding: 0,
            background: 'none',
            border: 'none',
            cursor: 'pointer',
          }}
          aria-expanded={expanded}
        >
          {expanded ? <ChevronUp size={12} /> : <ChevronDown size={12} />}
          {expanded ? 'Show fewer' : `Show ${sources.length - 3} more`}
        </button>
      )}
    </div>
  );
}
