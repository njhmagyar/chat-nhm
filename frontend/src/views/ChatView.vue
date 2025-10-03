<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <!-- Header -->
    <header class="bg-white border-b border-gray-200 px-4 py-4">
      <div class="max-w-4xl mx-auto flex items-center justify-between">
        <div>
          <h1 class="text-xl font-semibold text-gray-900">
            {{ personalInfo?.name || 'Portfolio Chat' }}
          </h1>
          <p class="text-sm text-gray-600">
            {{ personalInfo?.title || 'Ask me about my work and experience' }}
          </p>
        </div>
        
        <!-- Session actions -->
        <div class="flex items-center gap-3">
          <button
            v-if="currentSession"
            @click="startNewSession"
            class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
          >
            New Chat
          </button>
          
          <div v-if="currentSession" class="text-sm text-gray-500">
            {{ chatStore.messages.length }} messages
          </div>
        </div>
      </div>
    </header>

    <!-- Main Chat Area -->
    <div class="flex-1 flex flex-col max-w-4xl mx-auto w-full">
      <!-- Welcome Section (shown when no messages) -->
      <div 
        v-if="chatStore.messages.length <= 1"
        class="flex-1 flex flex-col justify-center px-4 py-8"
      >
        <div class="text-center mb-8">
          <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-3.582 8-8 8a8.955 8.955 0 01-4.126-.98L3 20l1.98-5.874A8.955 8.955 0 013 12c0-4.418 3.582-8 8-8s8 3.582 8 8z"/>
            </svg>
          </div>
          <h2 class="text-2xl font-bold text-gray-900 mb-2">
            Hi! I'm here to help you explore my work
          </h2>
          <p class="text-gray-600 max-w-lg mx-auto">
            Ask me anything about my design projects, skills, experience, or process. 
            I'll provide detailed answers with examples from my portfolio.
          </p>
        </div>

        <!-- Suggested Questions -->
        <SuggestedQuestions 
          :questions="chatStore.suggestedQuestions" 
          @question-selected="handleQuestionSelected"
        />

        <!-- Quick stats if personal info is available -->
        <div 
          v-if="personalInfo"
          class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-8"
        >
          <div class="bg-white rounded-lg p-4 text-center border">
            <div class="text-2xl font-bold text-primary-600">{{ personalInfo.years_of_experience }}+</div>
            <div class="text-sm text-gray-600">Years Experience</div>
          </div>
          <div class="bg-white rounded-lg p-4 text-center border">
            <div class="text-2xl font-bold text-primary-600">{{ featuredProjects.length }}</div>
            <div class="text-sm text-gray-600">Featured Projects</div>
          </div>
          <div class="bg-white rounded-lg p-4 text-center border">
            <div class="text-2xl font-bold text-primary-600">{{ personalInfo.availability_status.includes('Open') ? '✓' : '○' }}</div>
            <div class="text-sm text-gray-600">{{ personalInfo.availability_status }}</div>
          </div>
        </div>
      </div>

      <!-- Messages Area -->
      <div 
        v-else
        ref="messagesContainer"
        class="flex-1 overflow-y-auto chat-container px-4 py-6"
      >
        <div class="space-y-4">
          <ChatMessage 
            v-for="message in chatStore.messages" 
            :key="message.id"
            :message="message"
          />
          
          <TypingIndicator v-if="isTyping" />
        </div>
      </div>

      <!-- Input Area -->
      <div class="border-t border-gray-200 bg-white px-4 py-4">
        <div class="flex items-end gap-3">
          <div class="flex-1">
            <textarea
              v-model="currentMessage"
              @keydown.enter.exact.prevent="sendMessage"
              @keydown.enter.shift.exact="currentMessage += '\n'"
              placeholder="Ask me about my projects, skills, or experience..."
              rows="1"
              class="w-full resize-none border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              :disabled="isLoading || isTyping"
            />
            <div class="text-xs text-gray-500 mt-1">
              Press Enter to send, Shift+Enter for new line
            </div>
          </div>
          
          <button
            @click="sendMessage"
            :disabled="!currentMessage.trim() || isLoading || isTyping"
            class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <svg 
              v-if="isLoading || isTyping"
              class="w-5 h-5 animate-spin" 
              fill="none" 
              viewBox="0 0 24 24"
            >
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
            </svg>
            <svg 
              v-else
              class="w-5 h-5" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Error Message -->
    <div 
      v-if="error"
      class="fixed bottom-4 right-4 bg-red-100 border border-red-300 text-red-700 px-4 py-3 rounded-lg shadow-lg"
    >
      <div class="flex items-center justify-between">
        <span>{{ error }}</span>
        <button 
          @click="clearError"
          class="ml-4 text-red-500 hover:text-red-700"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useChatStore } from '@/stores/chat'
import { useContentStore } from '@/stores/content'
import ChatMessage from '@/components/ChatMessage.vue'
import TypingIndicator from '@/components/TypingIndicator.vue'
import SuggestedQuestions from '@/components/SuggestedQuestions.vue'

interface Props {
  sessionId?: string
}

const props = defineProps<Props>()

const route = useRoute()
const router = useRouter()
const chatStore = useChatStore()
const contentStore = useContentStore()

const currentMessage = ref('')
const messagesContainer = ref<HTMLElement>()

// Computed properties
const {
  currentSession,
  isLoading,
  isTyping,
  error,
} = chatStore

const { personalInfo, featuredProjects } = contentStore

// Scroll to bottom when new messages arrive
const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// Watch for new messages to auto-scroll
watch(chatStore.messages, scrollToBottom, { deep: true })
watch(isTyping, scrollToBottom)

// Initialize chat
onMounted(async () => {
  await contentStore.loadAllContent()
  await chatStore.loadSuggestedQuestions()
  
  const sessionId = props.sessionId || route.params.sessionId
  
  if (sessionId && typeof sessionId === 'string') {
    try {
      await chatStore.loadSession(sessionId)
    } catch (err) {
      console.error('Failed to load session:', err)
      // Redirect to new chat if session doesn't exist
      router.push('/')
    }
  } else {
    // Create new session
    try {
      const newSession = await chatStore.createSession()
      router.push(`/session/${newSession.id}`)
    } catch (err) {
      console.error('Failed to create session:', err)
    }
  }
})

// Send message
const sendMessage = async () => {
  const message = currentMessage.value.trim()
  if (!message || isLoading.value || isTyping.value) return
  
  currentMessage.value = ''
  
  try {
    await chatStore.sendMessage(message)
    scrollToBottom()
  } catch (err) {
    console.error('Failed to send message:', err)
  }
}

// Handle suggested question selection
const handleQuestionSelected = async (question: string) => {
  currentMessage.value = question
  await sendMessage()
}

// Start new session
const startNewSession = async () => {
  try {
    const newSession = await chatStore.createSession()
    router.push(`/session/${newSession.id}`)
  } catch (err) {
    console.error('Failed to create new session:', err)
  }
}

// Clear error
const clearError = () => {
  chatStore.clearError()
}
</script>