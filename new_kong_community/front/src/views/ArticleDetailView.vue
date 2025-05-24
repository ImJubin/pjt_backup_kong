<template>
  <div>
    <h2>{{ article.title }}</h2>
    <p>{{ article.content }}</p>

    <div>
      <RouterLink :to="{ name: 'ArticleUpdateView', params: { id: article.id } }">
        <button>✏ 수정</button>
      </RouterLink>
      <button @click="deleteArticle">🗑 삭제</button>
    </div>

    <hr />
    <h3>💬 댓글</h3>
    <ul>
      <li v-for="comment in comments" :key="comment.id">
        {{ comment.content }}
        <span> ❤️ {{ comment.likes }}</span>
        <button @click="likeComment(comment.id)">좋아요</button>
      </li>
    </ul>

    <form @submit.prevent="createComment">
      <textarea v-model="newComment" placeholder="댓글을 입력하세요" required></textarea>
      <button type="submit">댓글 작성</button>
    </form>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useArticleStore } from '@/stores/articles'

const route = useRoute()
const router = useRouter()
const store = useArticleStore()

const article = ref({})
const comments = ref([])
const newComment = ref("")

// 게시글 + 댓글 불러오기
onMounted(async () => {
  const res = await axios.get(`${store.API_URL}/api/v1/articles/${route.params.id}/`)
  article.value = res.data

  const resComment = await axios.get(`${store.API_URL}/api/v1/articles/${route.params.id}/comments/`)
  comments.value = resComment.data
})

// 게시글 삭제
const deleteArticle = async () => {
  if (confirm('정말 삭제할까요?')) {
    await axios.delete(`${store.API_URL}/api/v1/articles/${route.params.id}/`, {
      headers: {
        Authorization: `Token ${localStorage.getItem("token")}`,
      }
    })
    router.push({ name: 'ArticleList' })
  }
}

// 댓글 작성
const createComment = async () => {
  const res = await axios.post(`${store.API_URL}/api/v1/articles/${route.params.id}/comments/`, {
    content: newComment.value
  }, {
    headers: {
      Authorization: `Token ${localStorage.getItem("token")}`,
    }
  })
  comments.value.push(res.data)
  newComment.value = ""
}

// 댓글 좋아요
const likeComment = async (commentId) => {
  const res = await axios.post(`${store.API_URL}/api/v1/comments/${commentId}/like/`, {}, {
    headers: {
      Authorization: `Token ${localStorage.getItem("token")}`,
    }
  })
  const updated = res.data
  const idx = comments.value.findIndex(c => c.id === commentId)
  if (idx !== -1) {
    comments.value[idx].likes = updated.likes
  }
}
</script>

<style scoped>
textarea {
  width: 100%;
  height: 80px;
  margin-top: 8px;
  margin-bottom: 8px;
}
</style>
