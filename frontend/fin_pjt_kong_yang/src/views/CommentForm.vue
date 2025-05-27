<template>
  <form @submit.prevent="submitComment">
    <input v-model="content" placeholder="댓글을 입력하세요" />
    <button type="submit">작성</button>
  </form>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
const props = defineProps({ articlePk: Number });

const content = ref("");

const submitComment = async () => {
  try {
    await axios.post(
      `http://127.0.0.1:8000/api/v1/articles/${props.articlePK}/comments/`,
      {
        content: content.value,
      },
      {
        headers: {
          Authorization: `Token ${sessionStorage.getItem("authToken")}`,
        },
      }
    );
    content.value = "";
    alert("댓글이 추가되었습니다!");
  } catch (err) {
    console.error("에러 발생:", err.response?.data || err);
  }
};
</script>

<style scoped></style>
