import { apiService } from './api'

export interface Instruction {
  id?: number
  instructions: string
  created_at?: string
  updated_at?: string
}

export interface FAQ {
  id?: number
  question: string
  answer: string
  priority?: number
  created_at?: string
  updated_at?: string
}

export class InstructionsService {
  // Instructions
  async getInstructions(): Promise<Instruction> {
    return await apiService.get('/instructions')
  }

  async updateInstructions(instructions: string): Promise<Instruction> {
    return await apiService.post('/instructions', { instructions })
  }

  async parseInstructionsFile(file: File): Promise<{ instructions: string }> {
    const formData = new FormData()
    formData.append('file', file)
    return await apiService.upload('/parse-instructions-file', formData)
  }

  // FAQs
  async getFAQs(): Promise<FAQ[]> {
    return await apiService.get('/faqs')
  }

  async createFAQ(question: string, answer: string, priority?: number): Promise<FAQ> {
    return await apiService.post('/faqs', { question, answer, priority })
  }

  async updateFAQ(
    id: number,
    question: string,
    answer: string,
    priority?: number
  ): Promise<FAQ> {
    return await apiService.put(`/faqs/${id}`, { question, answer, priority })
  }

  async deleteFAQ(id: number): Promise<void> {
    return await apiService.delete(`/faqs/${id}`)
  }

  async parseFAQFile(file: File): Promise<{ faqs: FAQ[] }> {
    const formData = new FormData()
    formData.append('file', file)
    return await apiService.upload('/parse-faq-file', formData)
  }
}

export const instructionsService = new InstructionsService()

