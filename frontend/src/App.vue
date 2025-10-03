<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <router-view />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useContentStore } from '@/stores/content'

const contentStore = useContentStore()

onMounted(() => {
  // Load basic content on app startup
  contentStore.loadPersonalInfo()
  contentStore.loadFeaturedProjects()
})
</script>