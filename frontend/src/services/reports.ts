import { apiService } from './api'

export interface ReportData {
  date: string
  sessions: number
  sessions_growth: number
  messages: number
  messages_growth: number
  avg_response_time: number
  response_time_trend: number
  satisfaction: number
}

export interface RecentSession {
  id: number
  title: string
  username: string
  created_at: string
}

export interface DashboardStats {
  total_users: number
  sessions_in_period: number
  messages_in_period: number
  knowledge_files_count: number
  active_users_in_period: number
  period_from: string
  period_to: string
  chart_labels: string[]
  daily_sessions: number[]
  daily_messages: number[]
  knowledge_file_type_labels: string[]
  knowledge_file_type_counts: number[]
  recent_sessions: RecentSession[]
}

export class ReportsService {
  async getReports(days?: number): Promise<ReportData[]> {
    return await apiService.get('/reports', days ? { days } : undefined)
  }

  async getDashboardStats(days?: number): Promise<DashboardStats> {
    return await apiService.get('/dashboard-stats', days ? { days } : undefined)
  }
}

export const reportsService = new ReportsService()

