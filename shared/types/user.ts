export interface User {
  id: string;
  email: string;
  created_at: string;
  updated_at: string;
  is_active?: boolean;
}

export interface UserRegistration {
  email: string;
  password: string;
}

export interface UserLogin {
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}