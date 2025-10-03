<template>
  <div class="chat-message assistant-message">
    <div class="typing-indicator">
      <div 
        v-for="i in 3" 
        :key="i"
        class="typing-dot"
        :style="{ '--delay': i - 1 }"
      />
    </div>
    <span class="ml-3 text-gray-500 text-sm">Thinking...</span>
  </div>
</template>

<script setup lang="ts">
// No props needed for this component
</script>