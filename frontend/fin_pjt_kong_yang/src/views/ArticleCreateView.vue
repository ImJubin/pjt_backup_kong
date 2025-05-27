<template>
  <div class="form-container">
    <h2>글 작성</h2>
    <br />
    <form @submit.prevent="createArticle">
      <!-- input 태그와 textarea가 비었을떄는... 좀 처리가 되도록... -->
      <label for="title">제목: </label>
      <input type="text" id="title" v-model="title" class="input-box" />
      <label for="content">내용: </label>
      <textarea
        id="content"
        v-model="content"
        rows="5"
        class="input-box"
      ></textarea>
      <input type="submit" value="create" class="submit-btn" />
    </form>
  </div>
</template>

<script setup>
import axios from "axios";
import { useArticleStore } from "@/stores/articles.js";
import { ref } from "vue";
import { useRouter } from "vue-router";

const title = ref(null);
const content = ref(null);
const router = useRouter();

const store = useArticleStore();

const createArticle = function () {
  axios({
    method: "post",
    url: `${store.API_URL}/api/v1/articles/`,
    data: {
      title: title.value,
      content: content.value,
    },
  })
    .then((res) => {
      console.log(res);
      console.log(res.data);
      router.push({ name: "Home" });
    })
    .catch((err) => console.log(err));
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
  margin-top: 1.2rem;
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
  background-color: #ffdc52; /* 새로운 노란색 */
  color: #333;
  font-family: "Noto Sans KR", sans-serif;
  font-weight: 600;
  font-size: 1.1rem; /* 폰트 크기 키움 */
  padding: 0.8rem 1.6rem; /* 더 넓은 버튼 */
  border: none;
  border-radius: 0.75rem;
  cursor: pointer;
  margin-top: 1rem;
  transition: background-color 0.2s ease;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1); /* 부드러운 그림자 */
}

.submit-btn:hover {
  background-color: #fdc200; /* hover 시 좀 더 진한 색 */
}

.form-group {
  display: flex;
  flex-direction: column;
  width: 100%;
}
</style>
