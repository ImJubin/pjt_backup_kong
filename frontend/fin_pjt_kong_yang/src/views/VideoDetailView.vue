<script setup>
import { useRoute } from 'vue-router'
import { useYoutubeStore } from '@/stores/YoutubeStore.js'
import { onMounted, computed, ref } from 'vue'

const route = useRoute()
const store = useYoutubeStore()

const videoId = route.params.videoId
const video = ref(null)

// 저장 여부 확인
const isSaved = computed(() =>
  store.laterVideos.some(v => {
    const savedId = typeof v.id === 'object' ? v.id.videoId : v.id
    return savedId === videoId
  })
)

onMounted(async () => {
  const API_KEY = import.meta.env.VITE_YOUTUBE_API_KEY
  const url = `https://www.googleapis.com/youtube/v3/videos?part=snippet&id=${videoId}&key=${API_KEY}`
  const res = await fetch(url)
  const data = await res.json()
  video.value = data.items[0]
})

// 저장 토글
function toggleSave() {
    console.log(video)
  if (!video.value) return
  const videoData = { ...video.value, id: videoId }
  if (isSaved.value) {
    store.removeLaterVideo(videoId)
  } else {
    store.saveLaterVideo(videoData)
  }
}
</script>

<template>
  <div v-if="video">
    <h2>{{ video.snippet.title }}</h2>
    <iframe
      width="560"
      height="315"
      :src="`https://www.youtube.com/embed/${videoId}`"
      frameborder="0"
      allowfullscreen
    ></iframe>

    <p>{{ video.snippet.description }}</p>

    <button @click="toggleSave">
      {{ isSaved ? '저장 취소' : '나중에 보기' }}
    </button>
  </div>

  <div v-else>
    <p>로딩 중...</p>
  </div>
</template>
