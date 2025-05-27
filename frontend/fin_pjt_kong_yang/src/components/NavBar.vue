<script setup>
import { useUserStore } from '@/stores/user'
const userStore = useUserStore()
</script>

<template>
  <div v-if="userStore.user">
    <span>{{ userStore.user.first_name }}님</span>
    <button @click="userStore.logOut">로그아웃</button>
  </div>
  <div v-else>
    <router-link to="/users/login">로그인</router-link>
  </div>
</template>