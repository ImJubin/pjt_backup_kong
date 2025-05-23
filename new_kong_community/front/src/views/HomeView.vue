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
// izmport { getArticles } from "@/stores/articles";
import { useArticleStore } from "@/stores/articles";
import ArticleList from "@/components/ArticleList.vue";
import { RouterLink } from "vue-router";
import { useRoute } from "vue-router";

// const store = getArticles();
const store = useArticleStore();
const route = useRoute;

onMounted(() => {
  store.getArticles();
});
</script>

<style lang="scss" scoped></style>
