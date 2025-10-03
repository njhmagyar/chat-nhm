import axios from 'axios'
import type { 
  ChatSession, 
  SendMessageRequest, 
  SendMessageResponse,
  Project,
  Skill,
  Experience,
  PersonalInfo,
  Testimonial 
} from '@/types'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Chat API
export const chatApi = {
  createSession: (): Promise<ChatSession> =>
    api.post('/chat/sessions/').then(res => res.data),
  
  getSession: (sessionId: string): Promise<ChatSession> =>
    api.get(`/chat/sessions/${sessionId}/`).then(res => res.data),
  
  sendMessage: (sessionId: string, data: SendMessageRequest): Promise<SendMessageResponse> =>
    api.post(`/chat/sessions/${sessionId}/send_message/`, data).then(res => res.data),
  
  rateSession: (sessionId: string, rating: number): Promise<void> =>
    api.post(`/chat/sessions/${sessionId}/rate_session/`, { rating }),
  
  getActiveSessions: (): Promise<ChatSession[]> =>
    api.get('/chat/sessions/active_sessions/').then(res => res.data),
  
  getSuggestedQuestions: (): Promise<{ questions: string[] }> =>
    api.get('/rag/suggested-questions/').then(res => res.data),
}

// Content API
export const contentApi = {
  getProjects: (params?: any): Promise<{ results: Project[] }> =>
    api.get('/content/projects/', { params }).then(res => res.data),
  
  getProject: (id: string): Promise<Project> =>
    api.get(`/content/projects/${id}/`).then(res => res.data),
  
  getFeaturedProjects: (): Promise<Project[]> =>
    api.get('/content/projects/featured/').then(res => res.data),
  
  getSkills: (): Promise<Skill[]> =>
    api.get('/content/skills/').then(res => res.data.results || res.data),
  
  getSkillsByCategory: (): Promise<Record<string, { label: string; skills: Skill[] }>> =>
    api.get('/content/skills/by_category/').then(res => res.data),
  
  getExperiences: (): Promise<Experience[]> =>
    api.get('/content/experience/').then(res => res.data.results || res.data),
  
  getPersonalInfo: (): Promise<PersonalInfo> =>
    api.get('/content/profile/profile/').then(res => res.data),
  
  getTestimonials: (): Promise<Testimonial[]> =>
    api.get('/content/testimonials/').then(res => res.data.results || res.data),
  
  getFeaturedTestimonials: (): Promise<Testimonial[]> =>
    api.get('/content/testimonials/featured/').then(res => res.data),
}

export default api