<script setup>
import { ref } from 'vue'
import UserInfoForm from '@/components/UserInfoForm.vue'
import PasswordChangeForm from '@/components/PasswordChangeForm.vue'

const activeTab = ref('info')
</script>

<template>
  <div>
    <h1>회원정보 관리</h1>
    <div class="tabs">
      <button :class="{ active: activeTab === 'info' }" @click="activeTab = 'info'">회원정보 수정</button>
      <button :class="{ active: activeTab === 'password' }" @click="activeTab = 'password'">비밀번호 변경</button>
    </div>
    <div class="tab-content">
      <UserInfoForm v-if="activeTab === 'info'" />
      <PasswordChangeForm v-if="activeTab === 'password'" />
    </div>
  </div>
</template>