export interface User {
  id: number
  username: string
  email?: string
  kommo_integration_key?: string
  profile?: UserProfile
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

export interface UserProfile {
  first_name?: string
  last_name?: string
  xelence_x_api_key?: string
  xelence_affiliateid?: string
  chat_rate?: number
  kommo_widget_installed?: boolean
  // AI settings
  response_delay_seconds?: number
  ai_provider?: string
  // User customization
  custom_logo_url?: string
  custom_favicon_url?: string
  custom_website_name?: string
}

export interface UserProfileUpdate extends UserProfile {
  new_password?: string
  confirm_password?: string
}
