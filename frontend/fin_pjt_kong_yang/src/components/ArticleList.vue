<template>
  <div class="article-list">
    <ul>
      <li
        v-for="article in store.articles"
        :key="article.id"
        class="article-card"
      >
        <RouterLink
          :to="{ name: 'ArticleDetailView', params: { id: article.id } }"
        >
          <p class="clickable-title">{{ article.title }}</p>
        </RouterLink>
        <p>{{ article.content }}</p>
        <div class="button-group">
          <RouterLink
            :to="{ name: 'ArticleUpdateView', params: { id: article.id } }"
          >
            <button>수정</button>
          </RouterLink>

          <button @click="deleteArticle(article.id)">삭제</button>
        </div>
      </li>
    </ul>
    <!-- 
    <RouterLink :to="{ name: 'create' }"> [글쓰기] </RouterLink> -->
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { useArticleStore } from "@/stores/articles";
import { RouterLink } from "vue-router";
import axios from "axios";

// const router = useRouter();
const store = useArticleStore();

// 이동: 수정 페이지로
const goEdit = (articleId) => {
  router.push({ name: "ArticleUpdateView", params: { id: articleId } });
};

// 삭제
const deleteArticle = async (articleId) => {
  if (confirm("정말 삭제할까요?")) {
    await store.deleteArticle(articleId);
    store.getArticles(); // 삭제 후 목록 새로고침
  }
};

onMounted(() => {
  store.getArticles(); // ✅ store 내부에서 axios 처리
});
</script>

<style scoped>
.article-list {
  font-family: "Noto Sans KR", sans-serif;
  color: #333333;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 2.5rem; /* 카드 사이 간격 */
  padding: 2rem; /* 전체 여백 */
}

.article-card {
  background-color: #fafafa;
  border: 1px solid #dddddd;
  border-radius: 1rem;
  padding: 1.5rem;
  margin-bottom: 1rem;
  font-family: "Noto Sans KR", sans-serif;
  color: #333;
  box-shadow: 0 2px 5px rgba(170, 170, 170, 0.1);
  transition: box-shadow 0.2s;
}

.article-card:hover {
  box-shadow: 0 4px 8px rgba(170, 170, 170, 0.2);
}

.title {
  font-size: 1.2rem;
  font-weight: bold;
  color: #fdc200;
  margin-bottom: 0.3rem;
  cursor: pointer;
}

.content {
  font-size: 0.95rem;
  margin-bottom: 1rem;
}

.clickable-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #fdc200;
  margin-bottom: 0.6rem; /* 여백 추가 → 이 값 늘려줘도 OK */
}

.button-group {
  display: flex;
  gap: 0.75rem;
  margin-top: 1.25rem; /* 내용과 버튼 사이 여백 추가 */
}

button {
  font-family: "Noto Sans KR", sans-serif;
  font-size: 0.85rem;
  border: none;
  padding: 0.4rem 0.9rem;
  border-radius: 6px;
  cursor: pointer;
}

.edit-btn {
  background-color: #fdde88;
  color: #333;
}

.edit-btn:hover {
  background-color: #ffdc52;
}

.delete-btn {
  background-color: #aaaaaa;
  color: white;
}

.delete-btn:hover {
  background-color: #888888;
}

ul {
  list-style: none;
  padding-left: 0;
  margin: 0;
}
</style>
