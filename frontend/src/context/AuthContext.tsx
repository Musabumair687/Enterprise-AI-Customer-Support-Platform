/**
 * AuthContext — Authentication state management.
 *
 * DEV mode:  Mock authentication — credentials from .env.local (never committed)
 *            Defaults: VITE_DEV_EMAIL / VITE_DEV_PASSWORD
 *
 * PROD mode: Structured for POST /api/v1/auth/login → JWT
 *            Replace the `loginDev` branch with `loginProd` when the auth
 *            endpoint is built.
 *
 * The logged-in user is persisted to localStorage as `corvex_user`.
 * The auth token is stored separately as `corvex_token`.
 */

import React, { createContext, useCallback, useContext, useEffect, useState } from 'react';
import type { AuthUser } from '@/types';

// ─── Demo user for development ───────────────────────────────────────────────
// Credentials are read from .env.local — never hardcode in source.
const DEV_EMAIL = (import.meta.env.VITE_DEV_EMAIL as string | undefined) ?? 'admin@corvex.ai';
const DEV_PASSWORD = (import.meta.env.VITE_DEV_PASSWORD as string | undefined) ?? 'corvex2024';

const DEV_USER: AuthUser = {
  id: 1,
  name: 'Musab',
  email: DEV_EMAIL,
  role: 'admin',
};

// ─── Context shape ─────────────────────────────────────────────────────────────

interface AuthContextValue {
  user: AuthUser | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  error: string | null;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

// ─── Provider ─────────────────────────────────────────────────────────────────

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Restore session from localStorage on mount
  useEffect(() => {
    try {
      const stored = localStorage.getItem('corvex_user');
      if (stored) {
        setUser(JSON.parse(stored) as AuthUser);
      }
    } catch {
      localStorage.removeItem('corvex_user');
    } finally {
      setIsLoading(false);
    }
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    setIsLoading(true);
    setError(null);

    try {
      if (import.meta.env.DEV) {
        // ── DEV: Mock auth ────────────────────────────────────────────────────
        await new Promise((r) => setTimeout(r, 600)); // simulate network

        if (email !== DEV_EMAIL || password !== DEV_PASSWORD) {
          throw new Error('Invalid credentials. Check .env.local for dev credentials.');
        }

        const token = `mock-jwt-token-${Date.now()}`;
        localStorage.setItem('corvex_token', token);
        localStorage.setItem('corvex_user', JSON.stringify(DEV_USER));
        setUser(DEV_USER);
      } else {
        // ── PROD: Replace with real JWT endpoint ──────────────────────────────
        // const { data } = await client.post<APIResponse<{ token: string; user: AuthUser }>>(
        //   '/auth/login',
        //   { email, password },
        // );
        // localStorage.setItem('corvex_token', data.data.token);
        // localStorage.setItem('corvex_user', JSON.stringify(data.data.user));
        // setUser(data.data.user);
        throw new Error('Production auth endpoint not yet implemented.');
      }
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Login failed. Please try again.';
      setError(message);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem('corvex_token');
    localStorage.removeItem('corvex_user');
    setUser(null);
  }, []);

  return (
    <AuthContext.Provider
      value={{ user, isAuthenticated: !!user, isLoading, login, logout, error }}
    >
      {children}
    </AuthContext.Provider>
  );
}

// ─── Hook ─────────────────────────────────────────────────────────────────────

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within <AuthProvider>');
  return ctx;
}
