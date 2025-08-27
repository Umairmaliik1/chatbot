// frontend/src/services/kommo.ts
import { apiService } from './api'

export interface IntegrationStatus {
  active: boolean
  kommo_domain?: string
  last_sync?: string
  integration_key?: string
  webhook_url?: string
  created_at?: string
  updated_at?: string
  message?: string
}

export class KommoService {
  getStatus(): Promise<IntegrationStatus> {
    return apiService.kommoGet('/status')
  }

  configure(payload: {
    api_key?: string // your long-lived access token or access_token
    access_token?: string
    refresh_token?: string
    webhook_secret?: string
    subdomain: string // "theaiexpert735.kommo.com" OR "theaiexpert735"
  }): Promise<any> {
    return apiService.kommoPost('/configure', payload)
  }

  getIntegrationKey(): Promise<{ integration_key: string, webhook_url: string }> {
    return apiService.kommoGet('/integration/key')
  }

  rotateIntegrationKey(): Promise<{ integration_key: string, webhook_url: string }> {
    return apiService.kommoPost('/integration/key/rotate', {})
  }

  testConnection(): Promise<any> {
    return apiService.kommoPost('/integration/test', {})
  }
}

export const kommoService = new KommoService()
