import React, { useState, useMemo, useEffect, useRef } from 'react';
import { MessageSquare, Sparkles, AlertTriangle, Ticket, ArrowRight, User } from 'lucide-react';
import { useConversations } from '@/hooks/useConversations';
import { useCustomers } from '@/hooks/useCustomers';
import { chatApi } from '@/api/chat';
import AIBadge from '@/components/ai/AIBadge';
import AIActivityPanel from '@/components/ai/AIActivityPanel';
import AISourcesPanel from '@/components/ai/AISourcesPanel';
import EscalationPanel from '@/components/ai/EscalationPanel';
import EscalationModal from '@/components/tickets/EscalationModal';
import { EmptyState } from '@/components/ui/EmptyState';
import { Badge } from '@/components/ui/Badge';
import { formatRelativeTime, formatCurrencyShort, initials } from '@/utils/formatters';
import type { AIResponse, ChatEscalation } from '@/types';

interface LocalMessage {
  id: string;
  role: 'customer' | 'ai' | 'agent' | 'system';
  content: string;
  timestamp: string;
  aiResponse?: AIResponse;
}

export default function ChatPage() {
  const { conversations, isLoading: isLoadingConvos } = useConversations({ limit: 100 });
  const { customers } = useCustomers({ limit: 500 });

  const [activeSessionId, setActiveSessionId] = useState<string | null>(null);
  const [message, setMessage] = useState('');
  const [isSending, setIsSending] = useState(false);
  const [localMessages, setLocalMessages] = useState<Record<string, LocalMessage[]>>({});
  const [escalationConfirmed, setEscalationConfirmed] = useState(false);
  const [showEscalationModal, setShowEscalationModal] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Group conversations into sessions for the left panel
  const sessions = useMemo(() => {
    if (!conversations) return [];
    const map = new Map<string, typeof conversations[0][]>();
    conversations.forEach((c) => {
      if (!map.has(c.session_id)) {
        map.set(c.session_id, []);
      }
      map.get(c.session_id)!.push(c);
    });

    const list = Array.from(map.entries()).map(([session_id, msgs]) => {
      const sorted = msgs.sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime());
      const lastMsg = sorted[sorted.length - 1];
      const hasEscalation = sorted.some(m => m.content.toLowerCase().includes('escalated') || m.sender_role === 'agent');
      
      return {
        session_id,
        customer_id: sorted[0]?.customer_id,
        lastMessage: lastMsg?.content || '',
        timestamp: lastMsg?.created_at || '',
        isEscalated: hasEscalation,
        allMessages: sorted
      };
    });

    return list.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
  }, [conversations]);

  const [searchQuery, setSearchQuery] = useState('');
  
  const filteredSessions = useMemo(() => {
    if (!searchQuery) return sessions;
    const lowerQuery = searchQuery.toLowerCase();
    return sessions.filter(s => 
      s.session_id.toLowerCase().includes(lowerQuery) || 
      s.lastMessage.toLowerCase().includes(lowerQuery) ||
      (s.customer_id && customers.find(c => c.id === s.customer_id)?.name.toLowerCase().includes(lowerQuery))
    );
  }, [sessions, searchQuery, customers]);

  // Load existing messages when switching sessions
  useEffect(() => {
    if (!activeSessionId) return;
    if (!localMessages[activeSessionId]) {
      const session = sessions.find(s => s.session_id === activeSessionId);
      if (session) {
        const loadedMsgs: LocalMessage[] = session.allMessages.map(m => ({
          id: m.id.toString(),
          role: m.sender_role,
          content: m.content,
          timestamp: m.created_at
        }));
        setLocalMessages(prev => ({ ...prev, [activeSessionId]: loadedMsgs }));
      }
    }
  }, [activeSessionId, sessions, localMessages]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [localMessages, activeSessionId]);

  const activeMessages = activeSessionId ? localMessages[activeSessionId] || [] : [];
  const activeSessionData = sessions.find(s => s.session_id === activeSessionId);
  const activeCustomer = customers.find(c => c.id === activeSessionData?.customer_id);

  const handleAskAI = async () => {
    if (!message.trim() || !activeSessionId) return;
    const content = message;
    setMessage('');
    setIsSending(true);
    setEscalationConfirmed(false);

    const userMsg: LocalMessage = {
      id: Date.now().toString(),
      role: 'agent', // Actually, UI says "Ask AI", maybe it acts as customer? or we type as an agent testing AI?
      content,
      timestamp: new Date().toISOString()
    };

    setLocalMessages(prev => ({
      ...prev,
      [activeSessionId]: [...(prev[activeSessionId] || []), userMsg]
    }));

    try {
      const response = await chatApi.send({
        message: content,
        session_id: activeSessionId,
        customer_id: activeCustomer?.id
      });

      const aiData = response.data;
      const aiMsg: LocalMessage = {
        id: Date.now().toString() + '-ai',
        role: 'ai',
        content: aiData.response,
        timestamp: new Date().toISOString(),
        aiResponse: aiData
      };
      
      setLocalMessages(prev => ({
        ...prev,
        [activeSessionId]: [...(prev[activeSessionId] || []), aiMsg]
      }));

    } catch (err) {
      console.error(err);
      // fallback error message
    } finally {
      setIsSending(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleAskAI();
    }
  };

  const lastAiMessage = activeMessages.slice().reverse().find(m => m.role === 'ai' && m.aiResponse);
  const isEscalated = lastAiMessage?.aiResponse?.escalated;

  const handleEscalationSubmit = async (data: any) => {
    // In a real app, call a backend API here.
    // For now, we simulate success and add a system message.
    alert('Ticket escalated successfully');
    setShowEscalationModal(false);
    setEscalationConfirmed(true);
  };

  const computeHealthScore = (plan?: string | null) => {
    if (!plan) return 0;
    if (plan.toLowerCase().includes('enterprise')) return 92;
    if (plan.toLowerCase().includes('pro')) return 78;
    return 54;
  };

  const customerOpenTickets = conversations.filter(c => c.customer_id === activeCustomer?.id && c.ticket_id).length; // Rough approximation

  return (
    <div className="chat-layout">
      {/* LEFT PANEL */}
      <div className="conversations-panel" style={{ borderRight: '1px solid var(--border-color)', display: 'flex', flexDirection: 'column', height: '100%', overflow: 'hidden', background: 'var(--bg-card)' }}>
        <div style={{ padding: 'var(--space-4)', borderBottom: '1px solid var(--border-color)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-3)' }}>
            <h2 style={{ fontSize: 'var(--font-size-lg)', fontWeight: 600, margin: 0 }}>Conversations</h2>
            <button className="btn btn--secondary" style={{ padding: 'var(--space-1) var(--space-2)' }}>New Chat</button>
          </div>
          <input
            type="text"
            placeholder="Search conversations..."
            className="input-field"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
        <div style={{ overflowY: 'auto', flex: 1 }}>
          {filteredSessions.map(session => {
            const customer = customers.find(c => c.id === session.customer_id);
            const title = customer?.name || session.session_id.substring(0, 8);
            return (
              <div
                key={session.session_id}
                style={{
                  padding: 'var(--space-3) var(--space-4)',
                  borderBottom: '1px solid var(--border-color)',
                  cursor: 'pointer',
                  background: activeSessionId === session.session_id ? 'var(--bg-active)' : 'transparent',
                  display: 'flex',
                  gap: 'var(--space-3)'
                }}
                onClick={() => setActiveSessionId(session.session_id)}
              >
                <div style={{
                  width: '40px', height: '40px', borderRadius: '50%', background: 'var(--color-primary-bg)', color: 'var(--color-primary)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold', flexShrink: 0
                }}>
                  {initials(title)}
                </div>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
                    <div style={{ fontWeight: 500, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{title}</div>
                    <div style={{ fontSize: 'var(--font-size-xs)', color: 'var(--text-muted)' }}>{formatRelativeTime(session.timestamp)}</div>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-2)' }}>
                    <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: session.isEscalated ? 'var(--color-danger)' : 'var(--color-primary)' }} />
                    <div style={{ fontSize: 'var(--font-size-sm)', color: 'var(--text-secondary)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{session.lastMessage}</div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* CENTER WORKSPACE */}
      <div className="chat-workspace" style={{ display: 'flex', flexDirection: 'column', height: '100%', overflow: 'hidden', background: 'var(--bg-main)' }}>
        {!activeSessionId ? (
          <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <EmptyState icon={<MessageSquare size={48} />} title="Select a conversation" description="Choose a conversation from the left panel to view the chat history and AI insights." />
          </div>
        ) : (
          <>
            <div style={{ padding: 'var(--space-4)', borderBottom: '1px solid var(--border-color)', display: 'flex', alignItems: 'center', gap: 'var(--space-3)', background: 'var(--bg-card)' }}>
              <div style={{ flex: 1 }}>
                <h3 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: 'var(--space-2)' }}>
                  {activeCustomer?.name || 'Unknown Customer'}
                  <Badge variant={activeSessionData?.isEscalated ? 'danger' : 'primary'}>{activeSessionData?.isEscalated ? 'Escalated' : 'Active'}</Badge>
                </h3>
                <div style={{ fontSize: 'var(--font-size-sm)', color: 'var(--text-muted)' }}>Session: {activeSessionId}</div>
              </div>
            </div>

            <div className="conversation-messages" style={{ flex: 1, overflowY: 'auto', padding: 'var(--space-4)', display: 'flex', flexDirection: 'column', gap: 'var(--space-4)' }}>
              {activeMessages.map((msg, i) => (
                <div key={msg.id} style={{ display: 'flex', flexDirection: 'column', alignItems: msg.role === 'customer' ? 'flex-start' : 'flex-end' }}>
                  {msg.role === 'ai' && <div style={{ marginBottom: '4px', alignSelf: 'flex-start' }}><AIBadge /></div>}
                  <div className={`message message--${msg.role}`} style={{
                    maxWidth: '80%', padding: 'var(--space-3)', borderRadius: 'var(--radius-lg)',
                    background: msg.role === 'customer' ? 'var(--bg-card)' : msg.role === 'ai' ? 'var(--color-primary-bg)' : 'var(--bg-card)',
                    border: '1px solid var(--border-color)'
                  }}>
                    {msg.content}
                  </div>
                  {msg.role === 'ai' && msg.aiResponse && (
                    <div style={{ marginTop: 'var(--space-2)', alignSelf: 'flex-start', display: 'flex', flexDirection: 'column', gap: 'var(--space-2)', maxWidth: '100%' }}>
                       {msg.aiResponse.agents_used && msg.aiResponse.agents_used.length > 0 && (
                          <AIActivityPanel 
                            agents={msg.aiResponse.agents_used} 
                            tools={msg.aiResponse.tools_used || []} 
                            latencyMs={0} 
                            confidence={msg.aiResponse.confidence || 0.9} 
                          />
                       )}
                       <AISourcesPanel sources={msg.aiResponse.sources || []} available={false} />
                    </div>
                  )}
                  {msg.role === 'ai' && msg.aiResponse?.escalated && i === activeMessages.length - 1 && (
                     <div style={{ alignSelf: 'flex-start', marginTop: 'var(--space-3)', width: '100%' }}>
                        <EscalationPanel 
                           escalation={msg.aiResponse.escalation || { ticket_id: null, reason: 'AI triggered escalation', assigned_employee: null }}
                           showActions={!escalationConfirmed}
                           onEscalate={() => setShowEscalationModal(true)}
                           onContinue={() => setEscalationConfirmed(true)}
                        />
                     </div>
                  )}
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>

            <div style={{ padding: 'var(--space-4)', borderTop: '1px solid var(--border-color)', background: 'var(--bg-card)' }}>
              <textarea
                className="conversation-input input-field"
                placeholder="Type a message to simulate customer or ask AI..."
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyDown={handleKeyDown}
                rows={2}
                style={{ resize: 'none', marginBottom: 'var(--space-3)' }}
              />
              <div style={{ display: 'flex', gap: 'var(--space-2)' }}>
                <button className="btn btn--ai" onClick={handleAskAI} disabled={isSending || !message.trim()}>
                  {isSending ? <span className="spinner" /> : <Sparkles size={16} />} Ask AI
                </button>
                <button className="btn btn--secondary"><AlertTriangle size={16} /> Escalate</button>
                <button className="btn btn--secondary"><Ticket size={16} /> Create Ticket</button>
              </div>
            </div>
          </>
        )}
      </div>

      {/* RIGHT PANEL */}
      <div className="customer-context" style={{ borderLeft: '1px solid var(--border-color)', display: 'flex', flexDirection: 'column', height: '100%', overflow: 'hidden', background: 'var(--bg-card)' }}>
        {!activeCustomer ? (
           <div style={{ padding: 'var(--space-4)' }}>No customer data</div>
        ) : (
          <div style={{ padding: 'var(--space-4)', display: 'flex', flexDirection: 'column', gap: 'var(--space-4)', overflowY: 'auto' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)' }}>
               <div style={{ width: '48px', height: '48px', borderRadius: '50%', background: 'var(--color-primary)', color: 'white', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold', fontSize: 'var(--font-size-lg)' }}>
                 {initials(activeCustomer.name)}
               </div>
               <div>
                 <div style={{ fontWeight: 600, fontSize: 'var(--font-size-lg)' }}>{activeCustomer.name}</div>
                 <div style={{ display: 'flex', gap: 'var(--space-2)', marginTop: '4px' }}>
                   <Badge variant="primary">{activeCustomer.subscription_plan || 'Free'}</Badge>
                   <Badge variant={activeCustomer.status === 'active' ? 'success' : 'default'}>{activeCustomer.status}</Badge>
                 </div>
               </div>
            </div>

            <div style={{ padding: 'var(--space-3)', background: 'var(--bg-main)', borderRadius: 'var(--radius-md)' }}>
              <div style={{ fontSize: 'var(--font-size-sm)', color: 'var(--text-secondary)', marginBottom: '4px' }}>Health Score</div>
              <div style={{ fontSize: '24px', fontWeight: 'bold', color: computeHealthScore(activeCustomer.subscription_plan) > 80 ? 'var(--color-success)' : 'var(--color-warning)' }}>
                {computeHealthScore(activeCustomer.subscription_plan)}/100
              </div>
            </div>

            <div className="customer-stats-grid" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--space-3)' }}>
               <div style={{ padding: 'var(--space-3)', background: 'var(--bg-main)', borderRadius: 'var(--radius-md)' }}>
                 <div style={{ fontSize: 'var(--font-size-xs)', color: 'var(--text-secondary)' }}>Open Tickets</div>
                 <div style={{ fontWeight: 600, fontSize: 'var(--font-size-lg)' }}>{customerOpenTickets}</div>
               </div>
               <div style={{ padding: 'var(--space-3)', background: 'var(--bg-main)', borderRadius: 'var(--radius-md)' }}>
                 <div style={{ fontSize: 'var(--font-size-xs)', color: 'var(--text-secondary)' }}>LTV</div>
                 <div style={{ fontWeight: 600, fontSize: 'var(--font-size-lg)' }}>{formatCurrencyShort(activeCustomer.lifetime_value)}</div>
               </div>
               <div style={{ padding: 'var(--space-3)', background: 'var(--bg-main)', borderRadius: 'var(--radius-md)' }}>
                 <div style={{ fontSize: 'var(--font-size-xs)', color: 'var(--text-secondary)' }}>Monthly Rev</div>
                 <div style={{ fontWeight: 600, fontSize: 'var(--font-size-lg)' }}>{formatCurrencyShort(activeCustomer.monthly_revenue)}</div>
               </div>
               <div style={{ padding: 'var(--space-3)', background: 'var(--bg-main)', borderRadius: 'var(--radius-md)' }}>
                 <div style={{ fontSize: 'var(--font-size-xs)', color: 'var(--text-secondary)' }}>Last Interaction</div>
                 <div style={{ fontWeight: 600, fontSize: 'var(--font-size-sm)' }}>{formatRelativeTime(activeSessionData?.timestamp)}</div>
               </div>
            </div>

            <button className="btn btn--secondary" style={{ width: '100%', justifyContent: 'center' }}>
              View Profile
            </button>
          </div>
        )}
      </div>

      {showEscalationModal && activeCustomer && (
        <EscalationModal
          isOpen={showEscalationModal}
          onClose={() => setShowEscalationModal(false)}
          customerId={activeCustomer.id}
          customerName={activeCustomer.name}
          aiSummary={lastAiMessage?.aiResponse?.escalation?.reason || 'Escalated by AI'}
          onSubmit={handleEscalationSubmit}
        />
      )}
    </div>
  );
}
