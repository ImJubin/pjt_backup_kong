<template>
  <div class="form-container">
    <h2>게시글 수정</h2>
    <form @submit.prevent="updateArticle">
      <label for="title">제목: </label>
      <input type="text" id="title" v-model="title" />

      <label for="content">내용: </label>
      <textarea id="content" v-model="content"></textarea>

      <input type="submit" value="UPDATE" class="submit-btn" />
    </form>
  </div>
</template>

<script setup>
import axios from "axios";
import { useRoute, useRouter } from "vue-router";
import { useArticleStore } from "@/stores/articles.js";
import { ref, onMounted } from "vue";

const title = ref("");
const content = ref("");
const router = useRouter();
const route = useRoute();
const store = useArticleStore();
const articles = ref([]);

// 기존 게시글 내용 불러오기
onMounted(async () => {
  try {
    const res = await axios.get(
      `${store.API_URL}/api/v1/articles/${route.params.id}/`
    );
    title.value = res.data.title;
    content.value = res.data.content;
  } catch (err) {
    console.error("게시글 불러오기 실패", err);
  }
});

// 게시글 수정
const updateArticle = async () => {
  try {
    const res = await axios.put(
      `${store.API_URL}/api/v1/articles/${route.params.id}/`,
      {
        title: title.value,
        content: content.value,
      },
      {
        headers: {
          Authorization: `Token ${sessionStorage.getItem("authToken")}`,
        },
      }
    );
    console.log("수정 성공:", res.data);
    router.push({ name: "Home" }); // 수정 후 상세 페이지로 이동
  } catch (err) {
    console.error("수정 실패", err);
    router.push({ name: "Home" }); // or 상세 페이지로 이동
  }
};
</script>

<style scoped>
.form-container {
  max-width: 600px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: #fafafa;
  border-radius: 1rem;
  box-shadow: 0 4px 12px rgba(170, 170, 170, 0.15);
  font-family: "Noto Sans KR", sans-serif;
  color: #333;
}

h2 {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  font-weight: 700;
}

label {
  display: block;
  margin-top: 1rem;
  font-size: 1rem;
  font-weight: 500;
}

input[type="text"],
textarea {
  width: 100%;
  padding: 0.75rem;
  margin-top: 0.5rem;
  border: 1px solid #dddddd;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-family: "Noto Sans KR", sans-serif;
}

textarea {
  height: 150px;
  resize: vertical;
}

.submit-btn {
  margin-top: 1.5rem;
  background-color: #ffdc52;
  color: #333;
  font-weight: 600;
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 0.75rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.submit-btn:hover {
  background-color: #fdc200;
}
</style>
