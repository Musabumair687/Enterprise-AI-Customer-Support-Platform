import { useEffect, useState } from 'react';
import { conversationsApi } from '@/api/conversations';
import type { AppError } from '@/utils/errors';
import type { Conversation } from '@/types';

export function useConversations(params?: { skip?: number; limit?: number }) {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<AppError | null>(null);

  useEffect(() => {
    setIsLoading(true);
    conversationsApi
      .list(params)
      .then((res) => setConversations(res.data))
      .catch((err: AppError) => setError(err))
      .finally(() => setIsLoading(false));
  }, [params?.skip, params?.limit]); // eslint-disable-line react-hooks/exhaustive-deps

  return { conversations, isLoading, error };
}
