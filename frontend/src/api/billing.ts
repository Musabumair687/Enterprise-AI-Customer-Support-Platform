import { client } from './client';
import type { APIResponse, BillingRecord } from '@/types';

export const billingApi = {
  list: (params?: { skip?: number; limit?: number }) =>
    client.get<APIResponse<BillingRecord[]>>('/billing', { params }).then((r) => r.data),

  get: (id: number) =>
    client.get<APIResponse<BillingRecord>>(`/billing/${id}`).then((r) => r.data),
};
