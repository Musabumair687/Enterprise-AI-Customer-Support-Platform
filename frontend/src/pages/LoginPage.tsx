import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Mail, Lock, Eye, EyeOff, Loader2, ShieldCheck, Zap, Users } from 'lucide-react';
import { useAuth } from '@/context/AuthContext';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const navigate = useNavigate();
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);

    try {
      await login(email, password);
      navigate('/dashboard');
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('An unexpected error occurred.');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="login-page" style={{ display: 'flex', minHeight: '100vh' }}>
      <div className="login-page__left" style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', padding: '4rem', maxWidth: '500px', margin: '0 auto' }}>
        <div className="login-brand" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '3rem' }}>
          <ShieldCheck className="brand-icon" style={{ color: 'var(--color-primary-600)' }} />
          <span className="brand-name" style={{ fontSize: '1.5rem', fontWeight: 700 }}>CORVEX</span>
        </div>

        <div className="login-header" style={{ marginBottom: '2rem' }}>
          <h1 style={{ fontSize: '2rem', fontWeight: 700, marginBottom: '0.5rem' }}>Welcome back</h1>
          <p style={{ color: 'var(--text-secondary)' }}>Sign in to your Corvex Support workspace</p>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          {error && (
            <div className="login-error" style={{ color: 'var(--color-danger)', backgroundColor: 'var(--color-danger-50)', padding: '0.75rem', borderRadius: '4px', marginBottom: '1.5rem' }}>
              {error}
            </div>
          )}

          <div className="form-group" style={{ marginBottom: '1.25rem' }}>
            <label htmlFor="login-email" style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>Email</label>
            <div className="input-wrapper" style={{ position: 'relative' }}>
              <Mail style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-tertiary)' }} size={18} />
              <input
                id="login-email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                style={{ width: '100%', padding: '0.75rem 1rem 0.75rem 2.5rem', borderRadius: '6px', border: '1px solid var(--border-color)' }}
              />
            </div>
          </div>

          <div className="form-group" style={{ marginBottom: '1.5rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
              <label htmlFor="login-password" style={{ fontWeight: 500 }}>Password</label>
              <a href="#" style={{ color: 'var(--color-primary-600)', fontSize: '0.875rem' }}>Forgot password?</a>
            </div>
            <div className="input-wrapper" style={{ position: 'relative' }}>
              <Lock style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-tertiary)' }} size={18} />
              <input
                id="login-password"
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                style={{ width: '100%', padding: '0.75rem 2.5rem', borderRadius: '6px', border: '1px solid var(--border-color)' }}
              />
              <button
                type="button"
                id="toggle-pw"
                onClick={() => setShowPassword(!showPassword)}
                style={{ position: 'absolute', right: '1rem', top: '50%', transform: 'translateY(-50%)', background: 'none', border: 'none', cursor: 'pointer', color: 'var(--text-tertiary)' }}
              >
                {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
              </button>
            </div>
          </div>

          <button
            type="submit"
            id="login-submit"
            disabled={isSubmitting}
            style={{ width: '100%', padding: '0.75rem', backgroundColor: 'var(--color-primary-600)', color: 'white', border: 'none', borderRadius: '6px', fontWeight: 600, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '0.5rem', cursor: isSubmitting ? 'not-allowed' : 'pointer' }}
          >
            {isSubmitting && <Loader2 className="spinner" size={18} />}
            Sign In
          </button>
        </form>

        <div className="login-footer" style={{ marginTop: 'auto', paddingTop: '3rem', fontSize: '0.875rem', color: 'var(--text-tertiary)' }}>
          Enterprise AI Customer Support Platform
        </div>
      </div>

      <div className="login-page__right" style={{ flex: 1, backgroundColor: 'var(--bg-dark)', color: 'white', padding: '4rem', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <div className="feature-panel" style={{ maxWidth: '480px', margin: '0 auto' }}>
          <div className="icon-box" style={{ backgroundColor: 'var(--color-violet-600)', width: '48px', height: '48px', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '1.5rem' }}>
            <ShieldCheck size={24} color="white" />
          </div>
          <h2 style={{ fontSize: '2.5rem', fontWeight: 700, marginBottom: '1rem' }}>AI-Powered Support Platform</h2>
          <p style={{ fontSize: '1.125rem', color: 'var(--text-dark-secondary)', marginBottom: '3rem', lineHeight: 1.6 }}>
            Intelligent ticket routing, RAG-powered answers, and seamless human escalation — all in one workspace.
          </p>

          <div className="feature-list" style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
            <div className="feature-row" style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <div className="feature-icon" style={{ backgroundColor: 'var(--color-violet-600)', padding: '0.75rem', borderRadius: '8px' }}>
                <Zap size={20} color="white" />
              </div>
              <span style={{ fontSize: '1.125rem', fontWeight: 500 }}>AI Resolution — 74% of tickets resolved automatically</span>
            </div>
            <div className="feature-row" style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <div className="feature-icon" style={{ backgroundColor: 'var(--color-blue-600)', padding: '0.75rem', borderRadius: '8px' }}>
                <Users size={20} color="white" />
              </div>
              <span style={{ fontSize: '1.125rem', fontWeight: 500 }}>Human Escalation — Smart handoff with full context</span>
            </div>
            <div className="feature-row" style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <div className="feature-icon" style={{ backgroundColor: 'var(--color-green-600)', padding: '0.75rem', borderRadius: '8px' }}>
                <ShieldCheck size={20} color="white" />
              </div>
              <span style={{ fontSize: '1.125rem', fontWeight: 500 }}>RAG Knowledge — Answers grounded in your knowledge base</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
