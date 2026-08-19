import React, { useMemo, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useCustomer } from '@/hooks/useCustomers';
import { useTickets } from '@/hooks/useTickets';
import { useConversations } from '@/hooks/useConversations';
import { useBilling } from '@/hooks/useBilling';
import { EmptyState } from '@/components/ui/EmptyState';
import { PlanBadge, Badge, TicketStatusBadge, TicketPriorityBadge } from '@/components/ui/Badge';
import { formatDate, formatDateTime, formatCurrencyShort, formatCurrency, initials } from '@/utils/formatters';

export const CustomerDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const customerId = Number(id);

  const [activeTab, setActiveTab] = useState<'overview' | 'conversations' | 'tickets' | 'billing'>('overview');

  const { customer, isLoading: custLoading, error: custError } = useCustomer(customerId);
  const { tickets, isLoading: ticketsLoading } = useTickets({ limit: 500 });
  const { conversations, isLoading: convLoading } = useConversations({ limit: 500 });
  const { records: billingRecords, isLoading: billingLoading } = useBilling({ limit: 500 });

  const customerTickets = useMemo(() => tickets.filter(t => t.customer_id === customerId), [tickets, customerId]);
  const customerConversations = useMemo(() => conversations.filter(c => c.customer_id === customerId), [conversations, customerId]);
  const customerBilling = useMemo(() => billingRecords.filter(b => b.customer_id === customerId), [billingRecords, customerId]);

  // Group conversations by session_id
  const groupedConversations = useMemo(() => {
    const groups: Record<string, typeof conversations> = {};
    customerConversations.forEach(c => {
      if (!groups[c.session_id]) groups[c.session_id] = [];
      groups[c.session_id].push(c);
    });
    return Object.entries(groups).map(([sessionId, msgs]) => ({
      sessionId,
      messages: msgs.sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime()),
      lastMessage: msgs[msgs.length - 1]
    })).sort((a, b) => new Date(b.lastMessage.created_at).getTime() - new Date(a.lastMessage.created_at).getTime());
  }, [customerConversations]);

  if (custLoading) return <div className="page-container">Loading...</div>;
  if (custError) return <div className="page-container"><EmptyState title="Error" description={custError.message} /></div>;
  if (!customer) return <div className="page-container"><EmptyState title="Not Found" description="Customer not found" /></div>;

  return (
    <div className="page-container">
      <button className="btn btn--secondary" onClick={() => navigate('/customers')} style={{ marginBottom: '1.5rem' }}>
        ← Back to Customers
      </button>

      {/* Header */}
      <div className="customer-detail-header" style={{ display: 'flex', alignItems: 'center', gap: '1.5rem', marginBottom: '2rem', padding: '1.5rem', backgroundColor: 'var(--surface-color)', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
        <div style={{ width: '80px', height: '80px', borderRadius: '50%', backgroundColor: 'var(--primary-color)', color: 'white', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '2rem', fontWeight: 'bold' }}>
          {initials(customer.name)}
        </div>
        <div>
          <h1 style={{ margin: '0 0 0.5rem 0' }}>{customer.name}</h1>
          <div className="text-muted" style={{ marginBottom: '0.5rem' }}>{customer.email}</div>
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <PlanBadge plan={customer.subscription_plan} />
            <Badge className={customer.status === 'active' ? 'badge--success' : 'badge--secondary'}>{customer.status}</Badge>
          </div>
        </div>
      </div>

      {/* Stats row */}
      <div className="customer-detail-stats" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '1rem', marginBottom: '2rem' }}>
        <div className="stat-card" style={{ padding: '1rem', backgroundColor: 'var(--surface-color)', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
          <div className="text-muted" style={{ fontSize: '0.85rem', marginBottom: '0.5rem' }}>Plan</div>
          <div style={{ fontWeight: 'bold', fontSize: '1.1rem' }}>{customer.subscription_plan || '—'}</div>
        </div>
        <div className="stat-card" style={{ padding: '1rem', backgroundColor: 'var(--surface-color)', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
          <div className="text-muted" style={{ fontSize: '0.85rem', marginBottom: '0.5rem' }}>Status</div>
          <div style={{ fontWeight: 'bold', fontSize: '1.1rem', textTransform: 'capitalize' }}>{customer.status}</div>
        </div>
        <div className="stat-card" style={{ padding: '1rem', backgroundColor: 'var(--surface-color)', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
          <div className="text-muted" style={{ fontSize: '0.85rem', marginBottom: '0.5rem' }}>Member Since</div>
          <div style={{ fontWeight: 'bold', fontSize: '1.1rem' }}>{formatDate(customer.registration_date)}</div>
        </div>
        <div className="stat-card" style={{ padding: '1rem', backgroundColor: 'var(--surface-color)', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
          <div className="text-muted" style={{ fontSize: '0.85rem', marginBottom: '0.5rem' }}>LTV</div>
          <div style={{ fontWeight: 'bold', fontSize: '1.1rem' }}>{formatCurrencyShort(customer.lifetime_value)}</div>
        </div>
        <div className="stat-card" style={{ padding: '1rem', backgroundColor: 'var(--surface-color)', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
          <div className="text-muted" style={{ fontSize: '0.85rem', marginBottom: '0.5rem' }}>Monthly Revenue</div>
          <div style={{ fontWeight: 'bold', fontSize: '1.1rem' }}>{formatCurrencyShort(customer.monthly_revenue)}</div>
        </div>
        <div className="stat-card" style={{ padding: '1rem', backgroundColor: 'var(--surface-color)', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
          <div className="text-muted" style={{ fontSize: '0.85rem', marginBottom: '0.5rem' }}>Account Manager</div>
          <div style={{ fontWeight: 'bold', fontSize: '1.1rem' }}>{customer.account_manager || '—'}</div>
        </div>
      </div>

      {/* Tabs */}
      <div className="tabs-bar" style={{ display: 'flex', gap: '2rem', borderBottom: '1px solid var(--border-color)', marginBottom: '2rem' }}>
        {['overview', 'conversations', 'tickets', 'billing'].map(tab => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab as any)}
            style={{
              background: 'none', border: 'none', padding: '0.5rem 0', cursor: 'pointer',
              fontWeight: activeTab === tab ? 'bold' : 'normal',
              color: activeTab === tab ? 'var(--primary-color)' : 'var(--text-muted)',
              borderBottom: activeTab === tab ? '2px solid var(--primary-color)' : '2px solid transparent',
              textTransform: 'capitalize'
            }}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="tab-content">
        {activeTab === 'overview' && (
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
            <div className="card" style={{ padding: '1.5rem', backgroundColor: 'var(--surface-color)', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
              <h3 style={{ marginBottom: '1.5rem' }}>Contact Info</h3>
              <div style={{ display: 'grid', gridTemplateColumns: '100px 1fr', gap: '1rem', marginBottom: '1rem' }}>
                <span className="text-muted">Email</span><span>{customer.email}</span>
                <span className="text-muted">Phone</span><span>{customer.phone || '—'}</span>
                <span className="text-muted">Company</span><span>{customer.company || '—'}</span>
                <span className="text-muted">Country</span><span>{customer.country || '—'}</span>
                <span className="text-muted">Timezone</span><span>{customer.timezone || '—'}</span>
                <span className="text-muted">Language</span><span>{customer.preferred_language || '—'}</span>
              </div>
            </div>
            <div className="card" style={{ padding: '1.5rem', backgroundColor: 'var(--surface-color)', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
              <h3 style={{ marginBottom: '1.5rem' }}>Account</h3>
              <div style={{ display: 'grid', gridTemplateColumns: '120px 1fr', gap: '1rem', marginBottom: '1rem' }}>
                <span className="text-muted">Plan</span><span>{customer.subscription_plan || '—'}</span>
                <span className="text-muted">Tier</span><span>{customer.support_tier || '—'}</span>
                <span className="text-muted">Renewal Date</span><span>{formatDate(customer.renewal_date)}</span>
                <span className="text-muted">Account Mgr</span><span>{customer.account_manager || '—'}</span>
                <span className="text-muted">Last Login</span><span>{formatDate(customer.last_login)}</span>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'conversations' && (
          <div>
            {convLoading ? <div>Loading...</div> : groupedConversations.length === 0 ? (
              <EmptyState title="No conversations" description="This customer has not started any conversations." />
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                {groupedConversations.map(group => (
                  <div key={group.sessionId} style={{ padding: '1.5rem', backgroundColor: 'var(--surface-color)', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.5rem' }}>
                      <span style={{ fontWeight: 'bold' }}>Session: {group.sessionId.substring(0, 8)}...</span>
                      <span className="text-muted">{formatDate(group.lastMessage.created_at)}</span>
                    </div>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                      {group.messages.map(msg => (
                        <div key={msg.id} style={{ display: 'flex', gap: '1rem' }}>
                          <Badge className={msg.sender_role === 'ai' ? 'badge--info' : msg.sender_role === 'agent' ? 'badge--primary' : 'badge--secondary'}>
                            {msg.sender_role}
                          </Badge>
                          <div style={{ flex: 1 }}>
                            <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '0.25rem' }}>
                              {formatDateTime(msg.created_at)}
                            </div>
                            <div>{msg.content}</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'tickets' && (
          <div>
            {ticketsLoading ? <div>Loading...</div> : customerTickets.length === 0 ? (
              <EmptyState title="No tickets" description="This customer has no tickets." />
            ) : (
              <table className="table">
                <thead>
                  <tr>
                    <th>Status</th>
                    <th>Priority</th>
                    <th>Title</th>
                    <th>Date</th>
                  </tr>
                </thead>
                <tbody>
                  {customerTickets.map(t => (
                    <tr key={t.id} onClick={() => navigate(`/tickets/${t.id}`)} style={{ cursor: 'pointer' }}>
                      <td><TicketStatusBadge status={t.status} isEscalated={t.is_escalated} /></td>
                      <td><TicketPriorityBadge priority={t.priority} /></td>
                      <td>{t.title}</td>
                      <td>{formatDate(t.created_at)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        )}

        {activeTab === 'billing' && (
          <div>
            {billingLoading ? <div>Loading...</div> : customerBilling.length === 0 ? (
              <EmptyState title="No billing records" description="No billing history found." />
            ) : (
              <table className="table">
                <thead>
                  <tr>
                    <th>Invoice #</th>
                    <th>Type</th>
                    <th>Amount</th>
                    <th>Currency</th>
                    <th>Status</th>
                    <th>Date</th>
                  </tr>
                </thead>
                <tbody>
                  {customerBilling.map(b => (
                    <tr key={b.id}>
                      <td>{b.invoice_number || '—'}</td>
                      <td style={{ textTransform: 'capitalize' }}>{b.record_type}</td>
                      <td>{formatCurrency(b.amount, b.currency)}</td>
                      <td>{b.currency}</td>
                      <td>
                        <Badge className={
                          b.status === 'paid' ? 'badge--success' : 
                          b.status === 'pending' ? 'badge--warning' : 
                          b.status === 'failed' ? 'badge--danger' : 'badge--info'
                        }>
                          {b.status}
                        </Badge>
                      </td>
                      <td>{formatDate(b.created_at)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
