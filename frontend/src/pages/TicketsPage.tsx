import React, { useState, useMemo } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { useTickets } from '@/hooks/useTickets';
import { SkeletonTable } from '@/components/ui/Skeleton';
import { EmptyState } from '@/components/ui/EmptyState';
import { TicketStatusBadge, TicketPriorityBadge } from '@/components/ui/Badge';
import { formatRelativeTime } from '@/utils/formatters';
import { Modal } from '@/components/ui/Modal';
import type { TicketCreate } from '@/types';

export default function TicketsPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();
  const { tickets, isLoading, error, createTicket } = useTickets({ limit: 500 });

  const searchQuery = searchParams.get('q') || '';
  const view = searchParams.get('view') || 'all';

  const [statusFilter, setStatusFilter] = useState<string>('');
  const [priorityFilter, setPriorityFilter] = useState<string>('');
  const [departmentFilter, setDepartmentFilter] = useState<string>('');
  const [isModalOpen, setIsModalOpen] = useState(false);

  const [newTicket, setNewTicket] = useState<Partial<TicketCreate>>({
    title: '',
    description: '',
    customer_id: undefined,
    priority: 'medium',
    department: '',
  });

  const filteredTickets = useMemo(() => {
    return tickets.filter((t) => {
      // View filter
      if (view === 'escalated') {
        if (!t.is_escalated || t.status === 'resolved' || t.status === 'closed') return false;
      } else if (view === 'mine') {
        // TODO: show all for now, add auth user ID filtering later
      }

      // Search query
      if (searchQuery) {
        const query = searchQuery.toLowerCase();
        const title = t.title?.toLowerCase() || '';
        const desc = t.description?.toLowerCase() || '';
        const ext = t.external_id?.toLowerCase() || '';
        if (!title.includes(query) && !desc.includes(query) && !ext.includes(query)) {
          return false;
        }
      }

      // Dropdown filters
      if (statusFilter && t.status !== statusFilter) return false;
      if (priorityFilter && t.priority !== priorityFilter) return false;
      if (departmentFilter && t.department !== departmentFilter) return false;

      return true;
    });
  }, [tickets, view, searchQuery, statusFilter, priorityFilter, departmentFilter]);

  const setView = (newView: string) => {
    setSearchParams((prev) => {
      prev.set('view', newView);
      return prev;
    });
  };

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchParams((prev) => {
      if (e.target.value) {
        prev.set('q', e.target.value);
      } else {
        prev.delete('q');
      }
      return prev;
    });
  };

  const handleCreateSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTicket.customer_id || !newTicket.title || !newTicket.description) return;
    await createTicket({
      customer_id: Number(newTicket.customer_id),
      title: newTicket.title,
      description: newTicket.description,
      priority: newTicket.priority as any,
      department: newTicket.department || null,
      status: 'open',
    });
    setIsModalOpen(false);
    setNewTicket({ title: '', description: '', customer_id: undefined, priority: 'medium', department: '' });
  };

  return (
    <div className="page-container">
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <h1 className="page-title">Tickets</h1>
        <button className="btn btn--primary" onClick={() => setIsModalOpen(true)}>
          Create Ticket
        </button>
      </div>

      <div className="segment-control" style={{ marginBottom: '1rem', display: 'flex', gap: '0.5rem' }}>
        <button className={`btn ${view === 'all' ? 'btn--primary' : 'btn--secondary'}`} onClick={() => setView('all')}>
          All
        </button>
        <button className={`btn ${view === 'escalated' ? 'btn--primary' : 'btn--secondary'}`} onClick={() => setView('escalated')}>
          Escalated
        </button>
        <button className={`btn ${view === 'mine' ? 'btn--primary' : 'btn--secondary'}`} onClick={() => setView('mine')}>
          My Tickets
        </button>
      </div>

      <div className="filter-bar" style={{ display: 'flex', gap: '1rem', marginBottom: '1rem' }}>
        <input
          type="text"
          placeholder="Search tickets..."
          className="input-field"
          value={searchQuery}
          onChange={handleSearch}
        />
        <select className="input-field" value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
          <option value="">All Statuses</option>
          <option value="open">Open</option>
          <option value="in_progress">In Progress</option>
          <option value="resolved">Resolved</option>
          <option value="closed">Closed</option>
        </select>
        <select className="input-field" value={priorityFilter} onChange={(e) => setPriorityFilter(e.target.value)}>
          <option value="">All Priorities</option>
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
          <option value="urgent">Urgent</option>
        </select>
        <select className="input-field" value={departmentFilter} onChange={(e) => setDepartmentFilter(e.target.value)}>
          <option value="">All Departments</option>
          <option value="Technical Support">Technical Support</option>
          <option value="Billing">Billing</option>
          <option value="Customer Success">Customer Success</option>
          <option value="General">General</option>
        </select>
      </div>

      <div className="ticket-count" style={{ marginBottom: '1rem', color: 'var(--text-muted)' }}>
        {filteredTickets.length} tickets
      </div>

      {error ? (
        <EmptyState title="Error Loading Tickets" description={error.message} />
      ) : isLoading ? (
        <SkeletonTable columns={7} rows={10} />
      ) : (
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Subject</th>
                <th>Customer ID</th>
                <th>Priority</th>
                <th>Status</th>
                <th>Department</th>
                <th>Assignee</th>
                <th>Created</th>
              </tr>
            </thead>
            <tbody>
              {filteredTickets.map((t) => (
                <tr
                  key={t.id}
                  onClick={() => navigate(`/tickets/${t.id}`)}
                  className={t.is_escalated ? 'table-row--escalated' : ''}
                  style={{ cursor: 'pointer' }}
                >
                  <td className="text-muted">#{t.id}</td>
                  <td style={{ fontWeight: 'bold' }}>{t.title.length > 50 ? t.title.slice(0, 50) + '...' : t.title}</td>
                  <td className="text-muted">{t.customer_id}</td>
                  <td>
                    <TicketPriorityBadge priority={t.priority} />
                  </td>
                  <td>
                    <TicketStatusBadge status={t.status} isEscalated={t.is_escalated} />
                  </td>
                  <td>{t.department || '—'}</td>
                  <td>{t.assigned_agent_name || 'Unassigned'}</td>
                  <td>{formatRelativeTime(t.created_at)}</td>
                </tr>
              ))}
              {filteredTickets.length === 0 && (
                <tr>
                  <td colSpan={8}>
                    <EmptyState title="No tickets found" description="Try adjusting your filters" />
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Create Ticket" id="create-ticket-modal">
        <form onSubmit={handleCreateSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div className="form-group">
            <label>Customer ID</label>
            <input
              type="number"
              className="input-field"
              required
              value={newTicket.customer_id || ''}
              onChange={(e) => setNewTicket({ ...newTicket, customer_id: Number(e.target.value) })}
            />
          </div>
          <div className="form-group">
            <label>Title</label>
            <input
              type="text"
              className="input-field"
              required
              value={newTicket.title}
              onChange={(e) => setNewTicket({ ...newTicket, title: e.target.value })}
            />
          </div>
          <div className="form-group">
            <label>Description</label>
            <textarea
              className="input-field"
              required
              rows={4}
              value={newTicket.description}
              onChange={(e) => setNewTicket({ ...newTicket, description: e.target.value })}
            />
          </div>
          <div className="form-group">
            <label>Priority</label>
            <select
              className="input-field"
              value={newTicket.priority}
              onChange={(e) => setNewTicket({ ...newTicket, priority: e.target.value })}
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="urgent">Urgent</option>
            </select>
          </div>
          <div className="form-group">
            <label>Department</label>
            <input
              type="text"
              className="input-field"
              value={newTicket.department || ''}
              onChange={(e) => setNewTicket({ ...newTicket, department: e.target.value })}
            />
          </div>
          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.5rem' }}>
            <button type="button" className="btn btn--secondary" onClick={() => setIsModalOpen(false)}>
              Cancel
            </button>
            <button type="submit" className="btn btn--primary">
              Create
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
