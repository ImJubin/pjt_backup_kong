<script setup>
import { ref, computed } from 'vue'
import { useAccountStore } from '@/stores/userAccount'
import DepositDetailForm from './DepositDetailForm.vue'
import SavingsDetailForm from './SavingsDetailForm.vue'

const store = useAccountStore()

const form = ref({
  bank_name: '',
  account_number: '',
  account_type: '예금',
  alias_name: '',
  current_balance: 0,  // ✅ 추가
})


const depositDetail = ref({
  product_name: '',
  interest_rate: 0,
  duration_months: 12,
  started_at: '',
  ends_at: '',
})

const savingsDetail = ref({
  product_name: '',
  interest_rate: 0,
  duration_months: 12,
  started_at: '',
  ends_at: '',
  payment_date: '',
  round_number: 0,
  total_round: 12,
  goal_amount: 0,
})

const handleSubmit = async () => {
  const payload = {
    ...form.value,
    deposit_detail: form.value.account_type === '예금' ? depositDetail.value : null,
    savings_detail: form.value.account_type === '적금' ? savingsDetail.value : null,
  }

  await store.addAccount(payload)

  // 초기화
  form.value = {
    bank_name: '',
    account_number: '',
    account_type: '예금',
    alias_name: '',
  }
  depositDetail.value = {}
  savingsDetail.value = {}
}

const isDeposit = computed(() => form.value.account_type === '예금')
const isSavings = computed(() => form.value.account_type === '적금')
</script>

<template>
  <form @submit.prevent="handleSubmit" class="mt-4 p-4 bg-white rounded shadow">
    <h3 class="font-bold mb-2">새 계좌 등록</h3>

    <!-- 기본 계좌 정보 -->
    <div class="mb-2">
      <label>은행명</label>
      <input v-model="form.bank_name" required />
    </div>

    <div class="mb-2">
      <label>계좌번호</label>
      <input v-model="form.account_number" required />
    </div>

    <div class="mb-2">
  <label class="block text-sm font-medium">현재 잔액</label>
  <input
    type="number"
    v-model="form.current_balance"
    class="border p-2 w-full"
    required
  />
</div>


    <div class="mb-2">
      <label>계좌 타입</label>
      <select v-model="form.account_type" required>
        <option value="예금">예금</option>
        <option value="적금">적금</option>
      </select>
    </div>

    <div class="mb-2">
      <label>별칭 (선택)</label>
      <input v-model="form.alias_name" />
    </div>

    <!-- 타입에 따라 디테일 입력 -->
    <DepositDetailForm v-if="isDeposit" v-model="depositDetail" />
    <SavingsDetailForm v-if="isSavings" v-model="savingsDetail" />

    <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded">
      계좌 추가
    </button>
  </form>
</template>
