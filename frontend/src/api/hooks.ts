import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import client from './client';
import type {
  Employee,
  ListEmployeesResponse,
  InsightsResponse,
  SalaryHistoryRecord,
  CreateEmployeeRequest,
} from './types';

export const employeeQueryKeys = {
  all: ['employees'],
  list: (skip: number, limit: number, filters?: any) => ['employees', 'list', { skip, limit, filters }],
  detail: (id: number) => ['employees', 'detail', id],
  history: (id: number) => ['employees', 'history', id],
  search: (query: string) => ['employees', 'search', query],
};

const insightQueryKeys = {
  all: ['insights'],
  dashboard: ['insights', 'dashboard'],
};

// Employee queries
export function useListEmployees(
  skip: number,
  limit: number,
  filters?: { country?: string; department?: string; job_title?: string; search?: string }
) {
  return useQuery({
    queryKey: employeeQueryKeys.list(skip, limit, filters),
    queryFn: async () => {
      const params = new URLSearchParams({
        skip: String(skip),
        limit: String(limit),
      });
      if (filters?.country) params.append('country', filters.country);
      if (filters?.department) params.append('department', filters.department);
      if (filters?.job_title) params.append('job_title', filters.job_title);
      if (filters?.search) params.append('search', filters.search);

      const { data } = await client.get<ListEmployeesResponse>(`/employees?${params}`);
      return data;
    },
  });
}

export function useGetEmployee(id: number) {
  return useQuery({
    queryKey: employeeQueryKeys.detail(id),
    queryFn: async () => {
      const { data } = await client.get<Employee>(`/employees/${id}`);
      return data;
    },
  });
}

export function useCreateEmployee() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (req: CreateEmployeeRequest) => {
      const { data } = await client.post<Employee>('/employees', req);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: employeeQueryKeys.all });
    },
  });
}

export function useUpdateEmployee(id: number) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (req: Partial<CreateEmployeeRequest>) => {
      const { data } = await client.put<Employee>(`/employees/${id}`, req);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: employeeQueryKeys.all });
      queryClient.invalidateQueries({ queryKey: employeeQueryKeys.detail(id) });
    },
  });
}

export function useDeleteEmployee(id: number) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async () => {
      await client.delete(`/employees/${id}`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: employeeQueryKeys.all });
    },
  });
}

// Salary history
export function useSalaryHistory(id: number) {
  return useQuery({
    queryKey: employeeQueryKeys.history(id),
    queryFn: async () => {
      const { data } = await client.get<SalaryHistoryRecord[]>(`/employees/${id}/salary-history`);
      return data;
    },
  });
}

export function useUpdateSalary(id: number) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (req: { new_salary: number; currency: string; reason?: string; effective_date: string; old_salary?: number | null }) => {
      const { data } = await client.post(`/employees/${id}/salary-history`, req);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: employeeQueryKeys.all });
      queryClient.invalidateQueries({ queryKey: employeeQueryKeys.detail(id) });
      queryClient.invalidateQueries({ queryKey: employeeQueryKeys.history(id) });
      queryClient.invalidateQueries({ queryKey: insightQueryKeys.all });
    },
  });
}

// Insights
export function useInsights() {
  return useQuery({
    queryKey: insightQueryKeys.dashboard,
    queryFn: async () => {
      const { data } = await client.get<InsightsResponse>('/insights/dashboard');
      return data;
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}
