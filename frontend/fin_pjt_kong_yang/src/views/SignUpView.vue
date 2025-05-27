<template>
  <form @submit.prevent="signUp">

    <label for="username">아이디<span class = "require">*</span></label><br />
    <input id="username" v-model="username" />
    <p v-if="showError && !username" class="error-msg">이 칸은 비어있을 수 없습니다.</p><br />

    <label for="email">이메일<span class = "require">*</span></label><br />
    <input id="email" v-model="email" />
    <p v-if="showError && !email" class="error-msg">이 칸은 비어있을 수 없습니다.</p><br />

    <label for="password">비밀번호<span class = "require">*</span></label><br />
    <input id="password" v-model="password" type="password" />
    <p v-if="showError && !password" class="error-msg">이 칸은 비어있을 수 없습니다.</p><br />

    <label for="password2">비밀번호 확인<span class = "require">*</span></label><br />
    <input id="password2" v-model="password2" type="password" />
    <p v-if="showError && !password2" class="error-msg">이 칸은 비어있을 수 없습니다.</p>
    <p v-if="passwordMismatch" class="error-msg">비밀번호가 일치하지 않습니다.</p><br />

    <label for="first_name">이름<span class = "require">*</span></label><br />
    <input id="first_name" v-model="first_name" />
    <p v-if="showError && !first_name" class="error-msg">이 칸은 비어있을 수 없습니다.</p><br />

    <label for="last_name">성<span class = "require">*</span></label><br />
    <input id="last_name" v-model="last_name" />
    <p v-if="showError && !last_name" class="error-msg">이 칸은 비어있을 수 없습니다.</p><br />

    <label for="phone_number">전화번호<span class = "require">*</span></label><br />
    <input id="phone_number" v-model="phone_number" />
    <p v-if="showError && !phone_number" class="error-msg">이 칸은 비어있을 수 없습니다.</p><br />

    <button type="submit">회원가입</button>
  </form>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from "vue-router";
const router = useRouter()

const userStore = useUserStore()

const username = ref('')
const email = ref('')
const password = ref('')
const password2 = ref('')
const first_name = ref('')
const last_name = ref('')
const phone_number = ref('')

const showError = ref(false)

// ❗ 비밀번호 불일치 여부
const passwordMismatch = computed(() =>
  password.value && password2.value && password.value !== password2.value
)

const signUp = async () => {
  // ❗ 필수 필드 체크
  if (
    !username.value ||
    !email.value ||
    !password.value ||
    !password2.value ||
    !first_name.value ||
    !last_name.value ||
    !phone_number.value
  ) {
    showError.value = true
    return
  }

  if (passwordMismatch.value) {
    showError.value = true
    return
  }

  try {
    await userStore.signUp({
      username: username.value,
      email: email.value,
      password: password.value,
      password2: password2.value,
      first_name: first_name.value,
      last_name: last_name.value,
      phone_number: phone_number.value
    })
    router.push({ name: 'Home' }) 
  } 
  
  // 로그인 실패인 경우
  catch (err) {
  const errors = err.response?.data

  if (errors) {
    // 예: {"username": ["이미 존재하는 아이디입니다."], "password": ["너무 짧습니다."]}
    const messages = Object.entries(errors)
      .map(([field, msgs]) => `${field}: ${msgs.join(', ')}`)
      .join('\n')

    alert(`회원가입에 실패했습니다:\n${messages}`)
  } else {
    alert('알 수 없는 오류가 발생했습니다.')
  }
  console.error('전체 에러:', err)
  console.error('회원가입 실패:', err.response?.data)
}
}
</script>

<style scoped>
.require {
    color:red;
}
.error-msg {
  color: red;
  font-size: 0.85rem;
  margin: 2px 0;
}
</style>