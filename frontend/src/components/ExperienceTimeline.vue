<template>
  <div class="mt-4 bg-gray-50 rounded-lg p-4">
    <h4 class="text-sm font-semibold text-gray-700 mb-4">Related Experience</h4>
    <div class="space-y-4">
      <div 
        v-for="(experience, index) in experiences"
        :key="experience.id"
        class="relative flex items-start"
      >
        <!-- Timeline line -->
        <div 
          v-if="index < experiences.length - 1"
          class="absolute left-4 top-8 w-0.5 h-full bg-gray-300"
        />
        
        <!-- Timeline dot -->
        <div class="relative z-10 flex-shrink-0 w-8 h-8 bg-primary-500 rounded-full flex items-center justify-center">
          <div class="w-3 h-3 bg-white rounded-full" />
        </div>
        
        <!-- Content -->
        <div class="ml-4 flex-1 bg-white rounded-lg p-4 border">
          <div class="flex items-start justify-between mb-2">
            <div>
              <h5 class="font-semibold text-gray-900">{{ experience.title }}</h5>
              <p class="text-sm text-gray-600">{{ experience.organization }}</p>
            </div>
            <span class="text-xs text-gray-500 whitespace-nowrap ml-4">
              {{ formatDateRange(experience.start_date, experience.end_date, experience.current) }}
            </span>
          </div>
          
          <div class="text-sm text-gray-700 mb-3 line-clamp-3">
            {{ experience.description }}
          </div>
          
          <!-- Key achievements -->
          <div v-if="experience.key_achievements && experience.key_achievements.length > 0" class="mb-3">
            <h6 class="text-xs font-medium text-gray-500 uppercase tracking-wide mb-2">Key Achievements</h6>
            <ul class="space-y-1">
              <li 
                v-for="achievement in experience.key_achievements.slice(0, 3)"
                :key="achievement"
                class="text-sm text-gray-600 flex items-start"
              >
                <span class="text-primary-500 mr-2">•</span>
                <span class="line-clamp-2">{{ achievement }}</span>
              </li>
            </ul>
          </div>
          
          <!-- Skills gained -->
          <div v-if="experience.skills_gained && experience.skills_gained.length > 0">
            <h6 class="text-xs font-medium text-gray-500 uppercase tracking-wide mb-2">Skills</h6>
            <div class="flex flex-wrap gap-1">
              <span 
                v-for="skill in experience.skills_gained.slice(0, 5)"
                :key="skill.id"
                class="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded"
              >
                {{ skill.name }}
              </span>
              <span 
                v-if="experience.skills_gained.length > 5"
                class="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded"
              >
                +{{ experience.skills_gained.length - 5 }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Experience } from '@/types'

interface Props {
  experiences: Experience[]
}

defineProps<Props>()

const formatDateRange = (startDate: string, endDate: string | undefined, current: boolean): string => {
  const start = new Date(startDate).toLocaleDateString('en-US', { 
    month: 'short', 
    year: 'numeric' 
  })
  
  if (current) {
    return `${start} - Present`
  }
  
  if (endDate) {
    const end = new Date(endDate).toLocaleDateString('en-US', { 
      month: 'short', 
      year: 'numeric' 
    })
    return `${start} - ${end}`
  }
  
  return start
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>