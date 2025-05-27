<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const username = ref('')
const password = ref('')
const errorMsg = ref('')
const router = useRouter()
const userStore = useUserStore()

const logIn = async () => {
  errorMsg.value = '' // 에러 초기화

  if (!username.value || !password.value) {
    errorMsg.value = '아이디와 비밀번호를 모두 입력해주세요.'
    return
  }

  try {
    await userStore.logIn({
      username: username.value,
      password: password.value
    })
    // 로그인 성공 → 이동은 store 안에서 처리됨
  } catch (err) {
    errorMsg.value = '아이디 또는 비밀번호가 일치하지 않습니다.'
    console.error(err)
  }
}
</script>

<template>
  <div class="login-container">
    <h1>로그인</h1>
    <form @submit.prevent="logIn">
      <label for="username">아이디</label><br />
      <input id="username" v-model="username" /><br />

      <label for="password">비밀번호</label><br />
      <input id="password" v-model="password" type="password" /><br />

      <p v-if="errorMsg" style="color: red;">{{ errorMsg }}</p>

      <button type="submit">로그인</button>
    </form>
  </div>
</template>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 2rem auto;
}
input {
  width: 100%;
  padding: 0.5rem;
  margin: 0.25rem 0 1rem;
}
button {
  padding: 0.5rem 1rem;
}
</style>