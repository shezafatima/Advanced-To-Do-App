/**
 * Error handling utilities for the Todo Full-Stack Web Application frontend.
 *
 * This module provides error handling, user feedback mechanisms, and error reporting
 * for the frontend application.
 */

import { toast } from 'react-hot-toast'; // Assuming react-hot-toast is used for notifications

// Define application-specific error codes
export enum ErrorCode {
  // Authentication errors
  AUTHENTICATION_FAILED = 'AUTHENTICATION_FAILED',
  INVALID_CREDENTIALS = 'INVALID_CREDENTIALS',
  TOKEN_EXPIRED = 'TOKEN_EXPIRED',
  INSUFFICIENT_PERMISSIONS = 'INSUFFICIENT_PERMISSIONS',

  // User errors
  USER_NOT_FOUND = 'USER_NOT_FOUND',
  USER_ALREADY_EXISTS = 'USER_ALREADY_EXISTS',
  INVALID_USER_DATA = 'INVALID_USER_DATA',

  // Todo errors
  TODO_NOT_FOUND = 'TODO_NOT_FOUND',
  TODO_OWNER_MISMATCH = 'TODO_OWNER_MISMATCH',
  INVALID_TODO_DATA = 'INVALID_TODO_DATA',

  // Network errors
  NETWORK_ERROR = 'NETWORK_ERROR',
  TIMEOUT_ERROR = 'TIMEOUT_ERROR',
  SERVER_ERROR = 'SERVER_ERROR',

  // Validation errors
  VALIDATION_ERROR = 'VALIDATION_ERROR',
  INVALID_INPUT = 'INVALID_INPUT',

  // Unknown error
  UNKNOWN_ERROR = 'UNKNOWN_ERROR',
}

// Standard error response interface
export interface ErrorResponse {
  detail: string;
  error_code?: string;
  request_id?: string;
  timestamp?: string;
  path?: string;
}

// Error with additional metadata
export class AppError extends Error {
  public errorCode: ErrorCode;
  public statusCode?: number;
  public originalError?: Error;

  constructor(
    message: string,
    errorCode: ErrorCode = ErrorCode.UNKNOWN_ERROR,
    statusCode?: number,
    originalError?: Error
  ) {
    super(message);
    this.name = 'AppError';
    this.errorCode = errorCode;
    this.statusCode = statusCode;
    this.originalError = originalError;

    // Maintains proper stack trace for where our error was thrown (only available on V8)
    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, AppError);
    }
  }
}

/**
 * Maps HTTP status codes to application error codes.
 */
export const mapHttpStatusToErrorCode = (statusCode: number): ErrorCode => {
  switch (statusCode) {
    case 400:
      return ErrorCode.INVALID_INPUT;
    case 401:
      return ErrorCode.AUTHENTICATION_FAILED;
    case 403:
      return ErrorCode.INSUFFICIENT_PERMISSIONS;
    case 404:
      return ErrorCode.TODO_NOT_FOUND; // Could be TODO_NOT_FOUND or USER_NOT_FOUND depending on context
    case 409:
      return ErrorCode.USER_ALREADY_EXISTS; // Could be USER_ALREADY_EXISTS or similar
    case 422:
      return ErrorCode.VALIDATION_ERROR;
    case 408:
    case 504:
      return ErrorCode.TIMEOUT_ERROR;
    case 500:
    case 502:
    case 503:
      return ErrorCode.SERVER_ERROR;
    default:
      return ErrorCode.UNKNOWN_ERROR;
  }
};

/**
 * Formats error response for consistent display.
 */
export const formatErrorResponse = (error: any): ErrorResponse => {
  // If it's already a formatted error response
  if (error.detail) {
    return {
      detail: error.detail,
      error_code: error.error_code,
      request_id: error.request_id,
      timestamp: error.timestamp,
      path: error.path,
    };
  }

  // If it's a network error or fetch error
  if (error instanceof TypeError) {
    return {
      detail: 'Network error occurred. Please check your connection.',
      error_code: ErrorCode.NETWORK_ERROR,
    };
  }

  // If it's an HTTP error with response
  if (error.response) {
    return {
      detail: error.response.data?.detail || `HTTP ${error.response.status} error`,
      error_code: mapHttpStatusToErrorCode(error.response.status),
      request_id: error.response.headers?.['x-request-id'],
      timestamp: new Date().toISOString(),
    };
  }

  // If it's a regular error
  if (error.message) {
    return {
      detail: error.message,
      error_code: ErrorCode.UNKNOWN_ERROR,
    };
  }

  // Fallback
  return {
    detail: 'An unknown error occurred',
    error_code: ErrorCode.UNKNOWN_ERROR,
  };
};

/**
 * Displays user-friendly error messages based on error type.
 */
export const displayUserError = (error: any, customMessage?: string): void => {
  const errorResponse = formatErrorResponse(error);
  let userMessage = customMessage || errorResponse.detail;

  // Customize messages based on error code
  switch (errorResponse.error_code) {
    case ErrorCode.AUTHENTICATION_FAILED:
      userMessage = 'Authentication failed. Please log in again.';
      break;
    case ErrorCode.TOKEN_EXPIRED:
      userMessage = 'Session expired. Please log in again.';
      break;
    case ErrorCode.INSUFFICIENT_PERMISSIONS:
      userMessage = 'You do not have permission to perform this action.';
      break;
    case ErrorCode.NETWORK_ERROR:
      userMessage = 'Network error. Please check your connection.';
      break;
    case ErrorCode.TIMEOUT_ERROR:
      userMessage = 'Request timed out. Please try again.';
      break;
    case ErrorCode.SERVER_ERROR:
      userMessage = 'Server error. Please try again later.';
      break;
    case ErrorCode.VALIDATION_ERROR:
      userMessage = 'Invalid input. Please check the form and try again.';
      break;
    default:
      // Use the original message or a generic one
      break;
  }

  // Display error to user (using toast notification or similar)
  toast.error(userMessage);

  // Log error for debugging (in non-production environments)
  if (process.env.NODE_ENV !== 'production') {
    console.error('Error details:', {
      message: errorResponse.detail,
      code: errorResponse.error_code,
      requestId: errorResponse.request_id,
      timestamp: errorResponse.timestamp,
    });
  }
};

/**
 * Logs error to external service (could be integrated with Sentry, LogRocket, etc.)
 */
export const logErrorToService = (error: any, context?: string): void => {
  // In a real application, this would send error to an external service
  // like Sentry, LogRocket, or a custom error tracking service

  const errorResponse = formatErrorResponse(error);

  // Example logging to console (would be replaced with actual service)
  console.group('Error Report');
  console.error('Error:', errorResponse.detail);
  console.error('Code:', errorResponse.error_code);
  console.error('Context:', context || 'Unknown');
  console.error('Timestamp:', errorResponse.timestamp);
  console.error('Request ID:', errorResponse.request_id);
  console.groupEnd();
};

/**
 * Centralized error handler that combines all error handling strategies.
 */
export const handleError = (
  error: any,
  context?: string,
  customMessage?: string,
  shouldLogToService: boolean = true
): AppError => {
  // Format the error
  const errorResponse = formatErrorResponse(error);

  // Create AppError instance
  const appError = new AppError(
    errorResponse.detail,
    errorResponse.error_code as ErrorCode,
    undefined, // statusCode would come from response
    error instanceof Error ? error : undefined
  );

  // Display user-friendly error message
  displayUserError(error, customMessage);

  // Log to external service if enabled
  if (shouldLogToService) {
    logErrorToService(error, context);
  }

  // Return the formatted error for further handling if needed
  return appError;
};

/**
 * Higher-order function to wrap async operations with error handling.
 */
export const withErrorHandler = <T>(
  asyncOperation: () => Promise<T>,
  context?: string,
  customMessage?: string
): Promise<T> => {
  return asyncOperation().catch((error) => {
    handleError(error, context, customMessage);
    throw error; // Re-throw if needed for further handling
  });
};

/**
 * Validates form inputs and returns formatted errors.
 */
export const validateInputs = (
  inputs: Record<string, any>,
  rules: Record<string, (value: any) => string | null>
): Record<string, string> => {
  const errors: Record<string, string> = {};

  for (const [field, value] of Object.entries(inputs)) {
    const validate = rules[field];
    if (validate) {
      const error = validate(value);
      if (error) {
        errors[field] = error;
      }
    }
  }

  return errors;
};

/**
 * Checks if an error indicates the user needs to re-authenticate.
 */
export const isErrorRequiringReauth = (error: any): boolean => {
  const errorResponse = formatErrorResponse(error);
  return [
    ErrorCode.AUTHENTICATION_FAILED,
    ErrorCode.TOKEN_EXPIRED,
    ErrorCode.INSUFFICIENT_PERMISSIONS
  ].includes(errorResponse.error_code as ErrorCode);
};