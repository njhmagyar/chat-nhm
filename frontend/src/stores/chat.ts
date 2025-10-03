import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { ChatSession, ChatMessage, SendMessageRequest } from '@/types'
import { chatApi } from '@/utils/api'

export const useChatStore = defineStore('chat', () => {
  const currentSession = ref<ChatSession | null>(null)
  const sessions = ref<ChatSession[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const suggestedQuestions = ref<string[]>([])

  const messages = computed(() => currentSession.value?.messages || [])
  const isTyping = ref(false)

  // Create a new chat session
  async function createSession() {
    try {
      isLoading.value = true
      error.value = null
      
      const session = await chatApi.createSession()
      currentSession.value = session
      sessions.value.unshift(session)
      
      return session
    } catch (err) {
      error.value = 'Failed to create chat session'
      console.error('Error creating session:', err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  // Load an existing session
  async function loadSession(sessionId: string) {
    try {
      isLoading.value = true
      error.value = null
      
      const session = await chatApi.getSession(sessionId)
      currentSession.value = session
      
      return session
    } catch (err) {
      error.value = 'Failed to load chat session'
      console.error('Error loading session:', err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  // Send a message
  async function sendMessage(message: string) {
    if (!currentSession.value) {
      throw new Error('No active session')
    }

    try {
      isTyping.value = true
      error.value = null

      const request: SendMessageRequest = {
        message,
        session_id: currentSession.value.id
      }

      const response = await chatApi.sendMessage(currentSession.value.id, request)
      
      // Update current session with new messages
      if (!currentSession.value.messages) {
        currentSession.value.messages = []
      }
      currentSession.value.messages.push(response.user_message)
      currentSession.value.messages.push(response.assistant_message)
      
      // Update session metadata
      currentSession.value.total_messages = response.session_updated.total_messages
      currentSession.value.updated_at = response.session_updated.updated_at

      return response.assistant_message
    } catch (err) {
      error.value = 'Failed to send message'
      console.error('Error sending message:', err)
      throw err
    } finally {
      isTyping.value = false
    }
  }

  // Rate the current session
  async function rateSession(rating: number) {
    if (!currentSession.value) {
      throw new Error('No active session')
    }

    try {
      await chatApi.rateSession(currentSession.value.id, rating)
    } catch (err) {
      console.error('Error rating session:', err)
      throw err
    }
  }

  // Load suggested questions
  async function loadSuggestedQuestions() {
    try {
      const response = await chatApi.getSuggestedQuestions()
      suggestedQuestions.value = response.questions
    } catch (err) {
      console.error('Error loading suggested questions:', err)
    }
  }

  // Load recent sessions
  async function loadRecentSessions() {
    try {
      const recentSessions = await chatApi.getActiveSessions()
      sessions.value = recentSessions
    } catch (err) {
      console.error('Error loading recent sessions:', err)
    }
  }

  // Clear current session
  function clearSession() {
    currentSession.value = null
    error.value = null
  }

  // Clear error
  function clearError() {
    error.value = null
  }

  return {
    // State
    currentSession,
    sessions,
    messages,
    isLoading,
    isTyping,
    error,
    suggestedQuestions,

    // Actions
    createSession,
    loadSession,
    sendMessage,
    rateSession,
    loadSuggestedQuestions,
    loadRecentSessions,
    clearSession,
    clearError,
  }
})