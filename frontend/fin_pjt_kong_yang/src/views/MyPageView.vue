<script setup>
import { ref } from "vue";
import { useUserStore } from '@/stores/user'
import AccountOverview from '@/components/AccountOverview.vue'
import InterestComparisonChart from '@/components/InterestComparisonChart.vue'
import AccountAddForm from '@/components/AccountAddForm.vue'  // 계좌 추가 폼 컴포넌트
const userStore = useUserStore()
// const user = userStore.user
// ✅ 토글 상태 변수
const showAccountForm = ref(false)

const handleDelete = () => {
  if (confirm('정말 탈퇴하시겠어요?')) {
    userStore.deleteUser()
  }
}
</script>

<template>
  <div class="mypage-container">
    <h1>🧑 마이페이지</h1>

    <div v-if="userStore.user">
      <ul>
        <li><strong>아이디:</strong> {{ userStore.user.username }}</li>
        <li><strong>이메일:</strong> {{ userStore.user.email }}</li>
        <li><strong>이름:</strong> {{ userStore.user.first_name }} {{ userStore.user.last_name }}</li>
        <li><strong>전화번호:</strong> {{ userStore.user.phone_number }}</li>
        <li><strong>회원 번호 (pk):</strong> {{ userStore.user.pk }}</li>
      </ul>
       <!-- 🔘 계좌 추가 폼 토글 버튼 -->
      <button @click="showAccountForm = !showAccountForm">
        {{ showAccountForm ? '계좌 추가 폼 닫기' : '➕ 계좌 추가' }}
      </button>

      <!-- 📄 토글된 경우에만 폼 보여주기 -->
      <AccountAddForm v-if="showAccountForm" />

      <AccountOverview />
      <InterestComparisonChart />
      <button @click="handleDelete">회원 탈퇴</button>


    </div>
    
    <div v-else>
      <p>유저 정보를 불러오는 중이거나 로그인되지 않았습니다.</p>
    </div>
  </div>
</template>

<style scoped>
.mypage-container {
  max-width: 500px;
  margin: 2rem auto;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
}
ul {
  list-style: none;
  padding: 0;
}
li {
  margin-bottom: 0.75rem;
}
strong {
  display: inline-block;
  width: 120px;
}
</style>