import { client } from './client';
import type { APIResponse, Conversation } from '@/types';

export const conversationsApi = {
  list: (params?: { skip?: number; limit?: number }) =>
    client.get<APIResponse<Conversation[]>>('/conversations', { params }).then((r) => r.data),
};
