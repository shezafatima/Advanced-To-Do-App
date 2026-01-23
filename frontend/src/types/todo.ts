// Define the priority enum
export type Priority = 'low' | 'medium' | 'high';

// Define the role enum for task sharing
export type Role = 'owner' | 'editor' | 'viewer';

// Define the tag type
export interface Tag {
  id: string;
  name: string;
  color: string;
  createdAt: string;
}

// Define the basic todo type
export interface Todo {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  userId: string;
  createdAt: string;
  updatedAt: string;
}

// Define the advanced todo type with all new features
export interface AdvancedTodo extends Todo {
  priority: Priority;
  dueDate?: string; // ISO date string
  recurrenceRule?: string; // RFC 5545 format
  tags: Tag[];
  shares?: TaskShare[]; // Array of task shares
}

// Define the task share type
export interface TaskShare {
  id: string;
  taskId: string;
  userId: string;
  role: Role;
  sharedAt: string;
  permissions: {
    read: boolean;
    write: boolean;
    delete: boolean;
    manageAccess: boolean;
  };
}

// Define the user profile type
export interface UserProfile {
  id: string;
  userId: string;
  displayName: string;
  preferredLanguage: string; // e.g., 'en', 'ur'
  themePreference?: string; // e.g., 'dark', 'light'
  notificationPreferences: {
    toastNotifications: boolean;
    emailReminders: boolean;
  };
  avatar?: string; // base64 encoded image data
  createdAt: string;
  updatedAt: string;
}

// Define request/response types for API calls
export interface CreateTodoRequest {
  title: string;
  description?: string;
  priority?: Priority;
  dueDate?: string;
  recurrenceRule?: string;
  tags?: string[]; // Array of tag names to create/associate
}

export interface UpdateTodoRequest {
  title?: string;
  description?: string;
  completed?: boolean;
  priority?: Priority;
  dueDate?: string;
  recurrenceRule?: string;
}

export interface ShareTaskRequest {
  userEmail: string;
  role: Role;
}

export interface UpdateProfileRequest {
  displayName?: string;
  preferredLanguage?: string;
  themePreference?: string;
  notificationPreferences?: {
    toastNotifications: boolean;
    emailReminders: boolean;
  };
  avatar?: string;
}