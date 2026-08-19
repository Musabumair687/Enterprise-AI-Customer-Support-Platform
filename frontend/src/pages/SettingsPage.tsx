import React, { useState, useEffect } from 'react';
import { User, Cpu, Bell, Users } from 'lucide-react';
import { useAuth } from '@/context/AuthContext';
import { useEmployees } from '@/hooks/useEmployees';
import { initials } from '@/utils/formatters';
import { Badge } from '@/components/ui/Badge';
import { SkeletonTable } from '@/components/ui/Skeleton';

export default function SettingsPage() {
  const { user } = useAuth();
  const { employees, isLoading: isLoadingEmployees } = useEmployees({ limit: 100 });
  const [activeSection, setActiveSection] = useState('profile');

  // Handle ?section= URL param
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const sectionParam = params.get('section');
    if (sectionParam && ['profile', 'ai', 'notifications', 'team'].includes(sectionParam)) {
      setActiveSection(sectionParam);
    }
  }, []);

  const handleNavClick = (section: string) => {
    setActiveSection(section);
    const url = new URL(window.location.href);
    url.searchParams.set('section', section);
    window.history.pushState({}, '', url);
  };

  const navItems = [
    { id: 'profile', label: 'Profile', icon: <User size={18} /> },
    { id: 'ai', label: 'AI Configuration', icon: <Cpu size={18} /> },
    { id: 'notifications', label: 'Notifications', icon: <Bell size={18} /> },
    { id: 'team', label: 'Team', icon: <Users size={18} /> }
  ];

  return (
    <div className="settings-layout" style={{ display: 'grid', gridTemplateColumns: '200px 1fr', height: '100%' }}>
      {/* LEFT NAV */}
      <div className="settings-nav" style={{ borderRight: '1px solid var(--border-color)', padding: 'var(--space-4)', background: 'var(--bg-card)' }}>
        <h2 style={{ fontSize: 'var(--font-size-lg)', marginBottom: 'var(--space-4)', marginTop: 0 }}>Settings</h2>
        <nav style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-2)' }}>
          {navItems.map(item => (
            <button
              key={item.id}
              onClick={() => handleNavClick(item.id)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 'var(--space-3)',
                padding: 'var(--space-2) var(--space-3)',
                borderRadius: 'var(--radius-md)',
                background: activeSection === item.id ? 'var(--bg-active)' : 'transparent',
                color: activeSection === item.id ? 'var(--text-main)' : 'var(--text-secondary)',
                border: 'none',
                cursor: 'pointer',
                textAlign: 'left',
                fontWeight: activeSection === item.id ? 500 : 400
              }}
            >
              {item.icon}
              {item.label}
            </button>
          ))}
        </nav>
      </div>

      {/* CONTENT AREA */}
      <div style={{ padding: 'var(--space-6)', overflowY: 'auto', background: 'var(--bg-main)' }}>
        
        {/* PROFILE SECTION */}
        {activeSection === 'profile' && (
          <div className="settings-section" style={{ maxWidth: '600px' }}>
            <div className="settings-header" style={{ marginBottom: 'var(--space-6)' }}>
              <h1 style={{ fontSize: 'var(--font-size-2xl)', margin: '0 0 var(--space-2) 0' }}>Profile</h1>
              <p style={{ color: 'var(--text-secondary)', margin: 0 }}>Your personal information</p>
            </div>
            
            <div style={{ background: 'var(--bg-card)', padding: 'var(--space-6)', borderRadius: 'var(--radius-lg)', border: '1px solid var(--border-color)', display: 'flex', flexDirection: 'column', gap: 'var(--space-5)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-4)' }}>
                <div style={{ width: '64px', height: '64px', borderRadius: '50%', background: 'var(--color-primary)', color: 'white', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '24px', fontWeight: 'bold' }}>
                  {initials(user?.name || 'User')}
                </div>
                <div>
                  <h3 style={{ margin: '0 0 var(--space-1) 0' }}>Avatar</h3>
                  <p style={{ margin: 0, color: 'var(--text-muted)', fontSize: 'var(--font-size-sm)' }}>Generated from your name initials.</p>
                </div>
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-2)' }}>
                <label style={{ fontWeight: 500, fontSize: 'var(--font-size-sm)' }}>Name</label>
                <input type="text" className="input-field" value={user?.name || ''} readOnly disabled />
              </div>
              
              <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-2)' }}>
                <label style={{ fontWeight: 500, fontSize: 'var(--font-size-sm)' }}>Email</label>
                <input type="email" className="input-field" value={user?.email || ''} readOnly disabled />
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-2)' }}>
                <label style={{ fontWeight: 500, fontSize: 'var(--font-size-sm)' }}>Role</label>
                <div><Badge variant="primary">{user?.role || 'Admin'}</Badge></div>
              </div>

              <div style={{ marginTop: 'var(--space-4)' }}>
                <button className="btn btn--secondary" disabled title="Coming soon">Edit Profile</button>
              </div>
            </div>
          </div>
        )}

        {/* AI CONFIGURATION SECTION */}
        {activeSection === 'ai' && (
          <div className="settings-section" style={{ maxWidth: '800px' }}>
            <div className="settings-header" style={{ marginBottom: 'var(--space-6)' }}>
              <h1 style={{ fontSize: 'var(--font-size-2xl)', margin: '0 0 var(--space-2) 0' }}>AI Configuration</h1>
              <p style={{ color: 'var(--text-secondary)', margin: 0 }}>Read-only view of current AI system settings. These values are configured in the backend environment.</p>
            </div>

            <div className="alert alert--ai" style={{ background: 'var(--color-primary-bg)', color: 'var(--color-primary)', padding: 'var(--space-3)', borderRadius: 'var(--radius-md)', marginBottom: 'var(--space-6)', display: 'flex', gap: 'var(--space-2)', alignItems: 'center' }}>
              ✦ These settings reflect the live backend configuration. Edit them in the .env file or through the backend admin API when available.
            </div>

            <div style={{ background: 'var(--bg-card)', borderRadius: 'var(--radius-lg)', border: '1px solid var(--border-color)', overflow: 'hidden' }}>
               {[
                 { label: 'LLM Provider', value: 'Gemini (gemini-3.6-flash)' },
                 { label: 'Fallback Provider', value: 'Groq (llama-3.3-70b-versatile)' },
                 { label: 'Confidence Threshold', value: '0.50' },
                 { label: 'Human Escalation', value: 'Enabled', isToggle: true },
                 { label: 'RAG Top K', value: '5' },
                 { label: 'Reranker', value: 'Enabled' },
                 { label: 'Max Agent Steps', value: '5' },
                 { label: 'LLM Timeout', value: '60s' }
               ].map((setting, idx) => (
                 <div key={setting.label} className="settings-row" style={{ display: 'flex', justifyContent: 'space-between', padding: 'var(--space-4)', borderBottom: idx < 7 ? '1px solid var(--border-color)' : 'none' }}>
                   <div style={{ fontWeight: 500 }}>{setting.label}</div>
                   <div className="settings-readonly-value" style={{ color: 'var(--text-secondary)' }}>
                     {setting.isToggle ? (
                        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-2)' }}>
                          <span style={{ fontSize: 'var(--font-size-sm)' }}>{setting.value}</span>
                          <div style={{ width: '36px', height: '20px', background: 'var(--color-success)', borderRadius: '10px', position: 'relative', opacity: 0.7 }}>
                             <div style={{ width: '16px', height: '16px', background: 'white', borderRadius: '50%', position: 'absolute', top: '2px', right: '2px' }} />
                          </div>
                        </div>
                     ) : setting.value}
                   </div>
                 </div>
               ))}
            </div>
            
            <p style={{ marginTop: 'var(--space-4)', color: 'var(--text-muted)', fontSize: 'var(--font-size-sm)' }}>
              // TODO: Bind to GET /api/v1/settings/ai when available
            </p>
          </div>
        )}

        {/* NOTIFICATIONS SECTION */}
        {activeSection === 'notifications' && (
          <div className="settings-section" style={{ maxWidth: '600px' }}>
            <div className="settings-header" style={{ marginBottom: 'var(--space-6)' }}>
              <h1 style={{ fontSize: 'var(--font-size-2xl)', margin: '0 0 var(--space-2) 0' }}>Notifications</h1>
              <p style={{ color: 'var(--text-secondary)', margin: 0 }}>Manage your email and in-app alerts</p>
            </div>

            <div style={{ background: 'var(--bg-card)', borderRadius: 'var(--radius-lg)', border: '1px solid var(--border-color)', overflow: 'hidden' }}>
               {[
                 { label: 'Escalation Alerts', desc: 'Notify when AI escalates a ticket to human' },
                 { label: 'New Ticket', desc: 'Notify when a new ticket is created' },
                 { label: 'Ticket Resolved', desc: 'Notify when a ticket is resolved' }
               ].map((notif, idx) => (
                 <div key={notif.label} className="settings-row" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: 'var(--space-4)', borderBottom: idx < 2 ? '1px solid var(--border-color)' : 'none' }}>
                   <div>
                     <div style={{ fontWeight: 500 }}>{notif.label}</div>
                     <div style={{ fontSize: 'var(--font-size-sm)', color: 'var(--text-secondary)' }}>{notif.desc}</div>
                   </div>
                   <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-2)', opacity: 0.7 }}>
                      <div style={{ width: '36px', height: '20px', background: 'var(--color-success)', borderRadius: '10px', position: 'relative' }}>
                         <div style={{ width: '16px', height: '16px', background: 'white', borderRadius: '50%', position: 'absolute', top: '2px', right: '2px' }} />
                      </div>
                   </div>
                 </div>
               ))}
            </div>
          </div>
        )}

        {/* TEAM SECTION */}
        {activeSection === 'team' && (
          <div className="settings-section">
            <div className="settings-header" style={{ marginBottom: 'var(--space-6)' }}>
              <h1 style={{ fontSize: 'var(--font-size-2xl)', margin: '0 0 var(--space-2) 0' }}>Team</h1>
              <p style={{ color: 'var(--text-secondary)', margin: 0 }}>Manage agents and their roles</p>
            </div>

            <div style={{ background: 'var(--bg-card)', borderRadius: 'var(--radius-lg)', border: '1px solid var(--border-color)', overflow: 'hidden' }}>
              {isLoadingEmployees ? (
                 <div style={{ padding: 'var(--space-4)' }}>
                   {SkeletonTable && <SkeletonTable rows={5} />}
                 </div>
              ) : (
                <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                  <thead style={{ background: 'var(--bg-main)', borderBottom: '1px solid var(--border-color)' }}>
                    <tr>
                      <th style={{ padding: 'var(--space-3) var(--space-4)', fontWeight: 500, color: 'var(--text-secondary)', fontSize: 'var(--font-size-sm)' }}>Name</th>
                      <th style={{ padding: 'var(--space-3) var(--space-4)', fontWeight: 500, color: 'var(--text-secondary)', fontSize: 'var(--font-size-sm)' }}>Email</th>
                      <th style={{ padding: 'var(--space-3) var(--space-4)', fontWeight: 500, color: 'var(--text-secondary)', fontSize: 'var(--font-size-sm)' }}>Role</th>
                      <th style={{ padding: 'var(--space-3) var(--space-4)', fontWeight: 500, color: 'var(--text-secondary)', fontSize: 'var(--font-size-sm)' }}>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {employees.map(emp => (
                      <tr key={emp.id} style={{ borderBottom: '1px solid var(--border-color)' }}>
                        <td style={{ padding: 'var(--space-3) var(--space-4)' }}>
                          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)' }}>
                            <div style={{ width: '32px', height: '32px', borderRadius: '50%', background: 'var(--color-primary-bg)', color: 'var(--color-primary)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 'var(--font-size-xs)', fontWeight: 'bold' }}>
                              {initials(emp.first_name + ' ' + emp.last_name)}
                            </div>
                            <span style={{ fontWeight: 500 }}>{emp.first_name} {emp.last_name}</span>
                          </div>
                        </td>
                        <td style={{ padding: 'var(--space-3) var(--space-4)', color: 'var(--text-secondary)' }}>{emp.email}</td>
                        <td style={{ padding: 'var(--space-3) var(--space-4)' }}>
                          <Badge variant="default">{emp.role || 'Agent'}</Badge>
                        </td>
                        <td style={{ padding: 'var(--space-3) var(--space-4)' }}>
                          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-2)' }}>
                            <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: emp.is_active ? 'var(--color-success)' : 'var(--text-muted)' }} />
                            <span>{emp.is_active ? 'Active' : 'Inactive'}</span>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          </div>
        )}

      </div>
    </div>
  );
}
