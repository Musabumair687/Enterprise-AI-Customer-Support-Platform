import React, { useMemo } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useTicket } from '@/hooks/useTickets';
import { useConversations } from '@/hooks/useConversations';
import { TicketStatusBadge, TicketPriorityBadge } from '@/components/ui/Badge';
import { formatDateTime, formatDate } from '@/utils/formatters';
import { EmptyState } from '@/components/ui/EmptyState';
import { EscalationPanel } from '@/components/ai/EscalationPanel';

export const TicketDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const ticketId = Number(id);

  const { ticket, isLoading: ticketLoading, error: ticketError } = useTicket(ticketId);
  const { conversations, isLoading: convLoading } = useConversations({ limit: 500 });

  // TODO: backend doesn't support filtering by ticket_id yet, filter client-side
  const ticketConversations = useMemo(() => {
    return conversations.filter((c) => c.ticket_id === ticketId);
  }, [conversations, ticketId]);

  if (ticketLoading || convLoading) return <div className="page-container">Loading...</div>;
  if (ticketError) return <div className="page-container"><EmptyState title="Error" description={ticketError.message} /></div>;
  if (!ticket) return <div className="page-container"><EmptyState title="Not Found" description="Ticket not found" /></div>;

  return (
    <div className="page-container">
      <div className="ticket-detail-layout" style={{ display: 'grid', gridTemplateColumns: '1fr 300px', gap: '2rem' }}>
        
        {/* Left Column: Conversations */}
        <div className="ticket-main">
          <div className="messages-list" style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginBottom: '1rem' }}>
            {ticketConversations.map((msg) => (
              <div
                key={msg.id}
                className={`message message--${msg.sender_role}`}
                style={{
                  padding: '1rem',
                  borderRadius: '8px',
                  backgroundColor: msg.sender_role === 'customer' ? 'var(--bg-secondary)' : msg.sender_role === 'ai' ? 'var(--ai-bg)' : 'var(--primary-light)',
                  alignSelf: msg.sender_role === 'customer' ? 'flex-start' : 'flex-end',
                  maxWidth: '80%'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                  <span style={{ fontWeight: 'bold', textTransform: 'capitalize' }}>{msg.sender_role}</span>
                  <span>{formatDateTime(msg.created_at)}</span>
                </div>
                <div>{msg.content}</div>
              </div>
            ))}
            {ticketConversations.length === 0 && (
              <EmptyState title="No messages" description="No conversation history for this ticket yet." />
            )}
          </div>
          
          <div className="agent-reply-box" style={{ marginTop: 'auto', paddingTop: '1rem', borderTop: '1px solid var(--border-color)' }}>
            <textarea className="input-field" rows={3} placeholder="Add a reply or note..." style={{ width: '100%', marginBottom: '0.5rem' }} />
            <button className="btn btn--primary">Send</button>
          </div>
        </div>

        {/* Right Column: Sidebar */}
        <div className="ticket-sidebar" style={{ backgroundColor: 'var(--surface-color)', padding: '1.5rem', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
          <button className="btn btn--secondary" onClick={() => navigate('/tickets')} style={{ marginBottom: '1rem' }}>
            ← Back to Tickets
          </button>
          
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
            <h2 style={{ margin: 0 }}>Ticket #{ticket.id}</h2>
            <TicketStatusBadge status={ticket.status} isEscalated={ticket.is_escalated} />
          </div>
          <h1 style={{ fontSize: '1.25rem', marginBottom: '1.5rem' }}>{ticket.title}</h1>
          
          <hr style={{ borderTop: '1px solid var(--border-color)', marginBottom: '1rem' }} />
          <h3 style={{ marginBottom: '1rem', fontSize: '1rem' }}>Ticket Details</h3>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', marginBottom: '1.5rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span className="text-muted">Priority</span>
              <TicketPriorityBadge priority={ticket.priority} />
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span className="text-muted">Department</span>
              <span>{ticket.department || '—'}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span className="text-muted">Category</span>
              <span>{ticket.category || '—'}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span className="text-muted">Assignee</span>
              <span>{ticket.assigned_agent_name || 'Unassigned'}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span className="text-muted">Created</span>
              <span>{formatDate(ticket.created_at)}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span className="text-muted">Resolved</span>
              <span>{ticket.resolved_at ? formatDate(ticket.resolved_at) : '—'}</span>
            </div>
            {/* TODO: AI Confidence field doesn't exist yet on Ticket */}
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span className="text-muted">AI Confidence</span>
              <span>N/A</span>
            </div>
          </div>

          {ticket.is_escalated && (
            <div style={{ marginBottom: '1.5rem' }}>
              <h3 style={{ marginBottom: '0.5rem', fontSize: '1rem', color: 'var(--danger-color)' }}>Escalated</h3>
              <div style={{ marginBottom: '1rem', color: 'var(--text-muted)' }}>Reason: {ticket.escalation_reason || '—'}</div>
              <EscalationPanel escalation={{ ticket_id: ticket.id, reason: ticket.escalation_reason, assigned_employee: null }} showActions={false} />
            </div>
          )}

          {ticket.resolution && (
            <div>
              <h3 style={{ marginBottom: '0.5rem', fontSize: '1rem' }}>AI Summary</h3>
              <textarea
                className="input-field"
                rows={5}
                readOnly
                value={ticket.resolution}
                style={{ width: '100%', backgroundColor: 'var(--bg-secondary)' }}
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
