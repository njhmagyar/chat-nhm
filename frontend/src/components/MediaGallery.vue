<template>
  <div v-if="mediaUrls.length > 0" class="media-gallery mt-4">
    <div 
      v-for="(url, index) in mediaUrls.slice(0, 6)"
      :key="index"
      class="relative group cursor-pointer"
      @click="openLightbox(index)"
    >
      <img 
        v-if="isImage(url)"
        :src="url"
        :alt="`Media ${index + 1}`"
        class="w-full h-40 object-cover rounded-lg hover:opacity-90 transition-opacity"
        loading="lazy"
      />
      
      <div 
        v-else-if="isVideo(url)"
        class="relative w-full h-40 bg-gray-100 rounded-lg overflow-hidden hover:opacity-90 transition-opacity"
      >
        <video 
          :src="url"
          class="w-full h-full object-cover"
          muted
          preload="metadata"
        />
        <div class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-30">
          <svg class="w-12 h-12 text-white" fill="currentColor" viewBox="0 0 20 20">
            <path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z"/>
          </svg>
        </div>
      </div>
      
      <div 
        v-else
        class="w-full h-40 bg-gray-100 rounded-lg flex items-center justify-center hover:opacity-90 transition-opacity"
      >
        <div class="text-center text-gray-500">
          <svg class="w-8 h-8 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>
          </svg>
          <span class="text-sm">View File</span>
        </div>
      </div>
      
      <!-- Overlay for additional items -->
      <div 
        v-if="index === 5 && mediaUrls.length > 6"
        class="absolute inset-0 bg-black bg-opacity-50 rounded-lg flex items-center justify-center text-white font-semibold"
      >
        +{{ mediaUrls.length - 6 }} more
      </div>
    </div>
  </div>

  <!-- Lightbox Modal -->
  <div 
    v-if="lightboxOpen"
    class="fixed inset-0 z-50 bg-black bg-opacity-90 flex items-center justify-center p-4"
    @click="closeLightbox"
  >
    <div class="relative max-w-4xl max-h-full">
      <button 
        @click="closeLightbox"
        class="absolute -top-10 right-0 text-white hover:text-gray-300 z-10"
      >
        <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
        </svg>
      </button>
      
      <img 
        v-if="currentMedia && isImage(currentMedia)"
        :src="currentMedia"
        alt="Lightbox image"
        class="max-w-full max-h-full object-contain"
      />
      
      <video 
        v-else-if="currentMedia && isVideo(currentMedia)"
        :src="currentMedia"
        controls
        class="max-w-full max-h-full"
      />
      
      <!-- Navigation arrows -->
      <button 
        v-if="mediaUrls.length > 1 && currentIndex > 0"
        @click.stop="previousMedia"
        class="absolute left-4 top-1/2 transform -translate-y-1/2 text-white hover:text-gray-300"
      >
        <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
        </svg>
      </button>
      
      <button 
        v-if="mediaUrls.length > 1 && currentIndex < mediaUrls.length - 1"
        @click.stop="nextMedia"
        class="absolute right-4 top-1/2 transform -translate-y-1/2 text-white hover:text-gray-300"
      >
        <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Project } from '@/types'

interface Props {
  mediaUrls: string[]
  projects?: Project[]
}

const props = defineProps<Props>()

const lightboxOpen = ref(false)
const currentIndex = ref(0)

const currentMedia = computed(() => {
  return props.mediaUrls[currentIndex.value]
})

const isImage = (url: string): boolean => {
  return /\.(jpg|jpeg|png|gif|webp|svg)$/i.test(url)
}

const isVideo = (url: string): boolean => {
  return /\.(mp4|webm|ogg|mov)$/i.test(url)
}

const openLightbox = (index: number) => {
  currentIndex.value = index
  lightboxOpen.value = true
  document.body.style.overflow = 'hidden'
}

const closeLightbox = () => {
  lightboxOpen.value = false
  document.body.style.overflow = 'auto'
}

const nextMedia = () => {
  if (currentIndex.value < props.mediaUrls.length - 1) {
    currentIndex.value++
  }
}

const previousMedia = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--
  }
}
</script>