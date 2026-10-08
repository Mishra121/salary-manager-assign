export type EmploymentType = 'FULL_TIME' | 'PART_TIME' | 'CONTRACT';
export type EmployeeStatus = 'ACTIVE' | 'INACTIVE' | 'ON_LEAVE';

export interface Employee {
  id: number;
  name: string;
  email: string;
  job_title: string;
  department: string;
  country: string;
  employment_type: EmploymentType;
  hire_date: string;
  salary: number;
  currency: string;
  status: EmployeeStatus;
  created_at?: string;
  updated_at?: string;
}

export interface SalaryHistoryRecord {
  id: number;
  employee_id: number;
  old_salary: number | null;
  new_salary: number;
  currency: string;
  effective_date: string;
  reason?: string;
  created_at: string;
}

export interface ListEmployeesResponse {
  total: number;
  skip: number;
  limit: number;
  employees: Employee[];
}

export interface InsightsResponse {
  headline: {
    headcount: number;
    total_payroll_usd: number;
    avg_salary_usd: number;
    median_salary_usd: number;
    min_salary_usd: number;
    max_salary_usd: number;
  };
  by_country: Array<{
    country: string;
    headcount: number;
    avg_salary_usd: number;
    median_salary_usd: number;
    min_salary_usd: number;
    max_salary_usd: number;
  }>;
  by_department: Array<{
    department: string;
    headcount: number;
    avg_salary_usd: number;
    median_salary_usd: number;
  }>;
  by_job_title: Array<{
    job_title: string;
    count: number;
    avg_salary_usd: number;
    median_salary_usd: number;
  }>;
  distribution: Array<{
    bracket: string;
    count: number;
  }>;
  outliers: Array<{
    id: number;
    name: string;
    job_title: string;
    salary_usd: number;
    avg_for_title_usd: number;
    deviation_from_avg: number;
  }>;
}

export interface CreateEmployeeRequest {
  name: string;
  email: string;
  job_title: string;
  department: string;
  country: string;
  employment_type: EmploymentType;
  hire_date: string;
  salary: number;
  currency: string;
}

export interface UpdateEmployeeRequest extends Partial<CreateEmployeeRequest> {
  id: number;
}
