import React, { useMemo } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { useCustomers } from '@/hooks/useCustomers';
import { SkeletonTable } from '@/components/ui/Skeleton';
import { EmptyState } from '@/components/ui/EmptyState';
import { PlanBadge, Badge } from '@/components/ui/Badge';
import { formatCurrencyShort } from '@/utils/formatters';

export const CustomersPage: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();
  const { customers, isLoading, error } = useCustomers({ limit: 500 });

  const searchQuery = searchParams.get('q') || '';

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

  const filteredCustomers = useMemo(() => {
    if (!searchQuery) return customers;
    const query = searchQuery.toLowerCase();
    return customers.filter((c) => 
      c.name.toLowerCase().includes(query) || 
      c.email.toLowerCase().includes(query) || 
      (c.company && c.company.toLowerCase().includes(query))
    );
  }, [customers, searchQuery]);

  // TODO: health score logic based on plan
  const getHealthScore = (plan: string | null) => {
    if (!plan) return 55;
    const p = plan.toLowerCase();
    if (p.includes('enterprise')) return 90;
    if (p.includes('pro')) return 75;
    return 55;
  };

  return (
    <div className="page-container">
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <div>
          <h1 className="page-title" style={{ display: 'inline-block', marginRight: '1rem' }}>Customers</h1>
          <span className="text-muted">{filteredCustomers.length} total</span>
        </div>
      </div>

      <div className="filter-bar" style={{ marginBottom: '1rem' }}>
        <input
          type="text"
          placeholder="Search customers by name, email or company..."
          className="input-field"
          value={searchQuery}
          onChange={handleSearch}
          style={{ maxWidth: '400px' }}
        />
      </div>

      {error ? (
        <EmptyState title="Error Loading Customers" description={error.message} />
      ) : isLoading ? (
        <SkeletonTable columns={7} rows={10} />
      ) : (
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>Customer</th>
                <th>Company</th>
                <th>Plan</th>
                <th>Health Score</th>
                <th>Open Tickets</th>
                <th>Revenue</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {filteredCustomers.map((c) => (
                <tr key={c.id} onClick={() => navigate(`/customers/${c.id}`)} style={{ cursor: 'pointer' }}>
                  <td>
                    <div style={{ fontWeight: 'bold' }}>{c.name}</div>
                    <div className="text-muted" style={{ fontSize: '0.85rem' }}>{c.email}</div>
                  </td>
                  <td>{c.company || '—'}</td>
                  <td>
                    <PlanBadge plan={c.subscription_plan} />
                  </td>
                  <td>
                    <span style={{ 
                      color: getHealthScore(c.subscription_plan) >= 90 ? 'var(--success-color)' : 
                             getHealthScore(c.subscription_plan) >= 70 ? 'var(--warning-color)' : 'var(--danger-color)' 
                    }}>
                      {getHealthScore(c.subscription_plan)}
                    </span>
                  </td>
                  <td>—</td> {/* TODO: require extra API call for open tickets */}
                  <td>{formatCurrencyShort(c.monthly_revenue)}</td>
                  <td>
                    <Badge className={c.status === 'active' ? 'badge--success' : 'badge--secondary'}>
                      {c.status}
                    </Badge>
                  </td>
                </tr>
              ))}
              {filteredCustomers.length === 0 && (
                <tr>
                  <td colSpan={7}>
                    <EmptyState title="No customers found" description="Try adjusting your search" />
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
