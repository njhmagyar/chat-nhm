<template>
  <div v-if="questions.length > 0" class="mb-6">
    <h3 class="text-lg font-semibold text-gray-900 mb-4">Ask me about:</h3>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
      <button
        v-for="question in questions"
        :key="question"
        @click="$emit('questionSelected', question)"
        class="text-left p-4 bg-white border border-gray-200 rounded-lg hover:border-primary-300 hover:bg-primary-50 transition-colors duration-200 group"
      >
        <div class="flex items-start justify-between">
          <span class="text-gray-700 group-hover:text-primary-700 transition-colors">
            {{ question }}
          </span>
          <svg 
            class="w-4 h-4 text-gray-400 group-hover:text-primary-500 transition-colors mt-1 ml-2 flex-shrink-0" 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
          </svg>
        </div>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  questions: string[]
}

defineProps<Props>()

defineEmits<{
  questionSelected: [question: string]
}>()
</script>