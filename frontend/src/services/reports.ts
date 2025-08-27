import { apiService } from './api'

export interface ReportData {
  id: number
  title: string
  content: string
  created_at: string
  updated_at: string
}

export interface DashboardStats {
  total_chats: number
  total_sessions: number
  total_messages: number
  active_users: number
  recent_activity: any[]
}

export class ReportsService {
  async getReports(): Promise<ReportData[]> {
    return await apiService.get('/reports')
  }

  async getDashboardStats(): Promise<DashboardStats> {
    return await apiService.get('/dashboard-stats')
  }
}

export const reportsService = new ReportsService()

