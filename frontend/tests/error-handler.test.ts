/**
 * Tests for the error handling utilities in the Todo Full-Stack Web Application frontend.
 */

import {
  ErrorCode,
  formatErrorResponse,
  displayUserError,
  isErrorRequiringReauth,
  handleError,
  validateInputs
} from '../src/utils/error-handler';

// Mock the toast function for testing
jest.mock('react-hot-toast', () => ({
  toast: {
    error: jest.fn(),
    success: jest.fn(),
    loading: jest.fn(),
  },
}));

describe('Error Handler Utilities', () => {
  beforeEach(() => {
    // Clear console mocks before each test
    jest.clearAllMocks();
    console.error = jest.fn();
    console.group = jest.fn();
    console.groupEnd = jest.fn();
  });

  describe('formatErrorResponse', () => {
    it('should format error with detail property', () => {
      const input = { detail: 'Something went wrong', error_code: 'TEST_ERROR' };
      const result = formatErrorResponse(input);

      expect(result.detail).toBe('Something went wrong');
      expect(result.error_code).toBe('TEST_ERROR');
    });

    it('should handle network errors', () => {
      const networkError = new TypeError('Network error');
      const result = formatErrorResponse(networkError);

      expect(result.error_code).toBe(ErrorCode.NETWORK_ERROR);
      expect(result.detail).toContain('Network error');
    });

    it('should handle regular errors', () => {
      const error = new Error('Regular error');
      const result = formatErrorResponse(error);

      expect(result.detail).toBe('Regular error');
      expect(result.error_code).toBe(ErrorCode.UNKNOWN_ERROR);
    });
  });

  describe('displayUserError', () => {
    it('should display user-friendly authentication error', () => {
      const { toast } = require('react-hot-toast');
      const error = {
        response: {
          status: 401,
          data: { detail: 'Auth failed' }
        }
      };

      displayUserError(error);

      expect(toast.error).toHaveBeenCalledWith('Authentication failed. Please log in again.');
    });

    it('should display user-friendly validation error', () => {
      const { toast } = require('react-hot-toast');
      const error = {
        response: {
          status: 422,
          data: { detail: 'Validation failed' }
        }
      };

      displayUserError(error);

      expect(toast.error).toHaveBeenCalledWith('Invalid input. Please check the form and try again.');
    });

    it('should display custom message if provided', () => {
      const { toast } = require('react-hot-toast');
      const error = { detail: 'Generic error' };

      displayUserError(error, 'Custom error message');

      expect(toast.error).toHaveBeenCalledWith('Custom error message');
    });
  });

  describe('isErrorRequiringReauth', () => {
    it('should return true for authentication errors', () => {
      const authError = {
        response: {
          status: 401,
          data: { error_code: ErrorCode.AUTHENTICATION_FAILED }
        }
      };

      expect(isErrorRequiringReauth(authError)).toBe(true);
    });

    it('should return true for token expired errors', () => {
      const tokenError = {
        response: {
          status: 401,
          data: { error_code: ErrorCode.TOKEN_EXPIRED }
        }
      };

      expect(isErrorRequiringReauth(tokenError)).toBe(true);
    });

    it('should return false for other errors', () => {
      const otherError = {
        response: {
          status: 400,
          data: { error_code: ErrorCode.VALIDATION_ERROR }
        }
      };

      expect(isErrorRequiringReauth(otherError)).toBe(false);
    });
  });

  describe('handleError', () => {
    it('should handle and format errors properly', () => {
      const { toast } = require('react-hot-toast');
      const error = new Error('Test error');

      const result = handleError(error, 'test context', 'custom message');

      expect(result).toBeDefined();
      expect(result.name).toBe('AppError');
      expect(toast.error).toHaveBeenCalled();
    });
  });

  describe('validateInputs', () => {
    it('should return no errors for valid inputs', () => {
      const inputs = { email: 'test@example.com', name: 'John' };
      const rules = {
        email: (value: string) => !value.includes('@') ? 'Must be valid email' : null,
        name: (value: string) => value.length < 2 ? 'Must be at least 2 chars' : null
      };

      const errors = validateInputs(inputs, rules);

      expect(Object.keys(errors)).toHaveLength(0);
    });

    it('should return errors for invalid inputs', () => {
      const inputs = { email: 'invalid-email', name: 'J' };
      const rules = {
        email: (value: string) => !value.includes('@') ? 'Must be valid email' : null,
        name: (value: string) => value.length < 2 ? 'Must be at least 2 chars' : null
      };

      const errors = validateInputs(inputs, rules);

      expect(errors.email).toBe('Must be valid email');
      expect(errors.name).toBe('Must be at least 2 chars');
    });

    it('should return empty errors for inputs without validation rules', () => {
      const inputs = { age: 25 };
      const rules = {
        email: (value: string) => !value.includes('@') ? 'Must be valid email' : null,
      };

      const errors = validateInputs(inputs, rules);

      expect(Object.keys(errors)).toHaveLength(0);
    });
  });
});