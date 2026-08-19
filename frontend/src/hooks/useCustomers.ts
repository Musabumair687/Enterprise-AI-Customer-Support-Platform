import { useCallback, useEffect, useState } from 'react';
import { customersApi } from '@/api/customers';
import type { AppError } from '@/utils/errors';
import type { Customer } from '@/types';

export function useCustomers(params?: { skip?: number; limit?: number }) {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<AppError | null>(null);

  const fetchCustomers = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const res = await customersApi.list(params);
      setCustomers(res.data);
    } catch (err) {
      setError(err as AppError);
    } finally {
      setIsLoading(false);
    }
  }, [params?.skip, params?.limit]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    void fetchCustomers();
  }, [fetchCustomers]);

  return { customers, isLoading, error, refetch: fetchCustomers };
}

export function useCustomer(id: number) {
  const [customer, setCustomer] = useState<Customer | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<AppError | null>(null);

  useEffect(() => {
    setIsLoading(true);
    customersApi
      .get(id)
      .then((res) => setCustomer(res.data))
      .catch((err: AppError) => setError(err))
      .finally(() => setIsLoading(false));
  }, [id]);

  return { customer, isLoading, error };
}
