<template>
  <h2>게시글 생성 페이지</h2>
  <form @submit.prevent="createArticle">
    <!-- input 태그와 textarea가 비었을떄는... 좀 처리가 되도록... -->
    <label for="title">title: </label>
    <input type="text" id="title" v-model="title" />

    <label for="content">content: </label>
    <textarea id="content" v-model="content"></textarea>
    <input type="submit" value="[CREATE]" />
  </form>
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
      router.push({ name: "home" });
    })
    .catch((err) => console.log(err));
};
</script>

<style scoped></style>
