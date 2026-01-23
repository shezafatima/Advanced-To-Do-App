import axios, { AxiosInstance } from 'axios';

// Create an axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to attach JWT token
apiClient.interceptors.request.use(
  (config) => {
    // Get token from wherever you store it (localStorage, context, etc.)
    const token = localStorage.getItem('access_token');

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token expiration and other auth errors
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.code === 'NETWORK_ERROR' || error.code === 'ERR_NETWORK') {
      // Handle network/offline errors
      console.warn('Network error - possibly offline:', error.message);
      // Could implement offline queueing here
    } else if (error.response?.status === 401) {
      // Handle token expiration - redirect to login or refresh token
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    } else if (error.response?.status === 429) {
      // Handle rate limiting
      alert('Rate limit exceeded. Please try again later.');
    }
    return Promise.reject(error);
  }
);

// Function to check if we're online
export const isOnline = () => navigator.onLine;

// Function to handle offline queuing of requests
class OfflineRequestQueue {
  private queue: Array<{
    method: string;
    url: string;
    data?: any;
    headers?: any;
  }> = [];

  addRequest(method: string, url: string, data?: any, headers?: any) {
    this.queue.push({ method, url, data, headers });
  }

  getQueue() {
    return [...this.queue];
  }

  clearQueue() {
    this.queue = [];
  }

  async processQueue() {
    if (!isOnline()) {
      return false;
    }

    for (const request of this.queue) {
      try {
        await apiClient({
          method: request.method,
          url: request.url,
          data: request.data,
          headers: request.headers
        });
      } catch (error) {
        console.error('Failed to process queued request:', error);
        // Could implement retry logic here
      }
    }

    this.clearQueue();
    return true;
  }
}

const requestQueue = new OfflineRequestQueue();

// Add event listeners for online/offline events
if (typeof window !== 'undefined') {
  window.addEventListener('online', () => {
    console.log('Back online, processing queued requests...');
    requestQueue.processQueue();
  });

  window.addEventListener('offline', () => {
    console.log('Offline detected');
  });
}

export default apiClient;

// Export specific API functions
export const authService = {
  login: (email: string, password: string) =>
    apiClient.post('/auth/login', { email, password }),

  register: (email: string, password: string) =>
    apiClient.post('/auth/register', { email, password }),

  getCurrentUser: () =>
    apiClient.get('/auth/me'),

  logout: () => {
    localStorage.removeItem('access_token');
    return Promise.resolve();
  }
};

export const todoService = {
  getAll: () =>
    apiClient.get('/todos/'),

  getAdvanced: (params?: { priority?: string; tag?: string; due_date_from?: string; due_date_to?: string; sort_by?: string; status?: string }) =>
    apiClient.get('/todos/advanced', { params }),

  getById: (id: string) =>
    apiClient.get(`/todos/${id}`),

  create: (data: { title: string; description?: string; priority?: string; dueDate?: string; tags?: string[]; recurrenceRule?: string }) =>
    apiClient.post('/todos/advanced', data),

  update: (id: string, data: { title?: string; description?: string; completed?: boolean; priority?: string; dueDate?: string; recurrenceRule?: string; tags?: string[] }) =>
    apiClient.put(`/todos/${id}`, data),

  delete: (id: string) =>
    apiClient.delete(`/todos/${id}`),

  toggleComplete: (id: string, completed: boolean) =>
    apiClient.patch(`/todos/${id}/toggle`, { completed })
};

export const profileService = {
  getProfile: () =>
    apiClient.get('/profiles/me'),

  updateProfile: (data: any) =>
    apiClient.put('/profiles/me', data)
};