<script setup>
// import TheWelcome from '../components/TheWelcome.vue'
import { useUserStore } from '@/stores/user'
import MainCalendar from '@/components/MainCalendar.vue'
const userStore = useUserStore()
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

<template>
  <div>
    <h1>홈</h1>
      <div>
    <h1>게시글 목록 페이지</h1>
    <RouterLink :to="{ name: 'create' }">[게시글생성]</RouterLink>
    <ArticleList />
  </div>
    <p v-if="userStore.user">👋 {{ userStore.user.first_name }}님 환영합니다!</p>
    <p v-else>로그인 해주세요</p>
  </div>
</template>