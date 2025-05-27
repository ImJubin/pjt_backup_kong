<template>
  <RouterLink :to="{ name: 'ArticleDetailView', params: { id: article.id } }">
  <p>{{ article.title }}</p>
</RouterLink>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useArticleStore } from "@/stores/articles";
import axios from "axios";

const posts = ref([]);

onMounted(async () => {
  const res = await axios.get("http://localhost:8000/api/v1/posts/", {
    headers: {
      Authorization: `Token ${sessionStorage.getItem("authToken")}`,
    },
  });
  posts.value = res.data;
});
</script>

<style scoped></style>
