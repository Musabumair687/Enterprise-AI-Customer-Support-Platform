import { useCallback, useEffect, useState } from 'react';
import { ticketsApi } from '@/api/tickets';
import type { AppError } from '@/utils/errors';
import type { Ticket, TicketCreate, TicketUpdate } from '@/types';

export function useTickets(params?: { skip?: number; limit?: number }) {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<AppError | null>(null);

  const fetchTickets = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const res = await ticketsApi.list(params);
      setTickets(res.data);
    } catch (err) {
      setError(err as AppError);
    } finally {
      setIsLoading(false);
    }
  }, [params?.skip, params?.limit]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    void fetchTickets();
  }, [fetchTickets]);

  const createTicket = useCallback(async (payload: TicketCreate): Promise<Ticket | null> => {
    try {
      const res = await ticketsApi.create(payload);
      setTickets((prev) => [res.data, ...prev]);
      return res.data;
    } catch (err) {
      setError(err as AppError);
      return null;
    }
  }, []);

  const updateTicket = useCallback(async (id: number, payload: TicketUpdate): Promise<Ticket | null> => {
    try {
      const res = await ticketsApi.update(id, payload);
      setTickets((prev) => prev.map((t) => (t.id === id ? res.data : t)));
      return res.data;
    } catch (err) {
      setError(err as AppError);
      return null;
    }
  }, []);

  return { tickets, isLoading, error, refetch: fetchTickets, createTicket, updateTicket };
}

export function useTicket(id: number) {
  const [ticket, setTicket] = useState<Ticket | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<AppError | null>(null);

  useEffect(() => {
    setIsLoading(true);
    ticketsApi
      .get(id)
      .then((res) => setTicket(res.data))
      .catch((err: AppError) => setError(err))
      .finally(() => setIsLoading(false));
  }, [id]);

  return { ticket, isLoading, error };
}
