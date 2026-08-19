import { client } from './client';
import type { APIResponse, Ticket, TicketCreate, TicketUpdate } from '@/types';

export const ticketsApi = {
  list: (params?: { skip?: number; limit?: number }) =>
    client.get<APIResponse<Ticket[]>>('/tickets', { params }).then((r) => r.data),

  get: (id: number) =>
    client.get<APIResponse<Ticket>>(`/tickets/${id}`).then((r) => r.data),

  create: (payload: TicketCreate) =>
    client.post<APIResponse<Ticket>>('/tickets', payload).then((r) => r.data),

  update: (id: number, payload: TicketUpdate) =>
    client.put<APIResponse<Ticket>>(`/tickets/${id}`, payload).then((r) => r.data),

  delete: (id: number) =>
    client.delete<APIResponse<{ id: number }>>(`/tickets/${id}`).then((r) => r.data),
};
