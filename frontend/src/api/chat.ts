import { client } from './client';
import type { APIResponse, AIResponse, ChatRequest } from '@/types';

export const chatApi = {
  send: (payload: ChatRequest) =>
    client.post<APIResponse<AIResponse>>('/chat', payload).then((r) => r.data),
};
