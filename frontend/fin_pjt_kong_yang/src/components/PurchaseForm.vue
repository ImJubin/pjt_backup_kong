<template>
  <div class="mt-6 border p-4 rounded bg-white">
    <h3 class="text-lg font-bold">상품 가입</h3>

    <label class="block mt-2">예치 기간</label>
    <select v-model="selectedOptionId" class="w-full p-2 border rounded">
      <option disabled value="">선택</option>
      <option
        v-for="option in product.options"
        :key="option.id"
        :value="option.id"
      >
        {{ option.save_trm }}개월 ({{ option.intr_rate }}%)
      </option>
    </select>

    <!-- ✅ 예금/적금에 따라 라벨 변경 -->
    <label class="block mt-2">
      {{ type === 'savings' ? '월 납입 금액 (원)' : '예치 금액 (원)' }}
    </label>
    <input
      v-model.number="amount"
      type="number"
      placeholder="1000000"
      class="w-full p-2 border rounded"
    />

    <!-- 예상 이자 표시 -->
    <p class="mt-4 text-sm text-gray-700">
      예상 이자: <strong>{{ predictedInterest.toLocaleString() }}원</strong>
    </p>

    <button
      :disabled="!selectedOptionId || !amount"
      class="mt-4 w-full py-2 bg-blue-500 text-white rounded disabled:opacity-50"
      @click="handlePurchase"
    >
      구매하기
    </button>
  </div>
</template>

<!-- <template>
  <div class="mt-6 border p-4 rounded bg-white">
    <h3 class="text-lg font-bold">상품 가입</h3>

    <label class="block mt-2">예치 기간</label>
    <select v-model="selectedOptionId" class="w-full p-2 border rounded">
      <option disabled value="">선택</option>
      <option
        v-for="option in product.options"
        :key="option.id"
        :value="option.id"
      >
        {{ option.save_trm }}개월 ({{ option.intr_rate }}%)
      </option>
    </select>

    <label class="block mt-2">예치 금액 (원)</label>
    <input
      v-model.number="amount"
      type="number"
      placeholder="1000000"
      class="w-full p-2 border rounded"
    />

    
    <p class="mt-4 text-sm text-gray-700">
      예상 이자: <strong>{{ predictedInterest.toLocaleString() }}원</strong>
    </p>

    <button
      :disabled="!selectedOptionId || !amount"
      class="mt-4 w-full py-2 bg-blue-500 text-white rounded disabled:opacity-50"
      @click="handlePurchase"
    >
      구매하기
    </button>
  </div>
</template>-->

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'
import { useAccountStore } from '@/stores/userAccount'
import { useRouter } from 'vue-router'

const props = defineProps({
  product: Object,
  type: String // 'deposit' or 'savings'
})

const selectedOptionId = ref('')
const amount = ref(0)
const router = useRouter()
const store = useAccountStore()

// 계산된 금리
const selectedOption = computed(() => {
  return props.product.options.find(opt => opt.id === selectedOptionId.value)
})

// 예상 이자 계산
const predictedInterest = computed(() => {
  if (!selectedOption.value || !amount.value) return 0
  const rate = selectedOption.value.intr_rate
  const term = selectedOption.value.save_trm
  const principal = amount.value

  if (props.type === 'deposit') {
    // 단리 계산 = 원금 × (이율/100) × (개월 / 12)
    return Math.floor(principal * (rate / 100) * (term / 12))
  } else {
    // 적금 계산 = 매달 넣는 돈 × (개월 + 1) / 2 × (이율 / 100) × (1/12)
    const avgSaving = (term + 1) / 2
    return Math.floor((principal * avgSaving) * (rate / 100) / 12)
  }
})

// 구매 요청
const handlePurchase = async () => {
    const token = sessionStorage.getItem('authToken')
  try {
    await axios.post('http://127.0.0.1:8000/users/purchase/', {
      type: props.type,
      product_id: props.product.id,
      option_id: selectedOptionId.value,
      amount: amount.value
    },
    {
    headers: {
        Authorization: `Token ${token}`  // 만약 JWT라면 Bearer로
    } 
  })
    await store.fetchAccounts()
    alert('가입 완료!')
    router.push('/mypage/accounts')
  } catch (err) {
    alert('가입 실패')
    console.error(err)
  }
}
</script>
