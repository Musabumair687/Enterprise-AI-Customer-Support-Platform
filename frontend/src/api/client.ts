/**
 * Axios client instance.
 * - Base URL reads from Vite env (VITE_API_URL) or defaults to /api/v1
 * - Request interceptor attaches Bearer token from localStorage
 * - Response interceptor maps all errors to AppError before they reach hooks
 */

import axios from 'axios';
import { parseApiError } from '@/utils/errors';

const BASE_URL = (import.meta.env.VITE_API_URL as string | undefined) ?? '/api/v1';

export const client = axios.create({
  baseURL: BASE_URL,
  timeout: 30_000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ─── Request — attach auth token ─────────────────────────────────────────────

client.interceptors.request.use((config) => {
  const token = localStorage.getItem('corvex_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ─── Response — map errors ────────────────────────────────────────────────────

client.interceptors.response.use(
  (response) => response,
  (error) => {
    const appError = parseApiError(error);

    // 401 — clear session and redirect to login
    if (appError.status === 401) {
      localStorage.removeItem('corvex_token');
      localStorage.removeItem('corvex_user');
      window.location.href = '/login';
    }

    return Promise.reject(appError);
  },
);
