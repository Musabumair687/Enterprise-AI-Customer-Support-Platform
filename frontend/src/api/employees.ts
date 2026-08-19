import { client } from './client';
import type { APIResponse, Employee } from '@/types';

export const employeesApi = {
  list: (params?: { skip?: number; limit?: number }) =>
    client.get<APIResponse<Employee[]>>('/employees', { params }).then((r) => r.data),

  get: (id: number) =>
    client.get<APIResponse<Employee>>(`/employees/${id}`).then((r) => r.data),
};
