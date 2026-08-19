import { NavLink, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  MessageSquare,
  Ticket,
  Users,
  BarChart3,
  CreditCard,
  Settings,
  Zap,
  ShieldCheck,
} from 'lucide-react';
import { useTickets } from '@/hooks/useTickets';

const NAV_ITEMS = [
  { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/chat', label: 'Chat', icon: MessageSquare },
  { to: '/tickets', label: 'Tickets', icon: Ticket },
  { to: '/customers', label: 'Customers', icon: Users },
  { to: '/analytics', label: 'Analytics', icon: BarChart3 },
  { to: '/billing', label: 'Billing', icon: CreditCard },
];

const BOTTOM_ITEMS = [
  { to: '/settings', label: 'Settings', icon: Settings },
];

export default function Sidebar() {
  const location = useLocation();
  const { tickets } = useTickets({ limit: 500 });
  const escalatedCount = tickets.filter((t) => t.is_escalated && t.status !== 'resolved' && t.status !== 'closed').length;

  return (
    <aside className="sidebar" role="navigation" aria-label="Main navigation">
      {/* Brand */}
      <div className="sidebar__brand">
        <div className="sidebar__brand-logo" aria-hidden="true">
          <ShieldCheck />
        </div>
        <span className="sidebar__brand-name">CORVEX</span>
      </div>

      {/* Nav */}
      <nav className="sidebar__nav scrollbar-thin">
        {NAV_ITEMS.map(({ to, label, icon: Icon }) => {
          const isActive = location.pathname.startsWith(to);
          const showBadge = to === '/tickets' && escalatedCount > 0;
          return (
            <NavLink
              key={to}
              to={to}
              id={`nav-${label.toLowerCase()}`}
              className={`sidebar__link${isActive ? ' sidebar__link--active' : ''}`}
            >
              <Icon />
              {label}
              {showBadge && (
                <span className="sidebar__badge" aria-label={`${escalatedCount} escalated tickets`}>
                  {escalatedCount}
                </span>
              )}
            </NavLink>
          );
        })}

        <div className="divider" style={{ margin: '8px 16px' }} />

        {BOTTOM_ITEMS.map(({ to, label, icon: Icon }) => {
          const isActive = location.pathname.startsWith(to);
          return (
            <NavLink
              key={to}
              to={to}
              id={`nav-${label.toLowerCase()}`}
              className={`sidebar__link${isActive ? ' sidebar__link--active' : ''}`}
            >
              <Icon />
              {label}
            </NavLink>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="sidebar__footer">
        <div className="sidebar__ai-status" role="status" aria-label="AI system status">
          <div className="sidebar__ai-status-dot" />
          <Zap style={{ width: 12, height: 12, color: 'var(--color-ai-text)' }} />
          <span className="sidebar__ai-status-text">AI Active</span>
        </div>
        <div className="sidebar__version">Corvex Platform v0.1.0</div>
      </div>
    </aside>
  );
}
