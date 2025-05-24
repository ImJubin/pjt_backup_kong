<template>
  <h2>게시글 수정 페이지</h2>
  <form @submit.prevent="updateArticle">
    <label for="title">title: </label>
    <input type="text" id="title" v-model="title" />

    <label for="content">content: </label>
    <textarea id="content" v-model="content"></textarea>

    <input type="submit" value="[UPDATE]" />
  </form>
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
          Authorization: `Token ${localStorage.getItem("token")}`,
        },
      }
    );
    console.log("수정 성공:", res.data);
    router.push({ name: "home" }); // 수정 후 상세 페이지로 이동
  } catch (err) {
    console.error("수정 실패", err);
    router.push({ name: 'Home' })  // or 상세 페이지로 이동
  }
}


</script>

<style scoped></style>
