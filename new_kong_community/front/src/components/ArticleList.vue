<template>
  <div>
    <ul>
      <li v-for="article in store.articles" :key="article.id">
        <RouterLink :to="{ name: 'ArticleDetailView', params: { id: article.id } }">
          <p class="clickable-title">{{ article.title }}</p>
        </RouterLink>
        <p>{{ article.content }}</p>

        <RouterLink :to="{ name: 'ArticleUpdateView', params: { id: article.id } }">
          <button>수정</button>
        </RouterLink>

        <button @click="deleteArticle(article.id)">삭제</button>
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
import axios from 'axios'

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
  store.getArticles();  // ✅ store 내부에서 axios 처리
});

</script>

<style lang="scss" scoped>
</style>
