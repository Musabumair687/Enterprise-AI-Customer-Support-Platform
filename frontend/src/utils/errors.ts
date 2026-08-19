/**
 * Error utilities for Axios response handling.
 * Maps HTTP status codes and network errors to user-friendly messages.
 * The frontend NEVER crashes from API errors — always shows a graceful state.
 */

import axios, { AxiosError } from 'axios';

export interface AppError {
  code: string;
  message: string;
  detail?: string;
  status?: number;
}

const STATUS_MESSAGES: Record<number, string> = {
  400: 'The request was invalid. Please check your input and try again.',
  401: 'You are not authorized. Please sign in again.',
  403: 'You do not have permission to perform this action.',
  404: 'The requested resource was not found.',
  409: 'A conflict occurred. The resource may already exist.',
  422: 'Validation failed. Please check the submitted data.',
  429: 'Too many requests. Please wait a moment and try again.',
  500: 'An internal server error occurred. Please try again shortly.',
  502: 'The server is temporarily unavailable. Please try again.',
  503: 'The service is currently unavailable. Please try again.',
};

export function parseApiError(error: unknown): AppError {
  if (axios.isAxiosError(error)) {
    const axiosErr = error as AxiosError<{ message?: string; detail?: string }>;

    // Network error — backend is unreachable
    if (!axiosErr.response) {
      return {
        code: 'NETWORK_ERROR',
        message: 'Unable to connect to Corvex Support API. Please check your connection and try again.',
      };
    }

    const status = axiosErr.response.status;
    const responseData = axiosErr.response.data;
    const detail = responseData?.message ?? responseData?.detail;

    // 401 — redirect to login is handled by the Axios interceptor
    if (status === 401) {
      return {
        code: 'UNAUTHORIZED',
        message: STATUS_MESSAGES[401],
        status,
      };
    }

    return {
      code: `HTTP_${status}`,
      message: STATUS_MESSAGES[status] ?? 'An unexpected error occurred. Please try again.',
      detail: typeof detail === 'string' ? detail : undefined,
      status,
    };
  }

  // Timeout
  if (error instanceof Error && error.message.includes('timeout')) {
    return {
      code: 'TIMEOUT',
      message: 'The request timed out. Please try again.',
    };
  }

  // Unknown
  return {
    code: 'UNKNOWN_ERROR',
    message: 'An unexpected error occurred. Please try again.',
    detail: error instanceof Error ? error.message : undefined,
  };
}

export function isNetworkError(error: AppError): boolean {
  return error.code === 'NETWORK_ERROR' || error.code === 'TIMEOUT';
}

export function isAuthError(error: AppError): boolean {
  return error.code === 'UNAUTHORIZED' || error.status === 403;
}
