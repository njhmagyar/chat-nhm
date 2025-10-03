<template>
  <div 
    class="chat-message animate-slide-up"
    :class="{
      'user-message': message.message_type === 'user',
      'assistant-message': message.message_type === 'assistant'
    }"
  >
    <!-- Message Content -->
    <div class="message-content">
      <div 
        v-if="message.message_type === 'assistant' && message.response_type !== 'error'"
        class="markdown-content"
        v-html="formattedContent"
      />
      <div v-else class="whitespace-pre-wrap">
        {{ message.content }}
      </div>
    </div>

    <!-- Media Gallery for Project Showcases -->
    <MediaGallery 
      v-if="message.media_urls && message.media_urls.length > 0"
      :mediaUrls="message.media_urls"
      :projects="referencedProjects"
    />

    <!-- Project Cards -->
    <div 
      v-if="referencedProjects.length > 0 && message.response_type === 'project_showcase'"
      class="mt-4 space-y-4"
    >
      <ProjectCard 
        v-for="project in referencedProjects.slice(0, 3)"
        :key="project.id"
        :project="project"
      />
    </div>

    <!-- Skills Summary -->
    <SkillsSummary 
      v-if="referencedSkills.length > 0 && message.response_type === 'skill_summary'"
      :skills="referencedSkills"
    />

    <!-- Experience Timeline -->
    <ExperienceTimeline 
      v-if="referencedExperiences.length > 0 && message.response_type === 'experience_timeline'"
      :experiences="referencedExperiences"
    />

    <!-- Message Metadata -->
    <div 
      v-if="message.message_type === 'assistant'"
      class="mt-3 flex items-center justify-between text-xs text-gray-400"
    >
      <div>
        <span v-if="message.confidence_score">
          Confidence: {{ Math.round(message.confidence_score * 100) }}%
        </span>
        <span v-if="message.response_time_ms" class="ml-2">
          {{ message.response_time_ms }}ms
        </span>
      </div>
      <div>
        {{ formatTime(message.created_at) }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { marked } from 'marked'
import type { ChatMessage, Project, Skill, Experience } from '@/types'
import { useContentStore } from '@/stores/content'
import MediaGallery from './MediaGallery.vue'
import ProjectCard from './ProjectCard.vue'
import SkillsSummary from './SkillsSummary.vue'
import ExperienceTimeline from './ExperienceTimeline.vue'

interface Props {
  message: ChatMessage
}

const props = defineProps<Props>()
const contentStore = useContentStore()

const formattedContent = computed(() => {
  if (props.message.message_type === 'assistant') {
    return marked(props.message.content)
  }
  return props.message.content
})

const referencedProjects = computed((): Project[] => {
  if (!props.message.referenced_projects) return []
  
  return props.message.referenced_projects
    .map(id => contentStore.getProjectById(id))
    .filter((project): project is Project => project !== undefined)
})

const referencedSkills = computed((): Skill[] => {
  if (!props.message.referenced_skills) return []
  
  return props.message.referenced_skills
    .map(id => contentStore.skills.find(skill => skill.id === id))
    .filter((skill): skill is Skill => skill !== undefined)
})

const referencedExperiences = computed((): Experience[] => {
  if (!props.message.referenced_experiences) return []
  
  return props.message.referenced_experiences
    .map(id => contentStore.experiences.find(exp => exp.id === id))
    .filter((experience): experience is Experience => experience !== undefined)
})

const formatTime = (dateString: string): string => {
  const date = new Date(dateString)
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}
</script>