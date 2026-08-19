import { client } from './client';
import type { APIResponse, Customer } from '@/types';

export const customersApi = {
  list: (params?: { skip?: number; limit?: number }) =>
    client.get<APIResponse<Customer[]>>('/customers', { params }).then((r) => r.data),

  get: (id: number) =>
    client.get<APIResponse<Customer>>(`/customers/${id}`).then((r) => r.data),

  search: (query: string, params?: { skip?: number; limit?: number }) =>
    client
      .get<APIResponse<Customer[]>>('/customers/search', { params: { query, ...params } })
      .then((r) => r.data),
};
