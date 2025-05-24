<template>
  <div>
    <h1>게시글 목록 페이지</h1>
    <RouterLink :to="{ name: 'create' }">[게시글생성]</RouterLink>
    <ArticleList />
  </div>
</template>

<script setup>
import axios from "axios";
import { onMounted } from "vue";
import { useArticleStore } from "@/stores/articles";
import { RouterLink } from "vue-router";
import { useRoute } from "vue-router";
import ArticleList from "@/components/ArticleList.vue";

// const store = getArticles();
const store = useArticleStore();
// const route = useRoute();

onMounted(() => {
  store.getArticles();
});
</script>

<style lang="scss" scoped></style>
