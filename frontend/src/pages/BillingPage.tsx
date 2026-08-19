import React, { useMemo } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useBilling } from '@/hooks/useBilling';
import { SkeletonTable } from '@/components/ui/Skeleton';
import { EmptyState } from '@/components/ui/EmptyState';
import { Badge } from '@/components/ui/Badge';
import { formatCurrency, formatDate } from '@/utils/formatters';

export default function BillingPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const { records, isLoading, error } = useBilling({ limit: 500 });

  const activeTab = searchParams.get('tab') || 'overview';

  const setTab = (tab: string) => {
    setSearchParams((prev) => {
      prev.set('tab', tab);
      return prev;
    });
  };

  const filteredRecords = useMemo(() => {
    if (activeTab === 'invoices') return records.filter((r) => r.record_type === 'invoice');
    if (activeTab === 'payments') return records.filter((r) => r.record_type === 'payment');
    if (activeTab === 'refunds') return records.filter((r) => r.record_type === 'refund');
    return records;
  }, [records, activeTab]);

  const stats = useMemo(() => {
    let totalRevenue = 0;
    let paidCount = 0;
    let pendingCount = 0;
    let refundsCount = 0;

    records.forEach((r) => {
      if (r.status === 'paid') {
        totalRevenue += parseFloat(r.amount);
        paidCount++;
      } else if (r.status === 'pending') {
        pendingCount++;
      } else if (r.status === 'refunded') {
        refundsCount++;
      }
    });

    return { totalRevenue, paidCount, pendingCount, refundsCount };
  }, [records]);

  const getStatusBadgeClass = (status: string) => {
    switch (status) {
      case 'paid': return 'badge--success';
      case 'pending': return 'badge--warning';
      case 'failed': return 'badge--danger';
      case 'refunded': return 'badge--info';
      default: return 'badge--secondary';
    }
  };

  return (
    <div className="page-container">
      <div className="page-header" style={{ marginBottom: '2rem' }}>
        <h1 className="page-title">Billing</h1>
      </div>

      <div className="tabs-bar" style={{ display: 'flex', gap: '2rem', borderBottom: '1px solid var(--border-color)', marginBottom: '2rem' }}>
        {['overview', 'invoices', 'payments', 'refunds'].map((tab) => (
          <button
            key={tab}
            onClick={() => setTab(tab)}
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

      {activeTab === 'overview' && (
        <div className="billing-header-stats" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.5rem', marginBottom: '2rem' }}>
          <div className="stat-card" style={{ padding: '1.5rem', backgroundColor: 'var(--surface-color)', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
            <div className="text-muted" style={{ marginBottom: '0.5rem' }}>Total Revenue</div>
            <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{formatCurrency(stats.totalRevenue)}</div>
          </div>
          <div className="stat-card" style={{ padding: '1.5rem', backgroundColor: 'var(--surface-color)', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
            <div className="text-muted" style={{ marginBottom: '0.5rem' }}>Paid</div>
            <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'var(--success-color)' }}>{stats.paidCount}</div>
          </div>
          <div className="stat-card" style={{ padding: '1.5rem', backgroundColor: 'var(--surface-color)', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
            <div className="text-muted" style={{ marginBottom: '0.5rem' }}>Pending</div>
            <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'var(--warning-color)' }}>{stats.pendingCount}</div>
          </div>
          <div className="stat-card" style={{ padding: '1.5rem', backgroundColor: 'var(--surface-color)', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
            <div className="text-muted" style={{ marginBottom: '0.5rem' }}>Refunds</div>
            <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'var(--info-color)' }}>{stats.refundsCount}</div>
          </div>
        </div>
      )}

      {error ? (
        <EmptyState title="Error Loading Billing Records" description={error.message} />
      ) : isLoading ? (
        <SkeletonTable columns={9} rows={10} />
      ) : (
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>Invoice #</th>
                <th>Customer ID</th>
                <th>Plan</th>
                <th>Amount</th>
                <th>Currency</th>
                <th>Type</th>
                <th>Status</th>
                <th>Due Date</th>
                <th>Paid Date</th>
              </tr>
            </thead>
            <tbody>
              {filteredRecords.map((r) => (
                <tr key={r.id}>
                  <td>{r.invoice_number || '—'}</td>
                  <td className="text-muted">{r.customer_id}</td>
                  <td>{r.plan || '—'}</td>
                  <td style={{ fontWeight: 'bold' }}>{formatCurrency(r.amount, r.currency)}</td>
                  <td>{r.currency}</td>
                  <td style={{ textTransform: 'capitalize' }}>
                    <Badge className="badge--secondary">{r.record_type}</Badge>
                  </td>
                  <td>
                    <Badge className={getStatusBadgeClass(r.status)}>{r.status}</Badge>
                  </td>
                  <td>{formatDate(r.due_date)}</td>
                  <td>{formatDate(r.paid_date)}</td>
                </tr>
              ))}
              {filteredRecords.length === 0 && (
                <tr>
                  <td colSpan={9}>
                    <EmptyState title="No records found" description="There are no billing records matching this filter." />
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};
