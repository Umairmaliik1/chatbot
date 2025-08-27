export interface User {
  id: number
  username: string
  email: string
  is_active: boolean
  created_at: string
  updated_at: string
  kommo_integration_key?: string
  kommo_widget_installed?: boolean
}

export interface LoginCredentials {
  username: string
  password: string
  remember_me?: boolean
}

export interface SignupData {
  username: string
  password: string
  confirm_password: string
}

export interface ChangePasswordData {
  current_password: string
  new_password: string
  confirm_password: string
}
