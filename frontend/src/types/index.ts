export interface ChatMessage {
  id: string
  message_type: 'user' | 'assistant' | 'system'
  content: string
  response_type?: 'text' | 'text_with_media' | 'project_showcase' | 'skill_summary' | 'experience_timeline' | 'error'
  referenced_projects?: string[]
  referenced_skills?: number[]
  referenced_experiences?: number[]
  media_urls?: string[]
  confidence_score?: number
  created_at: string
  response_time_ms?: number
}

export interface ChatSession {
  id: string
  session_name?: string
  created_at: string
  updated_at: string
  total_messages: number
  is_active: boolean
  messages?: ChatMessage[]
  message_count?: number
}

export interface Project {
  id: string
  title: string
  slug: string
  description: string
  detailed_case_study?: string
  category: string
  tags: string[]
  featured_image?: string
  gallery_images?: string[]
  video_url?: string
  prototype_url?: string
  live_url?: string
  github_url?: string
  client?: string
  role: string
  duration: string
  team_size: number
  problem_statement?: string
  solution_overview?: string
  key_achievements?: string[]
  technologies_used?: string[]
  featured: boolean
  published: boolean
  created_at: string
  updated_at: string
}

export interface Skill {
  id: number
  name: string
  category: string
  proficiency: string
  years_of_experience: number
  description?: string
  projects_count?: number
}

export interface Experience {
  id: number
  title: string
  organization: string
  location?: string
  experience_type: string
  start_date: string
  end_date?: string
  current: boolean
  description: string
  key_achievements?: string[]
  skills_gained?: Skill[]
}

export interface PersonalInfo {
  name: string
  title: string
  bio: string
  location: string
  email: string
  linkedin_url?: string
  github_url?: string
  portfolio_url?: string
  behance_url?: string
  dribbble_url?: string
  years_of_experience: number
  availability_status: string
  fun_facts?: string[]
  design_philosophy?: string
  career_goals?: string
}

export interface Testimonial {
  id: number
  author_name: string
  author_title: string
  author_company?: string
  author_image?: string
  content: string
  rating: number
  project?: Project
  created_at: string
}

export interface SendMessageRequest {
  message: string
  session_id?: string
}

export interface SendMessageResponse {
  user_message: ChatMessage
  assistant_message: ChatMessage
  session_updated: ChatSession
}