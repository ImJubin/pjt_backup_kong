<template>
  <div>
    <ul>
      <li v-for="article in store.articles" :key="article.id">
        <p>{{ article.title }}</p>
        <p>{{ article.content }}</p>
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

const store = useArticleStore();

onMounted(() => {});
</script>

<style lang="scss" scoped></style>
