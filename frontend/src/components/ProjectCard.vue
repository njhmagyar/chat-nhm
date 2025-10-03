<template>
  <div class="project-card">
    <div v-if="project.featured_image" class="aspect-video overflow-hidden">
      <img 
        :src="project.featured_image"
        :alt="project.title"
        class="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
      />
    </div>
    
    <div class="p-6">
      <div class="flex items-start justify-between mb-3">
        <h3 class="text-lg font-semibold text-gray-900 line-clamp-2">
          {{ project.title }}
        </h3>
        <span class="ml-2 px-2 py-1 bg-primary-100 text-primary-700 text-xs rounded-full whitespace-nowrap">
          {{ formatCategory(project.category) }}
        </span>
      </div>
      
      <p class="text-gray-600 text-sm mb-4 line-clamp-3">
        {{ project.description }}
      </p>
      
      <div class="flex items-center justify-between text-sm text-gray-500 mb-4">
        <span>{{ project.role }}</span>
        <span v-if="project.client">{{ project.client }}</span>
      </div>
      
      <!-- Technologies -->
      <div v-if="project.technologies_used && project.technologies_used.length > 0" class="mb-4">
        <div class="flex flex-wrap gap-1">
          <span 
            v-for="tech in project.technologies_used.slice(0, 4)"
            :key="tech"
            class="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded"
          >
            {{ tech }}
          </span>
          <span 
            v-if="project.technologies_used.length > 4"
            class="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded"
          >
            +{{ project.technologies_used.length - 4 }}
          </span>
        </div>
      </div>
      
      <!-- Action Links -->
      <div class="flex items-center gap-3">
        <a 
          v-if="project.live_url"
          :href="project.live_url"
          target="_blank"
          rel="noopener noreferrer"
          class="text-primary-600 hover:text-primary-700 text-sm font-medium flex items-center gap-1"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
          </svg>
          Live Site
        </a>
        
        <a 
          v-if="project.prototype_url"
          :href="project.prototype_url"
          target="_blank"
          rel="noopener noreferrer"
          class="text-primary-600 hover:text-primary-700 text-sm font-medium flex items-center gap-1"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122"/>
          </svg>
          Prototype
        </a>
        
        <a 
          v-if="project.github_url"
          :href="project.github_url"
          target="_blank"
          rel="noopener noreferrer"
          class="text-gray-600 hover:text-gray-700 text-sm font-medium flex items-center gap-1"
        >
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
          </svg>
          Code
        </a>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Project } from '@/types'

interface Props {
  project: Project
}

defineProps<Props>()

const formatCategory = (category: string): string => {
  const categoryMap: Record<string, string> = {
    'web': 'Web Design',
    'mobile': 'Mobile App',
    'ux': 'UX Research',
    'branding': 'Branding',
    'prototype': 'Prototype',
    'other': 'Other'
  }
  return categoryMap[category] || category
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