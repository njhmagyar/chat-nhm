import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Project, Skill, Experience, PersonalInfo, Testimonial } from '@/types'
import { contentApi } from '@/utils/api'

export const useContentStore = defineStore('content', () => {
  const projects = ref<Project[]>([])
  const featuredProjects = ref<Project[]>([])
  const skills = ref<Skill[]>([])
  const skillsByCategory = ref<Record<string, { label: string; skills: Skill[] }>>({})
  const experiences = ref<Experience[]>([])
  const personalInfo = ref<PersonalInfo | null>(null)
  const testimonials = ref<Testimonial[]>([])
  const featuredTestimonials = ref<Testimonial[]>([])
  
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Load all content
  async function loadAllContent() {
    try {
      isLoading.value = true
      error.value = null

      const [
        projectsRes,
        featuredProjectsRes,
        skillsRes,
        skillsByCategoryRes,
        experiencesRes,
        personalInfoRes,
        testimonialsRes,
        featuredTestimonialsRes
      ] = await Promise.allSettled([
        contentApi.getProjects(),
        contentApi.getFeaturedProjects(),
        contentApi.getSkills(),
        contentApi.getSkillsByCategory(),
        contentApi.getExperiences(),
        contentApi.getPersonalInfo(),
        contentApi.getTestimonials(),
        contentApi.getFeaturedTestimonials()
      ])

      if (projectsRes.status === 'fulfilled') {
        projects.value = projectsRes.value.results
      }

      if (featuredProjectsRes.status === 'fulfilled') {
        featuredProjects.value = featuredProjectsRes.value
      }

      if (skillsRes.status === 'fulfilled') {
        skills.value = skillsRes.value
      }

      if (skillsByCategoryRes.status === 'fulfilled') {
        skillsByCategory.value = skillsByCategoryRes.value
      }

      if (experiencesRes.status === 'fulfilled') {
        experiences.value = experiencesRes.value
      }

      if (personalInfoRes.status === 'fulfilled') {
        personalInfo.value = personalInfoRes.value
      }

      if (testimonialsRes.status === 'fulfilled') {
        testimonials.value = testimonialsRes.value
      }

      if (featuredTestimonialsRes.status === 'fulfilled') {
        featuredTestimonials.value = featuredTestimonialsRes.value
      }

    } catch (err) {
      error.value = 'Failed to load content'
      console.error('Error loading content:', err)
    } finally {
      isLoading.value = false
    }
  }

  // Load projects
  async function loadProjects() {
    try {
      const response = await contentApi.getProjects()
      projects.value = response.results
    } catch (err) {
      console.error('Error loading projects:', err)
    }
  }

  // Load featured projects
  async function loadFeaturedProjects() {
    try {
      featuredProjects.value = await contentApi.getFeaturedProjects()
    } catch (err) {
      console.error('Error loading featured projects:', err)
    }
  }

  // Get project by ID
  function getProjectById(id: string): Project | undefined {
    return projects.value.find(project => project.id === id)
  }

  // Load skills
  async function loadSkills() {
    try {
      skills.value = await contentApi.getSkills()
    } catch (err) {
      console.error('Error loading skills:', err)
    }
  }

  // Load skills by category
  async function loadSkillsByCategory() {
    try {
      skillsByCategory.value = await contentApi.getSkillsByCategory()
    } catch (err) {
      console.error('Error loading skills by category:', err)
    }
  }

  // Load experiences
  async function loadExperiences() {
    try {
      experiences.value = await contentApi.getExperiences()
    } catch (err) {
      console.error('Error loading experiences:', err)
    }
  }

  // Load personal info
  async function loadPersonalInfo() {
    try {
      personalInfo.value = await contentApi.getPersonalInfo()
    } catch (err) {
      console.error('Error loading personal info:', err)
    }
  }

  // Load testimonials
  async function loadTestimonials() {
    try {
      testimonials.value = await contentApi.getTestimonials()
    } catch (err) {
      console.error('Error loading testimonials:', err)
    }
  }

  // Load featured testimonials
  async function loadFeaturedTestimonials() {
    try {
      featuredTestimonials.value = await contentApi.getFeaturedTestimonials()
    } catch (err) {
      console.error('Error loading featured testimonials:', err)
    }
  }

  // Clear error
  function clearError() {
    error.value = null
  }

  return {
    // State
    projects,
    featuredProjects,
    skills,
    skillsByCategory,
    experiences,
    personalInfo,
    testimonials,
    featuredTestimonials,
    isLoading,
    error,

    // Actions
    loadAllContent,
    loadProjects,
    loadFeaturedProjects,
    getProjectById,
    loadSkills,
    loadSkillsByCategory,
    loadExperiences,
    loadPersonalInfo,
    loadTestimonials,
    loadFeaturedTestimonials,
    clearError,
  }
})