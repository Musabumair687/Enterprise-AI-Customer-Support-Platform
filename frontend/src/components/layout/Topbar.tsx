import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Bell, ChevronDown, LogOut, User } from 'lucide-react';
import { useAuth } from '@/context/AuthContext';
import { initials } from '@/utils/formatters';

export default function Topbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [userMenuOpen, setUserMenuOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/tickets?q=${encodeURIComponent(searchQuery.trim())}`);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="topbar" role="banner">
      {/* Search */}
      <form className="topbar__search" onSubmit={handleSearch} role="search">
        <Search className="topbar__search-icon" aria-hidden="true" />
        <input
          id="topbar-search"
          type="search"
          className="topbar__search-input"
          placeholder="Search tickets, customers…"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          aria-label="Search tickets and customers"
        />
      </form>

      {/* Actions */}
      <div className="topbar__actions">
        {/* Notifications */}
        <button
          id="topbar-notifications"
          className="topbar__icon-btn"
          aria-label="Notifications"
          title="Notifications"
        >
          <Bell size={18} />
          <span className="topbar__notification-dot" aria-hidden="true" />
        </button>

        {/* User menu */}
        <div style={{ position: 'relative' }}>
          <button
            id="topbar-user-menu"
            className="topbar__user"
            onClick={() => setUserMenuOpen((o) => !o)}
            aria-haspopup="true"
            aria-expanded={userMenuOpen}
            aria-label="User menu"
          >
            <div className="topbar__avatar" aria-hidden="true">
              {user ? initials(user.name) : 'U'}
            </div>
            <span className="topbar__user-name">{user?.name ?? 'User'}</span>
            <ChevronDown size={14} style={{ color: 'var(--color-text-muted)' }} />
          </button>

          {userMenuOpen && (
            <>
              {/* Backdrop */}
              <div
                style={{ position: 'fixed', inset: 0, zIndex: 99 }}
                onClick={() => setUserMenuOpen(false)}
              />
              {/* Dropdown */}
              <div
                style={{
                  position: 'absolute',
                  right: 0,
                  top: 'calc(100% + 8px)',
                  minWidth: 200,
                  background: 'var(--color-surface)',
                  border: '1px solid var(--color-border)',
                  borderRadius: 'var(--radius-xl)',
                  boxShadow: 'var(--shadow-lg)',
                  zIndex: 100,
                  overflow: 'hidden',
                }}
                role="menu"
              >
                {/* User info */}
                <div style={{ padding: '12px 16px', borderBottom: '1px solid var(--color-border)' }}>
                  <div style={{ fontWeight: 600, fontSize: 'var(--text-sm)', color: 'var(--color-text-primary)' }}>
                    {user?.name}
                  </div>
                  <div style={{ fontSize: 'var(--text-xs)', color: 'var(--color-text-muted)', marginTop: 2 }}>
                    {user?.email}
                  </div>
                </div>
                {/* Items */}
                <div style={{ padding: '4px 0' }}>
                  <button
                    className="sidebar__link"
                    style={{ width: '100%', borderRadius: 0 }}
                    onClick={() => { navigate('/settings/profile'); setUserMenuOpen(false); }}
                    role="menuitem"
                  >
                    <User size={14} /> Profile
                  </button>
                  <div className="divider" />
                  <button
                    className="sidebar__link"
                    style={{ width: '100%', borderRadius: 0, color: 'var(--color-danger)' }}
                    onClick={handleLogout}
                    role="menuitem"
                  >
                    <LogOut size={14} /> Sign Out
                  </button>
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
