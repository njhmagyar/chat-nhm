<template>
  <div class="mt-4 bg-gray-50 rounded-lg p-4">
    <h4 class="text-sm font-semibold text-gray-700 mb-3">Related Skills</h4>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
      <div 
        v-for="skill in skills"
        :key="skill.id"
        class="flex items-center justify-between bg-white rounded-lg p-3 border"
      >
        <div>
          <div class="font-medium text-gray-900">{{ skill.name }}</div>
          <div class="text-sm text-gray-500">{{ formatCategory(skill.category) }}</div>
        </div>
        <div class="text-right">
          <div class="text-sm font-medium" :class="getProficiencyColor(skill.proficiency)">
            {{ formatProficiency(skill.proficiency) }}
          </div>
          <div class="text-xs text-gray-500">
            {{ skill.years_of_experience }}{{ skill.years_of_experience === 1 ? ' year' : ' years' }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Skill } from '@/types'

interface Props {
  skills: Skill[]
}

defineProps<Props>()

const formatCategory = (category: string): string => {
  const categoryMap: Record<string, string> = {
    'design': 'Design Tools',
    'research': 'Research Methods',
    'technical': 'Technical Skills',
    'soft': 'Soft Skills',
    'process': 'Process & Methods'
  }
  return categoryMap[category] || category
}

const formatProficiency = (proficiency: string): string => {
  const proficiencyMap: Record<string, string> = {
    'beginner': 'Beginner',
    'intermediate': 'Intermediate',
    'advanced': 'Advanced',
    'expert': 'Expert'
  }
  return proficiencyMap[proficiency] || proficiency
}

const getProficiencyColor = (proficiency: string): string => {
  const colorMap: Record<string, string> = {
    'beginner': 'text-yellow-600',
    'intermediate': 'text-blue-600',
    'advanced': 'text-green-600',
    'expert': 'text-purple-600'
  }
  return colorMap[proficiency] || 'text-gray-600'
}
</script>