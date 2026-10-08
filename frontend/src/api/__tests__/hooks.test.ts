import { describe, it, expect } from 'vitest';
import { employeeQueryKeys } from '../hooks';

describe('employeeQueryKeys', () => {
  it('should generate list query key', () => {
    const key = employeeQueryKeys.list(0, 50);
    expect(key).toEqual(['employees', 'list', { skip: 0, limit: 50, filters: undefined }]);
  });

  it('should generate detail query key', () => {
    const key = employeeQueryKeys.detail(1);
    expect(key).toEqual(['employees', 'detail', 1]);
  });

  it('should generate history query key', () => {
    const key = employeeQueryKeys.history(1);
    expect(key).toEqual(['employees', 'history', 1]);
  });

  it('should generate search query key', () => {
    const key = employeeQueryKeys.search('alice');
    expect(key).toEqual(['employees', 'search', 'alice']);
  });
});
