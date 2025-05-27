import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

const STORAGE_KEY = 'laterVideos'

export const useYoutubeStore = defineStore('video', () => {
  // 나중에 볼 동영상 리스트
  const laterVideos = ref([])

  // 로컬 스토리지에서 저장된 동영상 불러오기
  function loadLaterVideos() {
    const raw = localStorage.getItem(STORAGE_KEY)
    laterVideos.value = raw ? JSON.parse(raw) : []
  }

  // 로컬 스토리지 갱신
  function updateStorage() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(laterVideos.value))
  }

  // 동영상 저장
  function saveLaterVideo(video) {
    const incomingId = typeof video.id === 'object' ? video.id.videoId : video.id
    const exists = laterVideos.value.some(v => {
      const savedId = typeof v.id === 'object' ? v.id.videoId : v.id
      return savedId === incomingId
    })

    if (!exists) {
      laterVideos.value.push(video)
      updateStorage()
    }
  }

  // 동영상 삭제
  function removeLaterVideo(videoId) {
    laterVideos.value = laterVideos.value.filter(v => {
      const savedId = typeof v.id === 'object' ? v.id.videoId : v.id
      return savedId !== videoId
    })
    updateStorage()
  }

  // 저장 여부 확인
  function isLaterVideo(videoId) {
    return computed(() =>
      laterVideos.value.some(v => {
        const savedId = typeof v.id === 'object' ? v.id.videoId : v.id
        return savedId === videoId
      })
    )
  }

  return {
    laterVideos,
    loadLaterVideos,
    saveLaterVideo,
    removeLaterVideo,
    isLaterVideo,
    
  }
})