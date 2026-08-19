import { useEffect, useState } from 'react';
import { billingApi } from '@/api/billing';
import type { AppError } from '@/utils/errors';
import type { BillingRecord } from '@/types';

export function useBilling(params?: { skip?: number; limit?: number }) {
  const [records, setRecords] = useState<BillingRecord[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<AppError | null>(null);

  useEffect(() => {
    setIsLoading(true);
    billingApi
      .list(params)
      .then((res) => setRecords(res.data))
      .catch((err: AppError) => setError(err))
      .finally(() => setIsLoading(false));
  }, [params?.skip, params?.limit]); // eslint-disable-line react-hooks/exhaustive-deps

  return { records, isLoading, error };
}
