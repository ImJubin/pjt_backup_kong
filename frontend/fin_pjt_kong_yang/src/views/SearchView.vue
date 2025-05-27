<template>
<h2>비디오 검색</h2>
<input v-model="query" @keyup.enter="onSearch"></input>
<button @click="onSearch">찾기</button>

    <div class="video-list">
      <div v-for="video in videos" :key="video.id.videoId" class="video-card">
    <router-link
    :to="{ name: 'VideoDetail', params: { videoId: video.id.videoId } }"
    class="video-card"
    >
    <img :src="video.snippet.thumbnails.medium.url" :alt="video.snippet.title" />
    <p>{{ video.snippet.title }}</p>
    </router-link>
      </div>
    </div>

</template>

<script setup>
import { ref } from 'vue';

const query = ref('');
const videos = ref([]);

const API_KEY = import.meta.env.VITE_YOUTUBE_API_KEY;

const onSearch = async () => {
  if (!query.value) return;

  const url = `https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=8&q=${encodeURIComponent(query.value)}&type=video&key=${API_KEY}`;

  try {
    const res = await fetch(url)
    const data = await res.json()
    videos.value = data.items
  } catch (err) {
    console.error('유튜브 API 호출 실패:', err)
  }
}
</script>

<style scoped>
.search-page {
  padding: 20px;
}

.search-bar {
  margin-bottom: 20px;
}

input {
  padding: 8px;
  width: 300px;
  font-size: 16px;
}

button {
  padding: 8px 12px;
  font-size: 16px;
  margin-left: 8px;
  cursor: pointer;
}

.video-list {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
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