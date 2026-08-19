import { useCallback, useEffect, useState } from 'react';
import { employeesApi } from '@/api/employees';
import type { AppError } from '@/utils/errors';
import type { Employee } from '@/types';

export function useEmployees(params?: { skip?: number; limit?: number }) {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<AppError | null>(null);

  const fetchEmployees = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const res = await employeesApi.list(params);
      setEmployees(res.data);
    } catch (err) {
      setError(err as AppError);
    } finally {
      setIsLoading(false);
    }
  }, [params?.skip, params?.limit]);

  useEffect(() => {
    void fetchEmployees();
  }, [fetchEmployees]);

  return { employees, isLoading, error, refetch: fetchEmployees };
}
