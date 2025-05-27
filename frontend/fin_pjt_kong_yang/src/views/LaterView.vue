<script setup>
import { onMounted } from 'vue'
import { useYoutubeStore } from '@/stores/YoutubeStore.js'

const store = useYoutubeStore()

onMounted(() => {
  store.loadLaterVideos()
})
</script>

<template>
  <div>
    <h2>나중에 볼 동영상</h2>

    <div v-if="store.laterVideos.length === 0">
      등록된 비디오 없음
    </div>

    <div v-else class="video-list">
      <div
        v-for="video in store.laterVideos"
        :key="typeof video.id === 'object' ? video.id.videoId : video.id"
        class="video-card"
      >
        <router-link
          :to="{ name: 'VideoDetail', params: { videoId: typeof video.id === 'object' ? video.id.videoId : video.id } }"
        >
          <img :src="video.snippet.thumbnails.medium.url" :alt="video.snippet.title" />
          <p>{{ video.snippet.title }}</p>
        </router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.video-list {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-top: 16px;
}

.video-card {
  width: 240px;
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.2s;
}

.video-card:hover {
  transform: scale(1.03);
}

.video-card img {
  width: 100%;
}

.video-card p {
  margin: 8px;
  font-size: 14px;
}
</style>